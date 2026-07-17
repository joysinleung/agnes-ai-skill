#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agnes AI 转售型 Pay Skill 后端原型（零依赖：仅 Python 标准库）

职责：
  1. 接收 Agent 的 POST /v1/generate {type, prompt, ...}
  2. 校验开发者签名 (HMAC-SHA256)  —— 占位 DEV_SECRET，上线替换为平台颁发密钥
  3. X402 预下单占位 —— 返回支付信息结构（真实微信支付链路见注释）
  4. 后端持 AGNES_API_KEY 调 Agnes API，回传生成结果

注：X402 / 微信支付部分为占位实现，企业认证并绑定微信商户号后替换为真实 SDK。
    生成逻辑（调 Agnes）是完整可用的。

运行：
  export AGNES_API_KEY="sk-xxx"
  export DEV_SECRET="平台颁发的开发者密钥"
  python3 server.py        # 监听 :8080
"""
import os
import sys
import json
import time
import hmac
import hashlib
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_URL = "https://apihub.agnes-ai.com/v1"
MODELS = {"text": "agnes-2.0-flash", "image": "agnes-image-2.1-flash", "video": "agnes-video-v2.0"}
DEV_SECRET = os.environ.get("DEV_SECRET", "CHANGE_ME_DEV_SECRET")
PRICE_CNY = float(os.environ.get("PRICE_CNY", "0.5"))  # 建议单价


def _api_key() -> str:
    k = os.environ.get("AGNES_API_KEY")
    if not k:
        raise RuntimeError("后端缺少 AGNES_API_KEY")
    return k


def _post(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE_URL + path, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {_api_key()}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(path: str) -> dict:
    req = urllib.request.Request(BASE_URL + path, method="GET")
    req.add_header("Authorization", f"Bearer {_api_key()}")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def verify_signature(body: bytes, sig: str) -> bool:
    """校验平台下发的开发者签名（HMAC-SHA256）。上线替换为平台约定算法。"""
    expect = hmac.new(DEV_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expect, (sig or ""))


def x402_presign(order_id: str) -> dict:
    """
    X402 预下单占位：返回支付信息结构。
    真实实现应调用微信支付 Agent Pay X402，生成可支付的 payment header。
    """
    return {
        "x402": {
            "version": "1.0",
            "amount": PRICE_CNY,
            "currency": "CNY",
            "merchantId": "REPLACE_WITH_WECHAT_MCH_ID",
            "orderId": order_id,
            "payUrl": "REPLACE_WITH_X402_PAY_ENDPOINT",
            "note": "占位实现；企业认证后接入真实微信支付 Agent Pay",
        }
    }


def generate(kind: str, payload: dict) -> dict:
    """调 Agnes API 生成（后端持 Key）。"""
    if kind == "text":
        resp = _post("/chat/completions", {
            "model": payload.get("model", MODELS["text"]),
            "messages": [{"role": "user", "content": payload["prompt"]}],
            "max_tokens": payload.get("max_tokens", 1024),
        })
        return {"text": (resp["choices"][0]["message"]["content"])}
    if kind == "image":
        resp = _post("/images/generations", {
            "model": payload.get("model", MODELS["image"]),
            "prompt": payload["prompt"], "n": 1,
            "size": payload.get("size", "1024x1024"),
        })
        return {"url": resp["data"][0]["url"]}
    if kind == "video":
        task = _post("/videos", {
            "model": payload.get("model", MODELS["video"]),
            "prompt": payload["prompt"],
            "duration": payload.get("duration", 5),
        })
        tid = task.get("task_id") or task.get("id")
        waited = 0
        while waited <= 600:
            st = _get(f"/videos/{tid}")
            if st.get("status") == "completed":
                return {"url": (st.get("metadata") or {}).get("url")}
            if st.get("status") == "failed":
                raise RuntimeError("video failed")
            time.sleep(10); waited += 10
        raise RuntimeError("video timeout")
    raise ValueError(f"unknown type: {kind}")


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, obj: dict):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/v1/generate":
            self._send(404, {"error": "not found"}); return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        sig = self.headers.get("X-Dev-Signature", "")
        if not verify_signature(raw, sig):
            self._send(401, {"error": "invalid signature"}); return
        try:
            req = json.loads(raw.decode("utf-8"))
            kind = req.get("type")
            if kind not in ("text", "image", "video"):
                self._send(400, {"error": "type must be text|image|video"}); return
            # 1) X402 预下单（占位）
            presign = x402_presign(f"ord_{int(time.time())}")
            # 2) 真实环境：此处等待 Agent Pay 支付完成后再执行下方生成
            result = generate(kind, req)
            self._send(200, {**result, "payment": presign})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"Agnes Pay Skill 后端原型 监听 :{port}  (DEV_SECRET={'set' if DEV_SECRET != 'CHANGE_ME_DEV_SECRET' else 'PLACEHOLDER'})")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
