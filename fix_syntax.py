import sys

# Read the file
with open('maingui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the escaped docstring
content = content.replace('\\\"\\\"\\\"Cancel the ongoing download\\\"\\\"\\\"', '\"\"\"Cancel the ongoing download\"\"\"')

# Write it back
with open('maingui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed docstring syntax error")
