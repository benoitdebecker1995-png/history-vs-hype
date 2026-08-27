$ErrorActionPreference = 'Stop'

$ffmpeg = 'C:\Program Files\ShareX\ffmpeg.exe'
$native = 'G:\History vs Hype\video-projects\_IN_PRODUCTION\62-volhynia-massacre-untranslated-2026\assets\youtube-native'

function New-DocumentMotion {
    param(
        [Parameter(Mandatory)] [string] $Wide,
        [Parameter(Mandatory)] [string] $Detail,
        [Parameter(Mandatory)] [string] $Output
    )

    $filter = "[0:v]zoompan=z='min(zoom+0.00045,1.035)':d=90:s=1920x1080:fps=30,setsar=1[a];[1:v]zoompan=z='min(zoom+0.00035,1.028)':d=90:s=1920x1080:fps=30,setsar=1[b];[a][b]xfade=transition=fade:duration=0.30:offset=2.70,format=yuv420p[v]"
    & $ffmpeg -hide_banner -loglevel error -y `
        -loop 1 -t 3 -i (Join-Path $native $Wide) `
        -loop 1 -t 3 -i (Join-Path $native $Detail) `
        -filter_complex $filter -map '[v]' -t 5.70 -an `
        -c:v libx264 -crf 16 -preset medium -movflags +faststart `
        (Join-Path $native $Output)
    if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed for $Output" }
}

function New-MapMotion {
    param(
        [Parameter(Mandatory)] [string] $Still,
        [Parameter(Mandatory)] [string] $Output,
        [int] $Seconds = 7
    )

    $frames = $Seconds * 30
    $filter = "zoompan=z='min(zoom+0.00014,1.03)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${frames}:s=1920x1080:fps=30,setsar=1,format=yuv420p"
    & $ffmpeg -hide_banner -loglevel error -y `
        -loop 1 -t $Seconds -i (Join-Path $native $Still) `
        -vf $filter -t $Seconds -an `
        -c:v libx264 -crf 16 -preset medium -movflags +faststart `
        (Join-Path $native $Output)
    if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed for $Output" }
}

New-DocumentMotion '01-klymchak-page-wide.png' '02-klymchak-quote-detail.png' 'motion-klymchak-5s.mp4'
New-DocumentMotion '03-order11-page-wide.png' '04-order11-language-detail.png' 'motion-order11-5s.mp4'
New-DocumentMotion '06-kolodzinskyi-page-wide.png' '07-kolodzinskyi-quote-detail.png' 'motion-kolodzinskyi-5s.mp4'
New-DocumentMotion '08-stelmashchuk-page-wide.png' '09-stelmashchuk-directive-detail.png' 'motion-stelmashchuk-5s.mp4'
New-DocumentMotion '10-litopys-page-wide.png' '11-litopys-oleh-detail.png' 'motion-litopys-5s.mp4'
New-MapMotion '12-volhynia-map-fullscreen.png' 'motion-volhynia-map-7s.mp4' 7
New-MapMotion '13-poryck-map-fullscreen.png' 'motion-poryck-map-6s.mp4' 6

Write-Output 'Rendered seven silent YouTube-native motion clips.'
