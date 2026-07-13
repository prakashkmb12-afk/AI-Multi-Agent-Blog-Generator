import os
import streamlit as st
from dotenv import load_dotenv
from graph.workflow import create_workflow

# Page config
st.set_page_config(
    page_title="AI Multi-Agent Blog Generator",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"  # Collapsed by default to match screenshot
)

# Load env variables
load_dotenv()

# App header styling matching the screenshot
st.markdown("""
<div style="text-align: center; margin-top: 1.5rem; margin-bottom: 0.5rem;">
    <h1 style="color: #3B82F6; font-size: 2.8rem; font-weight: 700; font-family: 'Outfit', sans-serif; margin-bottom: 0.2rem;">AI Multi-Agent Blog Generator</h1>
    <p style="color: #9CA3AF; font-size: 1.1rem; margin-top: 0;">Collaborative Agentic AI using LangGraph, DuckDuckGo Search, and Groq Llama 3</p>
</div>
<hr style="border-color: #1F2937; margin-bottom: 2rem;">
""", unsafe_allow_html=True)

# Collapsible configuration sidebar
st.sidebar.image("https://img.icons8.com/color/96/robot.png", width=96)
st.sidebar.title("Configuration & Flow")

# Allow manual Groq API key input if not in .env
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.sidebar.warning("GROQ_API_KEY not found in .env file.")
    api_key_input = st.sidebar.text_input("Enter Groq API Key:", type="password")
    if api_key_input:
        os.environ["GROQ_API_KEY"] = api_key_input
        api_key = api_key_input
else:
    st.sidebar.success("Groq API Key loaded from .env")

# Model configuration
model_name = st.sidebar.selectbox(
    "Choose Writer LLM Model",
    ["llama-3.1-8b-instant", "llama3-8b-8192", "llama-3.3-70b-versatile"],
    index=0
)
temperature = st.sidebar.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

# Session state initialization
if "blog_post" not in st.session_state:
    st.session_state["blog_post"] = ""
if "research_data" not in st.session_state:
    st.session_state["research_data"] = ""
if "show_success" not in st.session_state:
    st.session_state["show_success"] = False

# Enter Topic Section
st.markdown("### Enter Topic")
topic = st.text_input(
    "What topic would you like the agents to research and write about?",
    placeholder="e.g., The Future of AI Agents",
    label_visibility="visible"
)

# Generate Button
generate_clicked = st.button("Generate Blog Post", type="primary")

if generate_clicked:
    if not api_key:
        st.error("Please configure the GROQ_API_KEY in your .env file or environment variables.")
    elif not topic.strip():
        st.warning("Please enter a valid topic.")
    else:
        # Reset state for fresh run
        st.session_state["blog_post"] = ""
        st.session_state["research_data"] = ""
        st.session_state["show_success"] = False
        
        try:
            # Set environmental configurations for LLM
            os.environ["GROQ_MODEL_NAME"] = model_name
            os.environ["GROQ_TEMPERATURE"] = str(temperature)
            
            # Create workflow graph
            app = create_workflow()
            
            initial_state = {
                "topic": topic,
                "research_data": "",
                "blog_post": ""
            }
            
            # Run stream with progress updates
            with st.status("🚀 Initializing Multi-Agent System...", expanded=True) as status:
                for event in app.stream(initial_state):
                    for node_name, state_update in event.items():
                        if node_name == "researcher":
                            status.write("🔍 **Researcher Agent** is running web searches...")
                            if "research_data" in state_update:
                                status.write("✅ **Researcher Agent** finished searching and saved findings to the shared state.")
                        elif node_name == "writer":
                            status.write("✍️ **Writer Agent** is analyzing research and composing the blog post...")
                            if "blog_post" in state_update:
                                status.write("✅ **Writer Agent** finished generating the blog using Llama 3.")
                
                status.update(label="🎉 Multi-Agent Workflow Completed!", state="complete", expanded=False)
            
            # Fetch final state
            final_state = app.invoke(initial_state)
            st.session_state["blog_post"] = final_state.get("blog_post", "")
            st.session_state["research_data"] = final_state.get("research_data", "")
            st.session_state["show_success"] = True
            
            # Force UI refresh to display results
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred during workflow execution: {str(e)}")

# Success box shown after generation
if st.session_state["show_success"]:
    st.success("Your blog post has been successfully generated!")

# Persistent Tabs layout matching the screenshot
tab1, tab2 = st.tabs(["Generated Blog Post", "Research Data Gathered"])

with tab1:
    st.markdown("### Preview")
    if st.session_state["blog_post"]:
        st.markdown(st.session_state["blog_post"])
        st.markdown("---")
        # Download button
        safe_title = "".join(c for c in topic.lower() if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
        if not safe_title:
            safe_title = "generated"
        st.download_button(
            label="Download Blog Post (.md)",
            data=st.session_state["blog_post"],
            file_name=f"{safe_title}_blog.md",
            mime="text/markdown"
        )
    else:
        st.text_area(
            "Preview",
            value="Generated blog post will appear here...",
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )

with tab2:
    if st.session_state["research_data"]:
        st.text_area(
            "Research Data",
            value=st.session_state["research_data"],
            height=400,
            disabled=True,
            label_visibility="collapsed"
        )
    else:
        st.text_area(
            "Research Data Area",
            value="Research data will appear here...",
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )
