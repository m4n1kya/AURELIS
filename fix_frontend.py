import os

def fix_file(path):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '\\"' in content or '\\n' in content:
        content = content.replace('\\"', '"').replace('\\n', '\n')
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed {path}")

def fix_dir(d):
    for root, dirs, files in os.walk(d):
        for f in files:
            if f.endswith(('.ts', '.tsx', '.css', '.json', '.js', '.jsx')):
                fix_file(os.path.join(root, f))

fix_dir(r"D:\Desktop\Vault\PROJECT\AURELIS\frontend\src")
fix_file(r"D:\Desktop\Vault\PROJECT\AURELIS\frontend\tailwind.config.ts")
fix_file(r"D:\Desktop\Vault\PROJECT\AURELIS\frontend\next.config.ts")
fix_file(r"D:\Desktop\Vault\PROJECT\AURELIS\frontend\postcss.config.js")
fix_file(r"D:\Desktop\Vault\PROJECT\AURELIS\frontend\tsconfig.json")
