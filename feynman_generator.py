import os
from openai import OpenAI
import doc_styler

def generate_feynman_doc(master_context, api_key, output_path):
    """
    Generates a Feynman Mastery Page using OpenRouter (MiMo-v2-Flash) and styles it using doc_styler.
    """
    print("\n--- [Phase 5] Feynman Mastery Module Initialized ---")
    print("Connecting to OpenRouter (Model: xiaomi/mimo-v2-flash:free) with Reasoning Enabled...")

    client = OpenAI(
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=api_key
    )

    prompt = """
    Act as Richard Feynman. Synthesize all previous context into a final **Feynman Mastery Page**.

    OUTPUT SECTIONS:
    1. **The Core Essence:** 1 sentence (no jargon).
    2. **The 12-Year-Old Analogy:** Use a relatable ==playground analogy==.
    3. **The Jargon Translator:** 3-column table: | Term | Academic | ==Human== |
    4. **The "Blind Spot" Audit:** Identify 3 common misconceptions in **bold**.
    5. **The Real-World "So What?":** Why this matters for a career.

    STRICT FORMATTING RULES:
    1. Wrap ALL formulas or technical math in $ ... $ (e.g. $F=ma$).
    2. Wrap ALL analogies in == ... ==.
    3. Use __underline__ for critical warnings or "blind spots".

    MASTER CONTEXT:
    ---
    {context}
    ---
    """.format(context=master_context)

    try:
        completion = client.chat.completions.create(
            model="xiaomi/mimo-v2-flash:free",
            messages=[
                {"role": "user", "content": prompt}
            ],
            extra_body={"reasoning_enabled": True} # Activate Reasoning Engine
        )
        
        markdown_text = completion.choices[0].message.content
        
        if not markdown_text:
            print("Error: Empty response from AI.")
            return False

        # --- Create Styled Document ---
        output_docx = output_path # Renaming for clarity as per the edit
        print(f"Styling Feynman Mastery Page to {output_docx}...")
        
        doc_styler.create_styled_docx(markdown_text, output_docx, title="Feynman Mastery")
        
        lines = markdown_text.split('\n')
        print(f"✅ Phase 5 Mastery Page Saved: {output_docx}")
        # print(f"   (Generated {len(lines)} lines of synthesized knowledge)") # Optional clutter removal

        # --- Extract and print the 12-Year-Old Analogy ---
        analogy_text = []
        capture = False
        found_analogy = False
        
        for line in lines:
            if "The 12-Year-Old Analogy" in line:
                capture = True
                found_analogy = True
                continue # Skip the header itself
            if capture:
                if any(header in line for header in ["The Jargon Translator", "The \"Blind Spot\" Audit"]):
                    capture = False
                    break
                analogy_text.append(line)
        
        if found_analogy:
            print("\n".join(analogy_text).strip())
        else:
            print("(Analogy section not strictly found in output, printing first 500 chars of response instead)")
            print(response_text[:500] + "...")
            
        return True

    except Exception as e:
        print(f"Error in Feynman Module: {e}")
        return False
