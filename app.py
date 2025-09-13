import streamlit as st
import json
import os

# ----------------- Page Config -----------------
st.set_page_config(page_title="Career & Skills Advisor", page_icon="⚡", layout="wide")

# ----------------- Custom CSS -----------------
st.markdown(
    """
    <style>
    body { background: #0f172a; color: #e2e8f0; }
    .header {
        background: linear-gradient(90deg,#0ea5a4,#6366f1);
        padding: 18px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 18px;
    }
    .card {
        background: #1e293b;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .section-title { font-size: 18px; font-weight: 600; color: #38bdf8; margin-top: 10px; }
    .badge {
        display:inline-block;
        padding:4px 10px;
        border-radius:20px;
        background:#2563eb;
        color:#fff;
        font-size:12px;
        margin-left:8px;
    }
    a.resource {
        display:inline-block;
        padding:6px 12px;
        margin:4px 6px 4px 0;
        border-radius:8px;
        background:#0ea5a4;
        color:white !important;
        text-decoration:none;
        font-size:13px;
    }
    a.resource:hover { background:#14b8a6; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- Header -----------------
st.markdown(
    """
    <div class="header">
        <h1>🎓 Career & Skills Advisor</h1>
        <p style="margin:0">Prototype by <b>Team Neuro Volt ⚡</b> — Semester-wise Career Guidance</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- Load JSON -----------------
file_path = os.path.join(os.path.dirname(__file__), "careers.json")
try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    st.error(f"❌ Could not load careers.json: {e}")
    st.stop()

# ----------------- Inputs -----------------
col1, col2 = st.columns([1,2])
with col1:
    branch_options = ["All"] + list(data.keys())
    branch = st.selectbox("Branch:", branch_options)
    sem_input = st.text_input("Semester (1–8):", value="3")
    try:
        semester = str(int(sem_input.strip()))
    except:
        semester = "3"
        st.warning("Invalid semester, defaulting to 3.")
    btn = st.button("✨ Get Recommendations")

with col2:
    st.markdown("### ℹ️ How it works")
    st.write("Select branch + semester → see **Career Paths, Skills, Projects, Resources** for that semester.")
    st.write("Resources are clickable. Works offline with JSON.")
    st.caption("Ask AI is optional (needs OpenAI key).")

# ----------------- Renderer -----------------
def render_branch_sem(branch_name, sem_key):
    branch_data = data.get(branch_name, {})
    entry = branch_data.get(sem_key)
    if not entry:
        st.warning(f"No data for {branch_name} semester {sem_key}")
        return

    st.markdown(f"<div class='card'><h2>{branch_name} <span class='badge'>Semester {sem_key}</span></h2>", unsafe_allow_html=True)

    # Career Paths
    st.markdown("<div class='section-title'>🎯 Career Paths</div>", unsafe_allow_html=True)
    for i, cp in enumerate(entry.get("career_paths", []), 1):
        st.write(f"{i}. {cp}")

    # Skills
    st.markdown("<div class='section-title'>🛠 Skills to Learn</div>", unsafe_allow_html=True)
    st.write(", ".join(entry.get("skills", [])) or "—")

    # Projects
    st.markdown("<div class='section-title'>💡 Project Ideas</div>", unsafe_allow_html=True)
    for i, p in enumerate(entry.get("projects", []), 1):
        st.write(f"{i}. {p}")

    # Resources
    st.markdown("<div class='section-title'>📚 Resources</div>", unsafe_allow_html=True)
    resources = entry.get("resources", [])
    for r in resources:
        if r.startswith("http"):
            st.markdown(f"<a href='{r}' target='_blank' class='resource'>{r}</a>", unsafe_allow_html=True)
        else:
            st.write(f"- {r}")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- Show Results -----------------
if btn:
    if branch == "All":
        for b in data.keys():
            render_branch_sem(b, semester)
    else:
        render_branch_sem(branch, semester)

# ----------------- Footer -----------------
st.markdown("---")
st.caption("Built with ❤️ by Team Neuro Volt ⚡")

