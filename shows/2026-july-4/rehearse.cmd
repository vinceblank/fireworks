@echo off
rem ── One-click virtual rehearsal for the 2026 July 4 show ──────────────
rem Starts a local web server at the repo root (needed so the browser may
rem auto-load the script/mix/effects) and opens the simulator pre-loaded.
rem Requires Python on PATH. Safe to run repeatedly (server reused).
setlocal
set PORT=8137
cd /d "%~dp0..\.."

netstat -an | findstr ":%PORT%" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
  start "fireworks-rehearsal-server" /min cmd /c "python -m http.server %PORT%"
  rem give the server a moment to come up
  ping -n 2 127.0.0.1 >nul
)

rem unique r= per launch defeats browser caching of the page itself
rem WAV, not MP3: our python-encoded MP3s lack the Xing seek header, so
rem browser timecodes drift ~1.3% (user-observed: seam at 2:16.7 read 2:18)
start "" "http://localhost:%PORT%/tools/rehearsal/rehearsal.html?r=%RANDOM%%RANDOM%&script=shows/2026-july-4/cobra.rehearsal.csv&audio=shows/2026-july-4/audio/2026-show-mix.wav&effects=shows/2026-july-4/effects.json&recipe=shows/2026-july-4/mix-recipe.json&highlights=shows/2026-july-4/highlights.json"
endlocal
