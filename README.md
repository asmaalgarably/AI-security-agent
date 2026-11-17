# 🛡️ Autonomous AI & Cybersecurity Intelligence Agent

An automated, production-ready AI agent built with **LangGraph** and **Gemini 2.5 Flash** that fetches live cybersecurity news, AI breakthroughs, and 2026 NVD vulnerability records, analyzes them through enforced reasoning pipelines, translates the intelligence into technical Arabic, and delivers a styled HTML briefing via email every morning using **GitHub Actions**.

---

## 🏗️ Architectural Highlights

Unlike basic LLM wrappers, this system implements core **AI Engineering** and **AppSec** patterns to ensure reliability and security in production:

* **Indirect Prompt Injection Defense:** All external data ingested from RSS feeds (The Hacker News, Hacker News AI) and the NVD API is isolated inside strict `<untrusted_data>` XML boundaries, preventing malicious payloads from hijacking agent instructions.
* **Enforced Chain-of-Thought (CoT) via Pydantic:** Using structured outputs, the `chain_of_thought` field is positioned *before* the `severity` classification field in the schema—forcing the LLM to evaluate technical impact step-by-step prior to assigning a risk level.
* **Self-Consistency Verification:** Any vulnerability initially classified as `Critical` triggers a 3-pass majority-voting loop at elevated temperature (`0.7`) to eliminate false positives and LLM hallucinations.
* **Stack-Aware Contextualization:** Tailored to prioritize threats and updates relevant to **Python, Django, React, and TypeScript** ecosystems.
* **Zero-Cost Cloud Automation:** Scheduled via GitHub Actions (`cron: '0 6 * * *'`) using `uv` for ultra-fast deterministic dependency management.

---

## 📂 Project Structure

```text
├── .github/workflows/
│   └── daily_briefing.yml   # GitHub Actions CI/CD daily cron scheduler
├── agent.py                 # LangGraph ReAct agent, Pydantic schemas, CoT & Self-Consistency
├── tools.py                 # Custom LangChain tools (NVD CVE API, Security & AI RSS feeds)
├── main.py                  # Dual-mode entrypoint (CLI interactive mode & --auto email pipeline)
├── pyproject.toml           # Project metadata and dependencies
└── uv.lock                  # Deterministic dependency lockfile
```

---

## 🚀 Setup & Local Execution

### 1. Clone the repository
```bash
git clone [https://github.com/asmaalgarably/AI-security-agent.git](https://github.com/asmaalgarably/AI-security-agent.git)
cd AI-security-agent
```

### 2. Install dependencies using `uv`
```bash
uv sync
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY="your_gemini_api_key"
SENDER_EMAIL="your_email@gmail.com"
SENDER_APP_PASSWORD="your_16_char_app_password"
RECEIVER_EMAIL="recipient_email@gmail.com"
```

### 4. Run the Agent
* **Interactive Mode (Chat & Tool Selection):**
  ```bash
  uv run main.py
  ```
* **Autonomous Production Mode (Generate & Email Report):**
  ```bash
  uv run main.py --auto
  ```

---

## ☁️ Cloud Deployment (GitHub Actions)

To run the agent automatically every morning:
1. Navigate to your repository **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions**.
2. Add the four environment variables (`GOOGLE_API_KEY`, `SENDER_EMAIL`, `SENDER_APP_PASSWORD`, `RECEIVER_EMAIL`) as repository secrets.
3. Trigger a manual test via **Actions** $\rightarrow$ **Daily AI & Cybersecurity Briefing** $\rightarrow$ **Run workflow**.
