import os
import re

# Walk through src directory
for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace ft.icons. with ft.Icons.
            new_content = content.replace('ft.icons.', 'ft.Icons.')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated: {filepath}")

print("Done!")
