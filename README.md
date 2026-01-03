
***

# AI Study Agent

A smart Python-based AI assistant that reads academic PDFs, structures them into multi-phase lecture notes, and automatically converts them into `.docx` exam-prep documents.  
Built using the **Google Gemini AI API**, this lightweight project demonstrates how generative AI can transform raw educational text into structured, self-guided study material.

***

## 🎯 Overview

**AI Study Agent** automates your study workflow by analyzing lecture PDFs and producing a complete multi-modal study pack:
1. **Lecture Architecture Guide** (Phase 1)
2. **Deep-Technical Systems Blueprint** (Phase 2)
3. **Exam Prep Notes** (Phase 3)
4. **Audio Overview Podcast** (Phase 4)
5. **Feynman Mastery Page** (Phase 5)

It also supports an **optional Phase 4 toolkit** for expanding details and validating code against source material context.

***

## ⚡ Features

- **Automatic PDF Detection** — Finds and processes the first PDF in its folder.  
- **Gemini AI Integration** — Generates guides, summaries, and exam notes using Google’s Gemini 1.5 Flash model.  
- **Reasoning Engine (OpenRouter)** — Uses `xiaomi/mimo-v2-flash` with **Reasoning Enabled** to generate deep analogies and synthesize content.
- **Multi-Phase Summarization Flow** — Five structured stages of output, from academic blueprints to conversational audio.  
- **Audio Overview Generation** — Creates a 7-minute dialogue-based podcast (`.mp3`) summarizing the material using `edge-tts`.
- **Feynman Technique Module** — Synthesizes all notes into a single "Mastery Page" with 12-year-old analogies and jargon decrypters.
- **Auto File Management** — Saves `.md`, `.docx`, and `.mp3` outputs, and cleans up temporary files.  

***

## 🧠 Project Architecture

| Stage | Description | Output |
|-------|--------------|--------|
| Phase 1 | Creates an engaging **Lecture Architecture Guide** with structured flow and learning objectives. | `{filename}_Phase1_Lecture_Guide.docx` |
| Phase 2 | Deconstructs concepts into a **Deep-Technical Blueprint** with rigorous system logic and edge cases. | `{filename}_Phase2_Structured_Guide.docx` |
| Phase 3 | Generates compact **Exam Prep Notes** with key definitions, formulas, and Q&A sections. | `{filename}_Phase3_Exam_Prep_Notes.docx` |
| Phase 4 | Synthesizes an **Audio Podcast** dialogue between two AI hosts covering the entire material. | `audio_overview.mp3` |
| Phase 5 | Distills everything into a **Feynman Mastery Page** using a logic-first reasoning engine. | `{filename}_Phase5_Feynman_Technique.docx` |

***

## 🧩 Requirements

- Python 3.10 or higher  
- Pandoc (for `.docx` conversion)  
- Google Generative AI SDK  
- `pdfplumber`, `pypandoc`, `python-docx`
- `edge-tts`, `openai`, `python-dotenv`

Install dependencies with:

```bash
pip install -r requirements.txt
```

Install **Pandoc** (system-wide):  
[https://pandoc.org/installing.html](https://pandoc.org/installing.html)

***

## ⚙️ Setup & Run

1. Place `agent.py` and **one** lecture PDF in a folder.  
2. Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```
3. Run the script:

```bash
python3 agent.py
```

4. After completion, check the **Final_Notes** folder for your study pack and audio.

All temporary Markdown files are automatically removed after conversion.

***

## 🛠️ Example Workflow

Input:  
Lecture slides or a PDF textbook chapter  

Output:  
- `Lecture Guide (Context & Hook)`  
- `Structured Guide (Technical Specs & Logic)`  
- `Exam Notes (Rapid Revision)`
- `Audio Podcast (7-minute overview)`
- `Feynman Mastery Page (Analogy & Synthesis)`

***

## 🧰 Optional Specialist Tools (Phase 4)

- **expand_on_detail()** — Deepens an existing section's content.  
- **ensure_source_accuracy()** — Aligns pseudocode closely with source material and provides plain-language explanations.

***

## 📁 Folder Structure

```
AI-Study-Agent/
├── agent.py
├── audio_generator.py
├── feynman_generator.py
├── .env
├── requirements.txt
├── Final_Notes/
│   ├── ...Phase1_Lecture_Guide.docx
│   ├── ...Phase2_Structured_Guide.docx
│   ├── ...Phase3_Exam_Prep_Notes.docx
│   ├── ...Phase5_Feynman_Technique.docx
│   ├── podcast_script.json
│   └── audio_overview.mp3
└── your_lecture.pdf
```

***

## 🚀 Project Goals

- Automate academic summarization
- Prototype self-improving AI study agents
- Demonstrate workflow orchestration via Gemini API and OpenRouter (MoE)

***

## 🪪 License

This project is licensed under the **MIT License**.  
You are free to clone, modify, and use the code for personal or research purposes.

***
