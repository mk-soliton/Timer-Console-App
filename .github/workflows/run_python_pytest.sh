# Search for pytest files
pytest_files=$(find tests -type f \( -name "test_*.py" -o -name "*_test.py" \))

# Check if pytest files are present
if [ -n "$pytest_files" ]; then
    printf "\nCheck for Test Files..................\e[42mtest files found\e[0m"
    printf "\nRunning test cases....................\e[43mstarted\e[0m\n"
    # since test files are present, run pytest with coverage
    poetry run pytest -v --cov=src 
else
    printf "\nCheck for Test Files..................\e[41mnot found\e[0m"
    printf "\nRunning test cases....................\e[43mskipping\e[0m\n"
fi
