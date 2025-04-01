#!/bin/bash

TEMPLATE=tests/_template_test_script.py

# Hardcoded folder-to-chapter map
declare -A FOLDER_TO_CHAPTER=(
  [ch2_getting_started]=ch2
  [ch3_chat_models]=ch3
  [ch4_prompt_templates]=ch4
  [ch5_chains]=ch5
  [ch6_structured_output]=ch6
  [ch7_messages]=ch7
)

echo "🧪 Generating test files from lesson scripts"

for script in ./ch*/*.py; do
  folder=$(dirname "$script" | sed 's|^\./||')   # e.g. ch3_chat_models
  file=$(basename "$script" .py)                # e.g. 3_model_parameters
  base=$(echo "$file" | sed -E 's/^[0-9]+_//')   # e.g. model_parameters
  num=$(echo "$file" | grep -oE '^[0-9]+')       # e.g. 3

  chapter=${FOLDER_TO_CHAPTER[$folder]}
  if [ -z "$chapter" ]; then
    echo "❌ Unknown folder $folder — skipping"
    continue
  fi

  test_folder="tests/$chapter/lesson$num"
  test_file="$test_folder/test_${base}.py"

  if [ -f "$test_file" ]; then
    echo "SKIP $test_file (already exists)"
    continue
  fi

  mkdir -p "$test_folder"
  sed "s|__SCRIPT__|$script|" "$TEMPLATE" > "$test_file"
  echo "✔︎ Created $test_file → from $script"
done
