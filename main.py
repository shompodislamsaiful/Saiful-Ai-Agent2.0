from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Saiful AI Agent",
    version="1.0.0",
    description="Starter backend and dashboard for an AI video workflow.",
)

jobs: dict[str, dict[str, Any]] = {}


class JobRequest(BaseModel):
    episode_title: str = Field(min_length=1, max_length=160)
    prompt: str = Field(min_length=1, max_length=4000)
    aspect_ratio: str = Field(default="9:16", pattern=r"^(9:16|16:9|1:1)$")
    voice_language: str = Field(default="English", max_length=40)


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return HTMLResponse(DASHBOARD_HTML)


@app.get("/health")
def health():
    return {"ok": True, "service": "Saiful AI Agent", "mode": "starter-demo"}


@app.get("/api/jobs")
def list_jobs():
    return {"jobs": list(jobs.values())}


@app.post("/api/jobs", status_code=202)
def create_job(payload: JobRequest):
    job_id = str(uuid4())
    job = {
        "job_id": job_id,
        "episode_title": payload.episode_title,
        "prompt": payload.prompt,
        "aspect_ratio": payload.aspect_ratio,
        "voice_language": payload.voice_language,
        "status": "queued_demo",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "upload_approved": False,
        "message": (
            "Demo request saved. Connect an AI video provider to generate a real video."
        ),
    }
    jobs[job_id] = job
    return {
        "job_id": job_id,
        "status": job["status"],
        "message": job["message"],
    }


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.post("/api/jobs/{job_id}/approve-upload")
def approve_upload(job_id: str):
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job["upload_approved"] = True
    job["message"] = (
        "Approval recorded in demo mode. Connect YouTube Data API to upload videos."
    )
    return {
        "job_id": job_id,
        "upload_approved": True,
        "status": "approval_recorded_demo",
    }


DASHBOARD_HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#101827">
<title>Saiful AI Agent</title>
<style>
:root{color-scheme:dark;--bg:#0b1220;--panel:#121d30;--panel2:#17243a;--text:#eef4ff;--muted:#9aabc4;--accent:#8b7cff;--line:#293750;--good:#49d6a2}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 80% 0%,#26315a 0,transparent 32%),var(--bg);color:var(--text);font:15px/1.5 Inter,system-ui,Arial,sans-serif}
.wrap{max-width:1100px;margin:auto;padding:28px 18px 60px}.top{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:28px}
.brand{display:flex;align-items:center;gap:12px}.logo{width:44px;height:44px;border-radius:14px;background:linear-gradient(135deg,#a18bff,#5c7cff);display:grid;place-items:center;font-weight:900;color:white;font-size:20px}
h1{font-size:22px;margin:0}.sub{color:var(--muted);font-size:13px}.pill{border:1px solid #36506b;border-radius:999px;padding:7px 12px;color:#b8c9df;font-size:12px}
.hero{padding:28px;border:1px solid var(--line);border-radius:22px;background:linear-gradient(120deg,rgba(139,124,255,.16),rgba(73,214,162,.06)),var(--panel);margin-bottom:20px}
.hero h2{font-size:clamp(24px,5vw,36px);line-height:1.15;margin:0 0 10px}.hero p{color:var(--muted);max-width:650px;margin:0}
.grid{display:grid;grid-template-columns:1.2fr .8fr;gap:18px}.card{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:22px}.card h3{margin:0 0 16px;font-size:17px}
label{display:block;color:#c7d4e7;font-size:13px;margin:14px 0 6px}input,textarea,select{width:100%;background:#0c1627;border:1px solid #34445f;border-radius:10px;padding:12px;color:var(--text);font:inherit;outline:none}textarea{min-height:135px;resize:vertical}input:focus,textarea:focus,select:focus{border-color:var(--accent)}
button{border:0;border-radius:11px;padding:12px 16px;background:linear-gradient(135deg,#9a83ff,#647dff);color:white;font-weight:700;font-size:14px;cursor:pointer;margin-top:16px}button:disabled{opacity:.55;cursor:wait}.secondary{background:#263650;border:1px solid #3a4d6b}.notice{margin-top:14px;padding:12px;border-radius:10px;background:#0d192b;color:#b8c9df;border:1px solid var(--line);font-size:13px}
.stat{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--line);gap:12px}.stat:last-child{border:0}.muted{color:var(--muted)}.job{padding:14px 0;border-bottom:1px solid var(--line)}.job:last-child{border:0}.job strong{display:block;overflow-wrap:anywhere}.status{font-size:12px;color:#f5c978}.empty{color:var(--muted);font-size:13px;padding:10px 0}
footer{color:#8294ae;text-align:center;font-size:12px;margin-top:22px}
@media(max-width:760px){.grid{grid-template-columns:1fr}.top{align-items:flex-start}.hero{padding:22px}.card{padding:18px}}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="brand"><div class="logo">S</div><div><h1>Saiful AI Agent</h1><div class="sub">Creator workspace</div></div></div>
    <div class="pill" id="apiState">Checking API…</div>
  </header>
  <section class="hero">
    <h2>Your AI video workflow,<br>in one workspace.</h2>
    <p>Create episode requests, choose a video format and voice language, then review each request before any future upload integration.</p>
  </section>
  <main class="grid">
    <section class="card">
      <h3>Create an episode request</h3>
      <form id="jobForm">
        <label for="title">Episode title</label>
        <input id="title" maxlength="160" required placeholder="Example: The Mystery of the Old House">
        <label for="prompt">Story / video instructions</label>
        <textarea id="prompt" maxlength="4000" required placeholder="Describe the episode, scenes, tone, and what the video should cover…"></textarea>
        <label for="ratio">Video aspect ratio</label>
        <select id="ratio"><option>9:16</option><option>16:9</option><option>1:1</option></select>
        <label for="voice">Voice language</label>
        <select id="voice"><option>English</option><option>Bangla</option><option>Hindi</option><option>Spanish</option></select>
        <button id="submitBtn" type="submit">Create request</button>
      </form>
      <div class="notice" id="message">Demo mode: requests are saved in this server's temporary memory. Real AI video generation is not connected yet.</div>
    </section>
    <aside class="card">
      <h3>Workspace status</h3>
      <div class="stat"><span class="muted">Backend</span><strong id="backendStatus">Checking…</strong></div>
      <div class="stat"><span class="muted">Video generation</span><strong>Not connected</strong></div>
      <div class="stat"><span class="muted">YouTube upload</span><strong>Approval demo</strong></div>
      <div class="notice">Your requests will not publish anything. YouTube upload requires a separate authorized API connection and your approval.</div>
    </aside>
  </main>
  <section class="card" style="margin-top:18px">
    <h3>Recent episode requests</h3>
    <div id="jobs"><div class="empty">No requests yet.</div></div>
  </section>
  <footer>Saiful AI Agent · Starter build · Securely add provider credentials through environment variables, never in source code.</footer>
</div>
<script>
const apiState=document.getElementById('apiState');
const backendStatus=document.getElementById('backendStatus');
const jobsEl=document.getElementById('jobs');
const message=document.getElementById('message');
async function checkHealth(){
  try{const r=await fetch('/health');if(!r.ok)throw new Error();const d=await r.json();apiState.textContent='API online';backendStatus.textContent='Online';}
  catch(e){apiState.textContent='API unavailable';backendStatus.textContent='Unavailable';}
}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
async function loadJobs(){
  try{const r=await fetch('/api/jobs');const d=await r.json();if(!d.jobs.length){jobsEl.innerHTML='<div class="empty">No requests yet.</div>';return;}
  jobsEl.innerHTML=d.jobs.slice().reverse().map(j=>`<div class="job"><strong>${esc(j.episode_title)}</strong><span class="status">${esc(j.status)} · ${esc(j.aspect_ratio)} · ${esc(j.voice_language)}</span><div class="muted">${esc(j.message)}</div>${j.upload_approved?'<div class="status">Approval recorded</div>':`<button class="secondary" onclick="approve('${esc(j.job_id)}')">Record upload approval</button>`}</div>`).join('');
  }catch(e){jobsEl.innerHTML='<div class="empty">Could not load requests.</div>';}
}
async function approve(id){
  try{const r=await fetch(`/api/jobs/${id}/approve-upload`,{method:'POST'});const d=await r.json();message.textContent=d.message||'Approval recorded in demo mode.';loadJobs();}
  catch(e){message.textContent='Could not record approval.';}
}
document.getElementById('jobForm').addEventListener('submit',async e=>{
  e.preventDefault();const btn=document.getElementById('submitBtn');btn.disabled=true;btn.textContent='Saving…';
  const payload={episode_title:document.getElementById('title').value.trim(),prompt:document.getElementById('prompt').value.trim(),aspect_ratio:document.getElementById('ratio').value,voice_language:document.getElementById('voice').value};
  try{const r=await fetch('/api/jobs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Request failed');message.textContent=d.message;document.getElementById('jobForm').reset();loadJobs();}
  catch(err){message.textContent='Could not save request: '+err.message;}
  finally{btn.disabled=false;btn.textContent='Create request';}
});
checkHealth();loadJobs();
</script>
</body>
</html>
"""
