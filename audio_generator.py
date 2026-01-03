import edge_tts
import json
import asyncio

async def synthesize_audio(script_json_path, output_path):
    """
    Reads a JSON script and synthesizes audio using edge-tts.
    
    Args:
        script_json_path (str): Path to the JSON script file.
        output_path (str): Path to save the generates MP3.
    """
    print(f"Reading script from {script_json_path}...")
    try:
        with open(script_json_path, 'r', encoding='utf-8') as f:
            script = json.load(f)
    except FileNotFoundError:
        print(f"Error: Script file {script_json_path} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {script_json_path}.")
        return

    # Voice assignments as per requirements
    # Alex: en-US-AndrewNeural (Energetic Male)
    # Jamie: en-US-AvaNeural (Professional Female)
    VOICE_MAP = {
        "Alex": "en-US-AndrewNeural",
        "Jamie": "en-US-AvaNeural"
    }

    print(f"Synthesizing audio to {output_path}...")
    
    # We will collect all audio data in memory and write it once (or append to file).
    # Ideally, for long audio, we might want to append to file to save memory, 
    # but for 7 minutes, memory should be fine.
    
    final_audio = b""
    
    for item in script:
        speaker = item.get("speaker")
        text = item.get("text")
        
        if not speaker or not text:
            continue
            
        voice = VOICE_MAP.get(speaker, "en-US-AndrewNeural") # Default to Alex
        
        # Rate set to -5% for natural study pace
        communicate = edge_tts.Communicate(text, voice, rate="-5%")
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                final_audio += chunk["data"]
                
    with open(output_path, "wb") as f:
        f.write(final_audio)

    print(f"Audio synthesis complete! Saved to {output_path}")

if __name__ == "__main__":
    # Test block
    dummy_script = [
        {"speaker": "Alex", "text": "Hey Jamie, are we ready to learn?"},
        {"speaker": "Jamie", "text": "Absolutely, Alex. Let's dive in."}
    ]
    with open("test_script.json", "w") as f:
        json.dump(dummy_script, f)
    
    asyncio.run(synthesize_audio("test_script.json", "test_audio.mp3"))
