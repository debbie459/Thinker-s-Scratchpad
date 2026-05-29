# Thinker's Scratchpad

Thinker's Scratchpad is an application engineered to transform messy, unstructured voice notes or audio recordings into clean, highly organized analytical assets. By leveraging Groq's high-speed inference engine, the application captures audio stream input, processes it through Whisper, and passes the text to a large language model to extract core arguments, headlines, hooks, and follow-up vectors.

## Features

* **Dual-Mode Audio Capture:** Input your voice notes via native microphone recording or direct file uploads (supporting MP3, WAV, and M4A formats).
* **Automated Audio Optimization:** Automatic background compression handles oversized raw WAV audio by converting it to efficient, low-bitrate MP3 structures before API delivery.
* **Instant Structured Parsing:** Transforms unstructured voice transcripts into an organized layout comprising a working headline, key points with supporting context, opening hooks, and loose thematic threads.
* **Seamless Export Architecture:** Rapidly review outputs in a beautifully formatted custom container layout, copy the formatted workspace as native Markdown syntax, or download it immediately as a pre-styled Microsoft Word `.docx` file.

## Tech Stack

* **Frontend Framework:** Streamlit
* **AI & Inference Engine:** Groq API (Models: `whisper-large-v3-turbo` and `llama-3.3-70b-versatile`)
* **Audio Engineering:** Pydub & Audio Recorder Streamlit
* **Document Generation:** Python-docx

## Repository Structure

```text
thinkers-scratchpad/
├── .streamlit/
│   └── secrets.toml
├── app.py
├── README.md
└── requirements.txt
```

## Prerequisites

Ensure you have System-level **FFmpeg** installed on your host machine to allow Pydub to process and convert audio files seamlessly.

### Mac
```bash
brew install ffmpeg
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows
1. Download the FFmpeg essentials build from the official site.
2. Extract the files to a folder (e.g., `C:\ffmpeg`).
3. Add the `bin` folder path to your System Environment variables.

## Installation

1. Clone the repository to your local directory:
```bash
git clone [https://github.com/yourusername/thinkers-scratchpad.git](https://github.com/yourusername/thinkers-scratchpad.git)
cd thinkers-scratchpad
```

2. Install the required project dependencies:
```bash
pip install streamlit groq pydub python-docx audio-recorder-streamlit
```

## Configuration

The application relies on Streamlit's internal secrets manager to communicate securely with the Groq API environment. 

Create a directory named `.streamlit` at the root of your project directory, add a `secrets.toml` file inside it, and insert your API token:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

## Running the Application

Launch the local development server directly via your terminal:

```bash
streamlit run app.py
```

## How It Works

1. **Capture:** Choose between recording audio live using the interactive microphone widget or uploading an existing recording file.
2. **Transcribe:** The audio is processed locally, compressed to MP3 if uploaded as a heavy WAV file, and transcribed using the high-speed `whisper-large-v3-turbo` model.
3. **Structure:** The raw text is passed to `llama-3.3-70b-versatile` with custom system blueprints to isolate core thoughts into structured JSON elements.
4. **Export:** View the final segmented presentation, copy the clean Markdown compilation from the interactive popover container, or generate an absolute `.docx` document copy instantly.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
