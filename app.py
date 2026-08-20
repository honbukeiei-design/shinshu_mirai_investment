import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="信州みらい病院 重点投資を考える",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE = Path(__file__).resolve().parent
CONFIG = json.loads((BASE / "scenario.json").read_text(encoding="utf-8"))


from embedded_assets import ASSETS


def embedded_uri(kind: str, filename: str) -> str:
    key = f"static/{kind}/{filename}"
    try:
        return ASSETS[key]
    except KeyError as exc:
        raise RuntimeError(f"Embedded asset is missing: {key}") from exc


characters = {}
for cid, meta in CONFIG["characters"].items():
    characters[cid] = {
        **meta,
        "src": embedded_uri("characters", meta["file"]),
    }

backgrounds = {}
for key, filename in CONFIG["backgrounds"].items():
    backgrounds[key] = embedded_uri("backgrounds", filename)

music = {}
for key, filename in CONFIG["music"].items():
    music[key] = embedded_uri("audio", filename)

payload = {
    "title": CONFIG["title"],
    "characters": characters,
    "backgrounds": backgrounds,
    "music": music,
    "sections": CONFIG["sections"],
}

payload_json = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")

st.markdown(
    """
<style>
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
    width: 100vw !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: #102d42 !important;
}
header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stStatusWidget"] {
    display: none !important;
}
.block-container {
    max-width: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
iframe {
    display: block !important;
    width: 100vw !important;
    height: 100vh !important;
    border: 0 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

html_doc = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<style>
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  font-family: "Yu Gothic UI", "Yu Gothic", Meiryo, sans-serif;
  background: #102d42;
  color: #eef6fb;
}}
button {{ font: inherit; }}
#app {{ position: relative; width: 100vw; height: 100vh; overflow: hidden; }}
.stage {{
  position: absolute;
  inset: 10px 14px 82px;
  border-radius: 2px;
  overflow: hidden;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  box-shadow: 0 14px 38px rgba(0,0,0,.22);
}}
.stage::after {{
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(5,24,36,.04), rgba(5,24,36,.11));
  pointer-events: none;
  z-index: 2;
}}
.cast {{
  position: absolute;
  left: 2%;
  right: 2%;
  top: 18px;
  bottom: 145px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: clamp(2px, 1vw, 18px);
  z-index: 8;
}}
.char-wrap {{
  position: relative;
  height: min(58vh, 600px);
  max-width: 22vw;
  min-width: 88px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  transition: filter .22s ease, opacity .22s ease, transform .22s ease;
  filter: brightness(.56) saturate(.72);
  opacity: .72;
  transform: scale(.98);
}}
.char-wrap.active {{
  filter: brightness(1.12) saturate(1.04);
  opacity: 1;
  transform: scale(1.025);
  z-index: 12;
}}
.char-wrap img {{
  display: block;
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
  object-position: bottom center;
  filter: drop-shadow(0 10px 16px rgba(0,0,0,.16));
}}
.cast.count-1 .char-wrap {{ max-width: 28vw; }}
.cast.count-2 .char-wrap {{ max-width: 25vw; }}
.cast.count-3 .char-wrap {{ max-width: 22vw; }}
.dialogue-wrap {{
  position: absolute;
  left: 3%;
  right: 3%;
  bottom: 18px;
  z-index: 20;
}}
.dialogue-card {{
  min-height: 126px;
  background: rgba(250,253,255,.965);
  color: #15394d;
  border: 1px solid rgba(255,255,255,.9);
  border-radius: 24px;
  padding: 12px 20px 16px;
  box-shadow: 0 20px 54px rgba(0,0,0,.2);
}}
.nameplate {{
  display: inline-flex;
  align-items: center;
  gap: 9px;
  padding: 8px 14px;
  margin-bottom: 8px;
  border-radius: 999px;
  background: #238794;
  color: white;
  font-weight: 900;
}}
.role {{ font-size: .75rem; opacity: .86; }}
.speech {{
  font-size: clamp(1rem, 1.18vw, 1.23rem);
  line-height: 1.6;
  font-weight: 700;
  overflow-wrap: anywhere;
}}
.controls {{
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 14px;
  width: min(calc(100vw - 150px), 1500px);
  z-index: 100;
  display: flex;
  justify-content: flex-end;
}}
.next-btn {{
  width: min(350px, 34vw);
  min-height: 54px;
  border: 1px solid rgba(255,255,255,.28);
  border-radius: 14px;
  background: linear-gradient(135deg,#fff,#e3eef4);
  color: #15394d;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(0,0,0,.15);
}}
.next-btn:hover {{ transform: translateY(-1px); }}
.title-card, .transition-card, .end-card {{
  position: absolute;
  left: 50%;
  top: 55%;
  transform: translate(-50%,-50%);
  z-index: 30;
  width: min(900px, 82vw);
  text-align: center;
  border-radius: 30px;
  padding: 34px 40px;
  color: #f6fbfd;
  background: rgba(20,57,75,.84);
  box-shadow: 0 28px 90px rgba(0,0,0,.3);
  backdrop-filter: blur(8px);
}}
.title-card h1 {{ margin: 0 0 8px; font-size: clamp(2.3rem, 5vw, 4.5rem); }}
.title-card h2 {{ margin: 0 0 16px; font-size: clamp(1.35rem, 2.6vw, 2.2rem); color: #c6f1f3; }}
.title-card p {{ margin: 0; font-size: clamp(.95rem, 1.2vw, 1.12rem); line-height: 1.8; font-weight: 700; }}
.transition-stage {{
  background: radial-gradient(circle at 50% 40%, #173346 0, #07131d 48%, #02070b 100%) !important;
}}
.transition-card {{ background: rgba(2,10,15,.74); }}
.transition-card h2 {{ margin: 0; font-size: clamp(1.8rem, 3vw, 2.8rem); }}
.end-card h2 {{ margin: 0 0 10px; font-size: clamp(1.8rem, 3vw, 2.8rem); }}
.end-card p {{ margin: 0; line-height: 1.8; font-weight: 700; }}
.bgm-chip {{
  position: absolute;
  top: 16px;
  right: 18px;
  z-index: 60;
  padding: 7px 10px;
  border-radius: 10px;
  background: rgba(15,48,68,.84);
  border: 1px solid rgba(255,255,255,.22);
  color: white;
  font-size: .78rem;
  font-weight: 800;
  user-select: none;
}}
@media (max-height: 820px) {{
  .stage {{ inset: 7px 10px 72px; }}
  .cast {{ top: 10px; bottom: 130px; }}
  .char-wrap {{ height: min(51vh, 480px); }}
  .dialogue-wrap {{ bottom: 10px; }}
  .dialogue-card {{ min-height: 112px; padding: 10px 16px 12px; }}
  .speech {{ font-size: clamp(.88rem, 1.05vw, 1.05rem); line-height: 1.48; }}
  .controls {{ bottom: 8px; }}
  .next-btn {{ min-height: 50px; }}
}}
@media (max-width: 980px) {{
  .stage {{ inset: 6px 8px 68px; }}
  .cast {{ left: 1%; right: 1%; bottom: 126px; gap: 1px; }}
  .char-wrap {{ height: min(43vh, 350px); max-width: 28vw; min-width: 58px; }}
  .dialogue-wrap {{ left: 2%; right: 2%; bottom: 8px; }}
  .dialogue-card {{ border-radius: 18px; min-height: 112px; padding: 9px 12px 11px; }}
  .speech {{ font-size: .85rem; line-height: 1.43; }}
  .controls {{ width: calc(100vw - 24px); bottom: 7px; }}
  .next-btn {{ width: min(330px, 48vw); min-height: 48px; }}
}}
</style>
</head>
<body>
<div id="app"></div>
<audio id="bgm" loop preload="auto"></audio>
<script>
const DATA = {payload_json};
const app = document.getElementById('app');
const audio = document.getElementById('bgm');
audio.volume = 0.16;

let slides = [];
DATA.sections.forEach((section, index) => {{
  if (section.transition) {{
    slides.push({{ kind: 'transition', sectionIndex: index }});
  }}
  section.segments.forEach((segment, segmentIndex) => {{
    slides.push({{ kind: 'dialogue', sectionIndex: index, segmentIndex }});
  }});
}});
slides.push({{ kind: 'end' }});

let cursor = -1;
let started = false;
let currentTrack = null;

function esc(s) {{
  return String(s ?? '')
    .replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')
    .replaceAll('"','&quot;').replaceAll("'",'&#039;');
}}

function setMusic(key) {{
  if (!key || !DATA.music[key]) return;
  if (currentTrack === key) {{
    if (started && audio.paused) audio.play().catch(() => {{}});
    return;
  }}
  currentTrack = key;
  audio.src = DATA.music[key];
  audio.load();
  if (started) audio.play().catch(() => {{}});
}}

function backgroundStyle(key) {{
  const src = DATA.backgrounds[key];
  return src ? `background-image: linear-gradient(rgba(8,27,40,.06),rgba(8,27,40,.06)), url('${{src}}');` : '';
}}

function castHtml(section, speaker) {{
  const ids = section.characters || [];
  const chars = ids.map(cid => {{
    const c = DATA.characters[cid];
    const active = cid === speaker ? ' active' : '';
    return `<div class="char-wrap${{active}}"><img src="${{c.src}}" alt="${{esc(c.name)}}"></div>`;
  }}).join('');
  return `<div class="cast count-${{ids.length}}">${{chars}}</div>`;
}}

function controls(label) {{
  return `<div class="controls"><button class="next-btn" id="next">${{esc(label)}}</button></div>`;
}}

function bindNext(fn) {{
  const btn = document.getElementById('next');
  if (btn) btn.addEventListener('click', fn, {{ once: true }});
}}

function renderTitle() {{
  const first = DATA.sections[0];
  setMusic(first.music);
  const explainer = DATA.characters.explainer;
  app.innerHTML = `
    <div class="stage" style="${{backgroundStyle('entrance')}}">
      <div class="cast count-1"><div class="char-wrap active"><img src="${{explainer.src}}" alt=""></div></div>
      <div class="title-card">
        <h1>${{esc(DATA.title.headline)}}</h1>
        <h2>${{esc(DATA.title.subtitle)}}</h2>
        <p>${{esc(DATA.title.lead)}}</p>
      </div>
    </div>
    ${{controls('はじめる')}}`;
  bindNext(() => {{
    started = true;
    audio.play().catch(() => {{}});
    cursor = 0;
    renderCurrent();
  }});
}}

function renderTransition(section) {{
  setMusic(section.music);
  app.innerHTML = `
    <div class="stage transition-stage">
      <div class="transition-card"><h2>${{esc(section.transition)}}</h2></div>
    </div>
    ${{controls('場面を見る')}}`;
  bindNext(nextSlide);
}}

function renderDialogue(section, segment) {{
  setMusic(section.music);
  const c = DATA.characters[segment.speaker];
  app.innerHTML = `
    <div class="stage" style="${{backgroundStyle(section.background)}}">
      ${{castHtml(section, segment.speaker)}}
      <div class="dialogue-wrap">
        <div class="dialogue-card">
          <div class="nameplate">${{esc(c.name)}} <span class="role">${{esc(c.role)}}</span></div>
          <div class="speech">${{esc(segment.text)}}</div>
        </div>
      </div>
    </div>
    ${{controls('次へ')}}`;
  bindNext(nextSlide);
}}

function renderEnd() {{
  setMusic('resolution');
  app.innerHTML = `
    <div class="stage" style="${{backgroundStyle('meeting')}}">
      <div class="end-card">
        <h2>あなたなら何を優先しますか？</h2>
        <p>5つの投資案から、信州みらい病院にとって優先すべき投資を考えてみましょう。</p>
      </div>
    </div>
    ${{controls('タイトルへ戻る')}}`;
  bindNext(() => {{
    cursor = -1;
    currentTrack = null;
    audio.pause();
    audio.currentTime = 0;
    renderTitle();
  }});
}}

function renderCurrent() {{
  const slide = slides[cursor];
  if (!slide || slide.kind === 'end') {{ renderEnd(); return; }}
  const section = DATA.sections[slide.sectionIndex];
  if (slide.kind === 'transition') renderTransition(section);
  else renderDialogue(section, section.segments[slide.segmentIndex]);
}}

function nextSlide() {{
  cursor += 1;
  renderCurrent();
}}

renderTitle();
</script>
</body>
</html>"""

components.html(html_doc, height=900, scrolling=False)
