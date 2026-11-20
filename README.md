# Saiful AI Agent

A clean FastAPI starter project with a responsive episode-request dashboard.

## Deploy on Render
1. Upload these files to the root of a new GitHub repository.
2. In Render, choose **New + → Blueprint** and select the repository (or create a Web Service).
3. If creating a Web Service manually:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Wait for the deploy, then open the service URL.

## Endpoints
- `GET /` dashboard
- `GET /health` health check
- `GET /api/jobs` list in-memory demo requests
- `POST /api/jobs` create a demo request
- `GET /api/jobs/{job_id}` read a request
- `POST /api/jobs/{job_id}/approve-upload` record demo approval

## Important
This is a working starter dashboard and API, not a connected video-generation or YouTube-upload product. Requests are held in memory and reset when the service restarts. To generate real videos, connect a video provider and a persistent job queue. To upload to YouTube, configure YouTube Data API OAuth and explicit user approval. Store secrets only in Render environment variables, never in GitHub source files.
