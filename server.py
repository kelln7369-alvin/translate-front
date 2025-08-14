# server.py —— Flask 後端（OpenAI 代理）
# 需求：python3 -m pip install flask
# 金鑰：與 server.py 同資料夾放 .env，內容：OPENAI_API_KEY=sk-xxxx

import os, json, urllib.request
from flask import Flask, request

def load_env_from_file(path: str):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith("#"): 
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

# 讀取同資料夾 .env
load_env_from_file(os.path.join(os.path.dirname(__file__), ".env"))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("尚未提供 OPENAI_API_KEY，可在 .env 檔填入：OPENAI_API_KEY=sk-....")

app = Flask(__name__)

# 簡易 CORS
@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        # 這裡目前允許所有來源（*），方便測試。
# 小提醒：正式上線可將 CORS 限縮為你的前端網域，例如：
# resp.headers["Access-Control-Allow-Origin"] = "https://<YOUR-GITHUB-USER>.github.io"
    return resp

@app.route("/translate", methods=["POST", "OPTIONS"])
def translate():
    if request.method == "OPTIONS":
        return ("", 204)

    data   = request.get_json(force=True) or {}
    text   = data.get("text", "")
    target = data.get("target", "zh-TW")
    model  = data.get("model", "gpt-4o-mini")

    sys_prompt = (
        f"You are a professional translator. Detect the source language and "
        f"translate the user's text into {target} concisely. "
        f'Return JSON: {{"translation":"<text>"}} without explanations.'
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user",   "content": text}
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode("utf-8")
        obj = json.loads(raw)
        content = obj.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        return content, 200, {"Content-Type":"application/json"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5502))
    app.run(host="0.0.0.0", port=port)
