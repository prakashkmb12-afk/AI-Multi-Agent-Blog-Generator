import os
import json
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from graph.workflow import create_workflow

# Load env variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Multi-Agent Blog Generator",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern dark-themed SaaS dashboard
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Base structure */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide default streamlit menu and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Container width centering */
.block-container {
    max-width: 800px !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* Typography and headings */
h1, h2, h3, h4, h5, h6, p, span, label {
    font-family: 'Inter', sans-serif !important;
}

/* Input styles */
div[data-baseweb="input"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}
input[type="text"] {
    color: #F8FAFC !important;
}

/* Tab design overrides */
button[data-baseweb="tab"] {
    color: #94A3B8 !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #3B82F6 !important;
    border-bottom-color: #3B82F6 !important;
}

/* Card details */
.blog-preview-card {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 28px;
    border-radius: 12px;
    max-height: 480px;
    overflow-y: auto;
    color: #E2E8F0;
    margin-bottom: 1.5rem;
    line-height: 1.7;
    font-size: 1rem;
    border-color: #334155;
}

.source-card {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 16px;
    font-family: 'Inter', sans-serif;
}
.source-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #3B82F6;
    text-decoration: none;
    display: inline-block;
    margin-bottom: 6px;
}
.source-title:hover {
    text-decoration: underline;
}
.source-link {
    font-size: 0.8rem;
    color: #64748B;
    margin-bottom: 8px;
    word-break: break-all;
}
.source-snippet {
    font-size: 0.9rem;
    color: #94A3B8;
    line-height: 1.5;
}

/* Footer structure */
.custom-footer {
    text-align: center;
    color: #64748B;
    font-size: 0.85rem;
    margin-top: 5rem;
    border-top: 1px solid #1E293B;
    padding-top: 2rem;
    font-family: 'Inter', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# Helper function to render a clean progress stepper
def display_stepper(status_step: str):
    steps = {
        "researching": {"border": "#3B82F6", "text": "#3B82F6"},
        "writing": {"border": "#334155", "text": "#64748B"},
        "completed": {"border": "#334155", "text": "#64748B"}
    }
    if status_step == "writing":
        steps["researching"] = {"border": "#10B981", "text": "#10B981"}
        steps["writing"] = {"border": "#3B82F6", "text": "#3B82F6"}
    elif status_step == "completed":
        steps["researching"] = {"border": "#10B981", "text": "#10B981"}
        steps["writing"] = {"border": "#10B981", "text": "#10B981"}
        steps["completed"] = {"border": "#10B981", "text": "#10B981"}
        
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-top: 1.5rem; margin-bottom: 2rem; font-family: 'Inter', sans-serif;">
        <div style="flex: 1; text-align: center; padding: 12px; border-bottom: 3px solid {steps['researching']['border']}; color: {steps['researching']['text']}; font-weight: 600; font-size: 0.95rem; transition: all 0.3s;">
            Researching
        </div>
        <div style="flex: 1; text-align: center; padding: 12px; border-bottom: 3px solid {steps['writing']['border']}; color: {steps['writing']['text']}; font-weight: 600; font-size: 0.95rem; transition: all 0.3s;">
            Writing
        </div>
        <div style="flex: 1; text-align: center; padding: 12px; border-bottom: 3px solid {steps['completed']['border']}; color: {steps['completed']['text']}; font-weight: 600; font-size: 0.95rem; transition: all 0.3s;">
            Completed
        </div>
    </div>
    """, unsafe_allow_html=True)

# Helper function to generate clean javascript copy button inside an iframe
def get_copy_button_html(text: str) -> str:
    escaped_text = json.dumps(text)
    return f"""
    <div style="text-align: right; margin-bottom: 8px;">
        <button id="copy-btn" style="background-color: #1E293B; color: #F8FAFC; border: 1px solid #334155; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-family: 'Inter', sans-serif; font-size: 0.85rem; font-weight: 500; transition: background-color 0.2s;">
            Copy Blog Post
        </button>
    </div>
    <script>
    document.getElementById('copy-btn').onclick = function() {{
        var text = {escaped_text};
        navigator.clipboard.writeText(text).then(function() {{
            var btn = document.getElementById('copy-btn');
            btn.innerText = 'Copied!';
            btn.style.backgroundColor = '#10B981';
            btn.style.borderColor = '#10B981';
            setTimeout(function() {{
                btn.innerText = 'Copy Blog Post';
                btn.style.backgroundColor = '#1E293B';
                btn.style.borderColor = '#334155';
            }}, 2000);
        }}).catch(function(err) {{
            console.error('Clipboard copy failed: ', err);
        }});
    }}
    </script>
    """

# Sidebar overrides (Remove/disable any left sidebar visual widgets to keep main area centered)
# We handle the Groq configurations in the background using dotenv configs by default.
api_key = os.getenv("GROQ_API_KEY")

# Header Section
st.markdown("""
<div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
    <h1 style="color: #F8FAFC; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.025em;">AI Multi-Agent Blog Generator</h1>
    <p style="color: #94A3B8; font-size: 1.05rem; line-height: 1.6; max-width: 650px; margin: 0 auto;">
        Generate high-quality blog posts using a collaborative AI workflow powered by LangGraph, DuckDuckGo Search, and Groq Llama 3.
    </p>
</div>
""", unsafe_allow_html=True)

# Session State initialization
if "blog_post" not in st.session_state:
    st.session_state["blog_post"] = ""
if "research_data" not in st.session_state:
    st.session_state["research_data"] = []
if "status" not in st.session_state:
    st.session_state["status"] = "idle"

# Main section
st.markdown("### Enter Topic")
st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -0.5rem; margin-bottom: 1rem;'>Enter a topic for the AI agents to research and generate a professional blog post.</p>", unsafe_allow_html=True)

topic = st.text_input(
    "Topic Input Field",
    placeholder="Example: The Future of Artificial Intelligence",
    label_visibility="collapsed"
)

# Centered primary button
st.markdown("<div style='margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
generate_clicked = st.button("Generate Blog Post", type="primary")
st.markdown("</div>", unsafe_allow_html=True)

# Placeholder container for the stepper progress bar
stepper_placeholder = st.empty()

# Display stepper if a run has started/completed
if st.session_state["status"] != "idle":
    with stepper_placeholder:
        display_stepper(st.session_state["status"])

if generate_clicked:
    if not api_key:
        st.error("Please configure the GROQ_API_KEY inside your .env file to execute the agents.")
    elif not topic.strip():
        st.warning("Please enter a valid topic to proceed.")
    else:
        # Reset state parameters
        st.session_state["blog_post"] = ""
        st.session_state["research_data"] = []
        st.session_state["status"] = "researching"
        
        # Display initial progress bar state
        with stepper_placeholder:
            display_stepper("researching")
            
        try:
            # Instantiate workflow
            app = create_workflow()
            initial_state = {
                "topic": topic,
                "research_data": [],
                "blog_post": ""
            }
            
            # Execute and stream events in real time to update progress status
            for event in app.stream(initial_state):
                for node_name, state_update in event.items():
                    if node_name == "researcher":
                        st.session_state["status"] = "writing"
                        with stepper_placeholder:
                            display_stepper("writing")
                    elif node_name == "writer":
                        st.session_state["status"] = "completed"
                        with stepper_placeholder:
                            display_stepper("completed")
            
            # Retrieve final updated state
            final_state = app.invoke(initial_state)
            st.session_state["blog_post"] = final_state.get("blog_post", "")
            st.session_state["research_data"] = final_state.get("research_data", [])
            st.session_state["status"] = "completed"
            
            st.rerun()
            
        except Exception as e:
            st.session_state["status"] = "idle"
            st.error(f"An error occurred during workflow execution: {str(e)}")

# Display Tabs
tab1, tab2 = st.tabs(["Generated Blog", "Research Data"])

with tab1:
    if st.session_state["blog_post"]:
        # Render Javascript copy button
        components.html(get_copy_button_html(st.session_state["blog_post"]), height=45)
        
        # Scrollable preview container
        st.markdown(f'<div class="blog-preview-card">', unsafe_allow_html=True)
        st.markdown(st.session_state["blog_post"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button
        safe_title = "".join(c for c in topic.lower() if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
        if not safe_title:
            safe_title = "generated"
        st.download_button(
            label="Download Blog Post",
            data=st.session_state["blog_post"],
            file_name=f"{safe_title}_blog.md",
            mime="text/markdown"
        )
    else:
        st.markdown('<div class="blog-preview-card" style="text-align: center; color: #64748B; padding: 60px 0;">Generated blog post will appear here...</div>', unsafe_allow_html=True)

with tab2:
    if st.session_state["research_data"]:
        if isinstance(st.session_state["research_data"], list):
            st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
            for source in st.session_state["research_data"]:
                if isinstance(source, dict):
                    title = source.get("title", "No Title")
                    link = source.get("link", "#")
                    snippet = source.get("snippet", "No Description")
                    
                    st.markdown(f"""
                    <div class="source-card">
                        <a class="source-title" href="{link}" target="_blank">{title}</a>
                        <div class="source-link">{link}</div>
                        <div class="source-snippet">{snippet}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Fallback for list of strings
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-snippet">{str(source)}</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Fallback for plain string research_data (from older runs)
            st.text_area(
                "Research Data Raw",
                value=str(st.session_state["research_data"]),
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )
    else:
        st.markdown('<div class="blog-preview-card" style="text-align: center; color: #64748B; padding: 60px 0;">Research data will appear here...</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="custom-footer">
    Built with LangGraph • LangChain • Groq API • DuckDuckGo Search
</div>
""", unsafe_allow_html=True)
