import re

# Prompt for file paths
input_file = input("Enter the input file path: ").strip("\"")
output_file = input("Enter the output file path: ").strip("\"")

# Read the input file
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Prompt for regex pattern
pattern = input("Enter the pattern: ")

# Find all matches using the pattern
matches = re.findall(pattern, content)

# Output results separated by newlines
output = '\n'.join(matches)
print(output)

# Save to output file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(output)

