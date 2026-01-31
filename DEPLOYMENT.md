# Deployment Guide for Cyber Resilience Assessment App

To share this application with clients or run it publicly, you need to host it.
Here is a recommended guide for deploying this React (Frontend) + FastAPI (Backend) application.

## 1. Prerequisites
- A GitHub account (to push your code).
- Accounts on hosting platforms (recommended: **Vercel** for frontend, **Render** for backend).

## 2. Backend Deployment (Render.com)
The backend manages the logic and the database (ChromaDB).

1.  **Push code to GitHub**: ensure `backend/` and `frontend/` folders are in your repo.
2.  **Create New Web Service on Render**:
    -   Connect your GitHub repo.
    -   **Root Directory**: `backend`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `python main.py` OR `uvicorn main:app --host 0.0.0.0 --port $PORT`
3.  **Environment Variables**:
    -   Add any API keys if used.
4.  **Persistent Storage (Important)**:
    -   Since the app uses ChromaDB (a file-based DB), you MUST add a **Disk** on Render mounted to `/backend/data` (or wherever the DB saves).
    -   Without a distinct disk, your data will disappear every time the server restarts.

## 3. Frontend Deployment (Vercel)
The frontend is the visual interface.

1.  **Import Project in Vercel**:
    -   Connect your GitHub repo.
    -   **Root Directory**: `frontend` (Edit the settings to point here).
    -   **Framework Preset**: Vite
    -   **Build Command**: `npm run build`
    -   **Output Directory**: `dist`
2.  **Configure Environment**:
    -   You need to tell the frontend where the Backend lives.
    -   In `frontend/src/App.jsx` and other files, the URL `http://localhost:8000` is hardcoded.
    -   **CHANGE THIS**: Update the fetch URLs to use your new Render Backend URL (e.g., `https://my-api.onrender.com`).
    -   *Better approach*: Use `import.meta.env.VITE_API_URL` and set that variable in Vercel.

## 4. Final Verification
-   Open your Vercel URL (e.g., `https://cyber-assessment.vercel.app`).
-   Test the flow.
-   Ensure "Review & Submit" allows you to generate the Scorecard.

## "Do we have to host it?"
Yes. Currently, it runs on "localhost" which means *only you* can see it on this specific computer. Hosting puts it on the internet so you can send a link to a client like `assessment.sbainfosolutions.com`.
