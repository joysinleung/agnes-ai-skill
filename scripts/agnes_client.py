#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agnes AI API 客户端 (OpenAI 兼容接口)
Base URL: https://apihub.agnes-ai.com/v1

能力:
  - 文生图:  POST /v1/images/generations  (同步，返回图片 URL)
  - 文生视频: POST /v1/videos             (异步任务，需轮询 GET /v1/videos/{id})

用法:
  export AGNES_API_KEY="sk-xxx"
  python3 agnes_client.py text   "用一句话介绍 Agnes AI"            # 文生文
  python3 agnes_client.py image  "一只金毛幼犬在阳光草地上玩耍" -o out.png
  python3 agnes_client.py video  "一只金毛幼犬在阳光草地上奔跑" -o out.mp4 --duration 5
"""
import os
import sys
import time
import json
import urllib.request
import urllib.error

BASE_URL = "https://apihub.agnes-ai.com/v1"

MODELS = {
    "text": "agnes-2.0-flash",
    "image": "agnes-image-2.1-flash",
    "video": "agnes-video-v2.0",
}


def _api_key() -> str:
    key = os.environ.get("AGNES_API_KEY")
    if not key:
        raise SystemExit("缺少 API Key：请先 export AGNES_API_KEY=sk-xxx")
    return key


def _post(path: str, payload: dict) -> dict:
    url = BASE_URL + path
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {_api_key()}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get(path: str) -> dict:
    url = BASE_URL + path
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {_api_key()}")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _download(url: str, out_path: str):
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=120) as resp, open(out_path, "wb") as f:
        f.write(resp.read())


def generate_image(prompt: str, out_path: str, size: str = "1024x1024", model: str = None):
    model = model or MODELS["image"]
    resp = _post("/images/generations", {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
    })
    items = resp.get("data") or []
    if not items:
        raise SystemExit(f"图像生成返回为空: {resp}")
    url = items[0].get("url")
    if not url:
        raise SystemExit(f"图像生成未返回 URL: {resp}")
    _download(url, out_path)
    print(f"[image] 已完成 -> {out_path}  ({url})")
    return out_path


def generate_text(prompt: str, system: str = None, model: str = None,
                  temperature: float = 0.7, max_tokens: int = 1024):
    model = model or MODELS["text"]
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = _post("/chat/completions", {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    })
    choices = resp.get("choices") or []
    if not choices:
        raise SystemExit(f"文本生成返回为空: {resp}")
    content = (choices[0].get("message") or {}).get("content", "")
    usage = resp.get("usage") or {}
    print(content)
    print(f"\n[text] 模型={model} 消耗 tokens={usage.get('total_tokens')}")
    return content


def generate_video(prompt: str, out_path: str, duration: int = 5, model: str = None,
                   poll_interval: int = 10, max_wait: int = 600):
    model = model or MODELS["video"]
    resp = _post("/videos", {
        "model": model,
        "prompt": prompt,
        "duration": duration,
    })
    task_id = resp.get("task_id") or resp.get("id")
    if not task_id:
        raise SystemExit(f"视频任务创建失败: {resp}")
    print(f"[video] 任务已创建: {task_id}，开始轮询...")
    waited = 0
    while waited <= max_wait:
        status = _get(f"/videos/{task_id}")
        st = status.get("status")
        prog = status.get("progress")
        print(f"        状态={st} 进度={prog}")
        if st == "completed":
            url = (status.get("metadata") or {}).get("url")
            if not url:
                raise SystemExit(f"视频完成但未返回 URL: {status}")
            _download(url, out_path)
            print(f"[video] 已完成 -> {out_path}  ({url})")
            return out_path
        if st == "failed":
            raise SystemExit(f"视频任务失败: {status}")
        time.sleep(poll_interval)
        waited += poll_interval
    raise SystemExit("视频任务轮询超时")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit("参数不足")
    kind = sys.argv[1]
    prompt = sys.argv[2]
    out = "output"
    i = 3
    duration = 5
    system = None
    max_tokens = 1024
    while i < len(sys.argv):
        if sys.argv[i] in ("-o", "--output"):
            out = sys.argv[i + 1]; i += 2
        elif sys.argv[i] in ("-d", "--duration"):
            duration = int(sys.argv[i + 1]); i += 2
        elif sys.argv[i] in ("-s", "--system"):
            system = sys.argv[i + 1]; i += 2
        elif sys.argv[i] in ("-m", "--max-tokens"):
            max_tokens = int(sys.argv[i + 1]); i += 2
        else:
            i += 1
    if kind == "text":
        generate_text(prompt, system=system, max_tokens=max_tokens)
    elif kind == "image":
        generate_image(prompt, out)
    elif kind == "video":
        generate_video(prompt, out, duration=duration)
    else:
        raise SystemExit(f"未知类型: {kind} (text|image|video)")


if __name__ == "__main__":
    main()
