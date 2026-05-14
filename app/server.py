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
        if self.path == "/api/upload":
            return self._handle_upload()
        if self.path == "/api/save-cheatsheet":
            return self._handle_save_cheatsheet()
        if self.path == "/api/patch-cheatsheet":
            return self._handle_patch_cheatsheet()
        self.send_error(404, "POST not allowed for that path")

    def _handle_patch_cheatsheet(self):
        """Section-level patch.
        Body: {ops: [{op:"upsert", key:"...", html:"<section ...>...</section>", sheet_idx?:0},
                      {op:"delete", key:"..."}]}
        Reads cheatsheet.html, applies ops by data-key, writes back.
        Leaves all unmentioned sections untouched (so Claude's updates persist).
        """
        try:
            body = self._read_json_body()
        except Exception as exc:
            return self._send_json({"error": f"bad JSON: {exc}"}, 400)
        ops = body.get("ops") or []
        if not isinstance(ops, list):
            return self._send_json({"error": "ops must be array"}, 400)

        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "cheatsheet.html")
        try:
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
        except Exception as exc:
            return self._send_json({"error": f"read failed: {exc}"}, 500)

        import re
        applied = 0
        for op in ops:
            kind = op.get("op")
            key = op.get("key") or ""
            if not key:
                continue
            esc = re.escape(key)
            # match: <section ... data-key="KEY" ...>...</section>  (sections don't nest)
            pat = re.compile(
                r'<section\b[^>]*\bdata-key=["\']' + esc + r'["\'][^>]*>.*?</section>',
                re.DOTALL,
            )
            if kind == "upsert":
                new_html = op.get("html") or ""
                if not new_html.startswith("<section"):
                    continue
                if pat.search(html):
                    html = pat.sub(lambda m: new_html, html, count=1)
                else:
                    # not in file — append to the corresponding sheet's .cols
                    sheet_idx = int(op.get("sheet_idx") or 0)
                    sheets = list(re.finditer(r'<div\s+class="sheet"[^>]*>', html))
                    if not sheets:
                        continue
                    target = sheets[sheet_idx] if 0 <= sheet_idx < len(sheets) else sheets[-1]
                    # find this sheet's first `<div class="cols"`
                    after_sheet = html[target.end():]
                    cols_m = re.search(r'<div\s+class="cols"[^>]*>', after_sheet)
                    if not cols_m:
                        continue
                    # find next sheet boundary
                    next_sheet_m = re.search(r'<div\s+class="sheet"', after_sheet)
                    end_limit = next_sheet_m.start() if next_sheet_m else len(after_sheet)
                    # find matching </div> of cols by simple bracket tracking from cols start
                    # safer: insert before the closing tag of the cols block.
                    # heuristic: find last </section> within this sheet and insert after it
                    sheet_chunk = after_sheet[:end_limit]
                    last_sec_end = sheet_chunk.rfind("</section>")
                    if last_sec_end == -1:
                        continue
                    insert_pos = target.end() + last_sec_end + len("</section>")
                    html = html[:insert_pos] + "\n" + new_html + "\n" + html[insert_pos:]
                applied += 1
            elif kind == "delete":
                if pat.search(html):
                    html = pat.sub("", html, count=1)
                    applied += 1

        # rolling backup
        try:
            with open(path + ".bak", "w", encoding="utf-8") as f:
                pass  # touch
            with open(path, "r", encoding="utf-8") as src, open(path + ".bak", "w", encoding="utf-8") as dst:
                dst.write(src.read())
        except Exception:
            pass

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as exc:
            return self._send_json({"error": f"write failed: {exc}"}, 500)
        return self._send_json({"ok": True, "applied": applied})

    def _handle_save_cheatsheet(self):
        """Persist the browser's current cheatsheet body back to cheatsheet.html.
        Body: {html: "...", version: 5}
        We rewrite cheatsheet.html so future Claude edits flow on top of user edits.
        Keeps a rolling backup at cheatsheet.html.bak (last good version before write).
        """
        try:
            body = self._read_json_body()
        except Exception as exc:
            return self._send_json({"error": f"bad JSON: {exc}"}, 400)

        html = body.get("html") or ""
        if not html.strip():
            return self._send_json({"error": "empty html"}, 400)
        if len(html) > 4 * 1024 * 1024:
            return self._send_json({"error": "html too large (>4MB)"}, 413)

        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "cheatsheet.html")
        bak = path + ".bak"

        # rolling backup of previous file
        try:
            if os.path.exists(path):
                with open(path, "rb") as src, open(bak, "wb") as dst:
                    dst.write(src.read())
        except Exception:
            pass

        # bump version comment if present
        import re
        version = body.get("version")
        if version:
            try:
                version = int(version)
                if re.search(r"CHEATSHEET_VERSION:\s*\d+", html):
                    html = re.sub(r"CHEATSHEET_VERSION:\s*\d+",
                                  f"CHEATSHEET_VERSION: {version}", html, count=1)
                else:
                    html = f"<!-- CHEATSHEET_VERSION: {version} -->\n" + html
            except (TypeError, ValueError):
                pass

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as exc:
            return self._send_json({"error": f"write failed: {exc}"}, 500)
        return self._send_json({"ok": True, "bytes": len(html.encode("utf-8"))})

    def _handle_upload(self):
        """Accept JSON {dataUrl, filename?} and save the image to cheatsheet-assets/.
        Returns {path}.
        """
        try:
            body = self._read_json_body()
        except Exception as exc:
            return self._send_json({"error": f"bad JSON body: {exc}"}, 400)

        data_url = (body.get("dataUrl") or "").strip()
        if not data_url.startswith("data:"):
            return self._send_json({"error": "dataUrl must start with 'data:'"}, 400)
        header, _, b64 = data_url.partition(",")
        ext = "png"
        if "jpeg" in header or "jpg" in header:
            ext = "jpg"
        elif "gif" in header:
            ext = "gif"
        elif "webp" in header:
            ext = "webp"
        elif "svg" in header:
            ext = "svg"

        import base64
        import secrets
        import time

        try:
            data = base64.b64decode(b64, validate=True)
        except Exception as exc:
            return self._send_json({"error": f"bad base64: {exc}"}, 400)
        if len(data) > 8 * 1024 * 1024:
            return self._send_json({"error": "image too large (>8MB)"}, 413)

        ts = int(time.time() * 1000)
        suffix = secrets.token_hex(3)
        filename = f"cheat-{ts}-{suffix}.{ext}"
        here = os.path.dirname(os.path.abspath(__file__))
        out_dir = os.path.join(here, "cheatsheet-assets")
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, filename), "wb") as f:
            f.write(data)
        return self._send_json({"path": f"cheatsheet-assets/{filename}", "filename": filename, "size": len(data)})

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
