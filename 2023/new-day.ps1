$day = $args[0]
(get-content -path .\day_template.py -raw) -replace '9',$day | set-content .\day$day.py
(get-content -path .\day_template_tests.py -raw) -replace '9',$day | set-content .\day${day}_tests.py
new-item day${day}_input.txt -force | Out-Null
# copy-item .\day_template.py .\day$day.py
