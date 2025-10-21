# Microsoft Graph SDK API

A FastAPI-based REST API for capturing Outlook emails and Teams chat messages using the Microsoft Graph API with Azure Active Directory authentication.

## Prerequisites

- Python 3.11 or higher
- Azure AD application with the following permissions:
  - `ChannelMessage.Read.All`
  - `Chat.Read.All`
  - `Mail.Read`
  - `Mail.ReadWrite`
  - `Team.ReadBasic.All`
  - `User.Read`
  - `User.Read.All`

Got it! Here's the revised version with the FastAPI server step clearly placed **before** moving to the next setup:

---

Got it! Here’s the updated setup guide **without the dashboard dependencies step**:

---

## 🧩 Setup Guide

### 1. Pre-requisite: Install **uv**

Before proceeding, make sure **uv** is installed.
Refer to the official installation guide: [uv Installation](https://docs.astral.sh/uv/getting-started/installation/)

---

### 2. Sync the Project with `uv`

```bash
cd dashboard
uv sync
```

> This ensures your environment and dependencies are ready.

---

### 3. Run the FastAPI Server

```bash
# From the project root
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

✅ Server URL: `http://localhost:8000`

> Make sure the server is running before moving to the next step.

---

### 4. Run the Dashboard

```bash
cd dashboard
uv run streamlit run streamlit_app.py
```

🎉 Dashboard URL: `http://localhost:8501`

---





