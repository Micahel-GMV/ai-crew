#!/bin/bash

# Array of strings
strings=("human" "Stage" "REST service" "" "GET request" "localhost:8085" "endpoint" "/greet" "HTTP" "Status Code" "200" "400" "parameter: name" "\"answer\": \"Hello [NAME]!\"" "{" "}")

# Directory to search in (modify as needed)
search_directory="./"

# Destination folder (hardcoded)
dest_folder="./noticeable"

min_lines=5 # Minimum number of lines
max_lines=50 # Maximum number of lines

# Ensure the destination folder exists
mkdir -p "$dest_folder"

# Function to check if file has between min and max lines (inclusive)
function has_valid_num_lines() {
    local file=$1
    local num_lines=$(wc -l < "$file")
    if [[ $num_lines -lt $min_lines ]] || [[ $num_lines -gt $max_lines ]]; then
        return 1 # Not in range, return false
    fi
    return 0 # In range, return true
}

# Function to check if all strings are in file
function contains_all_strings() {
    local file=$1
    for str in "${strings[@]}"; do
        if ! grep -qFi "$str" "$file"; then
            echo "String $str is not found."
            return 1 # String not found, return false
        fi
    done
    return 0 # All strings found, return true
}

# Search files and copy if they contain all of the strings and have valid number of lines
for file in "$search_directory"/*; do
    if [[ -f "$file" ]] && has_valid_num_lines "$file"; then
        if contains_all_strings "$file"; then
            echo "Copying $file to $dest_folder because it contains all specified strings and has between $min_lines and $max_lines lines"
            cp "$file" "$dest_folder"
        else
            echo "Not copying $file because not all strings were found"
        fi
    else
        echo "Not copying $file because it does not have between $min_lines and $max_lines lines"
    fi
done

echo "Operation completed."