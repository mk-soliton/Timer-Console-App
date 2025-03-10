# issues_found will be true when any errors 
# are catched by the below packages
issues_found=false

# Flake8
printf "\nFlake8 Checking........."
result=$(poetry run flake8 src --show-source)
if [ ! -z "$result" ]; then
    printf "\e[41mIssues Found\e[0m"
    printf "\n\n$result\n"
    issues_found=true
else
    printf "\e[42mNo Issues Found\e[0m\n"
fi

# Pydocstyle
printf "\nPydocstyle Checking....."
result=$(poetry run pydocstyle src)
if [ ! -z "$result" ]; then
    printf "\e[41mIssues Found\e[0m"
    printf "\n\n$result\n"
    issues_found=true
else
    printf "\e[42mNo Issues Found\e[0m\n"
fi

# MyPy
printf "\nMyPy Checking..........."
result=$(poetry run mypy --pretty src)
if [[ $result =~ ^Success:\ no\ issues\ found\ in\ [0-9]+\ source\ (file|files)$ ]]; then
    printf "\e[42mNo Issues Found\e[0m\n"
else
    printf "\e[41mIssues Found\e[0m\n"
    printf "\n\n$result\n"
    issues_found=true
fi

if [ $issues_found == true ]; then
    printf "\nIssues Found in your code...\nPlease format your code based on the above suggestions given...\n"
    exit 1
fi
