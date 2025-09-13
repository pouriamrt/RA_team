# Research Assistant Team 🤖

A **multi-agent research assistant** built with [Agno](https://pypi.org/project/agno/) and powered by **OpenAI models**.  
This project coordinates a team of specialist AI agents—each with dedicated tools—to perform tasks such as web searches, website crawling, YouTube analysis, GitHub exploration, Hacker News monitoring, email drafting, and general Q&A synthesis.  

The agents collaborate under a **Team Coordinator** that delegates tasks, manages memory, and synthesizes results into clear, well-formatted answers.

--- 

## 🚀 Features

- **Specialist Agents**
  - 🌐 **InternetSearcher** – Web searches with DuckDuckGo  
  - 🕸 **WebCrawler** – Extracts and summarizes website content  
  - 📺 **YouTubeAnalyst** – Analyzes YouTube videos and captions  
  - 📧 **EmailAssistant** – Drafts and sends professional emails via Resend  
  - 💻 **GitHubResearcher** – Explores repositories, pull requests, and issues  
  - 📰 **HackerNewsMonitor** – Tracks trending Hacker News stories  
  - 🤝 **GeneralAssistant** – Synthesizes information and handles broad queries  

- **Team Coordinator**
  - Delegates tasks intelligently to relevant agents  
  - Synthesizes multi-agent outputs into a coherent final answer  
  - Maintains **session memory** for contextual follow-ups  
  - Handles retries with exponential backoff  

- **Streamlit UI**
  - Chat interface for interacting with the assistant  
  - Sidebar with debugging options (team memory & tool logs)  
  - Session reset for fresh conversations  

---

## 📂 Project Structure

```
.gitignore
.python-version
all_agents.py       # Defines specialist agents
create_team.py      # Builds the team of agents
main.py             # Streamlit app entry point
pyproject.toml      # Dependencies and project metadata
```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/my-agents-crew.git
cd my-agents-crew
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -e .
```

Dependencies include:
- [agno](https://pypi.org/project/agno/) – Multi-agent framework  
- [streamlit](https://streamlit.io) – Frontend for chat UI  
- [duckduckgo-search](https://pypi.org/project/duckduckgo-search/) – Web search  
- [crawl4ai](https://pypi.org/project/crawl4ai/) – Website crawling  
- [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) – Video transcript extraction  
- [resend](https://resend.com/) – Email sending  
- [PyGithub](https://pygithub.readthedocs.io/en/latest/) – GitHub API  
- [hackernews](https://pypi.org/project/hackernews/) – Hacker News API  
- [python-dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management  

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key
MODEL_NAME=gpt-4.1
RESEND_API_KEY=your_resend_key
EMAIL_FROM=your_email@example.com
EMAIL_TO=default_recipient@example.com
GITHUB_ACCESS_TOKEN=your_github_token
```

---

## ▶️ Usage

### Run the Streamlit App
```bash
streamlit run main.py
```

### Example Queries
- **Web Search:**  
  _“What are the latest AI breakthroughs?”_ → Uses InternetSearcher  
- **Crawl a Website:**  
  _“Crawl https://example.com and summarize the homepage.”_ → Uses WebCrawler  
- **YouTube Analysis:**  
  _“Summarize this video: https://youtu.be/dQw4w9WgXcQ”_ → Uses YouTubeAnalyst  
- **Send Email:**  
  _“Draft an email to bob@example.com about our project.”_ → Uses EmailAssistant  
- **GitHub Research:**  
  _“Find trending Python repositories this week.”_ → Uses GitHubResearcher  
- **Hacker News Trends:**  
  _“What’s trending on Hacker News today?”_ → Uses HackerNewsMonitor  
- **Memory Check:**  
  _“What was my first question to you?”_ → Tests memory persistence  

---

## 🧠 Memory & Debugging

- **Team Memory**: Agents remember past interactions during a session.  
- **Sidebar Controls**: Toggle memory view, enable tool logs, and reset the session.  

---

## 🛠 Development Notes

- Python version: **3.13** (see `.python-version`)  
- Use `pyproject.toml` for dependency management  
- Memory is **session-based** and resets when the Streamlit app restarts or via the sidebar button  

---

## 📜 License
MIT License – feel free to use, modify, and distribute.  
