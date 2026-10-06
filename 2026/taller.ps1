param(
    [ValidateSet('probar', 'servir', 'exportar')]
    [string]$Accion = 'probar'
)
$ErrorActionPreference = 'Stop'
$pythonTaller = Join-Path $PSScriptRoot '../.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonTaller)) {
    throw 'Falta el entorno .venv. Sigue la sección de preparación del README de 2026.'
}
Push-Location $PSScriptRoot
try {
    if ($Accion -eq 'servir') {
        & $pythonTaller app.py
    } elseif ($Accion -eq 'exportar') {
        & $pythonTaller freeze.py
    } else {
        & $pythonTaller validate.py
        if ($LASTEXITCODE -ne 0) { throw 'Hay snippets inválidos.' }
        & $pythonTaller -m unittest discover -s tests -v
    }
    if ($LASTEXITCODE -ne 0) { throw 'La operación no terminó correctamente.' }
} finally {
    Pop-Location
}
