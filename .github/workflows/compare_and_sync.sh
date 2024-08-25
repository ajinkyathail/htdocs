#!/bin/bash

# Compare local and remote files
while read -r remote_file; do
  # Extract the modified date and size from the remote file list
  remote_mod_time=$(echo "$remote_file" | awk '{print $1}')
  remote_size=$(echo "$remote_file" | awk '{print $2}')
  remote_path=$(echo "$remote_file" | awk '{print $3}')

  # Find corresponding local file
  local_file=$(echo "$remote_path" | sed 's|./remote_files/||')
  local_path="./$local_file"

  if [ -f "$local_path" ]; then
    local_mod_time=$(stat --format='%Y' "$local_path")
    local_size=$(stat --format='%s' "$local_path")

    # Compare modification time and size
    if [ "$remote_mod_time" -gt "$local_mod_time" ] || [ "$remote_size" -ne "$local_size" ]; then
      echo "Syncing modified file: $local_path"
      cp "$remote_path" "$local_path"
    fi
  else
    echo "New file detected: $local_path"
    cp "$remote_path" "$local_path"
  fi
done < remote_files.txt

# Remove files that are no longer in the remote directory
while read -r local_file; do
  if [ ! -f "./remote_files/$(basename "$local_file")" ]; then
    echo "Deleting local file: $local_file"
    rm "$local_file"
  fi
done < local_files.txt
