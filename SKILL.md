---
name: agnes-ai-free
slug: agnes-ai-free
displayName: "Agnes AI 多模态生成"
description: "Use this skill when the user wants to call Agnes AI (agnes-ai.com, Sapiens AI) for multimodal generation via its OpenAI-compatible API: text generation (文生文), image generation (文生图), and video generation (文生视频). Trigger on requests like 用 Agnes 生成文案/图片/视频, 调用 agnes 文生图, generate text/image/video with Agnes, or any task needing Agnes AI models. Free to use: users provide their own AGNES_API_KEY. See skillhub.json for category and details."
version: "1.1.2"
author: "joysinleung"
homepage: "https://github.com/joysinleung/agnes-ai-skill"
agent_created: true
---

# Agnes AI 多模态接入

## Overview

Agnes AI 提供 OpenAI 兼容的多模态 API（Base URL `https://apihub.agnes-ai.com/v1`），
统一支持三种生成能力：文生文、文生图、文生视频。本 skill 自带零依赖的 Python
客户端 `scripts/agnes_client.py`（仅用标准库 urllib，无需 pip 安装），把三种
能力封装为统一命令行入口。

**本版本为免费版**：用户自备 `AGNES_API_KEY`，免费安装、免费使用，不收取任何中间费用。

## 前置条件

- Python 3（系统自带即可，无需虚拟环境）。
- 需设置环境变量 `AGNES_API_KEY`（用户的 Agnes API Key）。**不要把 Key 写死进文件或提交到仓库。**
- 尚无 Key 的用户：前往 [platform.agnes-ai.com](https://platform.agnes-ai.com) 免费注册，在控制台 **API Keys** 页面创建（形如 `sk-xxx`）。

## 快速开始

```bash
export AGNES_API_KEY="sk-xxx"

# 文生文
python3 scripts/agnes_client.py text "用一句话介绍 Agnes AI" -m 200

# 文生图（同步，自动下载图片）
python3 scripts/agnes_client.py image "一只金毛幼犬在阳光草地上玩耍" -o out.png

# 文生视频（异步任务，自动轮询并下载 mp4）
python3 scripts/agnes_client.py video "一只金毛幼犬在草地上奔跑" -o out.mp4 --duration 5
```

## 三种能力说明

### 1. 文生文（text）
- 接口：`POST /v1/chat/completions`（标准 OpenAI 格式）
- 默认模型：`agnes-2.0-flash`（另可选 `agnes-1.5-flash`）
- 客户端选项：`-s/--system` 系统提示，`-m/--max-tokens` 上限
- 输出直接打印回复文本，并显示消耗 tokens

### 2. 文生图（image）
- 接口：`POST /v1/images/generations`（同步）
- 默认模型：`agnes-image-2.1-flash`（另可选 `agnes-image-2.0-flash`）
- 返回 `data[].url` 图片直链，客户端自动下载到 `-o` 指定路径
- 请求参数支持 `size`（如 `1024x1024`）、`n`

### 3. 文生视频（video）
- 接口：`POST /v1/videos`（**异步任务**，注意不要误用 `/v1/videos/generations`）
- 默认模型：`agnes-video-v2.0`
- 返回 `task_id` → 轮询 `GET /v1/videos/{task_id}` 直到 `status=="completed"` → `metadata.url` 视频直链，客户端自动下载
- **重要限频：视频生成 1 次/分钟**，超限返回 `429 {"code":"rate_limit_exceeded"}`；若需连续生成多段视频，每次间隔 ≥ 60 秒

## 完整 API 细节

详见 `references/api_reference.md`（模型列表、各接口请求/响应字段、错误码、分辨率自动映射规则）。

## 资源

- `scripts/agnes_client.py` — 零依赖命令行客户端，支持 `text`/`image`/`video` 三个子命令
- `references/api_reference.md` — 完整 API 参考（端点、模型、参数、限频、错误码）
- `skillhub.json` — SkillHub 上架元信息（分类、标签）
- `examples/demo.md` — 作品案例（AURORA 极光品牌全案）
