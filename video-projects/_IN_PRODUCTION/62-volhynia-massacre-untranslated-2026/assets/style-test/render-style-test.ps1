$ErrorActionPreference = 'Stop'

$ffmpeg = 'C:\Program Files\ShareX\ffmpeg.exe'
$project = 'G:\History vs Hype\video-projects\_IN_PRODUCTION\62-volhynia-massacre-untranslated-2026'
$timeline = Join-Path $project 'rough cut.mov'
$page = Join-Path $project '_research\genealogy\mcbride-p648.png'
$filter = Join-Path $project 'assets\style-test\style-test-filter.txt'
$output = Join-Path $project 'assets\style-test\VOLHYNIA-STYLE-TEST-v1.mp4'

& $ffmpeg -hide_banner -y `
  -i $timeline `
  -loop 1 -framerate 30 -t 8.5 -i $page `
  -filter_complex_script $filter `
  -map '[v]' -map '0:a:0' `
  -t 46.733 `
  -c:v libx264 -preset medium -crf 17 -pix_fmt yuv420p `
  -c:a aac -b:a 256k `
  -movflags +faststart `
  $output

if ($LASTEXITCODE -ne 0) {
  throw "Style-test render failed with exit code $LASTEXITCODE"
}

Get-Item -LiteralPath $output | Select-Object FullName, Length, LastWriteTime
