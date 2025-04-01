#!/bin/bash

TEMPLATE=tests/_template_test_script.py

for script in ./ch*/*.py; do
  # derive test path from script path
  folder=$(dirname "$script")
  base=$(basename "$script" .py)
  test_folder="tests/${folder}"
  test_file="${test_folder}/test_${base}.py"

  mkdir -p "$test_folder"

  # skip if already exists
  if [ -f "$test_file" ]; then
    echo "SKIP $test_file (already exists)"
    continue
  fi

  # write new test file
  sed "s|__SCRIPT__|$script|" "$TEMPLATE" > "$test_file"
  echo "✔︎ Created $test_file"
done
