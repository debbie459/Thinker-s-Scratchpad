import io
import json
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from docx import Document
from groq import Groq
from pydub import AudioSegment

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400;1,500&display=swap');

:root {
    --bg:        #ffffff;
    --card:      #f9f9f9;
    --border:    #e5e5e5;
    --text:      #111111;
    --muted:     #6b6b6b;
    --dim:       #aaaaaa;
    --primary:   #111111;
    --pri-bg:    #f2f2f2;
    --pri-bdr:   #d4d4d4;
    --ok:        #4a9e72;
    --ok-bg:     #edf9f2;
    --ok-bdr:    #b8dfc8;
}

/* ── chrome ───────────────────────────────────────────── */
[data-testid="stHeader"], #MainMenu, footer,
[data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }

.block-container { padding-top:0 !important; padding-bottom:0 !important; max-width:960px !important; }
.stApp, [data-testid="stAppViewContainer"] { background:var(--bg) !important; }
html, body, [class*="css"], p, div, span, label { font-family:'Inter',sans-serif !important; color:var(--text); }

/* ── navbar ───────────────────────────────────────────── */
.navbar {
    display:flex; align-items:center; justify-content:space-between;
    padding:14px 0 14px; border-bottom:1px solid var(--border);
    margin-bottom:36px; background:var(--bg);
}
.nav-brand { display:flex; align-items:center; gap:10px; }
.nav-logo {
    width:36px; height:36px; background:var(--primary); border-radius:8px;
    display:flex; align-items:center; justify-content:center;
    color:#fff; font-weight:700; font-size:15px; flex-shrink:0;
}
.nav-appname { font-size:24px; font-weight:600; line-height:1.2; }
.nav-appsub  { font-size:11px; color:var(--muted); }

.nav-steps { display:flex; align-items:center; gap:6px; }
.nav-step {
    display:flex; align-items:center; gap:6px;
    font-size:13px; color:var(--dim); padding:4px 10px; border-radius:999px;
}
.nav-step.active { color:var(--primary); font-weight:600; }
.nav-step.done   { color:var(--muted); }
.step-num {
    width:22px; height:22px; border-radius:50%;
    background:var(--border); color:var(--muted);
    font-size:11px; font-weight:600;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.nav-step.active .step-num { background:var(--primary); color:#fff; }
.nav-step.done   .step-num { background:var(--ok);      color:#fff; }
.step-sep { color:var(--dim); font-size:14px; }

.nav-badge {
    font-size:12px; color:var(--muted);
    border:1px solid var(--border); border-radius:999px;
    padding:4px 14px; display:flex; align-items:center; gap:6px;
}
.dot-pri { color:var(--primary); font-size:8px; }

/* ── hero ─────────────────────────────────────────────── */
.hero { margin-bottom:50px; }
.hero-eyebrow {
    display:inline-block; font-size:10px; font-weight:600;
    letter-spacing:1.6px; text-transform:uppercase;
    color:var(--primary); background:var(--pri-bg);
    border:1px solid var(--pri-bdr); border-radius:4px;
    padding:3px 10px; margin-bottom:14px;
}
.hero-title {
    font-size:2.4rem !important; font-weight:700 !important;
    line-height:1.2 !important; color:var(--text) !important;
    margin:0 0 14px !important; letter-spacing:-0.5px !important;
}
.hero-desc {
    font-size:15px !important; color:var(--muted) !important;
    line-height:1.75 !important; max-width:580px; margin:0 !important;
}

[data-testid="stVerticalBlockBorderWrapper"] > div {
    border:1.5px dashed var(--border) !important;
    border-radius:16px !important;
    background:var(--card) !important;
}
.card-top {
    text-align:center; padding:20px 0 8px; margin-bottom: 15px; 
}
.card-icon-wrap {
    width:52px; height:52px; background:var(--pri-bg); border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    margin:0 auto 14px; font-size:22px;
}
.card-heading { font-size:20px; font-weight:600; margin:0 0 0px; }
.card-subdesc { font-size:10px; color:var(--muted); margin:0; line-height:1.55; }

/* ── trust strip ──────────────────────────────────────── */
.trust-strip {
    display:flex; align-items:center; justify-content:center;
    gap:28px; padding:14px 0 4px;
}
.trust-item { font-size:12px; color:var(--dim); display:flex; align-items:center; gap:5px; }

/* ── transcript card (page 1 below card) ─────────────── */
.tx-card {
    background:var(--card); border:1px solid var(--border);
    border-radius:12px; padding:18px 20px; margin-top:16px;
}
.tx-label {
    font-size:10px; letter-spacing:2px; text-transform:uppercase;
    color:var(--dim); margin:0 0 10px;
}
.tx-text {
    font-family:'Inter',sans-serif !important; font-style:normal;
    font-size:15px; line-height:1.85; color:var(--muted); margin:0;
}

/* ── buttons ──────────────────────────────────────────── */
.stButton > button {
    font-family:'Inter',sans-serif !important; font-size:13px !important;
    font-weight:500 !important; border-radius:8px !important;
    border:1px solid var(--border) !important; background:transparent !important;
    color:var(--muted) !important; padding:8px 20px !important;
    transition:all .15s !important;
    margin-bottom: 20px !important;
}
.stButton > button:hover:not(:disabled) {
    background: #f5f5f5; border-color:var(--primary) !important;
    color:#fff !important;
}
.stButton > button:disabled { opacity:.3 !important; }

/* ── file uploader ────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {
    border:1.5px dashed #4a250c !important;
    border-radius:10px !important; background:var(--bg) !important;
}
[data-testid="stFileUploaderDropzone"] button span:first-child {
    display: none !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span[data-testid="stMarkdownContainer"] {
    display: none !important;
}

/* ── audio player ─────────────────────────────────────── */
audio { border-radius:8px; width:100%; }

/* ── spinner ──────────────────────────────────────────── */
.stSpinner > div { border-top-color:var(--primary) !important; }

/* ── popover expand_more icon ─────────────────────────── */
[data-testid="stPopover"] button .material-symbols-rounded,
[data-testid="stPopoverButton"] .material-symbols-rounded,
[data-testid="stPopover"] .material-symbols-rounded,
[data-testid="stPopover"] button span[class*="material"] {
    display:none !important;
    font-size:0 !important;
    width:0 !important;
}

/* ── status banner ────────────────────────────────────── */
.status-banner {
    border-radius:10px; padding:12px 18px; margin-bottom:24px;
    display:flex; align-items:center; justify-content:space-between;
    font-size:14px;
}
.status-banner.ok {
    background:var(--ok-bg); border:1px solid var(--ok-bdr);
}
.status-main { font-weight:500; display:flex; align-items:center; gap:8px; }
.status-side { font-size:13px; color:var(--ok); }
.dot-ok   { color:var(--ok); font-size:9px; }

/* ── left panel (page 2) ──────────────────────────────── */
.left-panel {
    background:var(--card); border:1px solid var(--border);
    border-radius:12px; padding:18px 20px;
}
.panel-hdr {
    display:flex; align-items:center; justify-content:space-between;
    padding-bottom:12px; border-bottom:1px solid var(--border); margin-bottom:14px;
}
.panel-title { font-size:15px; font-weight:600; }
.panel-meta  { font-size:12px; color:var(--muted); }
.panel-text  {
    font-family:'Inter',sans-serif !important; font-style:normal;
    font-size:14px; line-height:1.85; color:var(--muted); margin:0;
}

/* ── right panel output cards ─────────────────────────── */
.out-hdr { margin-bottom:16px; }
.out-hdr-title    { font-size:18px; font-weight:600; }
.out-hdr-subtitle { font-size:12px; color:var(--muted); margin-top:2px; }

.out-card {
    background:var(--card);
    border:1px solid var(--border);
    border-radius:12px; padding:18px 20px; margin-bottom:10px;
}
.prompt-badge {
    display:inline-block; font-size:10px; font-weight:600;
    background:var(--pri-bg); color:var(--primary);
    border-radius:4px; padding:2px 8px; margin-bottom:8px; letter-spacing:.2px;
}
.out-card-title { font-size:16px; font-weight:600; margin:0 0 4px; }
.out-card-sub   { font-size:12px; color:var(--muted); margin:0 0 14px; font-style:italic; }
.out-quote {
    font-family:'Inter',sans-serif !important; font-style:normal;
    font-size:15px; line-height:1.65; color:var(--text);
    background:var(--bg); border-radius:8px; padding:14px 16px; margin:0;
}

.arg-row { display:flex; gap:14px; padding:12px 0; border-bottom:1px solid var(--border); }
.arg-row:last-child { border-bottom:none; padding-bottom:0; }
.arg-num {
    width:22px; height:22px; background:var(--pri-bg); color:var(--primary);
    border-radius:50%; font-size:11px; font-weight:600; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; margin-top:1px;
}
.arg-title { font-size:14px; font-weight:600; margin:0 0 3px; }
.arg-body  { font-size:13px; color:var(--muted); margin:0; line-height:1.55; }

.thread-row {
    display:flex; align-items:flex-start; gap:10px;
    background:var(--bg); border-radius:8px; padding:10px 14px;
    margin-bottom:6px; font-size:13px; color:var(--muted); line-height:1.5;
}
.thread-arrow { color:var(--dim); flex-shrink:0; font-size:13px; }

/* ── footer ───────────────────────────────────────────── */
.footer {
    border-top:1px solid var(--border); padding:20px 0;
    margin-top:40px; display:flex; align-items:flex-start; justify-content:space-between;
}
.footer-left { font-size:12px; color:var(--muted); line-height:1.8; }
.footer-right { display:flex; flex-direction:column; gap:6px; align-items:flex-end; }
.tech-tag {
    font-size:11px; border:1px solid var(--border); border-radius:999px;
    padding:3px 12px; color:var(--muted); display:inline-flex; align-items:center; gap:5px;
}
.dot-g { color:#4a9e72; font-size:8px; }
.dot-b { color:#5b8fd4; font-size:8px; }
.dot-r { color:#d45b5b; font-size:8px; }
</style>
""",
    unsafe_allow_html=True,
)

defaults = {
    "setup_complete": False,
    "transcription": None,
    "messages": [],
    "structured_output": None,
    "recording_method": "Record Audio",
    "md_output": None,
    "docx_bytes": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def complete_setup():
    if st.session_state.transcription:
        structure_thought(st.session_state.transcription)
    st.session_state.structured_output = None
    st.session_state.md_output = None
    st.session_state.docx_bytes = None
    st.session_state.setup_complete = True


def reset():
    st.session_state.setup_complete = False
    st.session_state.transcription = None
    st.session_state.messages = []
    st.session_state.structured_output = None
    st.session_state.md_output = None
    st.session_state.docx_bytes = None
    st.session_state["_upload_key"] = None
    st.session_state["_rec_key"] = None


@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def _compress_if_wav(audio_bytes, fmt):
    if fmt != "wav":
        return audio_bytes, f"audio.{fmt}"
    seg = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
    buf = io.BytesIO()
    seg.export(buf, format="mp3", bitrate="64k")
    return buf.getvalue(), "audio.mp3"


def transcribe_audio(audio_data, fmt="wav", compress=False):
    if compress:
        audio_data, filename = _compress_if_wav(audio_data, fmt)
    else:
        filename = f"audio.{fmt}"
    groq_client = get_groq_client()
    transcription = groq_client.audio.transcriptions.create(
        file=(filename, audio_data),
        model="whisper-large-v3-turbo",
        language="en",
        response_format="text",
    )
    return {"text": transcription}


def structure_thought(transcribed_text):
    system_instruction = (
        "You are a helpful assistant that takes the user's transcribed text and structures "
        "the transcript into: a working headline, three to five key arguments depending on "
        "the content of the transcription (each key argument should also contain a brief "
        "explanation of what the user mentioned), a suggested opening hook, and a list of "
        "loose threads worth following up. Do not write anything new for the user — just "
        "organise what the user said. The headline should be a concise summary of the main "
        "idea. Provide the structured output in JSON format with exactly these keys: "
        "'title', 'key_arguments', 'opening_hook', 'loose_threads'. "
        "Each item in 'key_arguments' must be an object with 'argument' and 'explanation' keys."
    )
    st.session_state.messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": transcribed_text},
    ]


def build_markdown_string(data, transcription=""):
    md = f"# {data['title']}\n\n"
    md += "## Key Arguments\n\n"
    for item in data["key_arguments"]:
        md += f"### {item['argument']}\n{item['explanation']}\n\n"
    md += f"## Suggested Opening Hook\n> {data['opening_hook']}\n\n"
    md += "## Loose Threads Worth Following Up\n\n"
    for thread in data["loose_threads"]:
        md += f"- {thread}\n"
    if transcription:
        md += f"\n\n---\n\n## Full Transcription\n\n{transcription}\n"
    return md


def build_docx_bytes(data, transcription=""):
    doc = Document()
    doc.add_heading(data["title"], level=1)

    doc.add_heading("Key Arguments", level=2)
    for item in data["key_arguments"]:
        doc.add_heading(item["argument"], level=3)
        doc.add_paragraph(item["explanation"])

    doc.add_heading("Suggested Opening Hook", level=2)
    doc.add_paragraph(data["opening_hook"], style="Quote")

    doc.add_heading("Loose Threads Worth Following Up", level=2)
    for thread in data["loose_threads"]:
        doc.add_paragraph(thread, style="List Bullet")

    if transcription:
        doc.add_page_break()
        doc.add_heading("Full Transcription", level=2)
        doc.add_paragraph(transcription)

    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()


if st.session_state.setup_complete:
    _step = 3
elif st.session_state.transcription:
    _step = 2
else:
    _step = 1


def _sc(n):
    if n < _step:
        return "done"
    if n == _step:
        return "active"
    return ""


st.markdown(
    f"""
<nav class="navbar">
  <div class="nav-brand">
    <div>
      <div class="nav-appname">Thinker's Scratchpad</div>
    </div>
  </div>
  <div class="nav-steps">
    <div class="nav-step {_sc(1)}">
       Capture
    </div>
    <span class="step-sep">›</span>
    <div class="nav-step {_sc(2)}">
       Transcribe
    </div>
    <span class="step-sep">›</span>
    <div class="nav-step {_sc(3)}">
       Structure
    </div>
  </div>
</nav>
""",
    unsafe_allow_html=True,
)


if not st.session_state.setup_complete:

    st.markdown(
        """
    <div class="hero">
      <div class="hero-eyebrow">IDEAS TO ASSETS</div>
      <div class="hero-title">Capture messy thoughts.<br>Return pure structure.</div>
      <p class="hero-desc">Good ideas arrive when you're busy. Record your unfiltered stream of consciousness and let the pipeline extract the key insights. No filler, no rewriting — just organising what you said.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown(
            """
        <div class="card-top">
          <div class="card-heading">Transcribe your voice memo</div>
          <p class="card-subdesc">Record directly or upload an audio file. We support MP3, WAV, and M4A.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        _, c1, c2, _ = st.columns([2, 1.6, 1.5, 2])
        with c1:
            if st.button("Upload Audio File"):
                st.session_state["recording_method"] = "Upload Recording"
                st.rerun()
        with c2:
            if st.button("Record Instantly"):
                st.session_state["recording_method"] = "Record Audio"
                st.rerun()

        audio_data = None
        audio_fmt = "wav"
        audio_compress = False

        if st.session_state.get("recording_method") == "Record Audio":
            _, mic_col, _ = st.columns([1, 0.15, 1])
            with mic_col:
                audio_bytes = audio_recorder(
                    text="",
                    recording_color="#e85a5a",
                    neutral_color="#6aa36f",
                    icon_size="3x",
                )
            st.markdown(
                '<p style="text-align:center;font-size:12px;color:#b8ada3;margin-top:6px;margin-bottom:8px;">Click to start · click again to stop</p>',
                unsafe_allow_html=True,
            )
            if audio_bytes:
                rec_key = len(audio_bytes)
                if st.session_state.get("_rec_key") != rec_key:
                    st.session_state.transcription = None
                    st.session_state["_rec_key"] = rec_key
                audio_data = audio_bytes
                audio_fmt = "wav"
                audio_compress = False

        elif st.session_state.get("recording_method") == "Upload Recording":
            _, up_col, _ = st.columns([0.5, 3, 0.5])
            with up_col:
                uploaded_file = st.file_uploader(
                    "Choose an audio file",
                    type=["mp3", "wav", "m4a"],
                    label_visibility="collapsed",
                )
            if uploaded_file is not None:
                file_key = f"{uploaded_file.name}_{uploaded_file.size}"
                if st.session_state.get("_upload_key") != file_key:
                    st.session_state.transcription = None
                    st.session_state["_upload_key"] = file_key
                audio_data = uploaded_file.read()
                audio_fmt = uploaded_file.name.rsplit(".", 1)[-1].lower()
                audio_compress = audio_fmt == "wav"
            else:
                if st.session_state.get("_upload_key") is not None:
                    st.session_state.transcription = None
                    st.session_state["_upload_key"] = None

        if audio_data:
            st.audio(audio_data, format="audio/wav")
            if st.session_state.transcription is None:
                with st.spinner("Transcribing your audio..."):
                    result = transcribe_audio(
                        audio_data, fmt=audio_fmt, compress=audio_compress
                    )
                    st.session_state.transcription = result["text"]

    st.markdown('<div style="margin-top:36px;"></div>', unsafe_allow_html=True)
    _, cta_col, _ = st.columns([3, 2, 3])
    with cta_col:
        if st.button(
            "Structure my thoughts",
            disabled=not st.session_state.transcription,
            use_container_width=True,
        ):
            complete_setup()


else:

    col_left, col_right = st.columns([2, 3])

    with col_left:
        st.markdown(
            f"""
        <div class="left-panel">
          <div class="panel-hdr">
            <div class="panel-title">Whisper Transcription</div>
          </div>
          <p class="panel-text">{st.session_state.transcription}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_right:
        if st.session_state.structured_output is None:
            client = get_groq_client()
            with st.spinner("Structuring your thought..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    response_format={"type": "json_object"},
                )
                st.session_state.structured_output = (
                    response.choices[0].message.content
                )

        data = json.loads(st.session_state.structured_output)

        if (
            st.session_state.md_output is None
            or st.session_state.docx_bytes is None
        ):
            st.session_state.md_output = build_markdown_string(data, st.session_state.transcription)
            st.session_state.docx_bytes = build_docx_bytes(data, st.session_state.transcription)

        st.markdown(
            """
        <div class="out-hdr">
          <div class="out-hdr-title">Structured Outputs</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
        <div class="out-card">
          <div class="out-card-title">Working Headline</div>
          <p class="out-quote">"{data['title']}"</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        args_html = "".join(
            [
                f"""<div class="arg-row">
                  <div class="arg-num">{i+1}</div>
                  <div>
                    <p class="arg-title">{item['argument']}</p>
                    <p class="arg-body">{item['explanation']}</p>
                  </div>
                </div>"""
                for i, item in enumerate(data["key_arguments"])
            ]
        )
        st.markdown(
            f"""
        <div class="out-card">
          <div class="out-card-title">Key Arguments</div>
          {args_html}
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
        <div class="out-card">
          <div class="out-card-title">Suggested Opening Hook</div>
          <p class="out-quote">"{data['opening_hook']}"</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        threads_html = "".join(
            [
                f'<div class="thread-row"><span class="thread-arrow">↗</span>{t}</div>'
                for t in data["loose_threads"]
            ]
        )
        st.markdown(
            f"""
        <div class="out-card">
          <div class="out-card-title">Loose Threads Worth Following Up</div>
          {threads_html}
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.write("---")
        btn_col_1, btn_col_2 = st.columns(2)

        with btn_col_1:
            with st.popover("Copy Markdown", use_container_width=True):
                st.code(st.session_state.md_output, language="markdown")

        with btn_col_2:
            st.download_button(
                label="Download .docx",
                data=st.session_state.docx_bytes,
                file_name=f"{data['title'].lower().replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

        if st.button("Start New Tracking", use_container_width=True):
            reset()
            st.rerun()

    st.markdown(
        """
    <div class="footer">
      <div class="footer-left">
        <div>All audio is processed locally. No data is stored.</div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )