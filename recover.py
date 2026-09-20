import json
import os

transcript_path = r"C:\Users\nariy\.gemini\antigravity\brain\0add8caa-7350-41b7-836d-781ac82bcf9a\.system_generated\logs\transcript.jsonl"
recover_dir = r"D:\Desktop\Vault\PROJECT\AURELIS\recovered"
os.makedirs(recover_dir, exist_ok=True)

files_content = {}

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except:
            continue
            
        # Extract from write_to_file
        if "tool_calls" in data:
            for tc in data["tool_calls"]:
                if tc.get("name") == "write_to_file":
                    args = tc.get("args", {})
                    path = args.get("TargetFile")
                    content = args.get("CodeContent")
                    if path and content:
                        files_content[os.path.basename(path)] = content
        
        # Extract from replace_file_content (if we need it, though write_to_file is usually full)
        
        # Extract from view_file response
        if data.get("type") == "TOOL_RESPONSE":
            content = data.get("content", "")
            if "Total Lines:" in content and "File Path:" in content:
                # Parse view_file output
                lines = content.split('\n')
                file_path = None
                code_lines = []
                capturing = False
                for i, l in enumerate(lines):
                    if l.startswith("File Path:"):
                        file_path = l.split("`")[1].split("file:///")[-1]
                        # handle windows paths
                        if file_path.startswith("d:"):
                            file_path = "d:" + file_path[2:]
                    elif "The following code has been modified to include a line number" in l:
                        capturing = True
                        continue
                    elif "The above content shows the entire, complete file contents" in l or "The above content shows a partial view" in l:
                        capturing = False
                    elif capturing:
                        # Format is <line_number>: <original_line>
                        if ": " in l:
                            code_lines.append(l.split(": ", 1)[1])
                
                if file_path and code_lines:
                    new_content = "\n".join(code_lines)
                    basename = os.path.basename(file_path)
                    if basename not in files_content or len(new_content) > len(files_content[basename]):
                        files_content[basename] = new_content

# Write out recovered files
for basename, content in files_content.items():
    basename = basename.strip('"\'')
    print(f"Recovered: {basename}")
    with open(os.path.join(recover_dir, basename), 'w', encoding='utf-8') as out:
        out.write(content)

print(f"Total recovered: {len(files_content)}")
