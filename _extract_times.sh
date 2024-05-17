#!/bin/bash

# Ensure times.txt exists and is empty
> times.txt

# Iterate over all files ending with 'stat.txt'
for file in *stat.txt; do
    # Extract the elapsed time and append it to times.txt
    grep "elapsed time" "$file" | awk -F': ' '{print $2}' >> times.txt
done

echo "Elapsed times have been copied to times.txt."