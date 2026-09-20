cd d:\\Desktop\\Vault\\PROJECT\\AURELIS\\hackerrank-orchestrate-september26\\code
python main.py
cd ..
if (Test-Path code.zip) { Remove-Item code.zip }
Compress-Archive -Path code -DestinationPath code.zip -Force
Write-Host \"Done!\"
