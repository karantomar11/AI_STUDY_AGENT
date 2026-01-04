import os
import re
import base64
import requests
import json
from openai import OpenAI

INTERNAL_VISUALIZER_PROMPT = """
ACT AS: A Senior Visual Strategist. 
TASK: Create a professional, MULTI-COLORED Mermaid.js Mindmap.

CONFIG (MANDATORY):
- Keyword: mindmap

VISUAL HIERARCHY & DENSITY CONTROL:
1. ROOT: (("Subject")) -> Double parentheses + quotes.
2. PILLARS (Level 1): ("Category") -> LIMIT TO EXACTLY 5 PILLARS.
   - These will receive distinct, high-contrast colors (Blue, Green, Yellow, Purple, Orange).
3. ATOMIC CONCEPTS (Level 2): ["Detail"] -> LIMIT TO EXACTLY 4 PER PILLAR.
   - This prevents the 'congested' look and ensures the diagram fits on one page.

FORMATTING RULES:
- Use 2-space indentation strictly.
- WRAP ALL TEXT IN DOUBLE QUOTES.
- USE ONLY ALPHANUMERIC CHARACTERS (No symbols like &, /, -, or %).

SOURCE CONTEXT:
---
{context}
---
"""

def generate_mindmap_png(context_text, api_key, output_path):
    print("\n--- [Phase 6] Visualizer Module Initialized ---")
    print("Connecting to Visualizer Model (xiaomi/mimo-v2-flash)...")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    try:
        # 1. Generate Mermaid Code
        completion = client.chat.completions.create(
            model="xiaomi/mimo-v2-flash:free",
            messages=[{"role": "user", "content": INTERNAL_VISUALIZER_PROMPT.format(context=context_text)}]
        )
        raw_response = completion.choices[0].message.content
        print("Visual Structure Generated. Sanitizing...")

        # 1. STRIP MARKDOWN ARTIFACTS
        clean_code = re.sub(r'```mermaid\s*|\s*```', '', raw_response).strip()

        # 2. THE NUCLEAR SCRUBBER (Preserves Indentation, Kills Special Chars)
        lines = clean_code.split('\n')
        sanitized_lines = []

        for line in lines:
            # SKIP empty lines or COMMENT/INIT lines to avoid 400 Errors
            if not line.strip() or "%%" in line:
                continue
            
            # Ensure mindmap keyword is preserved strictly
            if "mindmap" in line.lower():
                sanitized_lines.append("mindmap")
                continue

            # Preserve leading whitespace
            indent_match = re.match(r"^\s*", line)
            indent = indent_match.group(0) if indent_match else ""
            content = line.strip()

            # Identify brackets: ((" ")), (" "), or [" "]
            match = re.match(r"^([\(\[\)]+)(.+?)([\)\]\)]+)$", content)
            
            if match:
                opening = match.group(1)
                text = match.group(2)
                closing = match.group(3)

                # NUCLEAR SCRUB: Keep only letters, numbers, and spaces
                clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
                
                sanitized_lines.append(f"{indent}{opening}\"{clean_text.strip()}\"{closing}")
            else:
                # Fallback
                clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', content)
                sanitized_lines.append(f"{indent}\"{clean_text.strip()}\"")

        final_code = "\n".join(sanitized_lines)
        
        if not final_code.strip():
            print("❌ Error: Generated Mermaid code is empty after sanitization.")
            return False
        
        # 3. ENCODING (JSON State Protocol)
        # We use 'default' theme. Removed 'look': 'handDrawn' as it can cause 400 errors on some renderers.
        state = {
            "code": final_code,
            "mermaid": {"theme": "default"}
        }
        json_str = json.dumps(state)
        
        # Use urlsafe_b64encode to ensure the link doesn't break
        base64_str = base64.urlsafe_b64encode(json_str.encode('utf-8')).decode('ascii')
        
        url = f"https://mermaid.ink/img/{base64_str}"
        print("Rendering Infographic via Mermaid.Ink...")
        
        try:
            # Fix: Add User-Agent to avoid being blocked by the server
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Clean, Multi-Colored Infographic Saved: {output_path}")
                return True
            else:
                print(f"❌ Renderer Refused Request (Status {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            return False

    except Exception as e:
        print(f"❌ Visualizer Failed: {e}")
        return False