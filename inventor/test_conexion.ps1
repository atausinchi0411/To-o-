# Prueba de conexión con Autodesk Inventor
# Uso: con Inventor ABIERTO, ejecutar en Windows PowerShell 5.1 (no PowerShell 7):
#   powershell -ExecutionPolicy Bypass -File .\inventor\test_conexion.ps1
# Qué hace: se conecta a Inventor, muestra la versión y crea una pieza nueva
# con un cilindro de 125 mm de diámetro x 147 mm de alto (calibre y carrera del QSM11).
# No guarda nada ni modifica archivos existentes.

$ErrorActionPreference = 'Stop'

try {
    $inv = [Runtime.InteropServices.Marshal]::GetActiveObject('Inventor.Application')
} catch {
    Write-Host 'ERROR: no encuentro Inventor abierto. Abre Inventor y vuelve a ejecutar este script.' -ForegroundColor Red
    exit 1
}
Write-Host ('Conectado a Inventor ' + $inv.SoftwareVersion.DisplayVersion) -ForegroundColor Green

# Constantes de la API de Inventor
$kPartDocumentObject      = 12290
$kJoinOperation           = 20481
$kPositiveExtentDirection = 20993

# Pieza nueva con la plantilla por defecto
$template = $inv.FileManager.GetTemplateFile($kPartDocumentObject)
$doc = $inv.Documents.Add($kPartDocumentObject, $template, $true)
$cd  = $doc.ComponentDefinition
$tg  = $inv.TransientGeometry

# Boceto en el plano XY y círculo de radio 62,5 mm (la API trabaja en cm)
$sketch = $cd.Sketches.Add($cd.WorkPlanes.Item(3))
[void]$sketch.SketchCircles.AddByCenterRadius($tg.CreatePoint2d(0, 0), 6.25)
$profile = $sketch.Profiles.AddForSolid()

# Extrusión de 147 mm
$def = $cd.Features.ExtrudeFeatures.CreateExtrudeDefinition($profile, $kJoinOperation)
$def.SetDistanceExtent(14.7, $kPositiveExtentDirection)
[void]$cd.Features.ExtrudeFeatures.Add($def)

$inv.ActiveView.Fit()
Write-Host 'OK: pieza de prueba creada (cilindro 125 x 147 mm). La conexión funciona.' -ForegroundColor Green
