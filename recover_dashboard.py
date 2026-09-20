import json

with open(r'C:\Users\nariy\.gemini\antigravity\brain\0add8caa-7350-41b7-836d-781ac82bcf9a\.system_generated\logs\transcript.jsonl', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        calls = data.get('tool_calls', [])
        for call in calls:
            if call.get('name') == 'default_api:write_to_file':
                args = call.get('arguments', {})
                if 'Dashboard.tsx' in args.get('TargetFile', ''):
                    content = args.get('CodeContent', '')
                    if content:
                        with open(r'D:\Desktop\Vault\PROJECT\AURELIS\frontend\src\components\Dashboard.tsx', 'w', encoding='utf-8') as out:
                            out.write(content)
                        print("RECOVERED Dashboard.tsx!")
