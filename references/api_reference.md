# Agnes AI API 参考

Agnes AI（母公司 Sapiens AI）提供 OpenAI 兼容的多模态 API，支持文生文、文生图、文生视频。

## 基础信息

- **Base URL**：`https://apihub.agnes-ai.com/v1`
- **认证**：所有请求头 `Authorization: Bearer <API_KEY>`
- **兼容性**：OpenAI 风格接口，迁移只需改 Base URL / API Key / 模型名

## 模型列表（GET /v1/models）

| 类型 | 模型 ID | 说明 |
|------|---------|------|
| 文本 | `agnes-2.0-flash` | 默认文本模型 |
| 文本 | `agnes-1.5-flash` | 轻量文本模型 |
| 图像 | `agnes-image-2.1-flash` | 最新文生图 |
| 图像 | `agnes-image-2.0-flash` | 文生图 |
| 视频 | `agnes-video-v2.0` | 文生视频（含图生视频） |

## 文生文 — POST /v1/chat/completions（同步）

标准 OpenAI chat 格式：

```json
{
  "model": "agnes-2.0-flash",
  "messages": [{"role": "user", "content": "你好"}],
  "temperature": 0.7,
  "max_tokens": 1024
}
```

返回 `choices[0].message.content`，并含 `usage.total_tokens`。

## 文生图 — POST /v1/images/generations（同步）

```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "一只金毛幼犬在阳光草地上玩耍",
  "n": 1,
  "size": "1024x1024"
}
```

返回 `data[0].url`（图片直链，域名 `platform-outputs.agnes-ai.space`）。尚未发现限频。

## 文生视频 — POST /v1/videos（异步任务）

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "一只金毛幼犬在草地上奔跑",
  "duration": 5
}
```

- 返回 `task_id`（与 `id`/`video_id` 同值），`status` 初为 `queued`/`in_progress`。
- **轮询** `GET /v1/videos/{task_id}`，直到 `status == "completed"`。
- 完成后的视频直链在 `metadata.url`（域名 `platform-outputs.agnes-ai.space`）。
- 输出分辨率自动映射（例如请求 1152x768 → 720p/4:3 的 1088x832）。
- **限频：视频生成 1 次/分钟**，超限返回 `429 {"code":"rate_limit_exceeded"}`。图像与文本未见限频。

## 错误码

- `429` 视频生成限频（1 次/分钟）
- `404 Invalid URL` 路径错误（如误用 `/v1/videos/generations`，正确为 `/v1/videos`）
- `401` API Key 无效
