vschartTOpez Generator
=============

[English](./README.md) | **简体中文** 

vivid/stasis -> pez 转谱
解析vsb, vsd并转化打包为phi自制格式

### 运行环境

- Python 3.8+

- 依赖安装：

```bash
pip install -r requirements.txt
```

- 开始前请准备好以下目录：

```
vschartTOpez/
├─ vsb_parser.py
├─ vsb2pez.py
├─ vsd_parser.py
├─ Charts/              # 原始.vsb谱面（原目录结构）
├─ song_information.bin # 曲目.vsd数据
├─ audiogroup_default/  # 音源，music_chart_*.ogg/wav
├─ Sprites/             # 曲绘，song_*_0.png（可选）
└─ black.png            # 曲绘背景图
```
*只有**一个音频**是wav格式：`Farewell to Syzygia.wav`，还得为此做兼容，我草*

### 使用步骤

1. 解析`song_information.bin`
   ```bash
   python vsd_parser.py
   ```
   生成同级 `song_information.json`


2. 批量解析.vsb
   ```
   python vsb_parser.py
   ```
   输出到 `vsbjson/` 并保持原目录结构


3. 生成 pez 2包  
   ```
   python vsb2pez.py
   ```
   在 `pezOutput/` 得到 `.pez` 文件。


### 注意事项

- 音频缺失时该pez不会被打包；
- 封面缺失时脚本会警告，但仍视为转谱成功，直接以 black.png 为曲绘。