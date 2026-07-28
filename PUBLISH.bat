@echo off
setlocal
cd /d "%~dp0"

echo.
echo  ============================================================
echo   TPP Onboarding Portal  -  Publish Documents
echo  ============================================================
echo.
echo  Scanning the documents folders...
echo.

python build_manifest.py
if errorlevel 1 (
  echo.
  echo  Could not build the document list. Nothing has been published.
  echo  Send this window to Teon / your developer.
  echo.
  pause
  exit /b 1
)

echo.
echo  Publishing to the website...
echo.

git add -A
git diff --cached --quiet
if not errorlevel 1 (
  echo  No changes to publish - the site already matches your documents folder.
  echo.
  pause
  exit /b 0
)

git commit -m "Update portal documents" >nul
if errorlevel 1 (
  echo  Could not save the change. Nothing has been published.
  pause
  exit /b 1
)

git push
if errorlevel 1 (
  echo.
  echo  Could not upload. Check your internet connection and try again.
  echo  If it keeps failing you may need to sign in to GitHub again.
  echo.
  pause
  exit /b 1
)

echo.
echo  ============================================================
echo   Done. The portal updates in about a minute:
echo   https://teond1090.github.io/tpp-onboarding-portal/#documents
echo  ============================================================
echo.
pause
