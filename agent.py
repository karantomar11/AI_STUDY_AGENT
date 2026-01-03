# This is the code for AI Study Agent.
# It automatically finds the first PDF in the folder to process.
# It saves the final .docx files into a "Final_Notes" folder.
#  It automatically deletes the temporary .md files.
#
# --- SETUP ---
# 1. Install Pandoc: https://pandoc.org/installing.html
# 2. In your terminal, run: pip3 install google-generativeai pdfplumber pypandoc
#
# --- USAGE ---
# 1. Place this `agent.py` script and ONE lecture PDF in a folder.
# 2. Paste Google AI API key below.
# 3. Run `python3 agent.py` in your terminal.
# 4. Check the "Final_Notes" folder for your documents!

import pdfplumber
import google.generativeai as genai
import os
try:
    import pypandoc
except ImportError:
    pypandoc = None

import asyncio
import json
import re
from openai import OpenAI
import audio_generator

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 1. CONFIGURATION ---
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', "https://openrouter.ai/api/v1")

if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY not found in .env file.")
if not OPENROUTER_API_KEY:
    print("Warning: OPENROUTER_API_KEY not found in .env file.")

# The PDF_FILE_PATH is now found automatically!

# --- 2. HELPER FUNCTIONS (The Core Machinery) ---

def extract_text_from_pdf(pdf_path):
    """Opens and reads the text from a PDF file."""
    if not os.path.exists(pdf_path):
        return "Error: PDF file not found."
    print(f"Reading text from {pdf_path}...")
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    print("Text extraction complete.")
    return full_text

import time

def generate_ai_response(api_key, prompt):
    """Sends the request to the Gemini AI and gets the response, with retry logic."""
    print("Sending request to AI... This may take a moment.")
    
    # Retry configuration
    max_retries = 3
    retry_delay = 10  # seconds
    
    genai.configure(api_key=api_key)
    
    # Set up safe settings to avoid blocking academic content
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    
    # UPDATED: Using 'gemini-flash-latest' (1.5 Flash) which is more stable/generous than 2.0 Preview
    model = genai.GenerativeModel('gemini-flash-latest')

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt, safety_settings=safety_settings)
            print("AI response received.")
            return response.text
        except Exception as e:
            print(f"Warning: AI request failed (Attempt {attempt + 1}/{max_retries}). Details: {e}")
            if "429" in str(e):
                print(f"Quota exceeded. Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                # For non-quota errors, maybe waiting won't help, but let's try once more just in case
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    print("Error: Max retries reached. Could not get response.")
                    return None
    return None

def generate_podcast_script(context_text, api_key):
    """
    Generates a dialogue script using OpenRouter.
    """
    print("Connecting to OpenRouter for Script Generation...")
    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key
    )
    
    prompt = PHASE_4_PROMPT.format(input_text=context_text)
    
    try:
        completion = client.chat.completions.create(
            # extra_headers={
            #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            # },
            # UPDATED: Using the model ID you seemed to intend, based on your previous edit
            model="xiaomi/mimo-v2-flash:free", 
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating podcast script: {e}")
        return None

def save_output_to_md(output_text, filename, folder):
    """Saves the given text into a Markdown file in a specific folder."""
    md_filename = f"{filename}.md"
    full_path = os.path.join(folder, md_filename)
    print(f"Saving temporary Markdown file to {full_path}...")
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(output_text)
    print("Save complete.")
    return full_path # Return the path so we can delete it later

def convert_md_to_docx(md_content, filename, folder):
    """Converts the Markdown content to a .docx file in a specific folder."""
    if pypandoc is None:
        print("Skipping .docx conversion: pypandoc library not installed.")
        return
    
    # Fix: Sanitize content to prevent Pandoc from reading careless AI "---" dividers as failed YAML metadata
    if md_content.strip().startswith("---"):
        md_content = f"# {filename}\n\n" + md_content

    docx_filename = f"{filename}.docx"
    full_path = os.path.join(folder, docx_filename)
    print(f"Converting to Word document: {full_path}...")
    try:
        pypandoc.convert_text(md_content, 'docx', format='md', outputfile=full_path)
        print("Conversion complete.")
    except OSError:
        print("\nWARNING: Pandoc program not found. Please install from https://pandoc.org/installing.html\n")

# --- 3. THE PROMPT BLUEPRINTS (PHASES 1-4) ---
PHASE_1_PROMPT = """
Act as an expert in curriculum design. Transform the content of the provided text into an exceptionally engaging and informative **Lecture Guide**.
The guide should be structured with:
1.  **Overall Structure & Flow:** A fitting lecture title, 2-3 core learning objectives, an engaging introduction/hook, and logical segmentation of the content.
2.  **For Each Key Section:** Deep and clear key talking points, "make it click" explanations with vivid analogies, and interactive engagement strategies.
3.  **Anticipate Confusion:** Point out areas where students might get stuck and suggest ways to clarify.
4.  **Strong Conclusion:** A powerful summary of key takeaways.
Here is the raw text from the lecture:
---
{input_text}
---
"""
PHASE_2_PROMPT = """
Now, apply the specific for each part recipe for each key concept in the provided Lecture Guide.
Re-structure the entire guide so that for each topic, you provide these four distinct sections in order:
1.  **Formal Explanation:** The precise, academic definition.
2.  **Easy-to-Digest Explanation:** A simple, intuitive analogy or high-level summary.
3.  **Easy-to-Digest Example:** A concrete, step-by-step example.
4.  **Pseudocode & Explanation:** The explicit pseudocode, followed by a separate, clear explanation of how the code works.
Here is the Lecture Guide to transform:
---
{input_text}
---
"""
PHASE_3_PROMPT = """
Using the provided comprehensive guide, create a new document: **Exam Prep Notes**. The goal is to prepare a student for an exam.
The notes must be concise and focus on:
1.  **Key Definitions & Must-Memorize Concepts:** A quick-reference list.
2.  **Core Formulas & Complexities:** A summary of critical formulas and Big O complexities.
3.  **Algorithm Deep Dives:** A focused look at the mechanics of the core algorithms.
4.  **Potential Exam Questions & Detailed Answers:** A few likely exam-style questions with step-by-step solutions.
Here is the guide to distill:
---
{input_text}
---
"""

PHASE_4_PROMPT = """
Using the following comprehensive study notes (Phase 1, 2, and 3), write a dialogue script between Alex (host) and Jamie (expert).

Context Notes:
{input_text}

Requirements:
1. The script MUST be approximately 1,100 words long to ensure a 7-minute duration.
2. Alex should differ to Jamie for explanations but be a curious, energetic learner who uses relatable analogies.
3. Jamie should be the expert guide, clarifying technical logic clearly.
4. Output format MUST be a raw JSON list of objects: [{{ "speaker": "Alex", "text": "..." }}, {{ "speaker": "Jamie", "text": "..." }}]
5. Do not include any markdown formatting (like ```json ... ```) in the output, just the raw JSON string.
"""

# --- 4. THE MAIN ASSEMBLY LINE (UPGRADED) ---

def find_pdf_in_folder():
    """Scans the current folder and returns the name of the first .pdf file found."""
    for file in os.listdir('.'):
        if file.lower().endswith('.pdf'):
            print(f"Found PDF file: {file}")
            return file
    return None # Return None if no PDF is found

def clean_and_parse_json(raw_text):
    """
    Robustly cleans and parses JSON from LLM output.
    Handles markdown code blocks, missing delimiters, etc.
    """
    if not raw_text:
        return None
        
    # 1. Strip Markdown Code Blocks
    cleaned = re.sub(r'```json\s*|\s*```', '', raw_text, flags=re.IGNORECASE).strip()
    
    # 2. Try Standard Parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
        
    # 3. Aggressive Fixes (Common LLM Errors)
    try:
        # Fix 1: Missing comma between objects: } { -> }, {
        cleaned_fixed = re.sub(r'\}\s*\{', '}, {', cleaned)
        
        # Fix 2: Missing closing brace AND comma between objects: ... "text": "..." { "speaker": ...
        # We look for a closing quote, whitespace, and then the start of a new speaker object
        cleaned_fixed = re.sub(r'\"\s*\{\s*\"speaker\"', '"}, {"speaker"', cleaned_fixed)
        
        # Fix 3: Lists missing enclosing brackets
        if not cleaned_fixed.strip().startswith('['):
            cleaned_fixed = f"[{cleaned_fixed.strip()}]"
            
        return json.loads(cleaned_fixed)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON after aggressive cleaning: {e}")
        return None

async def run_workflow():
    """The main function that runs the automated workflow."""
    print("--- Main function has started. Beginning automated workflow... ---")
    
    # NEW: Debugging info
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Files in current folder: {os.listdir('.')}")
    
    # NEW: Automatically find the PDF instead of using a hardcoded path
    pdf_file_path = find_pdf_in_folder()
    if not pdf_file_path:
        print("\n❌ ERROR: No PDF file found in this folder.")
        print("Please add a PDF to this folder and run the script again.")
        return

    # NEW: Define the output folder and create it if it doesn't exist
    output_folder = "Final_Notes"
    os.makedirs(output_folder, exist_ok=True)
    print(f"Output will be saved in the '{output_folder}' folder.")
    
    base_filename = os.path.splitext(os.path.basename(pdf_file_path))[0]
    
    pdf_text = extract_text_from_pdf(pdf_file_path)
    if pdf_text and "Error" in pdf_text and len(pdf_text) < 100: # Simple check for the file-not-found error string from helper
        print(pdf_text)
        return

    # --- PHASE 1 ---
    print("\n[Phase 1] Generating Lecture Guide...")
    lecture_guide = generate_ai_response(GOOGLE_API_KEY, PHASE_1_PROMPT.format(input_text=pdf_text))
    if lecture_guide:
        print("✅ Connection to Google AI successful!")
        filename_p1 = f"{base_filename}_Phase1_Lecture_Guide"
        md_path = save_output_to_md(lecture_guide, filename_p1, output_folder)
        convert_md_to_docx(lecture_guide, filename_p1, output_folder)
        try:
            os.remove(md_path)
            print(f"Removed temporary file: {md_path}")
        except OSError as e:
            print(f"Error removing file: {e}")
    else:
        print(f"\n❌ Connection to Google AI failed. Check logs for details.")
        return

    # --- PHASE 2 ---
    print("\n[Phase 2] Applying Core Recipe...")
    structured_guide = generate_ai_response(GOOGLE_API_KEY, PHASE_2_PROMPT.format(input_text=lecture_guide))
    if structured_guide:
        filename_p2 = f"{base_filename}_Phase2_Structured_Guide"
        md_path = save_output_to_md(structured_guide, filename_p2, output_folder)
        convert_md_to_docx(structured_guide, filename_p2, output_folder)
        try:
            os.remove(md_path)
            print(f"Removed temporary file: {md_path}")
        except OSError as e:
            print(f"Error removing file: {e}")
    else:
        print("Failed to generate Phase 2 output.")
        return

    # --- PHASE 3 ---
    print("\n[Phase 3] Distilling Exam Prep Notes...")
    exam_notes = generate_ai_response(GOOGLE_API_KEY, PHASE_3_PROMPT.format(input_text=structured_guide))
    if exam_notes:
        filename_p3 = f"{base_filename}_Phase3_Exam_Prep_Notes"
        md_path = save_output_to_md(exam_notes, filename_p3, output_folder)
        convert_md_to_docx(exam_notes, filename_p3, output_folder)
        try:
            os.remove(md_path)
            print(f"Removed temporary file: {md_path}")
        except OSError as e:
            print(f"Error removing file: {e}")
    else:
        print("Failed to generate Phase 3 output.")
        return
        
    # --- PHASE 4: AUDIO OVERVIEW ---
    print("\n[Phase 4] Generating Audio Overview...")
    
    # 1. Generate Script
    print("Generating Podcast Script...")
    
    # Combine content from all phases for maximum context
    combined_context = f"""
    --- PHASE 1: LECTURE GUIDE ---
    {lecture_guide}
    
    --- PHASE 2: STRUCTURED GUIDE ---
    {structured_guide}
    
    --- PHASE 3: EXAM NOTES ---
    {exam_notes}
    """
    
    # NOTE: Using combined context (Phase 1-3) as requested
    raw_script_response = generate_podcast_script(combined_context, OPENROUTER_API_KEY)
    
    if raw_script_response:
        script_data = clean_and_parse_json(raw_script_response)
        
        if script_data:
            script_filename = "podcast_script.json"
            script_path = os.path.join(output_folder, script_filename)
        
            with open(script_path, 'w', encoding='utf-8') as f:
                json.dump(script_data, f, indent=2)
            print(f"Script saved to {script_path}")
            
            # 2. Synthesize Audio
            audio_filename = "audio_overview.mp3" # Requested name: audio_overview.mp3
            audio_path = os.path.join(output_folder, audio_filename)
            
            # Verify we are passing the output path correctly
            print(f"Synthesizing audio to: {audio_path}")
            await audio_generator.synthesize_audio(script_path, audio_path)
        else:
            print(f"Error: Failed to parse generated script as JSON details.\nRaw output:\n{raw_script_response}")
    else:
        print("Skipping Audio Phase: Script generation failed or returned empty.")

    
    print("\n--- AUTOMATED WORKFLOW COMPLETE ---")

def main():
    asyncio.run(run_workflow())

# --- 5. PHASE 4 - THE SPECIALIST TOOLKIT ---
# (This section remains the same, to be used manually)
def expand_on_detail(text_to_expand, api_key):
    """(Phase 4 Tool) Uses the AI to expand on a specific piece of text."""
    print("\n--- Using the Detail Expander Tool ---")
    prompt = f"""
    Expand on the selected text and make it longer by 25-50% by elaborating on existing ideas, providing more examples, and/or fleshing out an idea in more detail. Focus on enhancing and adding depth to existing topics instead of introducing new concepts. The added content should still flow well with the surrounding text.

    Here is the text to expand upon:
    ---
    {text_to_expand}
    ---
    """
    return generate_ai_response(api_key, prompt)

def ensure_source_accuracy(code_to_check, source_material_context, api_key):
    """(Phase 4 Tool) Asks the AI to rewrite code based on source material."""
    print("\n--- Using the Source Accuracy Tool ---")
    prompt = f"""
    Please analyze the following pseudocode. Your task is to rewrite it so it *explicitly* matches the logic implied in the provided source material context. After the code block, provide a separate, clear explanation of the code's logic, step-by-step, instead of using inline comments.

    Source Material Context: "{source_material_context}"
    
    Pseudocode to check and rewrite:
    ---
    {code_to_check}
    ---
    """
    return generate_ai_response(api_key, prompt)

# --- 6. SCRIPT IGNITION ---
if __name__ == "__main__":
    main()
