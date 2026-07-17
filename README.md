# Agnes AI 多模态生成 Skill（文 / 图 / 视频）

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

## 获取 Agnes API Key

本 Skill 完全免费，但需你自备自己的 Agnes API Key（Agnes 提供**免费**额度，注册即可使用，无需付费）。

1. 打开 Agnes 平台 👉 [platform.agnes-ai.com](https://platform.agnes-ai.com)
2. **注册 / 登录**账号（免费）
3. 进入控制台，找到 **API Keys（API 密钥）** 菜单
4. 点击 **Create Key / 创建密钥**，生成一条以 `sk-` 开头的密钥（形如 `sk-xxxx...`）
5. 复制该密钥，按下方「快速开始」设置为环境变量 `AGNES_API_KEY`

> ⚠️ **安全提示**：API Key 等同账号凭证，**不要**写进代码、提交到 Git 仓库或公开分享。仅通过环境变量注入（见下方第 1 步）。

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

## AI Agent 如何调用本 Skill

本 Skill 以 `SKILL.md` 为契约文件。Agent 加载本 Skill 后会自动读取其 `description`（触发条件 + 能力说明），在用户表达相关意图时自动启用——你**不需要**在对话里手动写「调用 agnes」。

### 标准调用流程（Agent 内部执行）

1. **确认凭证**：运行命令前，先确认环境变量 `AGNES_API_KEY` 已设置。未设置则提示用户配置，**不要**把 Key 写进文件或仓库。
2. **选择子命令**：按意图选 `text` / `image` / `video`。
3. **执行命令**：通过 Bash / execute_command 工具运行客户端：
   ```bash
   # 文生文
   python3 scripts/agnes_client.py text "用一句话介绍 Agnes AI"
   # 文生图（产物为本地图片文件）
   python3 scripts/agnes_client.py image "极光下的雪山，电影感，冷色调" -o aurora.png
   # 文生视频（8s，异步自动轮询并下载 mp4）
   python3 scripts/agnes_client.py video "极光在夜空中流动，缓慢运镜" -o aurora.mp4 -d 8
   ```
4. **返回结果**：文生图 / 文生视频的产物是本地文件，直接把**文件路径**回传给用户即可（可配合本 README 的示例作品展示效果）。

### 触发关键词（中 / 英）

- 中文：`用 Agnes 生成文案/图片/视频`、`调用 agnes 文生图`、`帮我生成一张…海报 / 一段…视频`
- 英文：`generate text/image/video with Agnes`、`use agnes-ai for image/video generation`

### 可直接粘贴给 Agent 的指令模板

> 当用户需要用 Agnes AI 生成文案 / 图片 / 视频时，调用本 Skill 的 `scripts/agnes_client.py`：先确认 `AGNES_API_KEY` 已设置，再按 `text` / `image` / `video` 子命令执行；文生图 / 视频产物为本地文件，返回其路径即可。视频生成限频 1 次/分钟，连续生成需间隔 ≥ 60 秒。

> ⚠️ **限频提醒**：文生视频 **1 次/分钟**，超限返回 `429`；如需连续生成多段视频，请间隔 ≥ 60 秒。

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
│   ├── demo.md              # 作品案例文案（AURORA 极光品牌全案）
│   ├── index.html           # AURORA 可交互作品集网页（浏览器打开）
│   ├── brand_copy.md        # 品牌文案（Slogan / 品牌故事 / 小红书）
│   ├── aurora_poster.png    # 主视觉海报
│   ├── aurora_product.png   # 产品概念图
│   └── aurora_film.mp4      # 电影感视频（8s）
└── assets/
    ├── cover.png                 # 展示封面（主视觉海报）
    ├── showcase-product.png      # 产品概念图
    ├── showcase-video.mp4        # 电影感视频（8s）
    └── showcase-video-poster.png # 视频封面（点击跳转播放）
```

---

## 示例作品

用本 Skill 一套命令产出的「AURORA 极光」品牌发布全案
（Slogan + 品牌故事 + 小红书文案 + 主视觉海报 + 产品概念图 + 8 秒电影感视频）。

<table>
  <tr>
    <td width="33%" align="center">
      <img src="https://raw.githubusercontent.com/joysinleung/agnes-ai-skill/main/assets/cover.png" alt="主视觉海报" width="100%"><br>
      <sub><b>主视觉海报</b> · 文生图</sub>
    </td>
    <td width="33%" align="center">
      <img src="https://raw.githubusercontent.com/joysinleung/agnes-ai-skill/main/assets/showcase-product.png" alt="产品概念图" width="100%"><br>
      <sub><b>产品概念图</b> · 文生图</sub>
    </td>
    <td width="33%" align="center">
      <a href="https://raw.githubusercontent.com/joysinleung/agnes-ai-skill/main/assets/showcase-video.mp4">
        <img src="https://raw.githubusercontent.com/joysinleung/agnes-ai-skill/main/assets/showcase-video-poster.png" alt="电影感视频（点击播放）" width="100%">
      </a><br>
      <sub><b>电影感视频</b> · 文生视频（8s，点击封面播放）</sub>
    </td>
  </tr>
</table>

> 完整全案（含文案、分镜脚本、8 秒电影感视频）见 [`examples/demo.md`](./examples/demo.md)。
> 可交互作品集网页：下载本仓库后浏览器打开 [`examples/index.html`](./examples/index.html)（含海报 / 产品图 / 视频联动展示）。

---

## 许可证

[MIT](./LICENSE) © joysinleung
