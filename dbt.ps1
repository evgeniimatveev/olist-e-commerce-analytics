$dbt = "C:\Users\GAMING\AppData\Roaming\Python\Python314\Scripts\dbt.exe"
Set-Location "C:\Users\GAMING\olist-dbt-duckdb"
& $dbt @args --profiles-dir .
