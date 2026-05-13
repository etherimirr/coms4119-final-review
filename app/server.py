#!/usr/bin/env python3
"""Combined static-file server + OpenAI proxy for the 4119 review app.

Usage:
    python3 server.py [port]

Defaults to port 8788. Serves the app/ directory.
POSTs to /api/ask are forwarded to OpenAI's Chat Completions API.

The OpenAI API key can be set either in the request body (apiKey field; the
frontend stores it in localStorage and sends it each time) or via the
OPENAI_API_KEY environment variable.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Quieter log so the OpenAI calls don't drown out static traffic.
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def do_POST(self):
        if self.path == "/api/ask":
            return self._handle_ask()
        self.send_error(404, "POST not allowed for that path")

    def _read_json_body(self):
        length = int(self.headers.get("content-length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_ask(self):
        try:
            body = self._read_json_body()
        except Exception as exc:
            return self._send_json({"error": f"bad JSON body: {exc}"}, 400)

        question = (body.get("question") or "").strip()
        context = body.get("context") or ""
        history = body.get("history") or []  # [{q, a}, ...] earlier same-page Q&A
        key = (body.get("apiKey") or os.environ.get("OPENAI_API_KEY") or "").strip()
        model = body.get("model") or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

        if not question:
            return self._send_json({"error": "empty question"}, 400)
        if not key:
            return self._send_json(
                {"error": "未设置 OpenAI API Key。点右下角『⚙️ 设置』粘贴 sk-... 后再试。"},
                400,
            )

        system_prompt = (
            "你是 Columbia COMS/CSEE 4119 Computer Networks 期末复习助教。"
            "面向考试帮学生答疑：中文回答，直击要点。"
            "概念题先一句话总结再展开；计算题给完整步骤+公式。"
            "公式用 KaTeX 语法写在 $...$ 或 $$...$$ 里。"
            "代码/表格用 markdown。回答控制在 250 字以内，除非问题确实需要长答。"
            "\n\n这是学生当前正在看的 slide 内容：\n"
            f"{context}"
        )

        messages = [{"role": "system", "content": system_prompt}]
        for turn in history[-6:]:  # cap context to last 6 turns
            if turn.get("q"):
                messages.append({"role": "user", "content": turn["q"]})
            if turn.get("a"):
                messages.append({"role": "assistant", "content": turn["a"]})
        messages.append({"role": "user", "content": question})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.3,
        }

        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.load(resp)
            answer = data["choices"][0]["message"]["content"]
            return self._send_json({"answer": answer, "model": model})
        except urllib.error.HTTPError as e:
            err_text = e.read().decode("utf-8", errors="replace")
            return self._send_json(
                {"error": f"OpenAI HTTP {e.code}: {err_text[:300]}"}, 502
            )
        except urllib.error.URLError as e:
            return self._send_json({"error": f"网络错误: {e.reason}"}, 502)
        except Exception as e:  # noqa: BLE001
            return self._send_json({"error": f"server error: {e}"}, 500)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8788
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"4119 server on http://localhost:{port}  (serving {here})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")


if __name__ == "__main__":
    main()
