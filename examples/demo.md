# 示例作品：AURORA 极光 — 品牌发布全案

> 全部用 `agnes-ai` 本地客户端一键生成，证明「文案 + 配图 + 视频」一条工作流闭环。
> 对应 SkillHub 最热品类「内容创作」，也是该 Skill 最好的销售素材。

## 产出清单

| 类型 | 模型 | 命令 | 产物 |
|---|---|---|---|
| 文案 | agnes-2.0-flash | `text "...品牌创意总监..."` | 品牌 Slogan + 故事 + 15s 分镜 + 小红书文案 |
| 主视觉海报 | agnes-image-2.1-flash | `image "未来都市夜景极光..."` | `aurora_poster.png` (1024×1024) |
| 产品概念图 | agnes-image-2.1-flash | `image "悬浮发光球体..."` | `aurora_product.png` (1024×1024) |
| 电影感视频 | agnes-video-v2.0 | `video "未来都市推进镜头..." -d 8` | `aurora_film.mp4` (8s) |

完整作品集页面：`/Users/joysinleung/WorkBuddy/Claw/agnes-showcase/index.html`

## 文案节选（agnes-2.0-flash 生成）

- **Slogan**：Capture the light that moves with you. / 捕捉随你而动的光。
- **品牌故事**：AURORA 把极光般的能量收进一方轻巧设备，让未来科技以温柔的姿态，照亮日常每一刻。
- **小红书标题**：被这只「极光球」美到失语｜未来轻奢科技的第一眼心动

## 说明

- 视频端点限频 1 次/分钟，本次示例仅出 1 条；批量出片需排队。
- 手持人物特写类图像生成较慢，示例未采用，改用产品概念图与海报覆盖视觉需求。
- 想复现：把上面命令的 prompt 复制到 `scripts/agnes_client.py` 即可（需 `AGNES_API_KEY`）。
