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
SAVED_EDITS_PATH = BASE / "saved_edits.json"
SAVED_EDITS = json.loads(SAVED_EDITS_PATH.read_text(encoding="utf-8")) if SAVED_EDITS_PATH.is_file() else None


import base64


def data_uri(path: Path, mime: str) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Required asset not found: {path}")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def asset_uri(kind: str, filename: str) -> str:
    path = BASE / "static" / kind / filename
    if kind == "audio":
        mime = "audio/mpeg"
    elif filename.lower().endswith(".png"):
        mime = "image/png"
    else:
        mime = "image/jpeg"
    return data_uri(path, mime)


characters = {}
for cid, meta in CONFIG["characters"].items():
    characters[cid] = {
        **meta,
        "src": asset_uri("characters", meta["file"]),
    }

backgrounds = {}
for key, filename in CONFIG["backgrounds"].items():
    backgrounds[key] = asset_uri("backgrounds", filename)

music = {}
for key, filename in CONFIG["music"].items():
    music[key] = asset_uri("audio", filename)

payload = {
    "title": CONFIG["title"],
    "characters": characters,
    "backgrounds": backgrounds,
    "music": music,
    "sections": CONFIG["sections"],
    "additional_sections": CONFIG.get("additional_sections", []),
    "saved_edits": SAVED_EDITS,
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
.home-controls {{ justify-content: center; }}
.home-buttons {{ display: flex; gap: 12px; justify-content: center; align-items: center; flex-wrap: wrap; width: min(760px, 90vw); }}
.home-buttons .next-btn {{ width: min(350px, 42vw); }}
.secondary-home {{ background: rgba(229,239,245,.96); }}
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

.utility-bar {{
  position: absolute;
  top: 16px;
  left: 18px;
  z-index: 80;
  display: flex;
  gap: 8px;
}}
.utility-btn {{
  min-height: 38px;
  padding: 7px 12px;
  border: 1px solid rgba(255,255,255,.28);
  border-radius: 10px;
  background: rgba(15,48,68,.88);
  color: white;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 7px 18px rgba(0,0,0,.16);
}}
.utility-btn:hover {{ background: rgba(22,70,92,.95); }}
.modal-backdrop {{
  position: absolute;
  inset: 0;
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(2,12,20,.68);
  backdrop-filter: blur(4px);
}}
.modal {{
  width: min(860px, 90vw);
  max-height: 82vh;
  overflow: hidden;
  border-radius: 22px;
  background: #f8fbfd;
  color: #15394d;
  box-shadow: 0 28px 90px rgba(0,0,0,.38);
  border: 1px solid rgba(255,255,255,.7);
}}
.modal-head {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 18px;
  border-bottom: 1px solid #dbe7ed;
  background: #edf5f8;
}}
.modal-head h3 {{ margin: 0; font-size: 1.08rem; }}
.close-btn {{
  border: 0;
  border-radius: 9px;
  padding: 7px 11px;
  background: #dce9ef;
  color: #15394d;
  font-weight: 900;
  cursor: pointer;
}}
.modal-body {{ padding: 16px 18px 18px; max-height: calc(82vh - 62px); overflow: auto; }}
.scene-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 10px; }}
.scene-btn {{
  width: 100%;
  min-height: 54px;
  border: 1px solid #bed2dc;
  border-radius: 13px;
  padding: 10px 12px;
  background: white;
  color: #15394d;
  font-weight: 900;
  text-align: left;
  cursor: pointer;
}}
.scene-btn:hover {{ background: #eaf4f7; }}
.edit-meta {{ margin: 0 0 10px; font-weight: 900; color: #238794; }}
.editor-text {{
  width: 100%;
  min-height: 220px;
  resize: vertical;
  border: 1px solid #adc7d3;
  border-radius: 14px;
  padding: 14px;
  color: #15394d;
  background: white;
  font: 700 1rem/1.65 "Yu Gothic UI", "Yu Gothic", Meiryo, sans-serif;
}}
.editor-actions {{ display: flex; justify-content: flex-end; gap: 9px; margin-top: 12px; }}
.save-btn {{
  border: 0;
  border-radius: 11px;
  padding: 10px 18px;
  background: #238794;
  color: white;
  font-weight: 900;
  cursor: pointer;
}}
.secondary-btn {{
  border: 1px solid #b8cdd7;
  border-radius: 11px;
  padding: 10px 16px;
  background: white;
  color: #15394d;
  font-weight: 900;
  cursor: pointer;
}}

.settings-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 12px; }}
.field-block {{ display: flex; flex-direction: column; gap: 6px; }}
.field-block.full {{ grid-column: 1 / -1; }}
.field-block label {{ font-size: .86rem; font-weight: 900; color: #3d6678; }}
.field-block input, .field-block select, .field-block textarea {{
  width: 100%; border: 1px solid #adc7d3; border-radius: 10px; padding: 10px 11px;
  background: #fff; color: #15394d; font: 700 .95rem/1.5 "Yu Gothic UI", "Yu Gothic", Meiryo, sans-serif;
}}
.field-block textarea {{ min-height: 130px; resize: vertical; }}
.range-row {{ display: grid; grid-template-columns: 1fr 72px; gap: 10px; align-items: center; }}
.range-row input[type="range"] {{ padding: 0; }}
.helper {{ margin: 8px 0 0; color: #597886; font-size: .82rem; line-height: 1.55; }}
.editor-actions.wrap {{ justify-content: space-between; flex-wrap: wrap; }}
.left-actions, .right-actions {{ display: flex; gap: 9px; flex-wrap: wrap; }}
.danger-btn {{ border: 1px solid #d3a6a6; border-radius: 11px; padding: 10px 16px; background: #fff5f5; color: #8b2e2e; font-weight: 900; cursor: pointer; }}
.file-btn {{ position: relative; overflow: hidden; }}
.file-btn input {{ position: absolute; inset: 0; opacity: 0; cursor: pointer; }}
@media (max-width: 680px) {{ .settings-grid {{ grid-template-columns: 1fr; }} .field-block.full {{ grid-column: auto; }} }}

@media (max-width: 680px) {{ .scene-grid {{ grid-template-columns: 1fr; }} }}
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
let currentMode = 'main';
function currentSections() {{ return currentMode === 'additional' ? (DATA.additional_sections || []) : DATA.sections; }}
function buildSlides() {{
  slides = [];
  currentSections().forEach((section, index) => {{
    if (section.transition) slides.push({{ kind: 'transition', sectionIndex: index }});
    section.segments.forEach((segment, segmentIndex) => slides.push({{ kind: 'dialogue', sectionIndex: index, segmentIndex }}));
  }});
  slides.push({{ kind: 'end' }});
}}
buildSlides();

let cursor = -1;
let started = false;
let currentTrack = null;
const STORAGE_KEY = 'shinshu_mirai_investment_editor_v6';
const COMPLETED_KEY = 'shinshu_mirai_investment_main_completed_v1';
const DEFAULT_STYLE = {{ speechPx: 19, namePx: 16, transitionPx: 42, titleHeadlinePx: 64, titleSubtitlePx: 32, titleLeadPx: 18 }};
let styleSettings = {{ ...DEFAULT_STYLE }};

function editableSnapshot() {{
  return {{
    version: 1,
    title: DATA.title,
    characterNames: Object.fromEntries(Object.entries(DATA.characters).map(([k,v]) => [k, v.name])),
    sections: DATA.sections.map(s => ({{
      id: s.id, transition: s.transition || '', background: s.background, music: s.music,
      characters: [...(s.characters || [])],
      segments: s.segments.map(x => ({{ speaker: x.speaker, text: x.text }}))
    }})),
    additionalSections: (DATA.additional_sections || []).map(s => ({{
      id: s.id, transition: s.transition || '', background: s.background, music: s.music,
      characters: [...(s.characters || [])],
      segments: s.segments.map(x => ({{ speaker: x.speaker, text: x.text }}))
    }})),
    style: styleSettings
  }};
}}
function applySnapshot(saved) {{
  if (!saved || typeof saved !== 'object') return;
  if (saved.title) Object.assign(DATA.title, saved.title);
  if (saved.characterNames) Object.entries(saved.characterNames).forEach(([k,v]) => {{ if (DATA.characters[k] && typeof v === 'string') DATA.characters[k].name = v; }});
  const applySections = (savedSections, targetSections) => {{
    if (!Array.isArray(savedSections)) return;
    savedSections.forEach(ss => {{
      const sec = targetSections.find(x => x.id === ss.id); if (!sec) return;
      if (typeof ss.transition === 'string') sec.transition = ss.transition;
      if (ss.background && DATA.backgrounds[ss.background]) sec.background = ss.background;
      if (ss.music && DATA.music[ss.music]) sec.music = ss.music;
      if (Array.isArray(ss.characters)) sec.characters = ss.characters.filter(cid => DATA.characters[cid]);
      if (Array.isArray(ss.segments)) ss.segments.forEach((seg,i) => {{ if (!sec.segments[i]) return; if (seg.speaker && DATA.characters[seg.speaker]) sec.segments[i].speaker = seg.speaker; if (typeof seg.text === 'string') sec.segments[i].text = seg.text; }});
    }});
  }};
  applySections(saved.sections, DATA.sections);
  applySections(saved.additionalSections, DATA.additional_sections || []);
  if (saved.style) styleSettings = {{ ...DEFAULT_STYLE, ...saved.style }};
}}
function loadSaved() {{ try {{ const raw=localStorage.getItem(STORAGE_KEY); if(raw) applySnapshot(JSON.parse(raw)); }} catch(e) {{ console.warn(e); }} }}
function persist() {{ try {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(editableSnapshot())); }} catch(e) {{ console.warn(e); }} }}
function downloadEdits() {{ const blob=new Blob([JSON.stringify(editableSnapshot(),null,2)],{{type:'application/json'}}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='saved_edits.json'; a.click(); URL.revokeObjectURL(a.href); }}
if (DATA.saved_edits) applySnapshot(DATA.saved_edits);
loadSaved();

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


function utilityBar() {{
  return `<div class="utility-bar">
    <button class="utility-btn" id="sceneMenu">場面</button>
    <button class="utility-btn" id="editScenario">編集</button>
  </div>`;
}}

function bindUtilities() {{
  const sceneBtn = document.getElementById('sceneMenu');
  if (sceneBtn) sceneBtn.addEventListener('click', openSceneMenu);
  const editBtn = document.getElementById('editScenario');
  if (editBtn) editBtn.addEventListener('click', openEditor);
}}

function slideIndexForSection(sectionIndex) {{
  return slides.findIndex(s => s.sectionIndex === sectionIndex);
}}
function mainCompleted() {{ try {{ return localStorage.getItem(COMPLETED_KEY) === '1'; }} catch(e) {{ return false; }} }}
function markMainCompleted() {{ try {{ localStorage.setItem(COMPLETED_KEY, '1'); }} catch(e) {{}} }}
function startExperience(mode) {{
  currentMode = mode;
  buildSlides();
  cursor = 0;
  started = true;
  audio.play().catch(() => {{}});
  renderCurrent();
}}

function sectionLabel(section, index) {{
  if (section.transition) return section.transition;
  if (section.id === 'intro') return '導入';
  if (section.id === 'ending') return 'まとめ';
  return `場面 ${{index + 1}}`;
}}

function openSceneMenu() {{
  const items = currentSections().map((section, index) =>
    `<button class="scene-btn" data-section="${{index}}">${{esc(sectionLabel(section, index))}}</button>`
  ).join('');
  const overlay = document.createElement('div');
  overlay.className = 'modal-backdrop';
  overlay.innerHTML = `<div class="modal">
    <div class="modal-head"><h3>場面を選ぶ</h3><button class="close-btn" id="closeModal">閉じる</button></div>
    <div class="modal-body"><div class="scene-grid">${{items}}</div></div>
  </div>`;
  app.appendChild(overlay);
  overlay.querySelector('#closeModal').addEventListener('click', () => overlay.remove());
  overlay.addEventListener('click', e => {{ if (e.target === overlay) overlay.remove(); }});
  overlay.querySelectorAll('.scene-btn').forEach(btn => btn.addEventListener('click', () => {{
    const sectionIndex = Number(btn.dataset.section);
    const idx = slideIndexForSection(sectionIndex);
    if (idx >= 0) {{ cursor = idx; started = true; renderCurrent(); }}
  }}));
}}

function currentContext() {{
  if (cursor < 0) return {{ kind: 'title' }};
  const slide = slides[cursor];
  if (!slide || slide.kind === 'end') return {{ kind: 'end' }};
  return {{ kind: slide.kind, slide, section: currentSections()[slide.sectionIndex] }};
}}
function optionHtml(obj, selected) {{ return Object.entries(obj).map(([k,v]) => `<option value="${{esc(k)}}" ${{k===selected?'selected':''}}>${{esc(v)}}</option>`).join(''); }}
function syncPair(overlay,a,b){{ const x=overlay.querySelector('#'+a), y=overlay.querySelector('#'+b); if(x&&y){{x.addEventListener('input',()=>y.value=x.value);y.addEventListener('input',()=>x.value=y.value);}} }}
function openEditor() {{
  const ctx=currentContext(); const overlay=document.createElement('div'); overlay.className='modal-backdrop'; let body='';
  const bgLabels={{meeting:'面談室',radiology:'放射線科',entrance:'エントランス'}};
  const musicLabels={{intro:'intro',field:'field',negotiation:'negotiation',reflection:'reflection',resolution:'resolution'}};
  if(ctx.kind==='dialogue'){{
    const seg=ctx.section.segments[ctx.slide.segmentIndex];
    body=`<div class="settings-grid">
      <div class="field-block full"><label>シナリオ本文</label><textarea id="edText">${{esc(seg.text)}}</textarea></div>
      <div class="field-block"><label>話者</label><select id="edSpeaker">${{optionHtml(Object.fromEntries(Object.entries(DATA.characters).map(([k,v])=>[k,v.name])),seg.speaker)}}</select></div>
      <div class="field-block"><label>話者表示名</label><input id="edSpeakerName" value="${{esc(DATA.characters[seg.speaker].name)}}"></div>
      <div class="field-block"><label>本文文字サイズ</label><div class="range-row"><input id="edSpeechPx" type="range" min="14" max="34" value="${{styleSettings.speechPx}}"><input id="edSpeechPxN" type="number" min="14" max="34" value="${{styleSettings.speechPx}}"></div></div>
      <div class="field-block"><label>話者名文字サイズ</label><div class="range-row"><input id="edNamePx" type="range" min="12" max="28" value="${{styleSettings.namePx}}"><input id="edNamePxN" type="number" min="12" max="28" value="${{styleSettings.namePx}}"></div></div>
      <div class="field-block"><label>背景</label><select id="edBackground">${{optionHtml(bgLabels,ctx.section.background)}}</select></div>
      <div class="field-block"><label>BGM</label><select id="edMusic">${{optionHtml(musicLabels,ctx.section.music)}}</select></div>
    </div>`;
  }} else if(ctx.kind==='transition'){{
    body=`<div class="settings-grid"><div class="field-block full"><label>場面タイトル</label><input id="edTransition" value="${{esc(ctx.section.transition||'')}}"></div><div class="field-block"><label>場面タイトル文字サイズ</label><div class="range-row"><input id="edTransitionPx" type="range" min="24" max="64" value="${{styleSettings.transitionPx}}"><input id="edTransitionPxN" type="number" min="24" max="64" value="${{styleSettings.transitionPx}}"></div></div><div class="field-block"><label>BGM</label><select id="edMusic">${{optionHtml(musicLabels,ctx.section.music)}}</select></div></div>`;
  }} else if(ctx.kind==='title'){{
    body=`<div class="settings-grid"><div class="field-block full"><label>タイトル</label><input id="edHeadline" value="${{esc(DATA.title.headline)}}"></div><div class="field-block full"><label>サブタイトル</label><input id="edSubtitle" value="${{esc(DATA.title.subtitle)}}"></div><div class="field-block full"><label>リード文</label><input id="edLead" value="${{esc(DATA.title.lead)}}"></div><div class="field-block"><label>タイトル文字サイズ</label><div class="range-row"><input id="edHeadlinePx" type="range" min="34" max="90" value="${{styleSettings.titleHeadlinePx}}"><input id="edHeadlinePxN" type="number" min="34" max="90" value="${{styleSettings.titleHeadlinePx}}"></div></div><div class="field-block"><label>サブタイトル文字サイズ</label><div class="range-row"><input id="edSubtitlePx" type="range" min="20" max="54" value="${{styleSettings.titleSubtitlePx}}"><input id="edSubtitlePxN" type="number" min="20" max="54" value="${{styleSettings.titleSubtitlePx}}"></div></div><div class="field-block"><label>リード文字サイズ</label><div class="range-row"><input id="edLeadPx" type="range" min="14" max="30" value="${{styleSettings.titleLeadPx}}"><input id="edLeadPxN" type="number" min="14" max="30" value="${{styleSettings.titleLeadPx}}"></div></div></div>`;
  }} else {{ body='<p>この画面には直接編集する項目はありません。</p>'; }}
  overlay.innerHTML=`<div class="modal"><div class="modal-head"><h3>編集</h3><button class="close-btn" id="closeModal">閉じる</button></div><div class="modal-body">${{body}}<p class="helper">編集内容はこのブラウザに自動保存されます。Ctrl + F5 や再起動後も保持されます。別のPCやGitHubへ移す場合は「設定を書き出す」を使用してください。</p><div class="editor-actions wrap"><div class="left-actions"><button class="secondary-btn" id="exportEdit">設定を書き出す</button><label class="secondary-btn file-btn">設定を読み込む<input id="importEdit" type="file" accept="application/json"></label><button class="danger-btn" id="resetEdit">編集をリセット</button></div><div class="right-actions"><button class="secondary-btn" id="cancelEdit">キャンセル</button><button class="save-btn" id="saveEdit">反映して保存</button></div></div></div></div>`;
  app.appendChild(overlay); const close=()=>overlay.remove();
  overlay.querySelector('#closeModal').addEventListener('click',close); overlay.querySelector('#cancelEdit').addEventListener('click',close); overlay.addEventListener('click',e=>{{if(e.target===overlay)close();}});
  overlay.querySelector('#exportEdit').addEventListener('click',downloadEdits);
  overlay.querySelector('#importEdit').addEventListener('change',e=>{{const f=e.target.files?.[0];if(!f)return;const r=new FileReader();r.onload=()=>{{try{{applySnapshot(JSON.parse(r.result));persist();close();renderCurrent();}}catch(err){{alert('設定ファイルを読み込めませんでした。');}}}};r.readAsText(f,'utf-8');}});
  overlay.querySelector('#resetEdit').addEventListener('click',()=>{{if(confirm('このブラウザに保存した編集内容をすべてリセットしますか？')){{localStorage.removeItem(STORAGE_KEY);location.reload();}}}});
  [['edSpeechPx','edSpeechPxN'],['edNamePx','edNamePxN'],['edTransitionPx','edTransitionPxN'],['edHeadlinePx','edHeadlinePxN'],['edSubtitlePx','edSubtitlePxN'],['edLeadPx','edLeadPxN']].forEach(([a,b])=>syncPair(overlay,a,b));
  const spSel=overlay.querySelector('#edSpeaker'),spName=overlay.querySelector('#edSpeakerName');if(spSel&&spName)spSel.addEventListener('change',()=>spName.value=DATA.characters[spSel.value].name);
  overlay.querySelector('#saveEdit').addEventListener('click',()=>{{
    if(ctx.kind==='dialogue'){{const seg=ctx.section.segments[ctx.slide.segmentIndex];seg.text=overlay.querySelector('#edText').value.trim();seg.speaker=overlay.querySelector('#edSpeaker').value;DATA.characters[seg.speaker].name=overlay.querySelector('#edSpeakerName').value.trim()||DATA.characters[seg.speaker].name;ctx.section.background=overlay.querySelector('#edBackground').value;ctx.section.music=overlay.querySelector('#edMusic').value;styleSettings.speechPx=Number(overlay.querySelector('#edSpeechPxN').value)||DEFAULT_STYLE.speechPx;styleSettings.namePx=Number(overlay.querySelector('#edNamePxN').value)||DEFAULT_STYLE.namePx;if(!ctx.section.characters.includes(seg.speaker))ctx.section.characters.push(seg.speaker);}}
    else if(ctx.kind==='transition'){{ctx.section.transition=overlay.querySelector('#edTransition').value.trim();ctx.section.music=overlay.querySelector('#edMusic').value;styleSettings.transitionPx=Number(overlay.querySelector('#edTransitionPxN').value)||DEFAULT_STYLE.transitionPx;}}
    else if(ctx.kind==='title'){{DATA.title.headline=overlay.querySelector('#edHeadline').value.trim();DATA.title.subtitle=overlay.querySelector('#edSubtitle').value.trim();DATA.title.lead=overlay.querySelector('#edLead').value.trim();styleSettings.titleHeadlinePx=Number(overlay.querySelector('#edHeadlinePxN').value)||DEFAULT_STYLE.titleHeadlinePx;styleSettings.titleSubtitlePx=Number(overlay.querySelector('#edSubtitlePxN').value)||DEFAULT_STYLE.titleSubtitlePx;styleSettings.titleLeadPx=Number(overlay.querySelector('#edLeadPxN').value)||DEFAULT_STYLE.titleLeadPx;}}
    persist();close();renderCurrent();
  }});
}}
function bindNext(fn) {{
  const btn = document.getElementById('next');
  if (btn) btn.addEventListener('click', fn, {{ once: true }});
}}

function renderTitle() {{
  currentMode = 'main';
  buildSlides();
  cursor = -1;
  const first = DATA.sections[0];
  setMusic(first.music);
  const explainer = DATA.characters.explainer;
  const extraButton = mainCompleted() && (DATA.additional_sections || []).length
    ? `<button class="next-btn secondary-home" id="startAdditional">地域の高齢化と職員負担</button>` : '';
  app.innerHTML = `
    <div class="stage" style="${{backgroundStyle('entrance')}}">
      <div class="cast count-1"><div class="char-wrap active"><img src="${{explainer.src}}" alt=""></div></div>
      <div class="title-card">
        <h1 style="font-size:${{styleSettings.titleHeadlinePx}}px">${{esc(DATA.title.headline)}}</h1>
        <h2 style="font-size:${{styleSettings.titleSubtitlePx}}px">${{esc(DATA.title.subtitle)}}</h2>
        <p style="font-size:${{styleSettings.titleLeadPx}}px">${{esc(DATA.title.lead)}}</p>
      </div>
    </div>
    ${{utilityBar()}}
    <div class="controls home-controls"><div class="home-buttons"><button class="next-btn" id="startMain">はじめる</button>${{extraButton}}</div></div>`;
  bindUtilities();
  document.getElementById('startMain').addEventListener('click', () => startExperience('main'));
  const extra = document.getElementById('startAdditional');
  if (extra) extra.addEventListener('click', () => startExperience('additional'));
}}

function renderTransition(section) {{
  setMusic(section.music);
  app.innerHTML = `
    <div class="stage transition-stage">
      <div class="transition-card"><h2 style="font-size:${{styleSettings.transitionPx}}px">${{esc(section.transition)}}</h2></div>
    </div>
    ${{utilityBar()}}
    ${{controls('場面を見る')}}`;
  bindUtilities();
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
          <div class="nameplate" style="font-size:${{styleSettings.namePx}}px">${{esc(c.name)}}</div>
          <div class="speech" style="font-size:${{styleSettings.speechPx}}px">${{esc(segment.text)}}</div>
        </div>
      </div>
    </div>
    ${{utilityBar()}}
    ${{controls('次へ')}}`;
  bindUtilities();
  bindNext(nextSlide);
}}

function renderEnd() {{
  setMusic('resolution');
  if (currentMode === 'main') {{
    markMainCompleted();
    app.innerHTML = `
      <div class="stage" style="${{backgroundStyle('meeting')}}">
        <div class="end-card">
          <h2>あなたなら何を優先しますか？</h2>
          <p>5つの投資案から、信州みらい病院にとって優先すべき投資を考えてみましょう。</p>
        </div>
      </div>
      ${{utilityBar()}}
      <div class="controls home-controls"><div class="home-buttons"><button class="next-btn" id="goAdditional">地域の高齢化と職員負担</button><button class="next-btn secondary-home" id="goHome">タイトルへ戻る</button></div></div>`;
    bindUtilities();
    document.getElementById('goAdditional').addEventListener('click', () => startExperience('additional'));
    document.getElementById('goHome').addEventListener('click', () => {{ currentTrack=null; audio.pause(); audio.currentTime=0; renderTitle(); }});
  }} else {{
    app.innerHTML = `
      <div class="stage" style="${{backgroundStyle('meeting')}}">
        <div class="end-card"><h2>信州みらい病院</h2><p>みなさんの検討で病院を一緒に変革していきましょう。</p></div>
      </div>
      ${{utilityBar()}}
      ${{controls('タイトルへ戻る')}}`;
    bindUtilities();
    bindNext(() => {{ currentTrack=null; audio.pause(); audio.currentTime=0; renderTitle(); }});
  }}
}}

function renderCurrent() {{
  const slide = slides[cursor];
  if (!slide || slide.kind === 'end') {{ renderEnd(); return; }}
  const section = currentSections()[slide.sectionIndex];
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
