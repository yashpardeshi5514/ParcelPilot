import streamlit as st

from agent.demo_agent import ask_demo_agent


st.set_page_config(
    page_title="ParcelPilot Support AI",
    page_icon="📦",
    layout="wide"
)

# ==================================================
# GLOBAL STYLING
# ==================================================

st.markdown("""
<style>

/* -------------------------------------------------
   FONT / BASE
------------------------------------------------- */
html, body, [class*="css"] {
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif;
}

/* -------------------------------------------------
   KEYFRAMES
------------------------------------------------- */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(16px) scale(0.98); }
    to   { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-16px) scale(0.98); }
    to   { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes pulseDot {
    0%   { box-shadow: 0 0 0 0 rgba(34,197,94,0.55); }
    70%  { box-shadow: 0 0 0 8px rgba(34,197,94,0); }
    100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
}
@keyframes floatY {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50%      { transform: translateY(-6px) rotate(-3deg); }
}
@keyframes shimmerBorder {
    0%   { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}
@keyframes popIn {
    0%   { opacity: 0; transform: scale(0.85); }
    70%  { transform: scale(1.03); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes bounceDots {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40%           { transform: scale(1); opacity: 1; }
}
@keyframes glowPulse {
    0%, 100% { opacity: 0.55; }
    50%      { opacity: 1; }
}
@keyframes orbDrift {
    0%   { transform: translate(0, 0) scale(1); }
    50%  { transform: translate(20px, -15px) scale(1.08); }
    100% { transform: translate(0, 0) scale(1); }
}

/* -------------------------------------------------
   APP-WIDE LIGHT THEME + PREMIUM BACKGROUND
   (overrides Streamlit's default/dark theme)
------------------------------------------------- */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    background:
        radial-gradient(ellipse 900px 500px at 8% -10%, rgba(37,99,235,0.07), transparent 60%),
        radial-gradient(ellipse 900px 500px at 95% 0%, rgba(124,58,237,0.06), transparent 60%),
        #fbfcfe !important;
    color: #0f172a !important;
    overflow-x: hidden;
}
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stToolbar"] { background-color: transparent !important; color: #0f172a !important; }
[data-testid="stDecoration"] { background: linear-gradient(90deg, #0f3d63, #2563eb, #7c3aed) !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

hr { border-color: #e2e8f0 !important; }

.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label {
    color: #0f172a;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #0f172a !important;
    line-height: 1.55;
}
[data-testid="stCaptionContainer"] { color: #64748b !important; }

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-color: #cbd5e1 !important;
    color: #0f172a !important;
    border-radius: 10px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
div[data-baseweb="select"]:hover > div {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08);
}

/* -------------------------------------------------
   SIDEBAR
------------------------------------------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    border-right: 1px solid #e2e8f0;
}
section[data-testid="stSidebar"] * { color: #1e293b !important; }
section[data-testid="stSidebar"] hr { border-color: #e2e8f0; }

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-color: #cbd5e1 !important;
}
section[data-testid="stSidebar"] code {
    background-color: #eef2f6 !important;
    color: #0f3d63 !important;
    border-radius: 4px;
}

.pp-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0 2px 0;
}
.pp-brand-icon {
    font-size: 26px;
    display: inline-block;
    animation: floatY 3.4s ease-in-out infinite;
    filter: drop-shadow(0 3px 6px rgba(15,61,99,0.25));
}
.pp-brand-name {
    font-size: 20px;
    font-weight: 800;
    background: linear-gradient(90deg, #0f3d63, #2563eb 55%, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.3px;
}

/* Account context card - glassmorphism + 3D tilt */
.pp-account-card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(8px);
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 14px 16px;
    margin-top: 8px;
    box-shadow: 0 1px 2px rgba(15,23,42,0.04);
    transition: transform 0.35s cubic-bezier(.2,.8,.2,1), box-shadow 0.35s ease, border-color 0.25s ease;
    transform-style: preserve-3d;
}
.pp-account-card:hover {
    border-color: #2563eb;
    box-shadow: 0 16px 30px rgba(37,99,235,0.16), 0 4px 10px rgba(124,58,237,0.08);
    transform: translateY(-4px) rotateX(4deg) rotateY(-2deg) scale(1.015);
}
.pp-account-card .pp-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    font-size: 13.5px;
}
.pp-account-card .pp-label {
    color: #64748b !important;
    letter-spacing: 0.2px;
    text-transform: uppercase;
    font-size: 11.5px;
    font-weight: 600;
}

.pp-pill {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    animation: popIn 0.4s cubic-bezier(.2,.8,.2,1) both;
    transition: transform 0.2s ease;
}
.pp-pill:hover { transform: scale(1.08); }
.pp-pill-active {
    background-color: #dcfce7;
    color: #16a34a !important;
}
.pp-pill-enterprise { background-color: #dbeafe; color: #1d4ed8 !important; }
.pp-pill-growth     { background-color: #ede9fe; color: #6d28d9 !important; }

/* Clear conversation - utility/destructive styling */
.pp-clear-btn div.stButton > button {
    background-color: #fff1f2 !important;
    border: 1px solid #fecdd3 !important;
    color: #be123c !important;
}
.pp-clear-btn div.stButton > button:hover {
    background-color: #ffe4e6 !important;
    border-color: #fb7185 !important;
    color: #9f1239 !important;
    box-shadow: 0 6px 14px rgba(225,29,72,0.15);
}

/* -------------------------------------------------
   HERO HEADER
------------------------------------------------- */
.pp-hero {
    position: relative;
    padding: 22px 26px;
    border-radius: 20px;
    margin-bottom: 8px;
    overflow: hidden;
    background: linear-gradient(#ffffff, #ffffff) padding-box,
                linear-gradient(120deg, #0f3d63, #2563eb, #7c3aed) border-box;
    border: 1.5px solid transparent;
    box-shadow: 0 10px 28px rgba(37,99,235,0.1), 0 2px 6px rgba(15,23,42,0.04);
    animation: fadeIn 0.6s ease;
}
.pp-hero-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.16;
    animation: orbDrift 9s ease-in-out infinite;
    pointer-events: none;
}
.pp-hero-orb.a { width: 180px; height: 180px; background: #2563eb; top: -60px; left: 10%; }
.pp-hero-orb.b { width: 220px; height: 220px; background: #7c3aed; bottom: -80px; right: 8%; animation-delay: -3s; }
.pp-hero-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(15,61,99,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15,61,99,0.035) 1px, transparent 1px);
    background-size: 34px 34px;
    mask-image: radial-gradient(ellipse 80% 100% at 50% 0%, #000 40%, transparent 90%);
    pointer-events: none;
}
.pp-hero-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 16px;
}
.pp-hero-title {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -0.4px;
    margin: 0;
    color: #0f172a;
}
.pp-hero-sub {
    font-size: 13.5px;
    color: #64748b;
    margin: 3px 0 0 0;
    letter-spacing: 0.1px;
}

/* -------------------------------------------------
   CHAT MESSAGES
------------------------------------------------- */
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 4px 6px !important;
    margin-bottom: 10px !important;
    border: 1px solid #eef1f5 !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
[data-testid="stChatMessage"]:active { transform: scale(0.995); }

/* Assistant bubble: glass card with blue/violet glow */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: rgba(255,255,255,0.85) !important;
    backdrop-filter: blur(6px);
    box-shadow: 0 2px 6px rgba(37,99,235,0.06), 0 10px 24px rgba(124,58,237,0.05);
    animation: slideInLeft 0.4s cubic-bezier(.2,.8,.2,1) both;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]):hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 14px rgba(37,99,235,0.1), 0 16px 30px rgba(124,58,237,0.1);
    border-color: #dbeafe !important;
}

/* User bubble: subtle gradient + depth */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%) !important;
    box-shadow: 0 2px 6px rgba(15,23,42,0.05), 0 10px 20px rgba(15,23,42,0.03);
    animation: slideInRight 0.4s cubic-bezier(.2,.8,.2,1) both;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]):hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 14px rgba(15,23,42,0.08), 0 16px 28px rgba(15,23,42,0.06);
}

[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08);
    border-radius: 50% !important;
    animation: floatY 4s ease-in-out infinite;
}

/* -------------------------------------------------
   THINKING INDICATOR
------------------------------------------------- */
.pp-thinking {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 2px;
    animation: fadeIn 0.3s ease;
}
.pp-thinking-text {
    font-size: 13.5px;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.1px;
}
.pp-thinking-dots { display: inline-flex; gap: 4px; }
.pp-thinking-dots span {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    animation: bounceDots 1.2s infinite ease-in-out;
}
.pp-thinking-dots span:nth-child(1) { animation-delay: -0.24s; }
.pp-thinking-dots span:nth-child(2) { animation-delay: -0.12s; }
.pp-thinking-dots span:nth-child(3) { animation-delay: 0s; }

/* -------------------------------------------------
   TOOL BADGES
------------------------------------------------- */
.pp-tools-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}
.pp-tool-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 11px;
    background: rgba(37,99,235,0.06);
    border: 1px solid rgba(37,99,235,0.18);
    color: #1e3a8a;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    backdrop-filter: blur(4px);
    animation: popIn 0.35s cubic-bezier(.2,.8,.2,1) both;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.pp-tool-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(37,99,235,0.18);
    border-color: #2563eb;
}
.pp-tool-badge .pp-tool-icon { animation: floatY 2.6s ease-in-out infinite; display: inline-block; }

/* -------------------------------------------------
   CHAT INPUT
------------------------------------------------- */
[data-testid="stBottom"] * { background-color: transparent !important; }
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stChatInputContainer"] {
    background: transparent !important;
}

[data-testid="stChatInput"] {
    background-color: rgba(255,255,255,0.85) !important;
    backdrop-filter: blur(10px);
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 16px !important;
    box-shadow: 0 6px 20px rgba(15,23,42,0.06);
    transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
    overflow: hidden;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
    color: #0f172a !important;
    caret-color: #0f3d63 !important;
}
[data-testid="stChatInput"]:hover:not(:focus-within) {
    border-color: #94a3b8 !important;
    transform: translateY(-1px);
}
[data-testid="stChatInput"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,0.12), 0 10px 24px rgba(37,99,235,0.1) !important;
}
[data-testid="stChatInput"]:has(textarea:not(:placeholder-shown)) {
    border: 1.5px solid transparent !important;
    background: linear-gradient(#ffffff, #ffffff) padding-box,
                linear-gradient(90deg, #0f3d63, #2563eb, #7c3aed, #2563eb, #0f3d63) border-box !important;
    background-size: 100% 100%, 300% 100%;
    animation: shimmerBorder 4s linear infinite;
}
[data-testid="stChatInput"]:has(textarea:not(:placeholder-shown)) textarea {
    background-color: #ffffff !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    transition: opacity 0.3s ease;
    color: #64748b !important;
    opacity: 1 !important;
}

[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #0f3d63, #2563eb) !important;
    border-radius: 10px !important;
    transition: transform 0.2s cubic-bezier(.34,1.56,.64,1), box-shadow 0.2s ease;
}
[data-testid="stChatInputSubmitButton"] svg { fill: #ffffff !important; }
[data-testid="stChatInputSubmitButton"]:hover {
    transform: scale(1.1) rotate(-6deg);
    box-shadow: 0 8px 18px rgba(37,99,235,0.4);
}
[data-testid="stChatInputSubmitButton"]:active {
    transform: scale(0.92) rotate(0deg);
}

/* -------------------------------------------------
   PENDING ESCALATION CARD
------------------------------------------------- */
.pp-pending-card {
    position: relative;
    background: linear-gradient(135deg, #fffbeb 0%, #fff7ed 100%);
    border: 1px solid #fbbf24;
    border-left: 4px solid #f59e0b;
    border-radius: 14px;
    padding: 20px 22px;
    margin-top: 10px;
    animation: popIn 0.45s cubic-bezier(.2,.8,.2,1) both;
    box-shadow: 0 10px 26px rgba(245,158,11,0.16);
    transition: box-shadow 0.25s ease;
}
.pp-pending-card:hover { box-shadow: 0 14px 32px rgba(245,158,11,0.22); }
.pp-pending-title {
    font-size: 15.5px;
    font-weight: 800;
    color: #92400e;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.pp-pending-icon { display: inline-block; animation: floatY 2s ease-in-out infinite; }
.pp-pending-row { font-size: 14px; color: #78350f; margin: 5px 0; }
.pp-pending-row b { color: #451a03; }
.pp-priority-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-left: 6px;
}
.pp-priority-high, .pp-priority-critical { background: #fee2e2; color: #b91c1c; }
.pp-priority-medium { background: #ffedd5; color: #c2410c; }
.pp-priority-low { background: #dcfce7; color: #15803d; }

/* -------------------------------------------------
   BUTTONS (general)
------------------------------------------------- */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: 8px 0;
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    transition: transform 0.15s ease, box-shadow 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(15,23,42,0.1);
    border-color: #2563eb;
    color: #2563eb;
}
div.stButton > button:active {
    transform: translateY(0) scale(0.97);
    box-shadow: 0 2px 4px rgba(15,23,42,0.15);
}

/* Confirm Escalation - success styling */
.pp-confirm-btn div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(21,128,61,0.3);
}
.pp-confirm-btn div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 10px 22px rgba(21,128,61,0.4);
    transform: translateY(-2px);
}
.pp-confirm-btn div.stButton > button[kind="primary"]:active {
    transform: translateY(0) scale(0.97);
}

/* Cancel - subtle danger styling */
.pp-cancel-btn div.stButton > button {
    background-color: #fff1f2 !important;
    border: 1px solid #fecdd3 !important;
    color: #be123c !important;
}
.pp-cancel-btn div.stButton > button:hover {
    background-color: #ffe4e6 !important;
    border-color: #fb7185 !important;
    color: #9f1239 !important;
}

/* -------------------------------------------------
   RESPONSIVE
------------------------------------------------- */
@media (max-width: 900px) {
    .pp-hero-title { font-size: 21px; }
    .pp-hero { padding: 16px 18px; }
}
 /* -------------------------------------------------
   USER CHAT BUBBLE
------------------------------------------------- */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: linear-gradient(
        135deg,
        #dbeafe 0%,
        #e0e7ff 100%
    ) !important;

    border: 1px solid #c7d2fe !important;
    border-radius: 18px !important;

    box-shadow:
        0 6px 18px rgba(79, 70, 229, 0.10) !important;
}

/* Also support newer Streamlit avatar selector */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) {
    background: linear-gradient(
        135deg,
        #dbeafe 0%,
        #e0e7ff 100%
    ) !important;

    border: 1px solid #c7d2fe !important;
    border-radius: 18px !important;

    box-shadow:
        0 6px 18px rgba(79, 70, 229, 0.10) !important;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

if "account_id" not in st.session_state:
    st.session_state.account_id = "ACCT-001"


# ==================================================
# TOOL BADGE ICON MAP
# ==================================================

TOOL_ICONS = {
    "search_parcelpilot_documents": "🔎",
    "get_my_order": "",
    "get_my_account": "👤",
}


def render_tool_badges(tools):
    badges_html = ""
    for tool in tools:
        icon = TOOL_ICONS.get(tool, "🔧")
        badges_html += (
            f'<span class="pp-tool-badge">'
            f'<span class="pp-tool-icon">{icon}</span>{tool}</span>'
        )
    st.markdown(f'<div class="pp-tools-wrap">{badges_html}</div>', unsafe_allow_html=True)


def priority_badge_class(priority):
    p = str(priority).strip().lower()
    if p in ("high", "critical"):
        return f"pp-priority-{p}"
    if p == "medium":
        return "pp-priority-medium"
    if p == "low":
        return "pp-priority-low"
    return "pp-priority-medium"


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div class="pp-brand">
            <span class="pp-brand-icon"></span>
            <span class="pp-brand-name">ParcelPilot</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption("Support Console")

    st.divider()

    st.subheader("Customer")

    account_options = {
        "Northstar Logistics": "ACCT-001",
        "LumenWorks": "ACCT-002"
    }

    selected_customer = st.selectbox(
        "Account",
        list(account_options.keys()),
        label_visibility="collapsed"
    )

    st.session_state.account_id = account_options[selected_customer]

    st.caption(f"Account ID: `{st.session_state.account_id}`")

    st.divider()

    st.subheader("Account Context")

    if st.session_state.account_id == "ACCT-001":
        plan_label, plan_class = "Enterprise", "pp-pill-enterprise"
    else:
        plan_label, plan_class = "Growth", "pp-pill-growth"

    st.markdown(
        f"""
        <div class="pp-account-card">
            <div class="pp-row">
                <span class="pp-label">Plan</span>
                <span class="pp-pill {plan_class}">{plan_label}</span>
            </div>
            <div class="pp-row">
                <span class="pp-label">Status</span>
                <span class="pp-pill pp-pill-active">Active</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown('<div class="pp-clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_action = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# HERO HEADER
# ==================================================

st.markdown(
    """
    <div class="pp-hero">
        <div class="pp-hero-orb a"></div>
        <div class="pp-hero-orb b"></div>
        <div class="pp-hero-grid"></div>
        <div class="pp-hero-content">
            <div>
                <p class="pp-hero-title">
                    ParcelPilot Support AI
                </p>
                <p class="pp-hero-sub">Customer support assistant</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar="🧑‍💼"
        ):
            st.markdown(
                message["content"]
            )

    else:

        with st.chat_message("assistant"):
            st.markdown(
                message["content"]
            )


# ==================================================
# CHAT INPUT
# ==================================================

user_message = st.chat_input(
    "Ask about your shipment, account, or support issue..."
)


if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message(
        "user",
        avatar="🧑‍💼"
    ):
        st.markdown(
            user_message
        )

    with st.chat_message("assistant"):

        thinking_placeholder = st.empty()

        thinking_placeholder.markdown(
            """
            <div class="pp-thinking">
                <span class="pp-thinking-text">
                    ParcelPilot AI is thinking
                </span>

                <span class="pp-thinking-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        try:

            result = ask_demo_agent(
                user_message
            )

            answer = result["answer"]

            if result.get("pending_action"):
                st.session_state.pending_action = (
                    result["pending_action"]
                )

        except Exception as e:

            result = {
                "tools": []
            }

            answer = (
                "Sorry, I encountered an error "
                "while processing your request."
            )

            thinking_placeholder.empty()

            st.error(str(e))

        else:

            thinking_placeholder.empty()

        st.markdown(answer)

        if result["tools"]:
            render_tool_badges(
                result["tools"]
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

# ==================================================
# PENDING ACTION CONFIRMATION
# ==================================================

if st.session_state.pending_action:

    action = st.session_state.pending_action

    priority_class = priority_badge_class(action["priority"])

    st.markdown(
        f"""
        <div class="pp-pending-card">
            <div class="pp-pending-title">
                <span class="pp-pending-icon">⚠️</span>
                This action requires your confirmation
            </div>
            <div class="pp-pending-row">
                <b>Priority:</b> {action['priority']}
                <span class="pp-priority-badge {priority_class}">{action['priority']}</span>
            </div>
            <div class="pp-pending-row"><b>Reason:</b> {action['reason']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="pp-confirm-btn">', unsafe_allow_html=True)

        if st.button(
            "✅ Confirm Escalation",
            use_container_width=True,
            type="primary"
        ):

            from tools.actions import create_escalation

            result = create_escalation(
                account_id=st.session_state.account_id,
                ticket_id="TKT-PENDING",
                priority=action["priority"],
                reason=action["reason"]
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    f"✅ Escalation created successfully.\n\n"
                    f"**Escalation ID:** "
                    f"{result['escalation_id']}\n\n"
                    f"**Priority:** {result['priority']}\n\n"
                    f"**Status:** {result['status']}"
                )
            })

            st.session_state.pending_action = None

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="pp-cancel-btn">', unsafe_allow_html=True)

        if st.button(
            "❌ Cancel",
            use_container_width=True
        ):

            st.session_state.pending_action = None

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)