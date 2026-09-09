# Regenera tools/img_pipeline/.certs/win-root-bundle.pem
#
# La red del estudio intercepta TLS con la CA "Avast Web/Mail Shield Root", asi
# que pip/git fallan con CERTIFICATE_VERIFY_FAILED contra PyPI y GitHub. Este
# script vuelca TODAS las raices de confianza de Windows (que incluyen la de
# Avast) a un bundle PEM, y le anexa el bundle de Mozilla que trae certifi.
#
# Uso:  powershell -ExecutionPolicy Bypass -File tools\img_pipeline\make_cert_bundle.ps1
# Luego: $env:PIP_CERT = "tools\img_pipeline\.certs\win-root-bundle.pem"
#        $env:GIT_SSL_CAINFO = $env:PIP_CERT

$ErrorActionPreference = "Stop"
$dir = Join-Path $PSScriptRoot ".certs"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$out = Join-Path $dir "win-root-bundle.pem"

$certs = @()
$certs += Get-ChildItem Cert:\LocalMachine\Root -ErrorAction SilentlyContinue
$certs += Get-ChildItem Cert:\CurrentUser\Root  -ErrorAction SilentlyContinue

$seen = @{}
$sb = New-Object System.Text.StringBuilder
foreach ($c in $certs) {
    if ($seen.ContainsKey($c.Thumbprint)) { continue }
    $seen[$c.Thumbprint] = $true
    $b64 = [System.Convert]::ToBase64String($c.RawData, 'InsertLineBreaks')
    [void]$sb.AppendLine("# " + $c.Subject)
    [void]$sb.AppendLine("-----BEGIN CERTIFICATE-----")
    [void]$sb.AppendLine($b64)
    [void]$sb.AppendLine("-----END CERTIFICATE-----")
}
Set-Content -Path $out -Value $sb.ToString() -Encoding ascii

# Anexar el bundle de Mozilla (certifi) si esta disponible en el Python del sistema.
try {
    $certifi = & "C:\tools\miniconda3\python.exe" -c "import certifi; print(certifi.where())" 2>$null
    if ($certifi -and (Test-Path $certifi)) {
        Add-Content -Path $out -Value "`n# --- Mozilla bundle (certifi) ---" -Encoding ascii
        Get-Content $certifi | Add-Content -Path $out -Encoding ascii
    }
} catch { }

$avast = (Select-String -Path $out -Pattern "Avast Web/Mail Shield Root" -Quiet)
"Bundle: $out"
"Raices de Windows exportadas: $($seen.Count)"
"CA de Avast incluida: $avast"
