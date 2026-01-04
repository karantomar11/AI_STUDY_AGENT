# AI Study Agent (Production Edition) 🚀

A high-density, multi-modal **AI Study Factory** that transforms raw academic PDFs into a professional study suite. This agent orchestrates multiple LLMs (Google Gemini 1.5 Flash & Xiaomi MiMo-V2-Flash) to produce textbook-quality notes, audio podcasts, and artistic infographics.

***

## 🎯 Overview

The **AI Study Agent** is no longer just a summarizer; it is a **full-scale academic production line**. It deconstructs complex technical material and rebuilds it across six specialized phases designed to target every learning pathway (Visual, Auditory, and Technical).

***

## ⚡ New & Advanced Features

- **Advanced Math Engine (OMML)**: Formulas are no longer "dirty" text. The agent renders LaTeX into **Native Microsoft Word Equation Objects**, making them perfectly formatted and fully editable.
- **Universal Styling Engine (`doc_styler.py`)**: Automatically applies professional branding (**Dark Blue** headers), highlights (==turquoise== for analogies), and bold/underline formatting across all phases.
- **Nuclear-Sanitized Visualizer (Phase 6)**: A robust Mermaid.js engine that uses a "Nuclear Scrubber" to ensure infographics are generated as **Hand-Drawn, Multi-colored PNGs** without rendering errors (Status 400 fix).
- **Reasoning-Driven Synthesis**: Uses OpenRouter’s **Reasoning models** to create deep, high-fidelity analogies (e.g., the "Lego Castle" for Process Models).
- **Audio Overview**: Generates a professional 2-person podcast dialogue using `edge-tts` with a **"JSON Rescue" layer** to prevent synthesis crashes.

***

## 🧠 The Six Phases of Mastery

| Stage | Name | Description | Output |
|-------|------|-------------|--------|
| **Phase 1** | **Lecture Guide** | High-level architecture, "The Hook," and learning objectives. | `{fn}_Phase1_Lecture_Guide.docx` |
| **Phase 2** | **Technical Blueprint** | Deconstructs concepts into Formal Specs, Analogies, and Pseudocode. | `{fn}_Phase2_Structured_Guide.docx` |
| **Phase 3** | **Exam Prep Notes** | Rapid revision definitions and step-by-step formula solutions. | `{fn}_Phase3_Exam_Prep_Notes.docx` |
| **Phase 4** | **Audio Overview** | Conversational 2-person podcast (`.mp3`) summarizing the core logic. | `audio_overview.mp3` |
| **Phase 5** | **Feynman Mastery** | Distills complex jargon into 12-year-old analogies and "Blind Spot" audits. | `{fn}_Phase5_Feynman_Technique.docx` |
| **Phase 6** | **Universal Visualizer** | A hand-drawn, multicolored mindmap summarizing technical pillars. | `Phase6_Infographic.png` |

***

## 🛠️ Technical Stack

- **Core AI**: Google Gemini 1.5 Flash (Phases 1-3)
- **Reasoning AI**: Xiaomi MiMo-V2-Flash via OpenRouter (Phases 4-6)
- **Math Rendering**: `math2docx` (Office Math Markup Language)
- **Document Logic**: `python-docx` + `pypandoc`
- **Visual Logic**: Mermaid.ink API (Base64 URL-Safe State Protocol)
- **Voice Synthesis**: `edge-tts` (Andrew & Ava Neural Voices)

***

## 🧩 Requirements

```bash
pip install -r requirements.txt
```

**Core dependencies**: `google-generativeai`, `openai`, `math2docx`, `python-docx`, `edge-tts`, `requests`, `python-dotenv`.

***

## ⚙️ Setup & Run

1. **API Keys**: Place your keys in a `.env` file.
   ```env
   GOOGLE_API_KEY=your_key
   OPENROUTER_API_KEY=your_key
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```

2. **Input**: Place your lecture PDF in the root folder.

3. **Execute**:
   ```bash
   python agent.py
   ```

4. **Result**: Open the `Final_Notes/` folder for your complete study package.

***

## � Project Architecture

```plaintext
AI-Study-Agent/
├── agent.py               # Main Workflow Orchestrator
├── doc_styler.py          # Universal Styling & Math Engine
├── doc_visualizer.py      # Nuclear Sanitizer & Mermaid Renderer
├── audio_generator.py     # TTS & Podcast Logic
├── feynman_generator.py   # Analogical Reasoning Module
├── Final_Notes/           # Production Output Folder
└── requirements.txt       # Project Dependencies
```

***

## 🚀 Future Roadmap

- **Phase 7**: Automatic Anki Flashcard generation via `.apkg` export.
- **Phase 8**: Interactive Q&A Chatbot trained on the generated Blueprint.

***

## 🪪 License

**MIT License**. Turn your PDFs into professional mastery suites today!
