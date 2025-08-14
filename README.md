
# translate-back (Render)

## Deploy (2 minutes)
1. Create a new repo and push these files (`server.py`, `requirements.txt`, `render.yaml`).
2. Go to https://render.com → New → Web Service → Connect this repo.
3. Confirm build command: `pip install -r requirements.txt`
4. Start command: `python server.py`
5. Add env vars (e.g., `OPENAI_API_KEY` if your code uses it).
6. After deploy, you will get: `https://<your-service>.onrender.com`

## Endpoints
- `GET /health` → `{"ok":true}`
- `POST /translate` → expects `{ "text": "...", "target": "en" }`
