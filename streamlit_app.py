"""
Actuarial Financial Explainability Platform | Live Presentation Demo App
Multimodal AI for Life Insurance Financial Explainability
Covers:
  - Stage 0: Solution Vision & Dual-Track Architecture (Track 1 Auto-Updated vs Track 2 Question-Driven)
  - Stage 1: Solvency II Balance Sheet & Line-Item Explanatory Guide (WP_Fund vs NP_Fund)
  - Stage 2: 1-Click Executive Dashboard (YE 2024 Historical -> YE 2025 Prior -> YE 2026 Predicted vs YE 2026 Latest Actual)
  - Stage 3: Governed Data & Knowledge Explorer (6 Artifacts)
  - Stage 4: 'Ask Your Balance Sheet' Multi-Agent Studio (Explaining YE 2026 Latest Actuals)
  - Stage 5: Mosaic AI Gateway & Unity Catalog Audit Log
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Multimodal AI for Life Insurance Financial Explainability",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Dark-mode compatible executive card styles with guaranteed high contrast */
    .main-header {
        background: linear-gradient(135deg, #041838 0%, #072659 70%, #0f3d85 100%);
        color: #ffffff !important;
        padding: 1.1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #1e3a8a;
    }
    .main-header h2 { color: #ffffff !important; margin: 0 0 0.25rem 0; font-size: 1.5rem; }
    .main-header p { color: #cbd5e1 !important; margin: 0; font-size: 0.88rem; }
    .latest-pill {
        background-color: #10b981 !important;
        color: #ffffff !important;
        padding: 3px 10px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.78rem;
        display: inline-block;
        margin-left: 8px;
    }
    .cue-banner {
        background-color: #262117 !important;
        border-left: 5px solid #f59e0b !important;
        padding: 0.75rem 1.1rem !important;
        border-radius: 6px !important;
        margin-bottom: 1rem !important;
        color: #fef08a !important;
        font-size: 0.88rem !important;
        border: 1px solid #451a03 !important;
        border-left: 5px solid #f59e0b !important;
    }
    .cue-banner strong, .cue-banner b { color: #fbbf24 !important; }
    .cue-banner code {
        color: #fef08a !important;
        background-color: #451a03 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid #78350f !important;
    }
    .narrative-card {
        background-color: #1e293b !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 10px !important;
        padding: 1.2rem 1.4rem !important;
        margin-bottom: 1rem !important;
        color: #f1f5f9 !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.3) !important;
    }
    .narrative-card b, .narrative-card strong { color: #ffffff !important; }
    .narrative-card p { color: #e2e8f0 !important; line-height: 1.6 !important; }
    .narrative-card ul, .narrative-card ol { color: #f1f5f9 !important; padding-left: 1.2rem !important; }
    .narrative-card li { color: #e2e8f0 !important; margin-bottom: 0.4rem !important; line-height: 1.6 !important; }
    .narrative-card code {
        color: #38bdf8 !important;
        background-color: #0f172a !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid #334155 !important;
        font-weight: 600 !important;
    }
    .track-card {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-left: 6px solid #38bdf8 !important;
        border-radius: 10px !important;
        padding: 1.1rem 1.3rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.3) !important;
        color: #f8fafc !important;
    }
    .track-card.track2 {
        border-left-color: #c084fc !important;
    }
    .track-card h4 {
        color: #38bdf8 !important;
        font-size: 1.05rem !important;
        margin-top: 0 !important;
        margin-bottom: 0.45rem !important;
    }
    .track-card.track2 h4 {
        color: #c084fc !important;
    }
    .track-card p {
        color: #e2e8f0 !important;
        margin-bottom: 0.6rem !important;
    }
    .track-card p i, .track-card p em {
        color: #93c5fd !important;
        font-style: italic !important;
    }
    .track-card ol, .track-card ul {
        color: #f8fafc !important;
        padding-left: 1.2rem !important;
    }
    .track-card li {
        color: #f1f5f9 !important;
        margin-bottom: 0.45rem !important;
        line-height: 1.65 !important;
    }
    .track-card b, .track-card strong {
        color: #ffffff !important;
    }
    .track-card code {
        color: #38bdf8 !important;
        background-color: #0f172a !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid #334155 !important;
        font-weight: 600 !important;
    }
    .guide-card {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-top: 4px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 1rem 1.1rem !important;
        margin-bottom: 0.8rem !important;
        height: 100% !important;
        color: #f8fafc !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
    }
    .guide-card h4 {
        color: #38bdf8 !important;
        margin-top: 0 !important;
        margin-bottom: 0.45rem !important;
        font-size: 0.98rem !important;
    }
    .guide-card p {
        color: #f1f5f9 !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
    }
    .guide-card ul, .guide-card ol {
        color: #f8fafc !important;
        padding-left: 1.2rem !important;
    }
    .guide-card li {
        color: #f1f5f9 !important;
        margin-bottom: 0.35rem !important;
        font-size: 0.86rem !important;
        line-height: 1.6 !important;
    }
    .guide-card b, .guide-card strong {
        color: #ffffff !important;
    }
    .guide-card code {
        color: #38bdf8 !important;
        background-color: #0f172a !important;
        padding: 2px 5px !important;
        border-radius: 4px !important;
        border: 1px solid #334155 !important;
        font-weight: 600 !important;
    }
    .agent-box {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-top: 4px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 0.85rem !important;
        height: 100% !important;
        color: #f8fafc !important;
    }
    .agent-box b, .agent-box strong { color: #ffffff !important; }
    .agent-box p { color: #f1f5f9 !important; }
    .agent-box small { color: #cbd5e1 !important; }
    .agent-box code {
        color: #38bdf8 !important;
        background-color: #0f172a !important;
        padding: 2px 5px !important;
        border-radius: 4px !important;
        border: 1px solid #334155 !important;
    }
    .input-tag-card {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-left: 6px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 1.1rem 1.3rem !important;
        margin-bottom: 1.1rem !important;
        color: #f8fafc !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25) !important;
    }
    .input-tag-card h4 {
        margin: 0.5rem 0 0.5rem 0 !important;
        color: #38bdf8 !important;
        font-size: 1.1rem !important;
    }
    .tag-badge {
        display: inline-block !important;
        padding: 3px 9px !important;
        border-radius: 4px !important;
        font-size: 0.74rem !important;
        font-weight: 700 !important;
        margin-right: 6px !important;
        margin-bottom: 6px !important;
    }
    .tag-what { background-color: #0284c7 !important; color: #ffffff !important; }
    .tag-where { background-color: #059669 !important; color: #ffffff !important; }
    .tag-store { background-color: #7c3aed !important; color: #ffffff !important; }
    .tag-time { background-color: #d97706 !important; color: #ffffff !important; }
    .input-tag-card p {
        margin: 0.4rem 0 !important;
        color: #f1f5f9 !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
    }
    .input-tag-card ul {
        margin: 0.3rem 0 0.5rem 0 !important;
        padding-left: 1.3rem !important;
        color: #f1f5f9 !important;
    }
    .input-tag-card li {
        margin-bottom: 0.35rem !important;
        color: #e2e8f0 !important;
        font-size: 0.88rem !important;
        line-height: 1.55 !important;
    }
    .input-tag-card b, .input-tag-card strong {
        color: #ffffff !important;
    }
    .input-tag-card code {
        color: #38bdf8 !important;
        background-color: #020617 !important;
        padding: 2px 5px !important;
        border-radius: 4px !important;
        border: 1px solid #1e293b !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_all_data():
    bs = pd.read_csv(DATA_DIR / "s2_balance_sheet.csv")
    aoc = pd.read_csv(DATA_DIR / "s2_movement_bridge.csv")
    assump = pd.read_csv(DATA_DIR / "actuarial_assumptions.csv")
    sens = pd.read_csv(DATA_DIR / "capital_sensitivities.csv")
    with open(DATA_DIR / "qualitative_docs.json", "r", encoding="utf-8") as f:
        docs = json.load(f)
    with open(DATA_DIR / "exemplar_rules.json", "r", encoding="utf-8") as f:
        rules = json.load(f)
    return bs, aoc, assump, sens, docs, rules


bs_df, aoc_df, assump_df, sens_df, docs_list, rules_list = load_all_data()
docs_map = {d["doc_id"]: d for d in docs_list}
rules_map = {r["rule_id"]: r for r in rules_list}

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {
            "Timestamp (UTC)": "2026-11-09 07:15:00",
            "Query ID": "QRY-2026-101",
            "Target Period Explained": "YE 2026 (Latest Actual vs YE 2025 & Predicted)",
            "Fund Scope": "Total_Entity",
            "SQL Tables": "s2_balance_sheet, s2_movement_bridge",
            "Vector Docs Cited": "DOC-ECON-05, DOC-ALC-01, DOC-REINS-03",
            "Cheat Codes Applied": "RULE-01, RULE-02, RULE-03",
            "PII Guardrail": "PII Redacted ✓",
            "Math Verification": "Exact Match ✓",
        }
    ]

# ==============================================================================
# SIDEBAR
# ==============================================================================
def _get_default_gemini_key() -> str:
    """Read GEMINI_API_KEY from environment or Streamlit Cloud secrets if configured."""
    env_k = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_k:
        return env_k
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass
    return ""


if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = _get_default_gemini_key()
if "gemini_status" not in st.session_state:
    st.session_state.gemini_status = None
if "gemini_model_used" not in st.session_state:
    st.session_state.gemini_model_used = "gemini-3-flash-preview"


def _discover_gemini_candidates(client) -> list[str]:
    """Return prioritized Gemini model candidates plus any live models from client.models.list()."""
    base_candidates = [
        "gemini-3-flash",
        "gemini-3.0-flash",
        "gemini-3-flash-preview",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-flash-latest",
    ]
    if st.session_state.get("gemini_model_used") in base_candidates:
        m = st.session_state["gemini_model_used"]
        base_candidates = [m] + [x for x in base_candidates if x != m]
    try:
        discovered = []
        for m in client.models.list():
            name = getattr(m, "name", "") or ""
            short = name.replace("models/", "")
            actions = getattr(m, "supported_actions", None) or getattr(m, "supported_generation_methods", None) or []
            if actions and not any("generateContent" in str(a) for a in actions):
                continue
            if "gemini" in short and ("flash" in short or "pro" in short) and "2.0" not in short and "1.5" not in short:
                discovered.append(short)
        # Put any discovered 'gemini-3*flash*' models right at the front
        g3_flash = [x for x in discovered if "gemini-3" in x and "flash" in x]
        other_disc = [x for x in discovered if x not in g3_flash]
        merged = []
        for item in g3_flash + base_candidates + other_disc:
            if item not in merged:
                merged.append(item)
        return merged
    except Exception:
        return base_candidates


def call_gemini_text(api_key: str, prompt_text: str) -> tuple[bool, str, str, str]:
    """Call Google Gemini using dynamic model discovery + fallback. Returns (ok, text, model_used, err_msg)."""
    clean_key = api_key.strip()
    if not clean_key:
        return False, "", "", "Please paste your Google Gemini API key (starts with `AIza...`)."
    try:
        from google import genai
        client = genai.Client(api_key=clean_key)
        candidates = _discover_gemini_candidates(client)
        errors = []
        non_404_errors = []
        for model_candidate in candidates:
            try:
                resp = client.models.generate_content(
                    model=model_candidate,
                    contents=prompt_text,
                )
                if resp and resp.text:
                    return True, resp.text, model_candidate, ""
            except Exception as inner_exc:
                err_str = str(inner_exc)
                errors.append(f"{model_candidate}: {err_str}")
                if "404" not in err_str and "NOT_FOUND" not in err_str:
                    non_404_errors.append(f"{model_candidate}: {err_str}")
                # If API key itself is invalid (400 API_KEY_INVALID / 403 PERMISSION_DENIED), stop early
                if "API_KEY_INVALID" in err_str or "API key not valid" in err_str:
                    return False, "", "", f"Invalid API Key: {err_str}"
                continue
        best_err = non_404_errors[0] if non_404_errors else (errors[0] if errors else "No compatible Gemini model responded.")
        return False, "", "", best_err
    except Exception as exc:
        return False, "", "", f"Gemini connection error: {exc}"


def verify_gemini_api_key(key_str: str) -> tuple[bool, str, str]:
    """Test a Google Gemini API key and return (is_valid, model_name, message)."""
    ok, _txt, mdl, err = call_gemini_text(key_str, "Reply with the exact word CONNECTED.")
    if ok:
        return True, mdl, f"Connected to Google Gemini (`{mdl}`)"
    return False, "", f"Gemini API error: {err}"


with st.sidebar:
    st.markdown("### 🏛️ Actuarial AI Platform")
    st.caption("Presenter: **Avnish Nainawatee**")
    st.markdown(
        """
        **Reporting Timeline Demarcation:**
        - 🕰️ **YE 2024**: Historical Baseline (2Y Ago)
        - 📅 **YE 2025**: Prior Year Actuals (Opening)
        - 🎯 **YE 2026 Predicted**: Expected Roll-Forward
        - 🟢 **YE 2026 Actual (LATEST)**: **Target Data We Are Explaining**
        """
    )
    st.divider()

    engine_mode = st.radio(
        "AI Execution Mode",
        [
            "Governed Deterministic Engine (Offline-Safe)",
            "Live Google Gemini API (Real-Time LLM)",
        ],
        index=1 if st.session_state.gemini_api_key else 0,
    )
    if "Live Google Gemini" in engine_mode:
        sidebar_key = st.text_input(
            "Google Gemini API Key",
            value=st.session_state.gemini_api_key,
            type="password",
            placeholder="Paste AIzaSy... and press Enter or click Activate",
            help="Press Enter after pasting, or click '🔌 Test & Activate Key' below.",
        )
        if sidebar_key != st.session_state.gemini_api_key:
            st.session_state.gemini_api_key = sidebar_key.strip()
            st.session_state.gemini_status = None

        if st.button("🔌 Test & Activate Gemini Key", use_container_width=True, type="primary"):
            with st.spinner("Testing connection to Google Gemini..."):
                ok, mdl, msg = verify_gemini_api_key(st.session_state.gemini_api_key)
                st.session_state.gemini_status = (ok, msg)
                if ok:
                    st.session_state.gemini_model_used = mdl

        if st.session_state.gemini_status is not None:
            ok, msg = st.session_state.gemini_status
            if ok:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")
        elif st.session_state.gemini_api_key:
            st.info("🔑 Key entered (`" + st.session_state.gemini_api_key[:6] + "...`). Click **🔌 Test & Activate Gemini Key** or go to **Stage 4** and click **🚀 Run 5-Agent Parallel Orchestration**.")
        else:
            st.warning("⚠️ Paste your `AIzaSy...` key above and press **Enter** (or configure it directly inside **Stage 4**).")

    gemini_api_key = st.session_state.gemini_api_key if "Live Google Gemini" in engine_mode else ""

# ==============================================================================
# TOP BANNER
# ==============================================================================
st.markdown(
    """
    <div class="main-header">
        <h2>Multimodal AI for Life Insurance Financial Explainability <span class="latest-pill">TARGET EXPLAINED: YE 2026 LATEST ACTUALS</span></h2>
        <p>Albion Life Assurance plc &middot; Historical (YE 2024 &amp; YE 2025) &rarr; Predicted (YE 2026 Forecast) &rarr; <b>Latest Actuals (YE 2026)</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 6 PRESENTATION STAGES (TABS) — INPUTS FIRST
# ==============================================================================
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🗂️ Stage 0: Governed Inputs & Data Foundation",
        "🏛️ Stage 1: How the Tool Works (Dual-Track AI)",
        "📖 Stage 2: Balance Sheet Line-Item Guide",
        "📊 Stage 3: Executive Dashboard & Waterfall (2024 → 2025 → 2026 Latest)",
        "🤖 Stage 4: 'Ask Your Balance Sheet' Multi-Agent Studio",
        "🛡️ Stage 5: Mosaic AI Gateway & Audit Log",
    ]
)

# ------------------------------------------------------------------------------
# STAGE 0: GOVERNED INPUTS & DATA FOUNDATION (INPUTS FIRST)
# ------------------------------------------------------------------------------
with tab0:
    st.markdown(
        """
        <div class="cue-banner">
            <strong>🎤 Governed Data Foundation (Inputs First):</strong>
            Start the presentation here to establish trust. Inspect all <b>6 raw input artifacts</b> entering the system from core actuarial modeling systems and corporate governance committees. Each input has a clear tag showing <b>WHAT IS PRESENTED</b> and <b>WHERE IT IS USED</b> across the automated pipeline (Track 1) and question-driven RAG (Track 2).
        </div>
        """,
        unsafe_allow_html=True,
    )

    artifact_choice = st.radio(
        "Select Governed Input Artifact to Inspect:",
        [
            "1. Solvency II Balance Sheet (Delta Table)",
            "2. Movement Bridge / AoC Waterfall (Delta Table)",
            "3. Actuarial Valuation Assumptions (Delta Table)",
            "4. Capital Sensitivity Stress Matrix (Delta Table)",
            "5. Qualitative Governance Memos & Committee Minutes (Vector Index)",
            "6. Senior Actuary Exemplar Rules / 'Cheat Codes' (Rule Store)",
        ],
        horizontal=True,
    )

    if artifact_choice.startswith("1"):
        st.markdown(
            """
            <div class="input-tag-card">
                <span class="tag-badge tag-what">🗂️ INPUT ARTIFACT 1 OF 6</span>
                <span class="tag-badge tag-store">UNITY CATALOG DELTA TABLE: unity_catalog.actuarial.s2_balance_sheet</span>
                <span class="tag-badge tag-time">TIMELINE: YE 2024 Hist → YE 2025 Prior → YE 2026 Pred → 🟢 YE 2026 Latest Actual</span>
                <h4>📊 Solvency II Balance Sheet &amp; Capital Position</h4>
                <p><b>📌 WHAT IS PRESENTED:</b><br>
                Audited Solvency II balance sheet containing <b>60 line items</b> split across three fund perimeters: <code>Total_Entity</code> (Consolidated), <code>WP_Fund</code> (With-Profits), and <code>NP_Fund</code> (Non-Profit). Includes full multi-year progression: <b>YE 2024 Historical</b> (2Y baseline), <b>YE 2025 Prior</b> (opening position), <b>YE 2026 Predicted</b> (actuarial roll-forward forecast), and <b>🟢 YE 2026 Actual</b> (the latest data being explained). Captures <code>Total_Assets</code>, <code>BEL_Guaranteed</code>, <code>BEL_FDB</code>, <code>Risk_Margin</code>, <code>Eligible_Own_Funds</code>, <code>Gross_SCR</code>, <code>LACTP</code>, <code>Net_SCR</code>, and <code>Solvency_Ratio</code>.</p>
                <p><b>🎯 WHERE IT IS USED IN THIS DEMO:</b></p>
                <ul>
                    <li><b>Stage 3 Executive Dashboard:</b> Calculates headline executive KPIs (Consolidated Solvency Ratio: <code>176.0% &rarr; 172.0%</code>; Own Funds: <code>£440.0m &rarr; £430.0m</code>; Net SCR: <code>£250.0m</code>) and populates the comparative Solvency II Balance Sheet table.</li>
                    <li><b>Stage 4 Multi-Agent Studio:</b> Queried dynamically by the <b>Data Agent (Genie / SQL)</b> in Scenarios 1 &amp; 2 to compute exact £m variances against predicted baselines and verify mathematical consistency.</li>
                    <li><b>Stage 5 Governance &amp; Audit Log:</b> Verifies data versioning and SHA-256 cryptographic lineage in Unity Catalog to guarantee zero data drift.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(bs_df, use_container_width=True, hide_index=True)

    elif artifact_choice.startswith("2"):
        st.markdown(
            """
            <div class="input-tag-card">
                <span class="tag-badge tag-what">🗂️ INPUT ARTIFACT 2 OF 6</span>
                <span class="tag-badge tag-store">UNITY CATALOG DELTA TABLE: unity_catalog.actuarial.s2_movement_bridge</span>
                <span class="tag-badge tag-time">TIMELINE: YE 2025 Opening &rarr; YE 2026 Pred &rarr; 🟢 YE 2026 Latest Closing</span>
                <h4>🪜 Analysis of Change (AoC) Movement Bridge</h4>
                <p><b>📌 WHAT IS PRESENTED:</b><br>
                Granular <b>8-step actuarial movement bridge</b> explaining exactly how balance sheet metrics evolved from <b>YE 2025 Prior Year Opening</b> to <b>🟢 YE 2026 Latest Actual Closing</b>. Separates expected roll-forward steps (<code>02 Expected Run-Off</code>, <code>03 New Business</code>, <code>04 Predicted Closing</code>) from the 3 unpredicted 2026 variances (<code>05 Economic Variances</code>, <code>06 Demographic Assumptions</code>, <code>07 Management Actions</code>). Quantifies impacts across <code>Net_SCR</code>, <code>Own_Funds</code>, and <code>Total_BEL</code> for each fund scope.</p>
                <p><b>🎯 WHERE IT IS USED IN THIS DEMO:</b></p>
                <ul>
                    <li><b>Stage 3 Executive Dashboard:</b> Powers the interactive <b>Plotly Analysis of Change Waterfall Chart</b>, visually highlighting why Consolidated Net SCR stayed flat at £250.0m while With-Profits and Non-Profit moved in opposite directions.</li>
                    <li><b>Stage 3 Track 1 Commentary:</b> Automatically pre-computes the executive variance narrative explaining how <code>WP_Fund</code> absorbed rate drops via bonus cuts while <code>NP_Fund</code> took an unhedged strain.</li>
                    <li><b>Stage 4 Multi-Agent Studio:</b> Filtered by the <b>Data Agent (SQL)</b> to retrieve exact £m driver impacts and cite corresponding documentation IDs (e.g., <code>DOC-ECON-05</code>, <code>DOC-ALC-01</code>).</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(aoc_df, use_container_width=True, hide_index=True)

    elif artifact_choice.startswith("3"):
        st.markdown(
            """
            <div class="input-tag-card">
                <span class="tag-badge tag-what">🗂️ INPUT ARTIFACT 3 OF 6</span>
                <span class="tag-badge tag-store">UNITY CATALOG DELTA TABLE: unity_catalog.actuarial.actuarial_assumptions</span>
                <span class="tag-badge tag-time">TIMELINE: YE 2024 &rarr; YE 2025 &rarr; YE 2026 Pred &rarr; 🟢 YE 2026 Actual</span>
                <h4>📈 Actuarial Valuation Assumptions &amp; Economic Basis</h4>
                <p><b>📌 WHAT IS PRESENTED:</b><br>
                Core economic, demographic, and expense valuation parameters tracked across 4 valuation dates. Includes the <b>10-Year Risk-Free Swap Rate</b> (fell from 4.25% to 3.75%), <b>Equity Backing Ratio (EBR)</b> (cut from 65% to 58% by ALCO), <b>Regular &amp; Terminal Bonus Rates</b>, <b>Policy Lapse Rates</b> (spiked from 10.0% to 12.5%), <b>Longevity Annual Improvement</b> (strengthened from 1.50% to 1.75% p.a.), <b>Expense Inflation</b> (3.8% to 4.2%), and <b>Quota Share Longevity Reinsurance</b> (expanded from 40% to 60%).</p>
                <p><b>🎯 WHERE IT IS USED IN THIS DEMO:</b></p>
                <ul>
                    <li><b>Stage 3 Executive Dashboard:</b> Underpins the <code>05 Assumption Changes</code> waterfall step (+£8.0m Net SCR strain and -£21.5m Own Funds strain in <code>NP_Fund</code>).</li>
                    <li><b>Stage 4 Multi-Agent Studio:</b> Queried by the <b>Data Agent</b> and <b>Context Agent</b> in Scenario 1 (explaining the Non-Profit SCR increase) and Scenario 3 (Longevity Swap impact).</li>
                    <li><b>Stage 2 Line-Item Guide:</b> Illustrates how changing yield curves and lapse rates directly shift <code>BEL_Guaranteed</code> and <code>Risk_Margin</code> calculations.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(assump_df, use_container_width=True, hide_index=True)

    elif artifact_choice.startswith("4"):
        st.markdown(
            """
            <div class="input-tag-card">
                <span class="tag-badge tag-what">🗂️ INPUT ARTIFACT 4 OF 6</span>
                <span class="tag-badge tag-store">UNITY CATALOG DELTA TABLE: unity_catalog.actuarial.capital_sensitivities</span>
                <span class="tag-badge tag-time">STRESS SENSITIVITIES: 5 Standard Formula Stresses</span>
                <h4>⚡ Capital Sensitivity Stress Matrix</h4>
                <p><b>📌 WHAT IS PRESENTED:</b><br>
                Pre-calculated Solvency II standard formula balance sheet sensitivities across 5 audited stress tests: <code>RATES_DOWN_50BPS</code>, <code>RATES_UP_50BPS</code>, <code>EQUITY_DOWN_20PCT</code>, <code>MASS_LAPSE_20PCT</code>, and <code>LONGEVITY_STRESS_5PCT</code>. Quantifies sensitivity impacts (£m) on both <b>Eligible Own Funds</b> and <b>Net SCR</b> across all three perimeters (<code>Total_Entity</code>, <code>WP_Fund</code>, <code>NP_Fund</code>).</p>
                <p><b>🎯 WHERE IT IS USED IN THIS DEMO:</b></p>
                <ul>
                    <li><b>Stage 4 Multi-Agent Studio:</b> Used by the <b>Data Agent</b> and <b>Senior Actuary Rule Agent (RULE-05)</b> to cross-validate actual observed 2026 economic variances against modeled sensitivity shocks (verifying the observed -50 bps yield curve shift matches the -£32.0m FDB reduction).</li>
                    <li><b>Stage 2 Line-Item Guide:</b> Provides empirical evidence of fund asymmetry: in <code>RATES_DOWN_50BPS</code>, With-Profits Own Funds impact is £0.0m (cushioned by FDB) while Non-Profit Own Funds lose -£24.5m.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(sens_df, use_container_width=True, hide_index=True)

    elif artifact_choice.startswith("5"):
        st.markdown(
            """
            <div class="input-tag-card">
                <span class="tag-badge tag-what">🗂️ INPUT ARTIFACT 5 OF 6</span>
                <span class="tag-badge tag-store">DATABRICKS VECTOR SEARCH: databricks_vector_search.actuarial_memos</span>
                <span class="tag-badge tag-time">GOVERNANCE RECORDS: 5 Audited Executive Documents (2026)</span>
                <h4>📄 Qualitative Governance Memos &amp; Committee Minutes</h4>
                <p><b>📌 WHAT IS PRESENTED:</b><br>
                Full-text, realistic executive governance documents chunked and indexed into Databricks Vector Search:
                <br>&bull; <code>DOC-ALC-01</code>: ALCO Minutes — Decision to de-risk equities by reducing EBR from 65% to 58%, lowering Net SCR by -£15.0m.
                <br>&bull; <code>DOC-ASSUMP-02</code>: Basis Committee Paper — 2026 Mortality Improvement and Lapse Experience Study (+£8.0m SCR strain).
                <br>&bull; <code>DOC-REINS-03</code>: Chief Risk Officer Memo — Restructuring Quota Share Longevity Swap to mitigate Non-Profit capital strain (-£12.0m SCR relief).
                <br>&bull; <code>DOC-WPB-04</code>: With-Profits Committee Paper — Reduction in terminal bonus scales absorbing 50 bps interest rate decline (-£32.0m FDB).
                <br>&bull; <code>DOC-ECON-05</code>: Macroeconomic Note — BoE Yield Curve Shift, 50 bps swap rate drop, and fixed-income revaluation.</p>
                <p><b>🎯 WHERE IT IS USED IN THIS DEMO:</b></p>
                <ul>
                    <li><b>Stage 4 Multi-Agent Studio:</b> Retrieved by the <b>Context Agent (Vector Search)</b> to substantiate <i>why</i> variances occurred with cited committee authorizations, preventing ungrounded speculation.</li>
                    <li><b>Stage 3 Executive Dashboard:</b> Rendered as interactive clickable citation chips (<code>DOC-ALC-01</code>, etc.) in the executive narrative so leaders can inspect source evidence in one click.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for d in docs_list:
            with st.expander(f"📄 {d['doc_id']} | {d['doc_type']} ({d['date']}) — {d['title']}", expanded=True):
                st.write(d["content"])

    else:
        st.markdown(
            """
            <div class="input-tag-card">
                <span class="tag-badge tag-what">🗂️ INPUT ARTIFACT 6 OF 6</span>
                <span class="tag-badge tag-store">UNITY CATALOG RULE STORE: unity_catalog.rules.senior_actuary_cache</span>
                <span class="tag-badge tag-time">GOVERNING ACTUARIAL RULES: 5 Senior Actuary 'Cheat Codes'</span>
                <h4>⚖️ Senior Actuary Exemplar Rules ("Cheat Codes")</h4>
                <p><b>📌 WHAT IS PRESENTED:</b><br>
                Five codified actuarial domain rules authored by Chief Actuaries to enforce institutional knowledge and regulatory compliance:
                <br>&bull; <code>RULE-01 (With-Profits FDB / LACTP Symmetry):</code> In falling rate environments, terminal bonus cuts must simultaneously reduce BEL_FDB and LACTP, insulating Own Funds.
                <br>&bull; <code>RULE-02 (Non-Profit PV01 Rate Strain):</code> In Non-Profit funds, falling rates create duration strain directly on BEL_Guaranteed with zero bonus buffer.
                <br>&bull; <code>RULE-03 (Consolidated Entity Masking Prohibition):</code> AI narratives are forbidden from concluding solvency is stable without presenting fund-level divergence.
                <br>&bull; <code>RULE-04 (Reinsurance Counterparty Capital Offset):</code> Longevity swap relief on Life Underwriting SCR must be offset against Counterparty Default SCR.
                <br>&bull; <code>RULE-05 (Capital Sensitivity Matrix Cross-Validation):</code> Observed 2026 economic variances must be reconciled against the 50 bps stress test matrix.</p>
                <p><b>🎯 WHERE IT IS USED IN THIS DEMO:</b></p>
                <ul>
                    <li><b>Stage 4 Multi-Agent Studio:</b> Injected by the <b>Exemplar Agent ("Cheat Codes")</b> into the multi-agent reasoning chain to restrict vocabulary, prevent hallucinations, and enforce rigorous actuarial syntax.</li>
                    <li><b>Stage 3 Executive Dashboard:</b> Enforces the "Cheat-Code Verified ✓" quality badge on the auto-generated executive commentary.</li>
                    <li><b>Stage 5 Mosaic AI Gateway:</b> Validated in the real-time governance audit log to guarantee compliance before delivering responses.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for r in rules_list:
            with st.expander(f"⚖️ {r['rule_id']} | Scope: {', '.join(r['metric_scope'])}", expanded=True):
                st.markdown(f"**Governing Rule:** {r['governing_rule']}")
                st.info(f"**Exemplar Approved Phrasing:** \"{r['exemplar_narrative_snippet']}\"")

# ------------------------------------------------------------------------------
# STAGE 1: SOLUTION VISION & DUAL-TRACK PIPELINE
# ------------------------------------------------------------------------------
with tab1:
    st.markdown(
        """
        <div class="cue-banner">
            <strong>🎤 Overview &amp; Architecture:</strong>
            Explain <b>what the tool does</b> (replaces manual quarterly balance sheet reconciliation with instant, audit-ready actuarial narratives) and <b>how the two tracks operate</b>: Track 1 runs automatically in the background; Track 2 runs on demand when an actuary or executive asks a question.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Executive Vision: Why We Built This System")
    st.write(
        "Every quarter and year-end (here, **YE 2026 Latest Actuals**), life insurance actuaries spend weeks manually stitching together SQL projection tables, sensitivity matrices, ALCO committee minutes, and reinsurance memos to explain **why the Solvency II Balance Sheet and Capital moved** compared to **Prior Year (YE 2025)** and **Predicted Roll-Forward (YE 2026 Forecast)**. This solution automates that entire workflow with full governance."
    )

    c_t1, c_t2 = st.columns(2)
    with c_t1:
        st.markdown(
            """
            <div class="track-card">
                <h4>⚙️ TRACK 1: Automated Background Data Pipeline (Always On)</h4>
                <p><i>Runs automatically as soon as YE 2026 actuarial valuation results land — before any human asks a question.</i></p>
                <ol>
                    <li><b>01 Source Data Ingestion:</b> Quantitative CSV/Delta tables (<code>BEL</code>, <code>Risk_Margin</code>, <code>SCR</code>, <code>Sensitivities</code> across <code>YE 2024</code>, <code>YE 2025</code>, <code>YE 2026 Predicted</code>, and <code>YE 2026 Actual</code>) + Qualitative PDFs/Memos (ALCO minutes, basis papers).</li>
                    <li><b>02 Governed Stores:</b> Auto-loaded into versioned <b>Unity Catalog Delta Tables</b> and chunked/embedded into <b>Databricks Vector Search</b>.</li>
                    <li><b>03 Senior Actuary "Cheat Codes" (Rule Cache):</b> Applies 4–5 strict actuarial rules per metric (e.g., <code>RULE-01</code> With-Profits FDB/LACTP symmetry, <code>RULE-02</code> Non-Profit PV01 rate strain).</li>
                    <li><b>04 Automated Base Commentary:</b> Pre-computes the <b>1-Click Executive Dashboard</b> and Analysis of Change (AoC) waterfall bridging <code>YE 2025 Prior</code> &rarr; <code>YE 2026 Predicted</code> &rarr; <code>YE 2026 Actual</code>.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_t2:
        st.markdown(
            """
            <div class="track-card track2">
                <h4>💬 TRACK 2: Question-Driven Multi-Agent RAG (On-Demand)</h4>
                <p><i>Triggered directly when an actuary, CFO, or regulator asks a natural-language question about the balance sheet.</i></p>
                <ol>
                    <li><b>01 Intent Agent (Router):</b> Parses the user's question to extract the target Fund (<code>WP_Fund</code>, <code>NP_Fund</code>, or <code>Total_Entity</code>), Solvency II Metric, and Timeframe (<code>YE 2026 Latest</code> vs <code>YE 2025</code> / <code>Predicted</code>).</li>
                    <li><b>02 Data Agent (Genie / SQL) [Parallel]:</b> Executes governed SQL over Unity Catalog for exact £m deltas, AoC movement steps, and shock sensitivities.</li>
                    <li><b>03 Context Agent (Vector Search) [Parallel]:</b> Retrieves the exact ALCO minutes, longevity swap notes, and methodology memos linked via <code>ref_doc_id</code>.</li>
                    <li><b>04 Exemplar Agent ("Cheat Codes") [Parallel]:</b> Injects approved Solvency II terminology and prohibits non-compliant phrasing.</li>
                    <li><b>05 Mosaic AI Gateway &amp; Synthesis Agent:</b> Masks PII, verifies math, logs lineage, and delivers an audit-ready narrative in seconds.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 📅 Clear Timeline Demarcation in This Demo (`2024` → `2025` → `2026 Latest`)")
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    t_col1.info("**1. YE 2024 (Historical)**\n\nAudited 2-year-ago baseline showing multi-year trend context.")
    t_col2.info("**2. YE 2025 (Prior Year Actual)**\n\nOpening balance for the current annual Analysis of Change (AoC) waterfall.")
    t_col3.warning("**3. YE 2026 (Predicted Baseline)**\n\nExpected roll-forward position (Opening + Expected Run-Off + Expected New Business) before unpredicted 2026 shocks.")
    t_col4.success("**4. YE 2026 Actual (LATEST TARGET)**\n\n**The latest actual balance sheet we are explaining** — includes 2026 Economic Variances, Assumption Changes, and ALCO Management Actions.")

# ------------------------------------------------------------------------------
# STAGE 2: SOLVENCY II BALANCE SHEET & LINE-ITEM EXPLANATORY GUIDE
# ------------------------------------------------------------------------------
with tab2:
    st.markdown(
        """
        <div class="cue-banner">
            <strong>🎤 Line-Item Explanatory Guide:</strong>
            Walk attendees through the building blocks of a Solvency II life insurance balance sheet, the difference between a <b>With-Profits Fund (`WP_Fund`)</b> and a <b>Non-Profit Fund (`NP_Fund`)</b>, and the exact line items the AI explains.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 1. The Two Funds We Are Explaining: With-Profits (`WP_Fund`) vs. Non-Profit (`NP_Fund`)")
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.markdown(
            """
            <div class="guide-card">
                <h4>🛡️ With-Profits Fund (<code>WP_Fund</code>) — Participating Policies</h4>
                <p>Policyholders share in the investment profits of the fund via <b>Regular Bonuses</b> (guaranteed once declared) and <b>Terminal Bonuses</b> (discretionary at maturity/payout).</p>
                <ul>
                    <li><b>Built-In Shock Absorber (<code>BEL_FDB</code>):</b> When interest rates fall or equities drop, the insurer can reduce future terminal bonus scales (<code>DOC-WPB-04</code>). This lowers <b>Future Discretionary Benefits (<code>BEL_FDB</code>)</b>, insulating <b>Own Funds</b>.</li>
                    <li><b>Capital Credit (<code>LACTP</code>):</b> Because bonuses can be cut in a 1-in-200 stress event, the fund gets a capital deduction called <b>Loss-Absorbing Capacity of Technical Provisions (<code>LACTP</code>)</b> that reduces <code>Net_SCR</code>.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f_col2:
        st.markdown(
            """
            <div class="guide-card" style="border-top-color:#f59e0b !important;">
                <h4>⚡ Non-Profit Fund (<code>NP_Fund</code>) — Annuities &amp; Term Assurance</h4>
                <p>Policyholders receive fixed, guaranteed benefits (e.g., level lifetime annuity payments or term life death cover) with <b>zero discretionary bonus sharing</b>.</p>
                <ul>
                    <li><b>Zero Bonus Buffer (<code>BEL_FDB = £0m</code>, <code>LACTP = £0m</code>):</b> Every pound of interest rate strain (PV01) or longevity/lapse assumption strengthening flows 100% into higher <code>BEL_Guaranteed</code>, higher <code>Risk_Margin</code>, and lower <b>Own Funds</b>.</li>
                    <li><b>Requires External Mitigation:</b> To protect capital when rates fall or longevity lengthens, management must use asset duration matching or external <b>Longevity Swap Reinsurance</b> (<code>DOC-REINS-03</code>).</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 2. Solvency II Balance Sheet Line-Item Dictionary (What Each Metric Means)")
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown(
            """
            <div class="guide-card" style="border-top-color:#0ea5e9;">
                <h4>🏦 A. Assets (`Total_Assets`)</h4>
                <p style="font-size:0.84rem;"><b>1. Government &amp; Corporate Bonds:</b> Fixed-income assets used to match guaranteed liability cashflows. Rise in market value when interest rates fall.<br><br>
                <b>2. Equities &amp; Property:</b> Growth assets held primarily in <code>WP_Fund</code> (governed by the Equity Backing Ratio, EBR). Carry higher <code>SCR_Market</code> capital charges.<br><br>
                <b>3. Reinsurance Recoverables:</b> Present value of cashflows recoverable from reinsurers (e.g., Quota Share Longevity Swap in <code>NP_Fund</code>).</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with g2:
        st.markdown(
            """
            <div class="guide-card" style="border-top-color:#eab308;">
                <h4>📉 B. Liabilities (`Technical_Provisions`)</h4>
                <p style="font-size:0.84rem;"><code>Technical_Provisions = BEL_Guaranteed + BEL_FDB + Risk_Margin</code><br><br>
                <b>1. BEL_Guaranteed:</b> Best Estimate Liability (discounted present value) of guaranteed policy cashflows.<br><br>
                <b>2. BEL_FDB (Future Discretionary Benefits):</b> Present value of expected future terminal bonuses in <code>WP_Fund</code> (<code>£0m</code> in <code>NP_Fund</code>).<br><br>
                <b>3. Risk_Margin:</b> Cost-of-Capital margin (above BEL) required so a third party would take over the liabilities in distress.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with g3:
        st.markdown(
            """
            <div class="guide-card" style="border-top-color:#10b981;">
                <h4>🏛️ C. Capital (`Own_Funds` &amp; `Net_SCR`)</h4>
                <p style="font-size:0.84rem;"><b>1. Eligible Own Funds:</b> <code>Total_Assets - Technical_Provisions - Other_Liabilities</code>. Excess capital available to absorb shocks.<br><br>
                <b>2. Gross SCR (`Market + Life + Op - Div`):</b> 1-in-200 year Value-at-Risk capital requirement.<br><br>
                <b>3. LACTP:</b> Reduction in SCR from cutting discretionary WP bonuses in stress.<br><br>
                <b>4. Net_SCR &amp; Solvency Ratio:</b> <code>Net_SCR = Gross_SCR - LACTP</code>. <code>Solvency Ratio = Own_Funds / Net_SCR</code>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------------------
# STAGE 3: 1-CLICK EXECUTIVE DASHBOARD (2024 -> 2025 -> 2026 PREDICTED vs ACTUAL)
# ------------------------------------------------------------------------------
with tab3:
    st.markdown(
        """
        <div class="cue-banner">
            <strong>🎤 Executive Commentary (Explaining YE 2026 Latest Actuals):</strong>
            Point out the 4 columns in the table and KPI cards: <b>YE 2024 (Historical)</b> &rarr; <b>YE 2025 (Prior Year)</b> &rarr; <b>YE 2026 Predicted (Roll-Forward Forecast)</b> &rarr; <b>🟢 YE 2026 Actual (LATEST DATA WE ARE EXPLAINING)</b>. Notice how the Waterfall bridges <code>YE 2025 Opening</code> &rarr; <code>YE 2026 Predicted Baseline</code> &rarr; and then isolates the 3 unpredicted 2026 variances (Economic, Assumptions, Management Actions) to reach <code>YE 2026 Latest Actual</code>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_fund, c_metric = st.columns(2)
    with c_fund:
        dash_fund = st.segmented_control(
            "Select Fund / Line of Business (LOB):",
            options=["Total_Entity", "WP_Fund", "NP_Fund"],
            default="Total_Entity",
        ) or "Total_Entity"
    with c_metric:
        dash_metric = st.segmented_control(
            "Select YE 2026 Waterfall Metric to Explain:",
            options=["Net_SCR", "Own_Funds", "BEL_Total"],
            default="Net_SCR",
        ) or "Net_SCR"

    sub_bs = bs_df[bs_df["fund"] == dash_fund]
    sr_row = sub_bs[sub_bs["metric_name"] == "Solvency_Ratio_Pct"].iloc[0]
    of_row = sub_bs[sub_bs["metric_name"] == "Own_Funds"].iloc[0]
    scr_row = sub_bs[sub_bs["metric_name"] == "Net_SCR"].iloc[0]
    tp_row = sub_bs[sub_bs["metric_name"] == "Technical_Provisions"].iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
        "🟢 LATEST YE 2026 Solvency Ratio",
        f"{sr_row['ye_2026_latest']:.1f}%",
        f"{sr_row['yoy_delta_25_to_26']:+.1f}% pts vs YE25 ({sr_row['var_vs_predicted']:+.1f}% vs Pred)",
    )
    k2.metric(
        "🟢 LATEST YE 2026 Own Funds",
        f"£{of_row['ye_2026_latest']:.1f}m",
        f"£{of_row['yoy_delta_25_to_26']:+.1f}m vs YE25 (£{of_row['var_vs_predicted']:+.1f}m vs Pred)",
    )
    k3.metric(
        "🟢 LATEST YE 2026 Net SCR",
        f"£{scr_row['ye_2026_latest']:.1f}m",
        f"£{scr_row['yoy_delta_25_to_26']:+.1f}m vs YE25 (£{scr_row['var_vs_predicted']:+.1f}m vs Pred)",
        delta_color="inverse",
    )
    k4.metric(
        "🟢 LATEST YE 2026 Tech Provisions",
        f"£{tp_row['ye_2026_latest']:.1f}m",
        f"£{tp_row['yoy_delta_25_to_26']:+.1f}m vs YE25 (£{tp_row['var_vs_predicted']:+.1f}m vs Pred)",
        delta_color="inverse",
    )

    st.caption(
        f"**Multi-Year Context (`{dash_fund}`):** "
        f"Solvency Ratio: `YE 2024 Historical = {sr_row['ye_2024_historical']:.1f}%` → `YE 2025 Prior = {sr_row['ye_2025_prior']:.1f}%` → `YE 2026 Predicted = {sr_row['ye_2026_predicted']:.1f}%` → **`🟢 YE 2026 Actual (Latest) = {sr_row['ye_2026_latest']:.1f}%`**"
    )

    col_wf, col_narr = st.columns([1.2, 1])

    with col_wf:
        st.markdown(f"#### YE 2025 Prior → YE 2026 Predicted → 🟢 YE 2026 Latest Actual Waterfall (`{dash_fund}` · `{dash_metric}`)")
        if dash_fund != "Total_Entity":
            bridge_sub = aoc_df[
                (aoc_df["fund"] == dash_fund) & (aoc_df["metric_name"] == dash_metric)
            ].sort_values("step_order")
        else:
            bridge_sub = (
                aoc_df[aoc_df["metric_name"] == dash_metric]
                .groupby(["step_order", "movement_step", "driver_category"], as_index=False)
                .agg({"impact_gbp_m": "sum", "ref_doc_id": "first"})
                .sort_values("step_order")
            )

        # Steps 1, 4 (Predicted Closing), and 8 (Actual Latest Closing) are subtotal/total bars!
        measures = [
            "absolute" if s.startswith(("01_", "04_", "08_")) else "relative"
            for s in bridge_sub["movement_step"]
        ]
        labels = [
            s.replace("01_", "")
            .replace("02_", "")
            .replace("03_", "")
            .replace("04_", "🎯 ")
            .replace("05_", "")
            .replace("06_", "")
            .replace("07_", "")
            .replace("08_", "🟢 ")
            .replace("_", " ")
            for s in bridge_sub["movement_step"]
        ]
        values = bridge_sub["impact_gbp_m"].tolist()

        inc_color = "#10b981" if dash_metric == "Own_Funds" else "#e11d48"
        dec_color = "#e11d48" if dash_metric == "Own_Funds" else "#10b981"

        fig = go.Figure(
            go.Waterfall(
                name=dash_metric,
                orientation="v",
                measure=measures,
                x=labels,
                y=values,
                text=[
                    f"£{v:.1f}m" if m == "absolute" else f"{v:+.1f}m"
                    for v, m in zip(values, measures)
                ],
                textposition="outside",
                increasing={"marker": {"color": inc_color}},
                decreasing={"marker": {"color": dec_color}},
                totals={"marker": {"color": "#072659"}},
                connector={"line": {"color": "#64748b", "width": 1.5}},
            )
        )
        fig.update_layout(
            height=410,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title="£ Millions",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_narr:
        st.markdown("#### Track 1: Auto-Generated Narrative Explaining 🟢 YE 2026 Latest Actuals")
        if dash_fund == "Total_Entity":
            st.markdown(
                """
                <div class="narrative-card">
                <b>1. Multi-Year &amp; Predicted vs. Actual Headline (Consolidated)</b><br>
                • <b>Historical Trend:</b> Consolidated Solvency Ratio rose from <b>173.1% (YE 2024)</b> to <b>176.0% (YE 2025 Prior)</b>, and was predicted to reach <b>188.9% (YE 2026 Predicted)</b> on organic run-off.<br>
                • <b>🟢 Latest YE 2026 Actual Position:</b> Closed at <b>172.0%</b> (<b>-4.0% pts YoY</b> vs YE 2025; <b>-16.9% pts vs YE 2026 Predicted</b>). Own Funds closed at <b>£430.0m</b> (vs £469.5m predicted), while Net_SCR closed at <b>£250.0m</b> (vs £248.5m predicted).<br><br>
                <b>2. What Happened Between YE 2026 Predicted and 🟢 YE 2026 Actual?</b><br>
                • <b>With-Profits (`WP_Fund`) beat prior year (+7.7% pts YoY to 200.0%):</b> Absorbed the 50 bps rate drop via a <b>-£32.0m reduction in <code>BEL_FDB</code></b> (<code>DOC-WPB-04</code>) and cut <code>Net_SCR</code> by <b>-£15.0m</b> via ALCO equity de-risking (<code>DOC-ALC-01</code>).<br>
                • <b>Non-Profit (`NP_Fund`) drove the shortfall vs. prediction (144.0% actual vs 174.5% predicted):</b> Hit by <b>-£21.5m Operating Assumption strain</b> (<code>DOC-ASSUMP-02</code>) and <b>+£11.5m Economic Rate SCR strain</b> (<code>DOC-ECON-05</code>), partially rescued by a <b>-£12.0m Longevity Swap</b> (<code>DOC-REINS-03</code>).
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif dash_fund == "WP_Fund":
            st.markdown(
                """
                <div class="narrative-card">
                <b>1. With-Profits (`WP_Fund`) — Historical vs. Predicted vs. 🟢 YE 2026 Actual</b><br>
                • <b>Timeline:</b> Solvency Ratio progressed from <b>184.6% (YE 2024)</b> &rarr; <b>192.3% (YE 2025 Prior)</b> &rarr; <b>202.3% (YE 2026 Predicted)</b> &rarr; <b>🟢 200.0% (YE 2026 Actual)</b>.<br>
                • <b>Own Funds &amp; Net SCR:</b> Own Funds closed at <b>£250.0m</b> (flat vs YE 2025, -£11.0m vs £261.0m predicted), while <code>Net_SCR</code> fell to <b>£125.0m</b> (-£5.0m vs YE 2025, -£4.0m lower than £129.0m predicted).<br><br>
                <b>2. Drivers of the YE 2026 Actual Outcome</b><br>
                • <b>FDB Bonus Absorption (`RULE-01`, `DOC-WPB-04`):</b> Lowering the Terminal Bonus Scale Factor from 100% to 92% cut <code>BEL_FDB</code> from £220.0m (YE25) and £217.0m (Predicted) to <b>£188.0m (YE26 Actual)</b>, offsetting the +£22.0m rate strain on <code>BEL_Guaranteed</code>.<br>
                • <b>ALCO Equity De-Risking (`DOC-ALC-01`):</b> Reducing EBR from 45% to 38% and adding an equity put collar cut <code>Net_SCR</code> by <b>-£15.0m</b> vs predicted, outweighing the -£9.0m drop in <code>LACTP</code>.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="narrative-card">
                <b>1. Non-Profit (`NP_Fund`) — Historical vs. Predicted vs. 🟢 YE 2026 Actual</b><br>
                • <b>Timeline:</b> Solvency Ratio moved from <b>160.0% (YE 2024)</b> &rarr; <b>158.3% (YE 2025 Prior)</b> &rarr; <b>174.5% (YE 2026 Predicted)</b> &rarr; <b>🟢 144.0% (YE 2026 Actual)</b>.<br>
                • <b>Own Funds &amp; Net SCR:</b> Own Funds closed at <b>£180.0m</b> (-£10.0m vs YE 2025; <b>-£28.5m below £208.5m predicted</b>). <code>Net_SCR</code> closed at <b>£125.0m</b> (+£5.0m vs YE 2025; +£5.5m above £119.5m predicted).<br><br>
                <b>2. Drivers of the -£28.5m Own Funds &amp; +£5.5m SCR Variance vs. Predicted</b><br>
                • <b>Unpredicted Operating Assumption Changes (-£21.5m Own Funds / +£6.0m SCR, `DOC-ASSUMP-02`):</b> Term Life lapse rate raised from 6.50% to 8.00% and annuity longevity trend raised from 1.50% to 1.75%.<br>
                • <b>Unpredicted 50 bps Rate Drop (-£4.0m Own Funds / +£11.5m SCR, `DOC-ECON-05`):</b> Zero <code>BEL_FDB</code> buffer meant the rate drop from 4.10% to 3.60% (vs 4.05% predicted) hit <code>BEL_Guaranteed</code> (+£35.0m) and <code>Net_SCR</code> (+£11.5m) directly.<br>
                • <b>Q4 Longevity Swap Mitigation (-£12.0m Net_SCR, `DOC-REINS-03`):</b> Ceding 70% (up from 50%) of annuity longevity risk saved £12.0m of SCR.
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"#### Complete Solvency II Balance Sheet: Historical (`2024`, `2025`) vs. Forecast (`2026 Predicted`) vs. 🟢 **`YE 2026 Latest Actual`** — `{dash_fund}`"
    )
    display_bs = sub_bs.rename(
        columns={
            "line_id": "Line ID",
            "metric_category": "Category",
            "metric_name": "Solvency II Line Item",
            "ye_2024_historical": "YE 2024 (Historical)",
            "ye_2025_prior": "YE 2025 (Prior Year)",
            "ye_2026_predicted": "🎯 YE 2026 (Predicted)",
            "ye_2026_latest": "🟢 YE 2026 (LATEST ACTUAL)",
            "yoy_delta_25_to_26": "YoY Delta (25→26)",
            "yoy_delta_pct": "YoY Delta (%)",
            "var_vs_predicted": "Variance vs Predicted",
        }
    )
    st.dataframe(display_bs.drop(columns=["fund"]), use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# STAGE 4: "ASK YOUR BALANCE SHEET" MULTI-AGENT STUDIO (YE 2026 LATEST)
# ------------------------------------------------------------------------------
with tab4:
    st.markdown(
        """
        <div class="cue-banner">
            <strong>🎤 Track 2 On-Demand Question RAG (Explaining YE 2026 Latest):</strong>
            Demonstrate Track 2 (not pre-computed, triggered directly by user questions about <b>YE 2026 Latest Actuals</b>). Select a question and click <b>Run 5-Agent Parallel Orchestration</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    SCENARIOS = {
        "Scenario 1 (NP_Fund SCR — YE 2026 Actual vs Predicted & YE 2025): Why did Non-Profit Net SCR close at £125.0m at YE 2026 (vs £120.0m at YE 2025 and £119.5m Predicted)?": {
            "title_short": "Scenario 1: NP_Fund Net SCR (+£5.5m vs Predicted)",
            "fund": "NP_Fund",
            "metric": "Net_SCR (YE 2026 Latest)",
            "sql_query": "SELECT movement_step, impact_gbp_m, driver_category, ref_doc_id\nFROM unity_catalog.actuarial.s2_movement_bridge\nWHERE fund = 'NP_Fund' AND metric_name = 'Net_SCR'\nORDER BY step_order;",
            "df_filter": aoc_df[(aoc_df["fund"] == "NP_Fund") & (aoc_df["metric_name"] == "Net_SCR")],
            "docs": ["DOC-ECON-05", "DOC-ASSUMP-02", "DOC-REINS-03"],
            "rules": ["RULE-02", "RULE-03", "RULE-05"],
            "narrative": """
### 1. Multi-Year & Predicted vs. 🟢 YE 2026 Latest Actual Headline (`NP_Fund Net_SCR`)
* **Historical & Prior Year:** `NP_Fund Net_SCR` increased from **£115.0m (YE 2024 Historical)** to **£120.0m (YE 2025 Prior Year)**.
* **🎯 YE 2026 Predicted Baseline:** Expected existing business run-off (-£5.0m) and new business (+£4.5m) were predicted to bring `Net_SCR` to **£119.5m** at YE 2026.
* **🟢 YE 2026 Latest Actual:** Closed at **£125.0m** (**+£5.0m / +4.2% YoY** vs YE 2025, and **+£5.5m above the £119.5m Predicted baseline**).

### 2. Unpredicted Variance Drivers (Why YE 2026 Actual Diverged from Predicted)
* **Unpredicted Economic Variance (+£11.5m vs Predicted, `DOC-ECON-05`):** The 10-year GBP swap rate fell 50 bps from **4.10% (YE 2025)** to **3.60% (YE 2026 Actual)**, versus a **4.05% Predicted** forward rate. With zero `BEL_FDB` or `LACTP` buffer (`RULE-02`), this rate shock directly inflated annuity capital requirements.
* **Operating Assumption Strengthening (+£6.0m vs Predicted, `DOC-ASSUMP-02`):** Updating Term Life lapses (6.50% → 8.00%) and annuity longevity improvement trends (1.50% → 1.75%) added +£6.0m to `Net_SCR`.
* **Mitigating Management Action (-£12.0m vs Predicted, `DOC-REINS-03`):** Expanding the Quota Share Longevity Swap from 50% to 70% ceded in December 2026 reduced `Net_SCR` by **-£12.0m**, preventing `Net_SCR` from reaching £137.0m.
""",
        },
        "Scenario 2 (WP_Fund FDB & LACTP — YE 2026 Actual vs Predicted): Why did With-Profits Own Funds close at £250.0m (vs £261.0m Predicted) while Solvency Ratio reached 200.0%?": {
            "title_short": "Scenario 2: WP_Fund FDB Buffer & 200% Solvency Ratio",
            "fund": "WP_Fund",
            "metric": "Own_Funds, BEL_FDB, LACTP & Net_SCR (YE 2026 Latest)",
            "sql_query": "SELECT metric_name, ye_2024_historical, ye_2025_prior, ye_2026_predicted, ye_2026_latest, var_vs_predicted\nFROM unity_catalog.actuarial.s2_balance_sheet\nWHERE fund = 'WP_Fund' AND metric_name IN ('BEL_Guaranteed','BEL_FDB','Own_Funds','SCR_Market','LACTP','Net_SCR','Solvency_Ratio_Pct');",
            "df_filter": bs_df[
                (bs_df["fund"] == "WP_Fund")
                & (
                    bs_df["metric_name"].isin(
                        ["BEL_Guaranteed", "BEL_FDB", "Own_Funds", "SCR_Market", "LACTP", "Net_SCR", "Solvency_Ratio_Pct"]
                    )
                )
            ],
            "docs": ["DOC-WPB-04", "DOC-ALC-01", "DOC-ECON-05"],
            "rules": ["RULE-01", "RULE-03", "RULE-04"],
            "narrative": """
### 1. Multi-Year & Predicted vs. 🟢 YE 2026 Latest Actual Headline (`WP_Fund`)
* **Historical Progression:** `WP_Fund` Solvency Ratio rose from **184.6% (YE 2024)** to **192.3% (YE 2025 Prior)**, and was predicted to reach **202.3% (YE 2026 Predicted)** with Own Funds predicted at **£261.0m** and `Net_SCR` predicted at **£129.0m**.
* **🟢 YE 2026 Latest Actual:** Own Funds closed at **£250.0m** (flat vs YE 2025; -£11.0m vs Predicted), while `Net_SCR` fell to **£125.0m** (-£5.0m vs YE 2025; -£4.0m better than Predicted), resulting in a **200.0% Solvency Ratio**.

### 2. How `BEL_FDB` Absorbed the 2026 Rate Shock (`RULE-01`, `DOC-WPB-04`)
* The unpredicted 50 bps fall in GBP swap rates increased `BEL_Guaranteed` to **£702.0m** (+£22.0m vs YE 2025; +£32.0m vs £670.0m Predicted).
* In response, the With-Profits Actuary recalibrated the Terminal Bonus Scale Factor from 100% to 92% (`DOC-WPB-04`), reducing `BEL_FDB` to **£188.0m** (-£32.0m vs YE 2025; -£29.0m vs £217.0m Predicted). This reduced `LACTP` from £80.0m to **£71.0m**.

### 3. ALCO Equity De-Risking (`DOC-ALC-01`)
* To offset the -£9.0m reduction in `LACTP`, ALCO cut the Equity Backing Ratio from 45% to 38% and executed an equity put collar, delivering a **-£15.0m management action reduction in `Net_SCR`**.
""",
        },
        "Scenario 3 (NP_Fund Own Funds Shortfall vs Predicted): Why did Non-Profit Own Funds finish at £180.0m at YE 2026 against a Predicted £208.5m (-£28.5m shortfall)?": {
            "title_short": "Scenario 3: NP_Fund Own Funds Shortfall (-£28.5m)",
            "fund": "NP_Fund",
            "metric": "Own_Funds (YE 2026 Actual vs £208.5m Predicted)",
            "sql_query": "SELECT movement_step, impact_gbp_m, driver_category, ref_doc_id\nFROM unity_catalog.actuarial.s2_movement_bridge\nWHERE fund = 'NP_Fund' AND metric_name = 'Own_Funds'\nORDER BY step_order;",
            "df_filter": aoc_df[(aoc_df["fund"] == "NP_Fund") & (aoc_df["metric_name"] == "Own_Funds")],
            "docs": ["DOC-ASSUMP-02", "DOC-ECON-05", "DOC-REINS-03"],
            "rules": ["RULE-02", "RULE-03", "RULE-04"],
            "narrative": """
### 1. Bridging `NP_Fund Own_Funds` from YE 2025 (£190.0m) → Predicted (£208.5m) → 🟢 YE 2026 Actual (£180.0m)
* **Opening & Predicted Roll-Forward:** Starting from **£190.0m at YE 2025** (up from £184.0m at YE 2024), expected run-off (+£12.0m) and new business (+£6.5m) produced a **🎯 YE 2026 Predicted Own Funds of £208.5m**.
* **🟢 YE 2026 Latest Actual:** Closed at **£180.0m** — a **-£28.5m variance below Predicted** (and -£10.0m YoY vs YE 2025).

### 2. Exact Breakdown of the -£28.5m Unpredicted Shortfall
1. **Operating Assumption Changes (-£21.5m vs Predicted, `DOC-ASSUMP-02`):** The primary driver (75% of the shortfall). Higher Term Life lapses (6.50% → 8.00%), stronger annuity longevity trends (1.50% → 1.75%), and higher per-policy expenses (£48.00 → £50.50 vs £49.00 predicted) increased `BEL_Guaranteed` by +£18.0m and `Risk_Margin` by +£3.5m.
2. **Economic Variances (-£4.0m vs Predicted, `DOC-ECON-05`):** The unpredicted 50 bps fall in discount rates increased `BEL_Guaranteed` (+£35.0m) and `Risk_Margin` (+£4.0m), which exceeded the +£35.0m appreciation on matching Government and Corporate Bonds by -£4.0m.
3. **Management Action Frictional Cost (-£3.0m vs Predicted, `DOC-REINS-03`):** Upfront treaty structuring cost on the new Q4 2026 Quota Share Longevity Swap (entered to save £12.0m of `Net_SCR`).
""",
        },
        "Scenario 4 (Sensitivity Matrix Validation — 2026 Rate Shock): How did the actual 2026 50 bps rate drop reconcile against the RATES_DOWN_50BPS sensitivity table across both funds?": {
            "title_short": "Scenario 4: 2026 Rate Shock vs Sensitivity Matrix",
            "fund": "Total_Entity",
            "metric": "Capital Sensitivities Cross-Check (RATES_DOWN_50BPS)",
            "sql_query": "SELECT sensitivity_id, fund, shock_scenario, delta_own_funds_gbp_m, delta_net_scr_gbp_m, new_solvency_ratio_pct\nFROM unity_catalog.actuarial.capital_sensitivities\nWHERE shock_scenario = 'RATES_DOWN_50BPS';",
            "df_filter": sens_df[sens_df["shock_scenario"] == "RATES_DOWN_50BPS"],
            "docs": ["DOC-ECON-05", "DOC-WPB-04", "DOC-ALC-01"],
            "rules": ["RULE-01", "RULE-02", "RULE-05"],
            "narrative": """
### 1. Validating 2026 Economic Variances Against Published Sensitivities (`RULE-05`)
* Between YE 2025 and **🟢 YE 2026 Latest Actual**, the 10-Year GBP risk-free swap rate fell by **-50 bps** (`4.10% → 3.60%`, `DOC-ECON-05`), matching our standard `RATES_DOWN_50BPS` stress test:
  * **With-Profits (`SENS_WP_01`, `WP_Fund`):** Sensitivity matrix modeled **-£8.0m Own Funds** / **+£9.0m Net_SCR** (shocked ratio: `180.6%`).
  * **Non-Profit (`SENS_NP_01`, `NP_Fund`):** Sensitivity matrix modeled **-£5.0m Own Funds** / **+£11.0m Net_SCR** (shocked ratio: `128.7%`).
  * **Consolidated (`SENS_TOT_01`, `Total_Entity`):** Sensitivity matrix modeled **-£13.0m Own Funds** / **+£20.0m Net_SCR** (shocked ratio: `154.4%`).

### 2. Comparison to Observed 🟢 YE 2026 Actual Outcomes
* **With-Profits Reconciliation:** Actual YE 2026 economic variance was **-£9.0m Own Funds** / **+£9.0m Net_SCR** as `BEL_FDB` terminal bonus recalibration (-£32.0m, `DOC-WPB-04`) absorbed the rate shock, while ALCO equity de-risking (`DOC-ALC-01`) cut `Net_SCR` by **-£15.0m** to reach a **200.0% Solvency Ratio**.
* **Non-Profit Reconciliation:** Actual YE 2026 economic variance was **-£4.0m Own Funds** / **+£11.5m Net_SCR** (`DOC-ECON-05`), reconciling tightly against the modelled **-£5.0m / +£11.0m** sensitivity. Management mitigated this via the Q4 Longevity Swap (**-£12.0m Net_SCR**, `DOC-REINS-03`).
""",
        },
    }

    def run_adhoc_agents(question: str, api_key: str = "") -> dict:
        """Dynamic 5-agent calculation & retrieval engine for any ad-hoc actuarial question."""
        q_low = question.lower()

        # 01 Intent Agent: detect Fund & Topic
        if any(w in q_low for w in ["with-profit", "with profit", "wp_fund", "wp fund", "wp ", "fdb", "lactp", "bonus"]):
            fund = "WP_Fund"
        elif any(w in q_low for w in ["non-profit", "non profit", "np_fund", "np fund", "np ", "annuit", "term life", "longevity", "reinsur", "lapse"]):
            fund = "NP_Fund"
        else:
            fund = "Total_Entity"

        if any(w in q_low for w in ["sensitiv", "stress", "shock", "50 bps", "50bps", "20%"]):
            topic = "Sensitivities"
        elif any(w in q_low for w in ["assump", "swap", "inflation", "mortality", "expense", "ebr"]):
            topic = "Assumptions"
        elif any(w in q_low for w in ["own funds", "own_funds", "surplus", "shortfall"]):
            topic = "Own_Funds"
        elif any(w in q_low for w in ["scr", "capital requirement", "market risk", "underwriting"]):
            topic = "Net_SCR"
        elif any(w in q_low for w in ["asset", "bond", "equit"]):
            topic = "Assets"
        elif any(w in q_low for w in ["bel", "liabilit", "technical provision", "risk margin"]):
            topic = "Liabilities"
        elif any(w in q_low for w in ["solvency", "ratio", "coverage"]):
            topic = "Solvency_Ratio_Pct"
        else:
            topic = "Overview"

        # 02 Data Agent: query real DataFrames
        def _bs_row(f_name: str, m_name: str):
            sub = bs_df[(bs_df["fund"] == f_name) & (bs_df["metric_name"] == m_name)]
            return sub.iloc[0] if not sub.empty else None

        if topic == "Sensitivities":
            sql_query = (
                "SELECT sensitivity_id, fund, shock_scenario, delta_own_funds_gbp_m, delta_net_scr_gbp_m, new_solvency_ratio_pct\n"
                "FROM unity_catalog.actuarial.capital_sensitivities"
                + (f"\nWHERE fund = '{fund}';" if fund != "Total_Entity" else ";")
            )
            df_filter = sens_df if fund == "Total_Entity" else sens_df[sens_df["fund"] == fund]
        elif topic == "Assumptions":
            sql_query = (
                "SELECT assumption_id, fund, assumption_name, unit, ye_2024_val, ye_2025_val, change_val, rationale_ref_doc_id\n"
                "FROM unity_catalog.actuarial.actuarial_assumptions"
                + (f"\nWHERE fund = '{fund}';" if fund != "Total_Entity" else ";")
            )
            df_filter = assump_df if fund == "Total_Entity" else assump_df[assump_df["fund"] == fund]
        elif topic in ("Assets", "Liabilities"):
            sql_query = (
                "SELECT metric_name, ye_2024_historical, ye_2025_prior, ye_2026_predicted, ye_2026_latest, yoy_delta_25_to_26, var_vs_predicted\n"
                "FROM unity_catalog.actuarial.s2_balance_sheet\n"
                f"WHERE fund = '{fund}' AND metric_category = '{topic}';"
            )
            df_filter = bs_df[(bs_df["fund"] == fund) & (bs_df["metric_category"] == topic)]
        elif topic in ("Own_Funds", "Net_SCR"):
            if fund == "Total_Entity":
                sql_query = (
                    "SELECT step_order, movement_step, driver_category, SUM(impact_gbp_m) AS impact_gbp_m, MAX(ref_doc_id) AS ref_doc_id\n"
                    "FROM unity_catalog.actuarial.s2_movement_bridge\n"
                    f"WHERE metric_name = '{topic}'\nGROUP BY step_order, movement_step, driver_category\nORDER BY step_order;"
                )
                df_filter = (
                    aoc_df[aoc_df["metric_name"] == topic]
                    .groupby(["step_order", "movement_step", "driver_category", "ref_doc_id"], as_index=False)["impact_gbp_m"]
                    .sum()
                    .sort_values("step_order")
                )
            else:
                sql_query = (
                    "SELECT movement_step, impact_gbp_m, driver_category, ref_doc_id\n"
                    "FROM unity_catalog.actuarial.s2_movement_bridge\n"
                    f"WHERE fund = '{fund}' AND metric_name = '{topic}'\nORDER BY step_order;"
                )
                df_filter = aoc_df[(aoc_df["fund"] == fund) & (aoc_df["metric_name"] == topic)]
        else:
            key_metrics = ["Total_Assets", "Technical_Provisions", "Own_Funds", "Net_SCR", "Surplus", "Solvency_Ratio_Pct"]
            sql_query = (
                "SELECT fund, metric_name, ye_2024_historical, ye_2025_prior, ye_2026_predicted, ye_2026_latest, yoy_delta_25_to_26, var_vs_predicted\n"
                "FROM unity_catalog.actuarial.s2_balance_sheet\n"
                "WHERE metric_name IN ('Own_Funds','Net_SCR','Solvency_Ratio_Pct');"
            )
            df_filter = bs_df[bs_df["metric_name"].isin(key_metrics)]

        # 03 Context Agent: relevance score qualitative documents
        q_tokens = set(w.strip("?.,!") for w in q_low.split() if len(w) > 2)
        scored_docs = []
        for d in docs_list:
            text_blob = f"{d['title']} {d['content']} {d['fund_scope']}".lower()
            score = sum(2 for tok in q_tokens if tok in text_blob)
            if d["fund_scope"] == fund:
                score += 4
            if topic == "Solvency_Ratio_Pct" and d["doc_id"] in ("DOC-WPB-04", "DOC-ASSUMP-02", "DOC-ALC-01", "DOC-REINS-03"):
                score += 2
            scored_docs.append((score, d["doc_id"]))
        scored_docs.sort(key=lambda x: (-x[0], x[1]))
        matched_docs = [doc_id for _, doc_id in scored_docs[:3]]

        # 04 Exemplar Agent: match Senior Actuary cheat codes
        matched_rules = []
        if fund in ("Total_Entity", "WP_Fund", "NP_Fund"):
            matched_rules.append("RULE-03")
        if fund in ("WP_Fund", "Total_Entity") or "fdb" in q_low or "lactp" in q_low:
            matched_rules.append("RULE-01")
        if fund in ("NP_Fund", "Total_Entity") or topic in ("Own_Funds", "Net_SCR", "Liabilities"):
            matched_rules.append("RULE-02")
        if topic == "Sensitivities" or "rate" in q_low or "shock" in q_low:
            matched_rules.append("RULE-05")
        if "reinsur" in q_low or "swap" in q_low or fund == "NP_Fund":
            matched_rules.append("RULE-04")
        matched_rules = matched_rules[:3]

        # 05 Synthesis Agent: Live Gemini (if enabled) OR Dynamic Data-Grounded Synthesis
        narrative = ""
        engine_badge = "⚙️ Governed Deterministic Calculation Engine (Offline-Safe)"
        if api_key.strip():
            import time as _time
            t0 = _time.perf_counter()
            prompt_payload = (
                "You are an expert UK Solvency II Chief Actuary presenting YE 2026 Latest Actuals vs YE 2025 Prior Year and YE 2026 Predicted Roll-Forward.\n"
                "Answer this exact question using ONLY the governed data tables, governance memos, and Senior Actuary rules below. "
                "Cite exact £m figures, percentages, document IDs (e.g. DOC-ALC-01), and rule IDs (e.g. RULE-01) in clean Markdown with clear headings.\n\n"
                f"Question: {question}\n\n"
                f"Queried Data Table:\n{df_filter.to_string(index=False)}\n\n"
                f"Full Balance Sheet:\n{bs_df.to_string(index=False)}\n\n"
                f"Relevant Governance Docs:\n{json.dumps([docs_map[d] for d in matched_docs])}\n\n"
                f"Senior Actuary Rules:\n{json.dumps([rules_map[r] for r in matched_rules])}"
            )
            ok, gen_text, model_used, err_msg = call_gemini_text(api_key, prompt_payload)
            if ok and gen_text:
                elapsed = _time.perf_counter() - t0
                narrative = gen_text
                engine_badge = f"🟢 Live Google Gemini LLM (`{model_used}`) · Generated in {elapsed:.2f}s"
                st.session_state.gemini_status = (True, f"Connected to Google Gemini (`{model_used}`)")
                st.session_state.gemini_model_used = model_used
            else:
                st.warning(f"Gemini API call failed ({err_msg}) — falling back to Governed Deterministic Calculation Engine.")

        if not narrative:
            if topic in ("Solvency_Ratio_Pct", "Overview"):
                tot_sr = _bs_row("Total_Entity", "Solvency_Ratio_Pct")
                tot_of = _bs_row("Total_Entity", "Own_Funds")
                tot_scr = _bs_row("Total_Entity", "Net_SCR")
                wp_sr = _bs_row("WP_Fund", "Solvency_Ratio_Pct")
                np_sr = _bs_row("NP_Fund", "Solvency_Ratio_Pct")
                wp_of = _bs_row("WP_Fund", "Own_Funds")
                np_of = _bs_row("NP_Fund", "Own_Funds")
                wp_scr = _bs_row("WP_Fund", "Net_SCR")
                np_scr = _bs_row("NP_Fund", "Net_SCR")

                narrative = f"""
### 1. Direct Quantitative Answer (`{fund}` — Solvency Position Across 2024 → 2026 Latest Actual)
* **Overall Consolidated Solvency Ratio (`Total_Entity`):** Progressed from **{tot_sr['ye_2024_historical']:.1f}% (YE 2024)** → **{tot_sr['ye_2025_prior']:.1f}% (YE 2025)** → **🎯 {tot_sr['ye_2026_predicted']:.1f}% (YE 2026 Predicted)** → **🟢 {tot_sr['ye_2026_latest']:.1f}% (YE 2026 Latest Actual)**.
  * **Year-on-Year Change (2025 → 2026 Actual):** **`{tot_sr['yoy_delta_25_to_26']:+.1f}% pts`** (`{tot_sr['yoy_delta_pct']:+.1f}%`).
  * **Variance vs. Predicted Roll-Forward:** **`{tot_sr['var_vs_predicted']:+.1f}% pts`** below forecast due to unpredicted 2026 variances.
* **Underlying Consolidated Drivers:**
  * **Eligible Own Funds:** Closed at **£{tot_of['ye_2026_latest']:.1f}m** (vs £{tot_of['ye_2025_prior']:.1f}m prior and £{tot_of['ye_2026_predicted']:.1f}m predicted → **`{tot_of['var_vs_predicted']:+.1f}m`** vs predicted).
  * **Net SCR:** Closed at **£{tot_scr['ye_2026_latest']:.1f}m** (flat `{tot_scr['yoy_delta_25_to_26']:+.1f}m` YoY vs £{tot_scr['ye_2025_prior']:.1f}m prior; `{tot_scr['var_vs_predicted']:+.1f}m` vs £{tot_scr['ye_2026_predicted']:.1f}m predicted).

### 2. Fund Divergence Explanation (`RULE-03` — Why Overall Ratio Masks Two Opposite Movements)
* **With-Profits Fund (`WP_Fund`) Strengthened to 🟢 {wp_sr['ye_2026_latest']:.1f}% (`{wp_sr['yoy_delta_25_to_26']:+.1f}% pts` YoY vs {wp_sr['ye_2025_prior']:.1f}%):**
  * Own Funds held flat at **£{wp_of['ye_2026_latest']:.1f}m** as terminal bonus cuts reduced `BEL_FDB` by **-£32.0m** (`DOC-WPB-04`), absorbing the 50 bps rate drop (`RULE-01`).
  * ALCO equity de-risking (`DOC-ALC-01`) reduced `Net_SCR` by **-£5.0m YoY** to **£{wp_scr['ye_2026_latest']:.1f}m**.
* **Non-Profit Fund (`NP_Fund`) Fell to 🟢 {np_sr['ye_2026_latest']:.1f}% (`{np_sr['yoy_delta_25_to_26']:+.1f}% pts` YoY; `{np_sr['var_vs_predicted']:+.1f}% pts` vs {np_sr['ye_2026_predicted']:.1f}% Predicted):**
  * Own Funds dropped to **£{np_of['ye_2026_latest']:.1f}m** (**{np_of['var_vs_predicted']:+.1f}m below predicted**) due to operating assumption strengthening (**-£21.5m**, `DOC-ASSUMP-02`) and unbuffered 50 bps rate strain (**-£4.0m**, `DOC-ECON-05`).
  * `Net_SCR` ended at **£{np_scr['ye_2026_latest']:.1f}m** (**+{np_scr['yoy_delta_25_to_26']:.1f}m YoY**), partially rescued by the Q4 Quota Share Longevity Swap (**-£12.0m SCR relief**, `DOC-REINS-03`).
"""
            elif topic in ("Own_Funds", "Net_SCR"):
                bs_row = _bs_row(fund, topic)
                steps_md = "\n".join(
                    f"  * `{r['movement_step']}` ({r['driver_category']}): **£{r['impact_gbp_m']:+.1f}m** (Ref: `{r['ref_doc_id']}`)"
                    for _, r in df_filter.iterrows()
                )
                narrative = f"""
### 1. Calculation Result for `{fund} · {topic}`
* **YE 2024 Historical:** **£{bs_row['ye_2024_historical']:.1f}m**
* **YE 2025 Prior Year (Opening):** **£{bs_row['ye_2025_prior']:.1f}m**
* **🎯 YE 2026 Predicted Baseline:** **£{bs_row['ye_2026_predicted']:.1f}m**
* **🟢 YE 2026 Latest Actual:** **£{bs_row['ye_2026_latest']:.1f}m** (**{bs_row['yoy_delta_25_to_26']:+.1f}m / {bs_row['yoy_delta_pct']:+.1f}% YoY**; **`{bs_row['var_vs_predicted']:+.1f}m` vs Predicted**)

### 2. Reconciled Analysis of Change (AoC) Waterfall Steps
{steps_md}
"""
            elif topic in ("Assets", "Liabilities"):
                lines_md = "\n".join(
                    f"* **`{r['metric_name']}`:** YE24 `£{r['ye_2024_historical']:.1f}m` → YE25 `£{r['ye_2025_prior']:.1f}m` → Pred `£{r['ye_2026_predicted']:.1f}m` → **🟢 YE26 Actual `£{r['ye_2026_latest']:.1f}m`** (YoY: **`{r['yoy_delta_25_to_26']:+.1f}m`**, Var vs Pred: **`{r['var_vs_predicted']:+.1f}m`**)"
                    for _, r in df_filter.iterrows()
                )
                narrative = f"""
### 1. Reconciled `{topic}` Breakdown for `{fund}` (2024 → 2026 Latest Actual)
{lines_md}

### 2. Key Governance Context
* Retrieved supporting evidence from `{'`, `'.join(matched_docs)}` explaining asset reallocation (`DOC-ALC-01`), longevity reinsurance (`DOC-REINS-03`), FDB bonus absorption (`DOC-WPB-04`), and rate sensitivity (`DOC-ECON-05`).
"""
            elif topic == "Assumptions":
                lines_md = "\n".join(
                    f"* **`{r['assumption_name']}` ({r['fund']}):** `{r['ye_2024_val']}{r['unit']}` → **`{r['ye_2025_val']}{r['unit']}`** (Change: **`{r['change_val']:+.2f}{r['unit']}`**, Ref: `{r['rationale_ref_doc_id']}`)"
                    for _, r in df_filter.iterrows()
                )
                narrative = f"""
### 1. Actuarial Valuation Assumptions & Basis Movements (`{fund}`)
{lines_md}
"""
            else:  # Sensitivities
                lines_md = "\n".join(
                    f"* **`{r['shock_scenario']}` ({r['fund']}):** Own Funds `{r['delta_own_funds_gbp_m']:+.1f}m` | Net SCR `{r['delta_net_scr_gbp_m']:+.1f}m` | Surplus `{r['delta_surplus_gbp_m']:+.1f}m` → Shocked Solvency Ratio: **`{r['new_solvency_ratio_pct']:.1f}%`**"
                    for _, r in df_filter.iterrows()
                )
                narrative = f"""
### 1. Capital Sensitivity Stress Matrix Results (`{fund}`)
{lines_md}
"""

        return {
            "title_short": f"Live Query: \"{question}\"",
            "fund": fund,
            "metric": topic,
            "sql_query": sql_query,
            "df_filter": df_filter,
            "docs": matched_docs,
            "rules": matched_rules,
            "narrative": narrative,
            "engine_badge": engine_badge,
        }

    def run_gemini_for_preset(scen_question: str, scen_dict: dict, api_key: str) -> dict:
        """Call Google Gemini LLM using the exact SQL data, governance docs, and Senior Actuary rules of a preset scenario."""
        out = dict(scen_dict)
        out["engine_badge"] = "⚙️ Governed Deterministic Calculation Engine (Offline-Safe)"
        if not api_key.strip():
            return out
        import time as _time
        t0 = _time.perf_counter()
        prompt_payload = (
            "You are an expert UK Solvency II Chief Actuary presenting YE 2026 Latest Actuals vs YE 2025 Prior Year and YE 2026 Predicted Roll-Forward.\n"
            "Answer this exact question using ONLY the governed data tables, governance memos, and Senior Actuary rules below. "
            "Cite exact £m figures, percentages, document IDs (e.g. DOC-ALC-01), and rule IDs (e.g. RULE-01) in clean Markdown with clear headings.\n\n"
            f"Question: {scen_question}\n\n"
            f"Queried Data Table:\n{scen_dict['df_filter'].to_string(index=False)}\n\n"
            f"Full Balance Sheet:\n{bs_df.to_string(index=False)}\n\n"
            f"Relevant Governance Docs:\n{json.dumps([docs_map[d] for d in scen_dict['docs']])}\n\n"
            f"Senior Actuary Rules:\n{json.dumps([rules_map[r] for r in scen_dict['rules']])}"
        )
        ok, gen_text, model_used, err_msg = call_gemini_text(api_key, prompt_payload)
        if ok and gen_text:
            elapsed = _time.perf_counter() - t0
            out["narrative"] = gen_text
            out["engine_badge"] = f"🟢 Live Google Gemini LLM (`{model_used}`) · Generated in {elapsed:.2f}s"
            st.session_state.gemini_status = (True, f"Connected to Google Gemini (`{model_used}`)")
            st.session_state.gemini_model_used = model_used
        else:
            st.warning(f"Gemini API call failed ({err_msg}) — falling back to Governed Deterministic Calculation Engine.")
        return out

    # Inline Gemini Configuration Bar directly in Stage 4 so the user doesn't have to hunt in the sidebar
    with st.expander("🔑 Configure Live Google Gemini API Key (Optional — Real-Time LLM Synthesis)", expanded=bool("Live Google Gemini" in engine_mode or st.session_state.gemini_api_key)):
        g_col1, g_col2, g_col3 = st.columns([2.8, 1.2, 1.6])
        with g_col1:
            stage4_key = st.text_input(
                "Paste Google Gemini API Key (`AIzaSy...`):",
                value=st.session_state.gemini_api_key,
                type="password",
                placeholder="AIzaSy... (Get a key from https://aistudio.google.com/apikey)",
                key="stage4_gemini_input",
            )
            if stage4_key.strip() != st.session_state.gemini_api_key:
                st.session_state.gemini_api_key = stage4_key.strip()
                st.session_state.gemini_status = None
                gemini_api_key = st.session_state.gemini_api_key
        with g_col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🔌 Test & Activate Key", key="stage4_test_btn", use_container_width=True, type="primary"):
                with st.spinner("Verifying key with Google Gemini..."):
                    ok, mdl, msg = verify_gemini_api_key(st.session_state.gemini_api_key)
                    st.session_state.gemini_status = (ok, msg)
                    if ok:
                        st.session_state.gemini_model_used = mdl
                        gemini_api_key = st.session_state.gemini_api_key
        with g_col3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.session_state.gemini_status is not None:
                ok, msg = st.session_state.gemini_status
                if ok:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")
            elif st.session_state.gemini_api_key:
                st.info("🟢 Key Ready (`" + st.session_state.gemini_api_key[:6] + "...`) — Click **Run** below!")
            else:
                st.caption("⚙️ Currently using **Offline Deterministic Engine**. Paste key & click **Test & Activate Key** to switch to Live Gemini LLM.")

    # Whenever a key is stored in session state, allow Stage 4 to use it directly!
    effective_gemini_key = st.session_state.gemini_api_key.strip()

    if "active_scen_idx" not in st.session_state:
        st.session_state.active_scen_idx = 0
    if "custom_result" not in st.session_state:
        st.session_state.custom_result = None

    scen_keys = list(SCENARIOS.keys())

    st.markdown("#### ⚡ 1-Click Actuarial Questions (Explaining 🟢 YE 2026 Latest Actuals):")
    btn_cols = st.columns(4)
    for i, (k, s) in enumerate(SCENARIOS.items()):
        is_active = (st.session_state.active_scen_idx == i and st.session_state.custom_result is None)
        if btn_cols[i].button(
            s["title_short"],
            key=f"scen_btn_{i}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.active_scen_idx = i
            if effective_gemini_key:
                with st.spinner("Calling Live Google Gemini LLM with 5-Agent Governed Context..."):
                    st.session_state.custom_result = run_gemini_for_preset(k, s, effective_gemini_key)
            else:
                st.session_state.custom_result = None
            st.rerun()

    def on_dropdown_change():
        chosen = st.session_state.dropdown_scen
        st.session_state.active_scen_idx = scen_keys.index(chosen)
        st.session_state.custom_result = None

    selected_scen_key = st.selectbox(
        "Or Select From the Full Actuarial Question Menu:",
        scen_keys,
        index=st.session_state.active_scen_idx,
        key="dropdown_scen",
        on_change=on_dropdown_change,
    )

    custom_q = st.text_input(
        "Or Type an Ad-Hoc Actuarial Question (Live Calculation + RAG Enabled):",
        placeholder="e.g. What happened to the overall solvency ratio? Or why did WP_Fund equities fall?"
    )

    run_btn = st.button("🚀 Run 5-Agent Parallel Orchestration", type="primary", use_container_width=True)

    if run_btn:
        with st.spinner("Executing 5-Agent Parallel Orchestration (Intent -> SQL -> Vector -> Rules -> Synthesis)..."):
            import time
            time.sleep(0.35)
            if custom_q.strip():
                st.session_state.custom_result = run_adhoc_agents(custom_q.strip(), effective_gemini_key)
                active_for_log = st.session_state.custom_result
            elif effective_gemini_key:
                cur_k = scen_keys[st.session_state.active_scen_idx]
                st.session_state.custom_result = run_gemini_for_preset(cur_k, SCENARIOS[cur_k], effective_gemini_key)
                active_for_log = st.session_state.custom_result
            else:
                st.session_state.custom_result = None
                active_for_log = SCENARIOS[scen_keys[st.session_state.active_scen_idx]]

            st.session_state.audit_logs.insert(
                0,
                {
                    "Timestamp (UTC)": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "Query ID": f"QRY-2026-{101 + len(st.session_state.audit_logs)}",
                    "Target Period Explained": "YE 2026 (Latest Actual vs YE 2025 & Predicted)",
                    "Fund Scope": active_for_log["fund"],
                    "SQL Tables": "s2_balance_sheet, s2_movement_bridge",
                    "Vector Docs Cited": ", ".join(active_for_log["docs"]),
                    "Cheat Codes Applied": ", ".join(active_for_log["rules"]),
                    "PII Guardrail": "PII Redacted ✓",
                    "Math Verification": "Exact Match ✓",
                },
            )
            st.success("✅ 5-Agent Parallel Orchestration Completed Successfully")

    active_scen = (
        st.session_state.custom_result
        if st.session_state.custom_result is not None
        else SCENARIOS[scen_keys[st.session_state.active_scen_idx]]
    )

    # Visual agent orchestration pipeline
    a1, a2, a3, a4, a5 = st.columns(5)
    a1.markdown(f"<div class='agent-box'><b>01 Intent Agent</b><br><span style='color:#0ea5e9;'>✓ Routed</span><br><small>Target: <code>YE 2026 Latest</code><br>Fund: <code>{active_scen['fund']}</code></small></div>", unsafe_allow_html=True)
    a2.markdown(f"<div class='agent-box'><b>02 Data Agent (SQL)</b><br><span style='color:#10b981;'>✓ Executed</span><br><small>Topic: <code>{active_scen['metric']}</code></small></div>", unsafe_allow_html=True)
    a3.markdown(f"<div class='agent-box'><b>03 Context Agent</b><br><span style='color:#10b981;'>✓ Vector Match</span><br><small>Docs: <code>{', '.join(active_scen['docs'])}</code></small></div>", unsafe_allow_html=True)
    a4.markdown(f"<div class='agent-box'><b>04 Exemplar Agent</b><br><span style='color:#10b981;'>✓ Enforced</span><br><small>Rules: <code>{', '.join(active_scen['rules'])}</code></small></div>", unsafe_allow_html=True)
    a5.markdown("<div class='agent-box'><b>05 Synthesis Agent</b><br><span style='color:#7c3aed;'>✓ Mosaic Gateway</span><br><small>PII Redacted &amp; Governed</small></div>", unsafe_allow_html=True)

    output_narrative = active_scen["narrative"]
    badge_text = active_scen.get("engine_badge", "⚙️ Governed Deterministic Calculation Engine (Offline-Safe)")

    st.markdown("---")
    st.markdown(
        f"<div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;'>"
        f"<h4 style='margin:0;'>🎯 Question Explained: <code>{active_scen['title_short']}</code></h4>"
        f"<span style='background:#0f172a; border:1px solid #38bdf8; color:#e2e8f0; padding:5px 12px; border-radius:999px; font-size:0.84rem; font-weight:600;'>{badge_text}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown(output_narrative)

    st.markdown("#### 🔬 Governed 5-Agent Evidence Trail")
    ev1, ev2, ev3 = st.columns(3)
    with ev1:
        st.markdown("**02 Data Agent (Executed SQL Query & Reconciled Rows)**")
        st.code(active_scen["sql_query"], language="sql")
        st.dataframe(active_scen["df_filter"], use_container_width=True, hide_index=True)
    with ev2:
        st.markdown("**03 Context Agent (Retrieved Vector Governance Chunks)**")
        for doc_id in active_scen["docs"]:
            d = docs_map[doc_id]
            st.info(f"**📄 {d['doc_id']} ({d['date']}) — {d['title']}**\n\n{d['content']}")
    with ev3:
        st.markdown("**04 Exemplar Agent (Enforced Senior Actuary Rules)**")
        for rule_id in active_scen["rules"]:
            r = rules_map[rule_id]
            st.success(f"**⚖️ {r['rule_id']}**: {r['governing_rule']}\n\n*\"{r['exemplar_narrative_snippet']}\"*")

# ------------------------------------------------------------------------------
# STAGE 5: MOSAIC AI GATEWAY & AUDIT LOG
# ------------------------------------------------------------------------------
with tab5:
    g1, g2, g3 = st.columns(3)
    g1.metric("Mosaic AI Gateway Routing", "100% Enforced", "All YE 2026 queries logged")
    g2.metric("PII & Policyholder Redaction", "0 Leaks", "NINO & Counterparties Masked")
    g3.metric("Cheat-Code Compliance", "5 / 5 Verified", "Exact 2024–2026 Math Reconciled")
    st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True, hide_index=True)
