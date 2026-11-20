# -*- coding: utf-8 -*-
"""
证件号生成器 · fnOS 版后端
仅使用 Python 标准库，无第三方依赖。
监听方式：优先 Unix socket（SOCKET_PATH，飞牛统一网关），否则 TCP（PORT）。
"""
import json
import os
import socket
import socketserver
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import idgen

BASE = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(BASE, "www")
if not os.path.isdir(WWW):
    WWW = os.path.join(os.path.dirname(BASE), "www")

PORT = 23180
for _k in ("PORT", "TRIM_SERVICE_PORT", "SERVICE_PORT"):
    if os.environ.get(_k):
        try:
            PORT = int(os.environ[_k])
            break
        except ValueError:
            pass
SOCKET_PATH = os.environ.get("SOCKET_PATH") or ""
PREFIX = (os.environ.get("GATEWAY_PREFIX") or "").rstrip("/")

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".ico": "image/x-icon",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
}

_DISTRICTS_CACHE = None


def districts_json():
    global _DISTRICTS_CACHE
    if _DISTRICTS_CACHE is None:
        _DISTRICTS_CACHE = json.dumps(
            {"provinces": idgen.districts_payload()},
            ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return _DISTRICTS_CACHE


class Handler(BaseHTTPRequestHandler):
    server_version = "ZJHSQL/1.0"

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()

    # ---------- 工具 ----------
    def _strip_prefix(self, path):
        path = urllib.parse.unquote(path.split("?", 1)[0])
        if PREFIX and path.startswith(PREFIX):
            path = path[len(PREFIX):] or "/"
        if not path.startswith("/"):
            path = "/" + path
        return path

    def _send(self, code, body, ctype, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   MIME[".json"])

    def _static(self, path):
        if path in ("/", ""):
            path = "/index.html"
        rel = path.lstrip("/")
        target = os.path.normpath(os.path.join(WWW, rel))
        if not target.startswith(os.path.normpath(WWW)) or not os.path.isfile(target):
            self._send(404, "Not Found".encode("utf-8"), "text/plain; charset=utf-8")
            return
        ext = os.path.splitext(target)[1].lower()
        with open(target, "rb") as f:
            body = f.read()
        self._send(200, body, MIME.get(ext, "application/octet-stream"))

    # ---------- 路由 ----------
    def do_GET(self):
        path = self._strip_prefix(self.path)
        if path == "/api/districts":
            self._send(200, districts_json(), MIME[".json"])
            return
        if path == "/api/health":
            self._json({"ok": True})
            return
        self._static(path)

    def do_POST(self):
        path = self._strip_prefix(self.path)
        if path != "/api/generate":
            self._json({"ok": False, "error": "not found"}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            self._json({"ok": False, "error": "请求体不是合法 JSON"}, 400)
            return

        kind = str(data.get("type") or "").strip()
        count = data.get("count", 1)
        codes, err = idgen.generate(kind, count=count,
                                    area=str(data.get("area") or ""),
                                    birthday=str(data.get("birthday") or ""),
                                    sex=str(data.get("sex") or "随机"))
        if err:
            self._json({"ok": False, "error": err}, 400)
            return
        self._json({"ok": True, "codes": codes})


class ThreadedTCP(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def make_unix_server(path):
    """兼容 Python 3.8~3.13：Unix 域套接字服务端按需动态构造。"""
    base = getattr(socketserver, "UnixStreamServer", None)
    if base is None:
        raise RuntimeError("当前平台的 socketserver 不支持 Unix 域套接字")

    class _UnixServer(socketserver.ThreadingMixIn, base):
        daemon_threads = True

        def get_request(self):
            request, _ = self.socket.accept()
            return request, ("unix", 0)

    return _UnixServer(path, Handler)


def main():
    if SOCKET_PATH:
        try:
            if os.path.exists(SOCKET_PATH):
                os.remove(SOCKET_PATH)
        except OSError:
            pass
        srv = make_unix_server(SOCKET_PATH)
        try:
            os.chmod(SOCKET_PATH, 0o666)
        except OSError:
            pass
        sys.stdout.write("listening on unix socket %s\n" % SOCKET_PATH)
    else:
        srv = ThreadedTCP(("0.0.0.0", PORT), Handler)
        sys.stdout.write("listening on 0.0.0.0:%d\n" % PORT)
    sys.stdout.flush()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
        if SOCKET_PATH and os.path.exists(SOCKET_PATH):
            try:
                os.remove(SOCKET_PATH)
            except OSError:
                pass


if __name__ == "__main__":
    main()
