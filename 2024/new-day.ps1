$day = $args[0]
$day = "{0:D2}" -f [int]$day
(get-content -path .\day_template._py -raw) -replace '9',$day | set-content .\day$day.py
(get-content -path .\day_template_tests._py -raw) -replace '9',$day | set-content .\day${day}_tests.py
new-item day${day}_input.txt -force | Out-Null
# copy-item .\day_template.py .\day$day.py
