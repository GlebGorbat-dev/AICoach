# Deploy to Render.com (Docker)

Deploy **backend** (FastAPI) and **frontend** (Next.js) on [Render](https://render.com) using Docker.  
You can use **GitHub**, **GitLab**, or **Bitbucket**.

---

## Deploy via GitHub (recommended)

### 1. Push code to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/FastApiFinal.git
git push -u origin main
```

(If the repo already exists on GitHub, just push your latest changes.)

### 2. Connect Render to GitHub

1. Go to [dashboard.render.com](https://dashboard.render.com).
2. **Account Settings** → **Integrations** → connect **GitHub** (if not already).
3. Authorize Render to access your repositories (you can allow all repos or only this one).

### 3. Create services from Blueprint

1. In Render Dashboard: **New** → **Blueprint**.
2. Select your **GitHub** account and choose the repo **FastApiFinal** (the one that contains `render.yaml`).
3. Render will read `render.yaml` and create two services:
   - **fastapi-backend** (Docker)
   - **nextjs-frontend** (Docker)

4. **Environment variables:**
   - **nextjs-frontend:** set `NEXT_PUBLIC_API_URL` = `https://fastapi-backend.onrender.com`  
     (use the actual backend URL from the backend service after the first deploy).
   - **fastapi-backend:** add your app variables (e.g. `MONGODB_URI`, `OPENAI_API_KEY`).

5. Click **Apply** — Render will build and deploy both services. Each push to `main` can trigger auto-deploy if enabled.

---

## Deploy via GitLab or Bitbucket

### 1. Push code to GitLab or Bitbucket

```bash
# GitLab
git remote add gitlab https://gitlab.com/YOUR_USERNAME/FastApiFinal.git
git push -u gitlab main

# Bitbucket
git remote add bitbucket https://bitbucket.org/YOUR_USERNAME/FastApiFinal.git
git push -u bitbucket main
```

### 2. Connect Render to GitLab or Bitbucket

1. [dashboard.render.com](https://dashboard.render.com) → **Account Settings** → **Integrations**.
2. Connect **GitLab** or **Bitbucket** and authorize access to your repos.

### 3. Create services from Blueprint

Same as GitHub: **New** → **Blueprint** → select your **GitLab** or **Bitbucket** repo. Render will use `render.yaml` and create both services. Set `NEXT_PUBLIC_API_URL` and backend env vars as above.

---

## Create services manually (without Blueprint)

### Backend

1. **New** → **Web Service**.
2. Connect your **GitHub** (or GitLab/Bitbucket) repo.
3. Settings:
   - **Name:** `fastapi-backend`
   - **Region:** your choice
   - **Branch:** `main` (or your default)
   - **Root Directory:** leave empty
   - **Runtime:** **Docker**
   - **Dockerfile Path:** `./Dockerfile`
   - **Instance Type:** Free or paid
4. Add env vars (e.g. `MONGODB_URI`, `OPENAI_API_KEY`). Render sets `PORT` automatically.
5. **Create Web Service**.

### Frontend

1. **New** → **Web Service**.
2. Same repo (GitHub / GitLab / Bitbucket).
3. Settings:
   - **Name:** `nextjs-frontend`
   - **Root Directory:** `frontend`
   - **Runtime:** **Docker**
   - **Dockerfile Path:** `frontend/Dockerfile`
   - **Instance Type:** Free or paid
4. **Environment:**
   - `NEXT_PUBLIC_API_URL` = `https://fastapi-backend.onrender.com` (your backend URL)
5. **Create Web Service**.

---

## 5. Deploy from a prebuilt Docker image (no Git)

If you prefer **not** to give Render access to Git at all:

1. Build and push images to a registry (Docker Hub, GitLab Container Registry, etc.):

   ```bash
   # Backend
   docker build -t YOUR_REGISTRY/fastapi-backend:latest .
   docker push YOUR_REGISTRY/fastapi-backend:latest

   # Frontend (from project root)
   docker build -t YOUR_REGISTRY/nextjs-frontend:latest -f frontend/Dockerfile frontend/
   docker push YOUR_REGISTRY/nextjs-frontend:latest
   ```

2. In Render: **New** → **Web Service** → **Deploy an existing image**.
3. **Image URL:** e.g. `registry.example.com/your-user/fastapi-backend:latest`.
4. Add **Registry credentials** in Render if the image is private.
5. Repeat for the frontend image.

---

## 6. After deploy

- **Backend:** `https://fastapi-backend.onrender.com` (or the URL Render shows).
- **Frontend:** `https://nextjs-frontend.onrender.com` (or the URL Render shows).

Set the frontend env var `NEXT_PUBLIC_API_URL` to the backend URL so the UI calls the correct API.  
On the free tier, services may spin down after inactivity; the first request can be slow.

---

## Files used for this setup

| File | Purpose |
|------|--------|
| `Dockerfile` (root) | Backend image; uses `PORT` from Render. |
| `frontend/Dockerfile` | Frontend (Next.js) image; uses `output: 'standalone'`. |
| `render.yaml` | Blueprint: defines both services for one-click setup. |
| `.dockerignore` (root) | Excludes frontend, `.venv`, etc. from backend build. |
| `frontend/.dockerignore` | Excludes `node_modules`, `.next` from frontend build. |

---

## Troubleshooting

- **Backend 503 / not starting:** Check that the app listens on `0.0.0.0` and uses the `PORT` env var (the root `Dockerfile` already does this).
- **Frontend can’t reach API:** Ensure `NEXT_PUBLIC_API_URL` is set to the **public** backend URL (e.g. `https://fastapi-backend.onrender.com`) and redeploy the frontend so the value is baked into the build.
- **CORS:** Backend already has `allow_origins=["*"]`; for production you can restrict to your frontend domain.
