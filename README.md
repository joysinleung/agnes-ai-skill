# Agnes AI 多模态生成 Skill（文 / 图 / 视频）

<p align="center">
  <img src="./assets/cover.png" alt="Agnes AI 多模态生成 Skill — AURORA 极光品牌全案封面" width="100%">
</p>

<p align="center">
  <em>👆 本封面由本 Skill 一条命令生成（文生图，<code>agnes-image-2.1-flash</code>）——作品即说明书</em>
</p>

> 一条命令，调用 Agnes AI 生成**文案、图片、视频**。OpenAI 兼容接口，零依赖 Python 客户端，开箱即用。
> **完全免费**：自备 Agnes API Key 即可使用，无任何中间收费。
>
> 🔗 GitHub：[joysinleung/agnes-ai-skill](https://github.com/joysinleung/agnes-ai-skill)
> 🛒 SkillHub：搜索 `agnes-ai`（免费版，需自备 API Key）

---

## 这是什么

[Agnes AI](https://agnes-ai.com) 是 Sapiens AI 推出的多模态大模型平台，提供 OpenAI 兼容的 API，
统一支持**文生文、文生图、文生视频**三种能力。本 Skill 把它们封装成一个本地命令行客户端，
让 Agent（或你自己）用一句命令就能产出可交付的素材。

### 为什么值得用

- **三合一**：文案 + 配图 + 视频，一条工作流闭环，正好覆盖内容创作最热的品类。
- **零依赖**：客户端只用 Python 标准库 `urllib`，无需 `pip install`，任何装了 Python 3 的机器都能跑。
- **完全免费**：用户自备 Agnes API Key 即可，本 Skill 不收取任何中间费用。

---

## 支持的模型

| 能力 | 模型 | 接口 | 模式 |
|---|---|---|---|
| 文生文 | `agnes-2.0-flash`（可选 `agnes-1.5-flash`） | `POST /v1/chat/completions` | 同步 |
| 文生图 | `agnes-image-2.1-flash`（可选 `agnes-image-2.0-flash`） | `POST /v1/images/generations` | 同步 |
| 文生视频 | `agnes-video-v2.0` | `POST /v1/videos` | 异步轮询 |

> ⚠️ 视频生成限频 **1 次 / 分钟**，超限返回 `429`。连续生成多段视频需间隔 ≥ 60 秒。

---

## 快速开始（免费版）

```bash
# 1. 设置你的 Agnes API Key（不要写死进文件）
export AGNES_API_KEY="sk-xxx"

# 2. 文生文
python3 scripts/agnes_client.py text "用一句话介绍 Agnes AI，并说明它支持哪三种生成能力" -m 200

# 3. 文生图
python3 scripts/agnes_client.py image "一只金毛幼犬在阳光草地上玩耍，电影感，暖色调" -o puppy.png

# 4. 文生视频（8 秒，自动轮询并下载 mp4）
python3 scripts/agnes_client.py video "一只金毛幼犬在草地上奔跑，电影感，平稳运镜" -o puppy.mp4 -d 8
```

### 参数说明

| 子命令 | 参数 | 说明 |
|---|---|---|
| `text` | `-s/--system` | 系统提示词 |
| `text` | `-m/--max-tokens` | 最大输出 token（默认 1024） |
| `image` | `-o/--output` | 输出图片路径（默认 `output`） |
| `image` | 支持在 prompt 中以 `size:` 控制尺寸（见 `references/api_reference.md`） | |
| `video` | `-o/--output` | 输出视频路径 |
| `video` | `-d/--duration` | 视频时长秒数（默认 5，最大 8） |

---

## 目录结构

```
agnes-ai-skill/
├── SKILL.md                 # Skill 定义（核心，Agent 读取）
├── README.md                # 本文件
├── skillhub.json            # SkillHub 上架元信息（分类/标签）
├── LICENSE                  # MIT
├── .gitignore
├── scripts/
│   └── agnes_client.py      # 零依赖命令行客户端
├── references/
│   └── api_reference.md     # 完整 API 参考
├── examples/
│   └── demo.md              # 作品案例（AURORA 极光品牌全案）
└── assets/
    ├── cover.png            # 展示封面（主视觉海报）
    └── showcase-product.png # 产品概念图
```

---

## 示例作品

用本 Skill 一套命令产出的「AURORA 极光」品牌发布全案
（Slogan + 品牌故事 + 小红书文案 + 主视觉海报 + 产品概念图 + 8 秒电影感视频）。

<table>
  <tr>
    <td width="50%" align="center">
      <img src="./assets/cover.png" alt="主视觉海报" width="100%"><br>
      <sub><b>主视觉海报</b> · 文生图</sub>
    </td>
    <td width="50%" align="center">
      <img src="./assets/showcase-product.png" alt="产品概念图" width="100%"><br>
      <sub><b>产品概念图</b> · 文生图</sub>
    </td>
  </tr>
</table>

> 完整全案（含文案、分镜脚本、8 秒电影感视频）见 [`examples/demo.md`](./examples/demo.md)。

---

## 许可证

[MIT](./LICENSE) © joysinleung
