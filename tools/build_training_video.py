#!/usr/bin/env python3
"""
build_training_video.py — build TPP training videos on HeyGen from a narration script.

Turns a markdown narration script into a set of avatar-presented video segments,
each with a branded slide behind the presenter, and writes a manifest the course
player can consume.

WHY SEGMENTS: HeyGen caps a single render at 5,000 characters of script. A full
course runs ~11,000. Segmenting on the script's own section breaks is therefore
required, and it happens to line up with the knowledge checks — each segment ends
where a quiz begins.

USAGE
    export HEYGEN_API_KEY=...            # https://app.heygen.com/settings (API tab)
    python3 build_training_video.py --script ../narration-script-v4.md \
        --slides-base https://teond1090.github.io/tpp-onboarding-portal/slides/secure \
        --out manifest-secure.json

    # Preview cost and segmentation without spending credits:
    python3 build_training_video.py --script ... --dry-run

NOTE: must run somewhere with network access to api.heygen.com.
"""

import argparse, json, os, re, sys, time
import urllib.request, urllib.error

API = "https://api.heygen.com"
MAX_SCRIPT_CHARS = 5000

# ---------------------------------------------------------------- presentation
# Annie: HeyGen pairs this avatar with the "Annie - Lifelike" voice by design, so
# face and voice read as the same person. Studio avatars on the Avatar V engine
# are the only ones that accept motion prompts — a studio avatar on Avatar III
# (the previous Adriana setup) is why the old videos stood perfectly still.
AVATAR = "Annie_Office_Standing_Front_public"
VOICE = "330290724a1b470fb63153f34d4c0183"
ENGINE = {"type": "avatar_v"}

BASE_MOTION = (
    "Animated, charismatic corporate trainer standing and presenting to camera. "
    "Expressive eyebrows, warm smiles, natural head movement and weight shifts, "
    "hands frequently in motion — energetic and personable, never static or stiff."
)

# Per-section gesture direction. Keyed by a substring of the section heading so
# the script can be reordered without breaking the mapping.
MOTION_BY_SECTION = {
    "Opening": "Big open welcoming arm gestures on the greeting; counts on fingers for the statistic; "
               "leans in toward the viewer on the closing line.",
    "Why": "Counts on fingers for statistics; hands framing contrasting ideas; "
           "an emphatic gesture on the rule about what never to call the plan.",
    "Plans": "Counts the plan levels on her fingers; hands framing 'which, not whether' as two distinct "
             "beats; open inviting gestures when role-playing the counter conversation.",
    "Coverage": "Counts off covered perils on her fingers; a firm downward gesture on the police-report "
                "rule; leans in on 'Call the police'.",
    "Filing": "Hands separating the tenant's responsibilities from the manager's; an emphatic gesture on "
              "the claims portal; a clear cautionary hand on never promising a payment date.",
    "Opt-Out": "Holds up ten fingers for the ten-day window; counts the three photo details as three "
               "clear beats; counts one-two-three through the submission steps.",
    "Close": "Warm, open-armed encouraging gestures; big genuine smile.",
}


def motion_for(title: str) -> str:
    for key, extra in MOTION_BY_SECTION.items():
        if key.lower() in title.lower():
            return f"{extra} {BASE_MOTION}"
    return BASE_MOTION


# ------------------------------------------------------------------ script I/O
def parse_script(path: str):
    """Split a narration markdown file into spoken sections.

    Everything above the first '---' is author notes, not narration. Knowledge
    check markers and markdown emphasis are stripped — they must never be spoken.
    """
    raw = open(path, encoding="utf-8").read()
    if "---" not in raw:
        sys.exit(f"{path}: expected a '---' separator between notes and narration")
    body = raw.split("---", 1)[1]

    sections = []
    for chunk in re.split(r"\n## ", body):
        if not chunk.strip():
            continue
        lines = chunk.split("\n")
        title = lines[0].strip()
        text = "\n".join(lines[1:])
        text = re.sub(r"\*\*\[Knowledge Check \d+\]\*\*", "", text)
        text = text.replace("**", "").replace("*", "")
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            sections.append({"title": title, "text": text})
    return sections


def group_segments(sections):
    """Merge adjacent sections into segments that fit HeyGen's 5,000-char cap.

    A section is never split across segments: a quiz follows each section, so a
    segment boundary that fell mid-section would interrupt the narration
    mid-thought.
    """
    segments, cur = [], None
    for s in sections:
        if len(s["text"]) > MAX_SCRIPT_CHARS:
            sys.exit(f"Section '{s['title']}' is {len(s['text'])} chars; "
                     f"split it in the script (cap is {MAX_SCRIPT_CHARS}).")
        if cur and len(cur["text"]) + 1 + len(s["text"]) <= MAX_SCRIPT_CHARS:
            cur["text"] += " " + s["text"]
            cur["titles"].append(s["title"])
        else:
            cur = {"titles": [s["title"]], "text": s["text"]}
            segments.append(cur)
    return segments


# ---------------------------------------------------------------- HeyGen calls
def call(path, payload=None, key=None, method=None):
    url = f"{API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"))
    req.add_header("X-Api-Key", key)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HeyGen {e.code} on {path}: {e.read().decode()[:400]}")


def render(seg, idx, total, key, slide_url, title_prefix):
    body = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": AVATAR,
                "avatar_style": "normal",
            },
            "voice": {"type": "text", "input_text": seg["text"], "voice_id": VOICE},
        }],
        "dimension": {"width": 1920, "height": 1080},
        "title": f"{title_prefix} - Part {idx} of {total}",
    }
    if slide_url:
        body["video_inputs"][0]["background"] = {"type": "image", "url": slide_url}
    res = call("/v2/video/generate", body, key)
    vid = (res.get("data") or {}).get("video_id")
    if not vid:
        sys.exit(f"No video_id returned: {json.dumps(res)[:400]}")
    return vid


def wait_for(video_id, key, poll=20, timeout=3600):
    """Poll until the render finishes. Renders take roughly 2-8 minutes each."""
    start = time.time()
    while time.time() - start < timeout:
        res = call(f"/v1/video_status.get?video_id={video_id}", key=key)
        d = res.get("data") or {}
        status = d.get("status")
        if status == "completed":
            return d
        if status == "failed":
            sys.exit(f"Render failed: {d.get('error') or d}")
        time.sleep(poll)
    sys.exit(f"Timed out waiting for {video_id}")


# ------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", required=True, help="narration markdown file")
    ap.add_argument("--slides-base", default="",
                    help="public base URL of the slide PNGs; HeyGen fetches them, "
                         "so the URLs must be reachable from the internet")
    ap.add_argument("--slide-map", default="",
                    help="JSON file mapping segment index -> slide filename")
    ap.add_argument("--title", default="TPP Training", help="title prefix in HeyGen")
    ap.add_argument("--out", default="manifest.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="show segmentation and estimated cost; spend nothing")
    args = ap.parse_args()

    sections = parse_script(args.script)
    segments = group_segments(sections)
    total_chars = sum(len(s["text"]) for s in segments)
    # Annie reads ~15.6 characters per second, measured across sample renders.
    est_seconds = total_chars / 15.6

    print(f"{len(sections)} sections -> {len(segments)} segments")
    for i, s in enumerate(segments, 1):
        print(f"  {i}. {' + '.join(s['titles'])[:60]:62s} {len(s['text']):5d} chars"
              f"  ~{len(s['text'])/15.6/60:.1f} min")
    print(f"TOTAL {total_chars} chars  ~{est_seconds/60:.1f} min of video")

    if args.dry_run:
        print("\nDry run — nothing rendered, no credits spent.")
        return

    key = os.environ.get("HEYGEN_API_KEY")
    if not key:
        sys.exit("Set HEYGEN_API_KEY (HeyGen > Settings > API).")

    slide_map = json.load(open(args.slide_map)) if args.slide_map else {}

    manifest = {"script": args.script, "avatar": AVATAR, "voice": VOICE, "segments": []}
    for i, seg in enumerate(segments, 1):
        slide = slide_map.get(str(i)) or slide_map.get(i)
        slide_url = f"{args.slides_base.rstrip('/')}/{slide}" if (slide and args.slides_base) else ""
        print(f"\n[{i}/{len(segments)}] rendering {' + '.join(seg['titles'])[:50]}...")
        vid = render(seg, i, len(segments), key, slide_url, args.title)
        print(f"    video_id={vid}  waiting...")
        d = wait_for(vid, key)
        print(f"    done: {d.get('duration')}s")
        manifest["segments"].append({
            "index": i,
            "titles": seg["titles"],
            "video_id": vid,
            "duration": d.get("duration"),
            "video_url": d.get("video_url"),
            "slide": slide,
            "chars": len(seg["text"]),
            "motion": motion_for(seg["titles"][0]),
        })
        json.dump(manifest, open(args.out, "w"), indent=2)

    print(f"\nWrote {args.out} — {len(manifest['segments'])} segments.")
    print("Download each video_url and commit as training-video-N.mp4 "
          "(signed URLs expire, so download promptly).")


if __name__ == "__main__":
    main()
