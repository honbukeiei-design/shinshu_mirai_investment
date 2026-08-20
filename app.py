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

try:
    SUPABASE_URL = str(st.secrets.get("SUPABASE_URL", "")).strip()
    SUPABASE_ANON_KEY = str(st.secrets.get("SUPABASE_ANON_KEY", "")).strip()
except Exception:
    SUPABASE_URL = ""
    SUPABASE_ANON_KEY = ""


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
    "submission_store": {
        "supabase_url": SUPABASE_URL,
        "supabase_anon_key": SUPABASE_ANON_KEY,
    },
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
.scene-home-btn {{ width: 100%; margin-bottom: 12px; background: #eef5f8; border: 1px solid #aac1cf; font-weight: 700; }}
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

/* proposal input + BI dashboard */
.work-screen {{
  position: absolute;
  inset: 10px 14px 82px;
  border-radius: 24px;
  overflow: hidden;
  background: linear-gradient(145deg,#f7fbfd,#e8f2f7);
  color: #17394d;
  box-shadow: 0 14px 38px rgba(0,0,0,.22);
  z-index: 5;
}}
.work-head {{
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 24px;
  background: rgba(255,255,255,.94);
  border-bottom: 1px solid #d6e4eb;
}}
.work-title {{ font-size: clamp(1.25rem,2.1vw,2rem); font-weight: 950; letter-spacing: .02em; }}
.work-badge {{ padding: 8px 14px; border-radius: 999px; background:#237ea8; color:white; font-weight:900; white-space:nowrap; }}
.form-shell {{ height: calc(100% - 70px); display:grid; grid-template-columns: minmax(430px, 650px) minmax(300px, 1fr); gap:18px; padding:16px 20px; }}
.entry-card, .summary-card, .bi-card {{
  background:#fff; border:1px solid #d3e1e8; border-radius:24px; box-shadow:0 12px 28px rgba(28,70,91,.10);
}}
.entry-card {{ padding:14px 18px; overflow:hidden; }}
.form-grid {{ display:grid; grid-template-columns: 1fr 1fr; gap:9px 12px; }}
.form-field {{ min-width:0; }}
.form-field.full {{ grid-column:1/-1; }}
.form-field label {{ display:block; margin:0 0 4px; font-weight:900; font-size:.88rem; color:#27546b; }}
.form-field input, .form-field select, .form-field textarea {{
  width:100%; border:1px solid #c7d8e1; border-radius:9px; background:#fbfdfe; color:#18394c;
  min-height:39px; padding:7px 10px; font:inherit; font-weight:750; outline:none;
}}
.form-field textarea {{ min-height:74px; max-height:90px; resize:none; line-height:1.45; }}
.form-field input:focus, .form-field select:focus, .form-field textarea:focus {{ border-color:#2f83ad; box-shadow:0 0 0 3px rgba(47,131,173,.12); }}
.alloc-head {{ grid-column:1/-1; display:grid; grid-template-columns: 1fr 150px; gap:10px; font-size:.8rem; font-weight:900; color:#658093; margin-top:2px; }}
.alloc-row {{ grid-column:1/-1; display:grid; grid-template-columns: 1fr 150px; gap:10px; }}
.total-strip {{ grid-column:1/-1; display:flex; align-items:center; justify-content:space-between; padding:8px 12px; border-radius:11px; background:#eef6fa; font-weight:950; }}
.total-strip.over {{ background:#fff0f0; color:#a92d2d; }}
.submit-row {{ grid-column:1/-1; display:flex; gap:8px; justify-content:flex-end; align-items:center; }}
.form-message {{ flex:1; min-height:1.2em; font-size:.84rem; font-weight:800; color:#246b47; }}
.form-message.error {{ color:#a72a2a; }}
.action-btn {{ min-height:43px; border:0; border-radius:11px; padding:9px 18px; background:#317ead; color:#fff; font-weight:950; cursor:pointer; }}
.action-btn.secondary {{ background:#e8f1f6; color:#214c64; border:1px solid #cbdce5; }}
.summary-card {{ padding:18px; display:flex; flex-direction:column; min-height:0; }}
.summary-card h3 {{ margin:0 0 12px; font-size:1.1rem; }}
.plan-list {{ display:grid; gap:8px; }}
.plan-line {{ display:grid; grid-template-columns: 1fr auto; gap:10px; align-items:center; padding:10px 12px; border-radius:12px; background:#f3f8fb; }}
.plan-line strong {{ font-size:.93rem; }}
.plan-line span {{ font-weight:950; color:#227da7; }}
.mini-note {{ margin-top:auto; padding-top:12px; color:#607b8b; font-size:.84rem; line-height:1.55; }}
.dashboard-shell {{ height:calc(100% - 70px); padding:12px 16px 14px; display:grid; grid-template-rows:auto auto 1fr; gap:10px; }}
.filter-row {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; background:#fff; padding:9px 12px; border:1px solid #d5e2e9; border-radius:14px; }}
.filter-row label {{ font-weight:900; font-size:.84rem; color:#536f80; }}
.filter-row select {{ min-height:35px; border:1px solid #c9dae3; border-radius:8px; padding:5px 8px; min-width:150px; background:#fff; }}
.kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:9px; }}
.kpi {{ background:#fff; border:1px solid #d7e3e9; border-radius:14px; padding:9px 12px; }}
.kpi .label {{ font-size:.76rem; font-weight:900; color:#688190; }}
.kpi .value {{ font-size:1.35rem; font-weight:950; margin-top:2px; }}
.bi-grid {{ min-height:0; display:grid; grid-template-columns: 1.15fr .85fr; gap:10px; }}
.bi-card {{ min-height:0; padding:12px 14px; overflow:hidden; }}
.bi-card h3 {{ margin:0 0 8px; font-size:1rem; }}
.chart-scroll, .table-scroll {{ height:calc(100% - 30px); overflow:auto; }}
.bar-group {{ margin:0 0 10px; }}
.bar-label {{ display:flex; justify-content:space-between; gap:10px; font-size:.78rem; font-weight:900; margin-bottom:4px; }}
.bar-track {{ height:14px; background:#edf3f6; border-radius:999px; overflow:hidden; margin-bottom:3px; }}
.bar-fill {{ height:100%; border-radius:999px; min-width:0; }}
.bar-fill.first {{ background:#61a5c9; }}
.bar-fill.final {{ background:#245f86; }}
.legend {{ display:flex; gap:12px; align-items:center; font-size:.76rem; font-weight:850; color:#5f7786; margin-bottom:7px; }}
.legend i {{ width:12px; height:12px; border-radius:3px; display:inline-block; margin-right:4px; vertical-align:-2px; }}
.legend .f1 {{ background:#61a5c9; }} .legend .f2 {{ background:#245f86; }}
.compare-table {{ width:100%; border-collapse:collapse; font-size:.78rem; }}
.compare-table th,.compare-table td {{ padding:6px 7px; border-bottom:1px solid #e0e9ee; text-align:left; vertical-align:top; }}
.compare-table th {{ position:sticky; top:0; background:#f7fafc; z-index:1; color:#4d6878; }}
.diff-plus {{ color:#176b49; font-weight:900; }} .diff-minus {{ color:#9c3434; font-weight:900; }}
.empty-state {{ height:100%; display:grid; place-items:center; color:#69808e; font-weight:850; text-align:center; padding:20px; }}
.home-tools {{ display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }}
.home-tools .next-btn {{ width:auto; min-width:220px; padding:0 18px; }}
@media (max-width: 900px) {{
  .work-screen {{ inset:5px 7px 66px; border-radius:16px; }}
  .work-head {{ height:58px; padding:8px 12px; }}
  .form-shell {{ height:calc(100% - 58px); grid-template-columns:1fr; padding:8px; }}
  .summary-card {{ display:none; }}
  .entry-card {{ padding:9px 10px; border-radius:16px; overflow:auto; }}
  .form-grid {{ gap:6px 8px; }}
  .form-field label {{ font-size:.75rem; margin-bottom:2px; }}
  .form-field input,.form-field select {{ min-height:34px; padding:5px 7px; font-size:.84rem; }}
  .form-field textarea {{ min-height:58px; max-height:62px; font-size:.84rem; }}
  .alloc-row {{ grid-template-columns:1fr 110px; gap:7px; }}
  .alloc-head {{ grid-template-columns:1fr 110px; }}
  .dashboard-shell {{ height:calc(100% - 58px); padding:6px; gap:6px; }}
  .kpis {{ grid-template-columns:repeat(2,1fr); }}
  .bi-grid {{ grid-template-columns:1fr; grid-template-rows:1fr 1fr; }}
  .filter-row {{ padding:6px; }}
  .filter-row select {{ min-width:110px; }}
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
const ADDITIONAL_COMPLETED_KEY = 'shinshu_mirai_investment_additional_completed_v1';
const SUBMISSION_KEY = 'shinshu_mirai_investment_submissions_v1';
const PLAN_LABELS = {{A:'A：MRI更新',B:'B：看護師採用',C:'C：小児科強化',D:'D：病院DX',E:'E：健診事業強化'}};
const PLAN_AMOUNTS = {{A:[70],B:[10,20,30],C:[30],D:[30,40,50,60],E:[10,20,30]}};
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
function additionalCompleted() {{ try {{ return localStorage.getItem(ADDITIONAL_COMPLETED_KEY) === '1'; }} catch(e) {{ return false; }} }}
function markAdditionalCompleted() {{ try {{ localStorage.setItem(ADDITIONAL_COMPLETED_KEY, '1'); }} catch(e) {{}} }}
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
    <div class="modal-body">
      <button class="scene-btn scene-home-btn" id="sceneHome">タイトルに戻る</button>
      <div class="scene-grid">${{items}}</div>
    </div>
  </div>`;
  app.appendChild(overlay);
  overlay.querySelector('#closeModal').addEventListener('click', () => overlay.remove());
  overlay.addEventListener('click', e => {{ if (e.target === overlay) overlay.remove(); }});
  overlay.querySelector('#sceneHome').addEventListener('click', () => {{
    overlay.remove();
    currentTrack = null;
    audio.pause();
    audio.currentTime = 0;
    renderTitle();
  }});
  overlay.querySelectorAll('.scene-btn[data-section]').forEach(btn => btn.addEventListener('click', () => {{
    const sectionIndex = Number(btn.dataset.section);
    const idx = slideIndexForSection(sectionIndex);
    if (idx >= 0) {{ overlay.remove(); cursor = idx; started = true; renderCurrent(); }}
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


function safeJsonParse(raw, fallback) {{ try {{ return JSON.parse(raw); }} catch(e) {{ return fallback; }} }}
function localSubmissions() {{ try {{ return safeJsonParse(localStorage.getItem(SUBMISSION_KEY)||'[]', []); }} catch(e) {{ return []; }} }}
function saveLocalSubmissions(rows) {{ try {{ localStorage.setItem(SUBMISSION_KEY, JSON.stringify(rows)); }} catch(e) {{}} }}
function identityKey(team,nickname) {{ return `${{team.trim()}}||${{nickname.trim()}}`.toLowerCase(); }}
function participantKey(team,nickname) {{ return identityKey(team,nickname); }}
function amountMap(record) {{
  const out={{A:0,B:0,C:0,D:0,E:0}};
  (record.allocations||[]).forEach(x=>{{ if(out[x.plan]!==undefined) out[x.plan]=Number(x.amount)||0; }});
  return out;
}}
function flattenForRemote(record) {{
  const m=amountMap(record); return {{participant_key:record.participant_key,team_name:record.team_name,nickname:record.nickname,round:record.round,a_amount:m.A,b_amount:m.B,c_amount:m.C,d_amount:m.D,e_amount:m.E,total_amount:record.total_amount,perspective:record.perspective||'',updated_at:new Date().toISOString()}};
}}
function remoteEnabled() {{ return !!(DATA.submission_store?.supabase_url && DATA.submission_store?.supabase_anon_key); }}
async function saveRemote(record) {{
  if(!remoteEnabled()) return true;
  const url=DATA.submission_store.supabase_url.replace(/\/$/,'')+'/rest/v1/investment_submissions?on_conflict=participant_key,round';
  const key=DATA.submission_store.supabase_anon_key;
  const res=await fetch(url,{{method:'POST',headers:{{'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json','Prefer':'resolution=merge-duplicates,return=minimal'}},body:JSON.stringify(flattenForRemote(record))}});
  if(!res.ok) throw new Error(`共有保存に失敗しました (${{res.status}})`); return true;
}}
async function loadRemote() {{
  if(!remoteEnabled()) return null;
  const url=DATA.submission_store.supabase_url.replace(/\/$/,'')+'/rest/v1/investment_submissions?select=*&order=updated_at.desc';
  const key=DATA.submission_store.supabase_anon_key;
  const res=await fetch(url,{{headers:{{'apikey':key,'Authorization':'Bearer '+key}}}}); if(!res.ok) throw new Error(`共有データを取得できません (${{res.status}})`);
  const rows=await res.json();
  return rows.map(r=>({{participant_key:r.participant_key,team_name:r.team_name,nickname:r.nickname,round:r.round,allocations:[['A',r.a_amount],['B',r.b_amount],['C',r.c_amount],['D',r.d_amount],['E',r.e_amount]].filter(x=>Number(x[1])>0).map(x=>({{plan:x[0],amount:Number(x[1])}})),total_amount:Number(r.total_amount)||0,perspective:r.perspective||'',updated_at:r.updated_at||''}}));
}}
function upsertLocal(record) {{
  const rows=localSubmissions(); const i=rows.findIndex(r=>r.participant_key===record.participant_key && r.round===record.round);
  if(i>=0) rows[i]=record; else rows.push(record); saveLocalSubmissions(rows);
}}
function latestIdentityRecord(round) {{
  const rows=localSubmissions().filter(r=>r.round===round); return rows.length?rows[rows.length-1]:null;
}}
function existingForIdentity(team,nickname,round) {{ const k=identityKey(team,nickname); return localSubmissions().find(r=>identityKey(r.team_name,r.nickname)===k && r.round===round); }}
function stopMusicForWork(){{ audio.pause(); currentTrack=null; }}
function homeButton(label,id,secondary=false){{ return `<button class="next-btn ${{secondary?'secondary-home':''}}" id="${{id}}">${{esc(label)}}</button>`; }}

function renderProposal(round) {{
  stopMusicForWork();
  const isFinal=round==='final';
  if(!mainCompleted()) {{ renderTitle(); return; }}
  if(isFinal && !additionalCompleted()) {{ renderTitle(); return; }}
  const seed = latestIdentityRecord(isFinal?'first':'first');
  const finalExisting = isFinal && seed ? existingForIdentity(seed.team_name,seed.nickname,'final') : null;
  const current = finalExisting || (isFinal ? seed : latestIdentityRecord('first')) || {{team_name:'',nickname:'',allocations:[],perspective:''}};
  const allocMap=Object.fromEntries((current.allocations||[]).map(x=>[x.plan,x.amount]));
  const selectedPlans=(current.allocations||[]).map(x=>x.plan);
  const rows=[0,1,2,3].map(i=>{{ const plan=selectedPlans[i]||''; const amount=plan?(allocMap[plan]||PLAN_AMOUNTS[plan][0]):''; return `<div class="alloc-row"><select class="plan-select" data-row="${{i}}"><option value="">選択してください</option>${{Object.entries(PLAN_LABELS).map(([k,v])=>`<option value="${{k}}" ${{k===plan?'selected':''}}>${{v}}</option>`).join('')}}</select><select class="amount-select" data-row="${{i}}"></select></div>`; }}).join('');
  app.innerHTML=`<div class="work-screen"><div class="work-head"><div class="work-title">${{isFinal?'最終案の入力':'第1回案の入力'}}</div><div class="work-badge">重点投資予算 100万円</div></div><div class="form-shell"><div class="entry-card"><div class="form-grid">
    <div class="form-field"><label>チーム名</label><input id="teamName" value="${{esc(current.team_name||'')}}" autocomplete="organization"></div>
    <div class="form-field"><label>呼び名</label><input id="nickname" value="${{esc(current.nickname||'')}}" autocomplete="nickname"></div>
    <div class="alloc-head"><span>投資案</span><span>金額</span></div>${{rows}}
    <div class="total-strip" id="totalStrip"><span>合計</span><span id="totalAmount">0万円</span></div>
    <div class="form-field full"><label>最も重視した視点</label><textarea id="perspective" placeholder="重視したことを入力してください">${{esc(current.perspective||'')}}</textarea></div>
    <div class="submit-row"><div class="form-message" id="formMessage"></div><button class="action-btn secondary" id="backHome">戻る</button><button class="action-btn" id="saveProposal">${{isFinal?'最終案を送信':'第1回案を提出'}}</button></div>
  </div></div><div class="summary-card"><h3>配分案</h3><div class="plan-list" id="proposalSummary"></div><div class="mini-note">投資案は最大4つまで選択できます。合計が100万円を超える組み合わせは選択できません。</div></div></div></div>`;
  const planEls=[...document.querySelectorAll('.plan-select')], amountEls=[...document.querySelectorAll('.amount-select')];
  function selections(){{ return planEls.map((p,i)=>({{plan:p.value,amount:Number(amountEls[i].value)||0}})).filter(x=>x.plan); }}
  function totalExcluding(row){{ return selections().reduce((sum,x,i)=>sum+x.amount,0) - (Number(amountEls[row]?.value)||0); }}
  function rebuildAmounts(row, keepValue=true){{
    const p=planEls[row].value, el=amountEls[row], old=keepValue?Number(el.value)||0:0; el.innerHTML='';
    if(!p){{ el.innerHTML='<option value="">—</option>'; el.disabled=true; return; }}
    el.disabled=false; const base=selections().reduce((s,x,idx)=> idx===row?s:s+x.amount,0); const opts=PLAN_AMOUNTS[p];
    opts.forEach(a=>{{ const disabled=base+a>100; const op=document.createElement('option'); op.value=a; op.textContent=`${{a}} 万円`; op.disabled=disabled; if((old===a || (!old && !disabled && !el.value))) op.selected=true; el.appendChild(op); }});
    if(![...el.options].some(o=>o.selected&&!o.disabled)){{ const first=[...el.options].find(o=>!o.disabled); if(first) first.selected=true; else {{ el.innerHTML='<option value="">上限超過</option>'; el.disabled=true; }} }}
  }}
  function refresh(){{
    const used=planEls.map(x=>x.value).filter(Boolean);
    planEls.forEach((sel,row)=>{{
      const otherTotal=planEls.reduce((sum,p,idx)=>idx===row?sum:sum+(Number(amountEls[idx]?.value)||0),0);
      [...sel.options].forEach(op=>{{
        if(!op.value)return;
        const duplicate=used.includes(op.value)&&op.value!==sel.value;
        const minAmount=Math.min(...PLAN_AMOUNTS[op.value]);
        const budgetBlocked=otherTotal+minAmount>100 && op.value!==sel.value;
        op.disabled=duplicate||budgetBlocked;
      }});
    }});
    amountEls.forEach((_,i)=>rebuildAmounts(i,true));
    const items=selections(), total=items.reduce((s,x)=>s+x.amount,0); document.getElementById('totalAmount').textContent=`${{total}}万円`; document.getElementById('totalStrip').classList.toggle('over',total>100);
    document.getElementById('proposalSummary').innerHTML=items.length?items.map(x=>`<div class="plan-line"><strong>${{esc(PLAN_LABELS[x.plan])}}</strong><span>${{x.amount}}万円</span></div>`).join(''):'<div class="empty-state">投資案を選択してください</div>';
  }}
  planEls.forEach((sel,i)=>sel.addEventListener('change',()=>{{
    rebuildAmounts(i,false);
    if(sel.value && amountEls[i].disabled){{ sel.value=''; rebuildAmounts(i,false); }}
    refresh();
  }})); amountEls.forEach(el=>el.addEventListener('change',refresh));
  for(let i=0;i<4;i++) rebuildAmounts(i,true); refresh();
  document.getElementById('backHome').addEventListener('click',renderTitle);
  document.getElementById('saveProposal').addEventListener('click',async()=>{{
    const team=document.getElementById('teamName').value.trim(), nick=document.getElementById('nickname').value.trim(), perspective=document.getElementById('perspective').value.trim(), allocations=selections(), total=allocations.reduce((s,x)=>s+x.amount,0), msg=document.getElementById('formMessage');
    msg.className='form-message'; msg.textContent='';
    if(!team||!nick){{ msg.classList.add('error'); msg.textContent='チーム名と呼び名を入力してください。'; return; }}
    if(!allocations.length){{ msg.classList.add('error'); msg.textContent='投資案を1つ以上選択してください。'; return; }}
    if(total>100){{ msg.classList.add('error'); msg.textContent='合計は100万円以内にしてください。'; return; }}
    const firstMatch=isFinal?existingForIdentity(team,nick,'first'):null;
    if(isFinal&&!firstMatch){{ msg.classList.add('error'); msg.textContent='同じチーム名・呼び名の第1回案が見つかりません。'; return; }}
    const pk=firstMatch?.participant_key || participantKey(team,nick);
    const record={{participant_key:pk,team_name:team,nickname:nick,round,allocations,total_amount:total,perspective,updated_at:new Date().toISOString()}};
    upsertLocal(record); msg.textContent=remoteEnabled()?'保存しています…':'保存しました。';
    try{{ await saveRemote(record); msg.textContent=remoteEnabled()?'保存・共有しました。':'保存しました。'; setTimeout(()=>renderDashboard(),450); }}catch(e){{ msg.classList.add('error'); msg.textContent=`ブラウザには保存しました。${{e.message}}`; }}
  }});
}}

function uniqueVals(rows,key){{ return [...new Set(rows.map(r=>r[key]).filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b),'ja')); }}
function aggregatePair(rows){{
  const result={{}}; for(const p of Object.keys(PLAN_LABELS)) result[p]={{first:[],final:[]}};
  rows.forEach(r=>{{ const m=amountMap(r); Object.keys(result).forEach(p=>result[p][r.round]?.push(m[p]||0)); }});
  const avg=a=>a.length?Math.round(a.reduce((s,x)=>s+x,0)/a.length):0; Object.keys(result).forEach(p=>{{result[p].first=avg(result[p].first);result[p].final=avg(result[p].final);}}); return result;
}}
function renderBars(agg){{ return `<div class="legend"><span><i class="f1"></i>第1回</span><span><i class="f2"></i>最終</span></div>${{Object.entries(PLAN_LABELS).map(([p,label])=>{{const a=agg[p];return `<div class="bar-group"><div class="bar-label"><span>${{esc(label)}}</span><span>${{a.first}} → ${{a.final}}万円</span></div><div class="bar-track"><div class="bar-fill first" style="width:${{Math.min(100,a.first)}}%"></div></div><div class="bar-track"><div class="bar-fill final" style="width:${{Math.min(100,a.final)}}%"></div></div></div>`;}}).join('')}}`; }}
function comparisonRows(rows){{
  const groups={{}}; rows.forEach(r=>{{const k=identityKey(r.team_name,r.nickname);groups[k]??={{team:r.team_name,nick:r.nickname,first:null,final:null}};groups[k][r.round]=r;}});
  return Object.values(groups).sort((a,b)=>(a.team+a.nick).localeCompare(b.team+b.nick,'ja'));
}}
async function renderDashboard(){{
  stopMusicForWork(); if(!mainCompleted()){{renderTitle();return;}}
  app.innerHTML=`<div class="work-screen"><div class="work-head"><div class="work-title">結果比較</div><div class="work-badge" id="dataMode">読み込み中</div></div><div class="dashboard-shell"><div class="filter-row"><label>チーム名</label><select id="teamFilter"><option value="">すべて</option></select><label>呼び名</label><select id="nickFilter"><option value="">すべて</option></select><button class="action-btn secondary" id="reloadData">更新</button><button class="action-btn secondary" id="dashHome">戻る</button></div><div class="kpis"><div class="kpi"><div class="label">回答者</div><div class="value" id="kpiPeople">0</div></div><div class="kpi"><div class="label">チーム</div><div class="value" id="kpiTeams">0</div></div><div class="kpi"><div class="label">第1回案</div><div class="value" id="kpiFirst">0</div></div><div class="kpi"><div class="label">最終案</div><div class="value" id="kpiFinal">0</div></div></div><div class="bi-grid"><div class="bi-card"><h3>投資配分の比較</h3><div class="chart-scroll" id="chartArea"><div class="empty-state">データを読み込んでいます</div></div></div><div class="bi-card"><h3>回答者別比較</h3><div class="table-scroll" id="tableArea"></div></div></div></div></div>`;
  document.getElementById('dashHome').addEventListener('click',renderTitle); document.getElementById('reloadData').addEventListener('click',()=>renderDashboard());
  let all=[]; try{{ const remote=await loadRemote(); all=remote??localSubmissions(); document.getElementById('dataMode').textContent=remote?'共有データ':'このブラウザ'; }}catch(e){{ all=localSubmissions(); document.getElementById('dataMode').textContent='このブラウザ'; }}
  const tf=document.getElementById('teamFilter'), nf=document.getElementById('nickFilter'); uniqueVals(all,'team_name').forEach(v=>tf.insertAdjacentHTML('beforeend',`<option>${{esc(v)}}</option>`)); uniqueVals(all,'nickname').forEach(v=>nf.insertAdjacentHTML('beforeend',`<option>${{esc(v)}}</option>`));
  function draw(){{
    const team=tf.value,nick=nf.value,rows=all.filter(r=>(!team||r.team_name===team)&&(!nick||r.nickname===nick)); const comps=comparisonRows(rows); document.getElementById('kpiPeople').textContent=comps.length;document.getElementById('kpiTeams').textContent=uniqueVals(rows,'team_name').length;document.getElementById('kpiFirst').textContent=rows.filter(r=>r.round==='first').length;document.getElementById('kpiFinal').textContent=rows.filter(r=>r.round==='final').length;
    document.getElementById('chartArea').innerHTML=rows.length?renderBars(aggregatePair(rows)):'<div class="empty-state">該当する回答はありません</div>';
    if(!comps.length){{document.getElementById('tableArea').innerHTML='<div class="empty-state">該当する回答はありません</div>';return;}}
    const tr=comps.map(g=>{{const fm=g.first?amountMap(g.first):{{}}, lm=g.final?amountMap(g.final):{{}}; const diffs=Object.keys(PLAN_LABELS).map(p=>{{const d=(lm[p]||0)-(fm[p]||0);return `${{p}}:${{d>0?'+':''}}${{d}}`}}).join(' / ');return `<tr><td>${{esc(g.team)}}</td><td>${{esc(g.nick)}}</td><td>${{g.first?g.first.total_amount+'万円':'—'}}</td><td>${{g.final?g.final.total_amount+'万円':'—'}}</td><td>${{esc(diffs)}}</td><td>${{esc(g.first?.perspective||'')}}</td><td>${{esc(g.final?.perspective||'')}}</td></tr>`;}}).join('');
    document.getElementById('tableArea').innerHTML=`<table class="compare-table"><thead><tr><th>チーム</th><th>呼び名</th><th>第1回</th><th>最終</th><th>A～Eの変化</th><th>第1回の視点</th><th>最終の視点</th></tr></thead><tbody>${{tr}}</tbody></table>`;
  }}
  tf.addEventListener('change',()=>{{ nf.innerHTML='<option value="">すべて</option>'+uniqueVals(all.filter(r=>!tf.value||r.team_name===tf.value),'nickname').map(v=>`<option>${{esc(v)}}</option>`).join(''); draw(); }}); nf.addEventListener('change',draw); draw();
}}

function renderTitle() {{
  currentMode = 'main';
  buildSlides();
  cursor = -1;
  const first = DATA.sections[0];
  setMusic(first.music);
  const explainer = DATA.characters.explainer;
  const doneMain=mainCompleted(), doneAdditional=additionalCompleted();
  let toolButtons='';
  if(doneMain){{
    toolButtons += homeButton(latestIdentityRecord('first')?'第1回案を確認・修正':'第1回案を入力','openFirst');
    toolButtons += homeButton('地域の高齢化と職員負担','startAdditional',true);
    toolButtons += homeButton('結果比較','openDashboard',true);
  }}
  if(doneAdditional) toolButtons += homeButton(latestIdentityRecord('final')?'最終案を確認・修正':'最終案を入力','openFinal');
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
    <div class="controls home-controls"><div class="home-tools">${{homeButton(doneMain?'もう一度見る':'はじめる','startMain')}}${{toolButtons}}</div></div>`;
  bindUtilities();
  document.getElementById('startMain').addEventListener('click', () => startExperience('main'));
  const a=document.getElementById('startAdditional'); if(a)a.addEventListener('click',()=>startExperience('additional'));
  const f=document.getElementById('openFirst'); if(f)f.addEventListener('click',()=>renderProposal('first'));
  const fin=document.getElementById('openFinal'); if(fin)fin.addEventListener('click',()=>renderProposal('final'));
  const d=document.getElementById('openDashboard'); if(d)d.addEventListener('click',renderDashboard);
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
      <div class="controls home-controls"><div class="home-tools"><button class="next-btn" id="goFirst">第1回案を入力</button><button class="next-btn secondary-home" id="goAdditional">地域の高齢化と職員負担</button><button class="next-btn secondary-home" id="goHome">タイトルへ戻る</button></div></div>`;
    bindUtilities();
    document.getElementById('goFirst').addEventListener('click',()=>renderProposal('first'));
    document.getElementById('goAdditional').addEventListener('click', () => startExperience('additional'));
    document.getElementById('goHome').addEventListener('click', () => {{ currentTrack=null; audio.pause(); audio.currentTime=0; renderTitle(); }});
  }} else {{
    markAdditionalCompleted();
    app.innerHTML = `
      <div class="stage" style="${{backgroundStyle('meeting')}}">
        <div class="end-card"><h2>信州みらい病院</h2><p>みなさんの検討で病院を一緒に変革していきましょう。</p></div>
      </div>
      ${{utilityBar()}}
      <div class="controls home-controls"><div class="home-tools"><button class="next-btn" id="goFinal">最終案を入力</button><button class="next-btn secondary-home" id="goDashboard">結果比較</button><button class="next-btn secondary-home" id="goHome">タイトルへ戻る</button></div></div>`;
    bindUtilities();
    document.getElementById('goFinal').addEventListener('click',()=>renderProposal('final'));
    document.getElementById('goDashboard').addEventListener('click',renderDashboard);
    document.getElementById('goHome').addEventListener('click',()=>{{ currentTrack=null; audio.pause(); audio.currentTime=0; renderTitle(); }});
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
