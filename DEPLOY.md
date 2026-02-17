# Deploy to Render.com (Docker)

Deploy **backend** (FastAPI) and **frontend** (Next.js) on [Render](https://render.com) using Docker.  
**Manual creation of two Web Services is free** (no Blueprint needed).

---

## Free deploy: create two Web Services manually (no Blueprint)

Репозиторий уже на **GitHub** (или GitLab/Bitbucket). Подключите его к Render и создайте два сервиса отдельно — Blueprint не нужен.

### 1. Подключите репозиторий к Render

1. Зайдите на [dashboard.render.com](https://dashboard.render.com).
2. **Account Settings** → **Integrations** → подключите **GitHub** (или GitLab/Bitbucket).
3. Дайте доступ к репозиторию с проектом (например, **AICoach**).

### 2. Создайте бэкенд (первый сервис)

1. **New** → **Web Service**.
2. Выберите репозиторий (например, `GlebGorbat-dev/AICoach`).
3. Настройки:
   - **Name:** `fastapi-backend` (или любое имя)
   - **Region:** любой
   - **Branch:** `main`
   - **Root Directory:** оставьте **пустым**
   - **Runtime:** **Docker**
   - **Dockerfile Path:** `./Dockerfile`
   - **Instance Type:** **Free**
4. **Environment:** добавьте переменные бэкенда:
   - **`FASTAPI_CONFIG`** = `production` (обязательно для продакшена)
   - `MONGO_DB_URL`, `OPENAI_API_KEY`, `SECRET_KEY`, `VS_ID`, `TAVILY_API_KEY` и др. (как в вашем `.env`). `PORT` Render подставит сам.
5. **Create Web Service** → дождитесь первого деплоя и скопируйте URL сервиса (типа `https://fastapi-backend-xxxx.onrender.com`).

### 3. Создайте фронтенд (второй сервис)

1. Снова **New** → **Web Service**.
2. Выберите **тот же репозиторий**.
3. Настройки:
   - **Name:** `nextjs-frontend`
   - **Root Directory:** `frontend`
   - **Runtime:** **Docker**
   - **Dockerfile Path:** `frontend/Dockerfile`
   - **Instance Type:** **Free**
4. **Environment:** добавьте переменную:
   - **Key:** `NEXT_PUBLIC_API_URL`
   - **Value:** URL бэкенда из шага 2, например `https://fastapi-backend-xxxx.onrender.com`
5. **Create Web Service**.

Готово: оба сервиса на бесплатном плане. После пуша в `main` можно включить **Auto-Deploy** в настройках каждого сервиса.

---

## Deploy from a prebuilt Docker image (no Git)

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
| `render.yaml` | Optional: for Blueprint (paid); not needed for manual deploy. |
| `.dockerignore` (root) | Excludes frontend, `.venv`, etc. from backend build. |
| `frontend/.dockerignore` | Excludes `node_modules`, `.next` from frontend build. |

---

## Troubleshooting

- **Backend 503 / not starting:** Check that the app listens on `0.0.0.0` and uses the `PORT` env var (the root `Dockerfile` already does this).
- **Frontend can’t reach API:** Ensure `NEXT_PUBLIC_API_URL` is set to the **public** backend URL (e.g. `https://fastapi-backend.onrender.com`) and redeploy the frontend so the value is baked into the build.
- **CORS:** Backend already has `allow_origins=["*"]`; for production you can restrict to your frontend domain.
