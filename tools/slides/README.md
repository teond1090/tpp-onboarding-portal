# Slide decks for the training videos

`gen_secure.py` and `gen_rv.py` write one HTML file per slide; `render_slides.py`
screenshots them at 1920x1080 into the portal's `slides/secure/` and `slides/rv/`.

    cd tools/slides
    python3 gen_secure.py && python3 render_slides.py html-secure ../../slides/secure
    python3 gen_rv.py     && python3 render_slides.py html-rv     ../../slides/rv

The right 640px of every slide is reserved for the presenter card. The
renderer prints `OVER` for any element that crosses that line, so a layout
fault shows up here rather than in a finished video.
