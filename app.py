import os
import streamlit as st
from dotenv import load_dotenv
from graph.workflow import create_workflow

# Page config
st.set_page_config(
    page_title="AI Multi-Agent Blog Generator",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load env variables
load_dotenv()

# App header styling
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #1E3A8A; font-family: 'Outfit', sans-serif;">🤖 AI Multi-Agent Blog Generator</h1>
    <p style="color: #4B5563; font-size: 1.1rem;">Collaborative Agentic AI using LangGraph, DuckDuckGo Search, and Groq Llama 3</p>
</div>
""", unsafe_allow_html=True)

# Sidebar config
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

# Workflow visualizer in sidebar
st.sidebar.markdown("""
### Agent Workflow Architecture
1. **User Topic Input** 📥
2. **Researcher Agent** 🔍
   * Uses DuckDuckGo search tool
   * Scrapes snippets and saves to Shared State
3. **Writer Agent** ✍️
   * Reads research from Shared State
   * Instructs Groq Llama 3 LLM
4. **Final Blog Output** 📄
""")

# Main UI layout
st.markdown("### 📝 Enter Topic")
topic = st.text_input("What topic would you like the agents to research and write about?", placeholder="e.g., Future of Artificial General Intelligence (AGI)")

# Execution
if st.button("Generate Blog Post", type="primary"):
    if not api_key:
        st.error("Please configure the GROQ_API_KEY in the sidebar or in your .env file to run the app.")
    elif not topic.strip():
        st.warning("Please enter a valid topic.")
    else:
        # Run workflow
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
            
            # Run stream
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
            blog_post = final_state.get("blog_post", "")
            research_data = final_state.get("research_data", "")
            
            if blog_post:
                st.success("✨ Your blog post has been successfully generated!")
                
                # Show results in tabs
                tab1, tab2 = st.tabs(["📄 Generated Blog Post", "🔍 Research Data Gathered"])
                
                with tab1:
                    st.markdown("### Preview")
                    st.markdown("---")
                    st.markdown(blog_post)
                    st.markdown("---")
                    
                    # Download button
                    safe_title = "".join(c for c in topic.lower() if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
                    st.download_button(
                        label="Download Blog Post (.md)",
                        data=blog_post,
                        file_name=f"{safe_title}_blog.md",
                        mime="text/markdown"
                    )
                    
                with tab2:
                    st.markdown("### Raw Search Results")
                    st.text_area("DuckDuckGo Search Results:", value=research_data, height=400)
            else:
                st.error("Failed to generate blog post content.")
                
        except Exception as e:
            st.error(f"An error occurred during workflow execution: {str(e)}")
