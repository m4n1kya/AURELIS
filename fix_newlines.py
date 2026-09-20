import os
import json

directory = r"D:\Desktop\Vault\PROJECT\AURELIS\engine"
for filename in os.listdir(directory):
    if filename.endswith(".py"):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('"') and content.endswith('"'):
            try:
                # Wrap it in quotes as a JSON string to parse
                real_content = json.loads(content)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(real_content)
                print(f"Fixed {filename}")
            except Exception as e:
                print(f"Error fixing {filename}: {e}")
