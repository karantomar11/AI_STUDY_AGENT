
***

# AI Study Agent

A smart Python-based AI assistant that reads academic PDFs, structures them into multi-phase lecture notes, and automatically converts them into `.docx` exam-prep documents.  
Built using the **Google Gemini AI API**, this lightweight project demonstrates how generative AI can transform raw educational text into structured, self-guided study material.

***

## 🎯 Overview

**AI Study Agent** automates your study workflow by analyzing lecture PDFs and producing three levels of notes plus an audio overview:
1. **Structured Lecture Guide**
2. **Readable Concept Breakdown**
3. **Concise Exam Preparation Notes**
4. **Audio Overview Podcast** (Hosted by "Alex" and "Jamie")

It also supports an **optional Phase 4 toolkit** for expanding details and validating code against source material context.

***

## ⚡ Features

- **Automatic PDF Detection** — Finds and processes the first PDF in its folder.  
- **Gemini AI Integration** — Generates guides, summaries, and exam notes using Google’s Gemini 1.5 Flash model.  
- **Multi-Phase Summarization Flow** — Three structured stages of output: *Lecture Guide → Structured Guide → Exam Notes*.  
- **Audio Overview Generation** — Creates a 7-minute dialogue-based podcast (`.mp3`) summarizing the material using `edge-tts` and OpenRouter.
- **Auto File Management** — Saves `.md` outputs, converts them to `.docx`, and cleans up temporary files.  
- **Expandable AI Tools** — Optional helpers for detailed text expansion and code accuracy verification.

***

## 🧠 Project Architecture

| Stage | Description | Output |
|-------|--------------|--------|
| Phase 1 | Creates an engaging **Lecture Guide** with structured flow, analogies, and learning objectives. | `{filename}_Phase1_Lecture_Guide.docx` |
| Phase 2 | Refines the lecture guide into **structured explanations and pseudocode examples**. | `{filename}_Phase2_Structured_Guide.docx` |
| Phase 3 | Generates compact **Exam Prep Notes** with key definitions, formulas, and Q&A sections. | `{filename}_Phase3_Exam_Prep_Notes.docx` |
| Phase 4 | Synthesizes a **Audio Podcast** dialogue between two AI hosts covering the entire material. | `audio_overview.mp3` |

***

## 🧩 Requirements

- Python 3.10 or higher  
- Pandoc (for `.docx` conversion)  
- Google Generative AI SDK  
- `pdfplumber` and `pypandoc`  
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

4. After completion, check the **Final_Notes** folder for `.docx` outputs and the `audio_overview.mp3`.  

All temporary Markdown files are automatically removed after conversion.

***

## 🛠️ Example Workflow

Input:  
Lecture slides or a PDF textbook chapter  

Output:  
- `Lecture Guide (Deep Understanding)`  
- `Structured Guide (with pseudocode)`  
- `Exam Notes (Concise Revision Sheet)`
- `Audio Podcast (7-minute overview)`

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
├── .env
├── requirements.txt
├── Final_Notes/
│   ├── Lecture_Guide.docx
│   ├── Structured_Guide.docx
│   ├── Exam_Prep_Notes.docx
│   └── audio_overview.mp3
└── your_lecture.pdf
```

***

## 🚀 Project Goals

- Automate academic summarization
- Prototype self-improving AI study agents
- Demonstrate workflow orchestration via Gemini API and OpenRouter

***

## 🪪 License

This project is licensed under the **MIT License**.  
You are free to clone, modify, and use the code for personal or research purposes.

***
