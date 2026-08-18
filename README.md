# pyimgstega

一个命令行工具，用于生成**幻影坦克**（Mirage Tank）和**光棱坦克**（Prism Tank）风格的图片。

- **幻影坦克**：在白色背景下显示一张图，在黑色背景下显示另一张图（利用 Alpha 通道）。
- **光棱坦克**：在正常亮度下显示一张图，拉高亮度后显示另一张图（利用棋盘格交错）。

---

## 🚀 快速开始

### 安装依赖

```bash
pip install pillow numpy
```

### 基本用法

```bash
# 灰度幻影坦克（白底/黑底切换）
python main.py alpha -l light.png -d dark.png -m mirage -i 0.8

# 彩色幻影坦克
python main.py alpha -l light.png -d dark.png -m color -i 0.8

# 光棱坦克（棋盘格交错，拉高亮度显形）
python main.py prism -l A.png -d B.png -i 0.25
```

---

## 📁 命令详解

### `alpha` 子命令（幻影坦克）

| 参数 | 说明 |
| :--- | :--- |
| `--light, -l` | 亮图路径（白色背景下显示） |
| `--dark, -d` | 暗图路径（黑色背景下显示） |
| `--mode, -m` | `mirage`（灰度）或 `color`（彩色），默认 `mirage` |
| `--intensity, -i` | 透明度对比度拉伸系数，默认 `0.8`（推荐） |

### `prism` 子命令（光棱坦克）

| 参数 | 说明 |
| :--- | :--- |
| `--light, -l` | 表层图路径（正常亮度下显示） |
| `--dark, -d` | 隐藏图路径（拉高亮度后显示） |
| `--intensity, -i` | 隐藏图压暗系数，默认 `0.25`（越小藏得越深） |

---

## 📤 输出

所有图片保存在 `output/` 目录下，文件名带时间戳，不会覆盖。

- **幻影坦克**：输出 PNG（带 Alpha 通道），需要在支持透明背景的查看器中预览（如浏览器、微信、PS）。
- **光棱坦克**：输出普通 PNG（RGB），需要在支持亮度调节的查看器中拉高曝光度查看隐藏内容。

---

## 📁 项目结构

```
pyimgstega/
├── main.py          # 入口
├── src/
│   ├── __init__.py  # 包标识
│   ├── cli.py       # 命令行解析
│   ├── imgio.py     # 文件 I/O
│   └── tank.py      # 核心算法（mirage/color/prism）
├── output/          # 生成图片存放目录
└── README.md
```

---

## 🛠️ 开发备注

- Python >= 3.8
- 依赖：`Pillow`, `numpy`
- 提交规范：后半程采用 Conventional Commits

---

## 📜 License

MIT © OTOHARiRiSA