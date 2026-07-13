# AI Multi-Agent Blog Generator

An Agentic AI application built using **LangGraph**, **LangChain**, **DuckDuckGo Search**, and the **Groq API** (Llama 3). The application divides the blog generation task into two specialized agents: a **Researcher Agent** and a **Writer Agent**, communicating via a shared state.

---

## System Architecture

```
                 +----------------+
                 |      User      |
                 +-------+--------+
                         |
                         ▼
                  Enter Topic
                         |
                         ▼
               +-------------------+
               |   LangGraph Flow  |
               +---------+---------+
                         |
             -------------------------
             |                       |
             ▼                       |
     Researcher Agent               |
             |                       |
     DuckDuckGo Search              |
             |                       |
             ▼                       |
        Shared State <---------------
             |
             ▼
        Writer Agent
     (Groq Llama 3)
             |
             ▼
      Generated Blog
             |
             ▼
            User
```

---

## Project Structure

```text
multi-agent-blog-generator/
│
├── agents/
│   ├── researcher.py      # Researcher Agent node logic
│   └── writer.py          # Writer Agent node logic
│
├── graph/
│   └── workflow.py        # LangGraph StateGraph orchestration
│
├── state/
│   └── agent_state.py     # Shared State definition (TypedDict)
│
├── tools/
│   └── search_tool.py     # DuckDuckGo search integration
│
├── prompts/
│   └── writer_prompt.py   # Prompts template for blog post writer
│
├── config/
│   └── groq_config.py     # ChatGroq LLM initialization config
│
├── main.py                # Main entry point (CLI application)
├── requirements.txt       # Project python dependencies
├── .env                   # Local API keys config (Git ignored)
├── .gitignore             # Git ignore configuration
└── README.md              # Project documentation
```

---

## Installation & Setup

1. **Clone or locate this workspace directory.**
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment**:
   - On Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure API Keys**:
   Create a `.env` file in the root directory (or use the pre-created one) and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

---

## Running the Application

To run the application, execute:
```bash
python main.py
```

### Steps:
1. Run the script.
2. Enter your blog topic (e.g., `Future of AI Agents`).
3. The **Researcher Agent** will run a web search using DuckDuckGo to pull relevant insights.
4. The **Writer Agent** will compile the findings and use Groq Llama 3 to generate a structured, SEO-friendly markdown blog post.
5. The generated post will be printed directly in the terminal and saved as a markdown file (e.g., `future_of_ai_agents_blog.md`).
