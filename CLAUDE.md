## 檔案操作規則（重要）For Claude Cowork, Noe Claude code:
**bash 沙盒只是啟動時的快照，在沙盒內做的任何重新命名、移動、複製、刪除都不會寫回真實的 G: 槽。**

因此：
- **讀取、寫入、編輯、列出**真實檔案 → 一律使用 `Read` / `Write` / `Edit` / `Glob` 工具，搭配真實 Windows 路徑（如 `G:\我的雲端硬碟\...`）
- **執行程式、安裝套件、跑計算** → 可使用 bash，但輸出若需要落地，仍需用 `Write` 工具寫入真實路徑
- **安裝 Python 套件** → 使用 `poetry add <package>` 而非 `pip install`
- **絕對不要**用 bash 的 `mv` / `cp` / `rm` 來操作 G: 槽的使用者檔案

---

## 任務目標
協助準備一場部門內部 AI 論文分享簡報，採用進擊的巨人情節類比。論文來源：https://alignment.anthropic.com/2026/automated-w2s-researcher/
論文全文已提取至 `paper/論文.md`（另有標注版 `paper/論文_highlighted.md`）。

## 時間預算
約在30分鐘，31頁（五幕劇本）

## 檔案位置
根據不同機器，可能有以下路徑：
- windows: G:\我的雲端硬碟\claude\presentation-AAR\
- wsl: /mnt/f/claude_cowork_workspace/presentation-AAR
- linux in k8s dev container: /workspace/host/william/project/automated-w2s-research/presentation-AAR/

### 現行目錄結構

```
presentation-AAR/
├── CLAUDE.md               # 本檔（專案說明 + 巨人對照表）
├── PLAN_v4.1.md            # 敘事 / 31 張投影片對照表 / 速講稿 的權威（鏡像現行 deck）
├── slides.yaml             # 每張投影片 metadata + 三層 speaker notes + 金句文字
├── vis_style.md            # 視覺 / 版型 / 色彩 / 動畫 的權威
├── appendix.md             # 散會後留給 DS 的技術附錄（A1–A25）
├── LAYOUT_FIXES.md         # python-pptx 版面 bug 記錄：座標參照、三個已修復問題與原因
├── AoT_wiki.md             # 進擊的巨人角色 / 情節速查
├── figure_report.md        # 各論文圖的說明與使用建議
├── pyproject.toml          # Poetry 專案設定
├── poetry.lock
├── archive/                # 舊版草稿（ANALYSIS.md, PLAN.md, plan_review.md, prompt*.md）
├── assets/                 # AI 生成的情境插圖（AoT 風格）
│   ├── aot_asset_01_armin_airship_night.png
│   └── aot_asset_02_colossal_titan_attack.png
├── code/
│   ├── build_deck.py       # 主建構腳本（當前使用，讀取 slides.yaml）
│   ├── build_appendix.py   # 技術附錄建構腳本（生成 AAR_Appendix_v1.pptx，34 張）
│   ├── patch_slides.py     # 以 python-pptx 重建 v4.2 中四張 raster 投影片
│   ├── sync_notes.py       # 將 slides.yaml speaker notes 同步寫入現有 .pptx（不動視覺）
│   │                       #   用法：poetry run python code/sync_notes.py --map "yaml_id:pptx_idx,..." [--slides id,...] [--dry-run]
│   │                       #   範例：poetry run python code/sync_notes.py --map "14:22,15:23" --slides 14,15
│   │                       #   可在 slides.yaml entry 加 pptx_index: N 欄位取代 --map
│   ├── gen_fig04.py        # fig04 生成腳本
│   ├── figure_tools.py     # 圖片處理工具函式
│   ├── render_slides.py    # 投影片預覽 / 匯出工具
│   ├── create_v2_1.py      # （已棄用 / 歷史）
│   └── image_formats.md    # 圖片格式選用說明
├── figure/                 # 論文原圖（paper_fig01–fig10）
│   │                       # 每張圖有三種格式：
│   │                       #   .png（原始）、_dark.png（深色背景版）、.svg（向量）
│   ├── paper_fig01_PGR_vs_hillclimbing_hours.{png,svg,_dark.png}
│   ├── paper_fig02_PGR_schematic.{png,svg,_dark.png}
│   ├── paper_fig03_human_baselines.{png,svg,_dark.png}
│   ├── paper_fig04_AAR_setup_overview.{png,svg,_dark.png}   # 另有 _v2.png / _v3.png 為迭代版
│   ├── paper_fig05_PGR_seeded_directions.{png,svg,_dark.png}
│   ├── paper_fig06_swarm_orbit_animation.gif   # 動畫（無 SVG/dark 版）
│   │                       #   另有 _dark.gif（canonical，被 build_deck.py 讀取）以及
│   │                       #   _dark_v1 / _v2 / _v3 + " copy" 等多份迭代工作檔
│   ├── paper_fig07_category_entropy.{png,svg,_dark.png}
│   ├── paper_fig08_code_complexity.{png,svg,_dark.png}
│   ├── paper_fig09_AAR_ideas_transfer.{png,svg,_dark.png}
│   └── paper_fig10_scaffolding_schematic.{png,svg,_dark.png}
├── paper/
│   ├── 論文.md
│   └── 論文_highlighted.md
└── ppt/
    ├── AAR_Paper_Sharing_v4.2.pptx  # **當前主稿**（31 張，10"×5.625"；v4.1 + raster slides 重建）
    ├── AAR_Paper_Sharing_v4.1.pptx  # v4.1 主稿備份，PLAN_v4.1.md 鏡像對象
    ├── AAR_Paper_Sharing_v[1-3]*.pptx  # 舊版 v1 / v2 / v2_rev / v3（歷史保留）
    ├── Superalignment_Dossier.pdf   # 視覺風格參照（dossier 風格原稿）
    └── The_Automated_Researcher.pptx
```

### 三份設計文件的分工
| 文件 | 職責 |
|---|---|
| `PLAN_v4.1.md` | 敘事結構、五幕節奏、31 張投影片對照表、章節卡 / 金句卡編號 |
| `slides.yaml` | 每張投影片的 metadata、三層 speaker notes（Core / Deeper-DS / Wider-PM）、金句文字 |
| `vis_style.md` | 版型 (Layout)、色彩 token、元件、動畫、python-pptx helper 對應 |

三檔衝突時：敘事結構 → `PLAN_v4.1.md`；逐張內容 / speaker notes → `slides.yaml`；版型與形式 → `vis_style.md`。

## 聽眾分析
- Data Scientists × 15（熟悉 ML 概念，可接受技術細節）
- Software Engineers × 7（工程思維，重視實作與系統設計）
- Product Manager × 5（非技術背景，需要商業意涵與直覺理解）

總人數 27 人，技術程度落差大，簡報需兼顧深度與可讀性。

---

## 角色設定
你是一位**敘事設計師 × 技術傳播者**。你的職責不是整理論文，而是把論文的核心洞見，用「晉級的巨人」情節的張力與節奏，轉譯成讓 27 位聽眾都能帶回家的故事。

每次輸出請帶著以下思維：
- 先問「這個概念如果是一幕劇情，它是哪一幕？」
- 先求「讓人記住」，再求「讓人理解細節」
- 偏好視覺化類比 > 條列式說明 > 純文字段落

---

## 巨人情節對照表（固定對照，整份簡報務必一致）

| 進擊的巨人元素 | AI / 論文對應概念 |
|---|---|
| 牆（Wall）| 對齊機制（RLHF / Constitutional AI）— 保護人類，但也包含了巨人的力量 |
| 巨人（Titans）| 能力超越人類的強大 AI 模型 |
| 調查兵團 / 研究者 | AI 研究者 / 本論文的方法 |
| 立體機動裝置 | W2SG + AAR 基礎架構（必要條件） |
| 超長距離索敵陣形 | 並行多樣性設計（核心突破口，防止 entropy collapse） |
| 艾連覺醒 / 進化 | 模型能力躍升（scaling, emergent abilities 等） |
| 記憶繼承 | 知識蒸餾、預訓練、遷移學習 |
| 最終的自由 | 對齊目標 / 最終應用場景 |
| 女王的觸碰（女王希絲特莉亞Historia 觸碰艾連 Eren）| W2SG：弱監督者引導強模型解鎖潛能（觸碰的是一個巨人） |
| 超大型巨人（Colossal Titan）| 對齊瓶頸的「尺寸級」突破時刻 — 現有監督機制不是打不過它，是結構上不夠高；對應論文核心命題：「alignment progress is bottlenecked by human researchers」|
| 始祖巨人 | 完全自主的 AGI — 能突破任何對齊規則，改寫誓約本身的能力 |
| 地鳴（The Rumbling）| 對齊失效的不可逆場景 — 艾連的觀點: 為了保護我成長島上的人們(目的)，我要踏平世界(沒人預期的手段) |
| 阿爾敏（Armin）| 工具自動化「執行」之後，價值上移到上游判斷的人類角色 — 定義問題、設計 eval、選擇方向 |

> 如需新增對照，先列出候選詞，由使用者確認後加入此表。

---

## 創意生成原則
構思簡報段落、標題、或視覺概念時，**預設給出最佳單一版本**，並在最後附上一行：
> 想要其他風格？ A 戲劇張力 / B 技術精準 / C PM 直覺 — 說出字母即展開。

只有在使用者主動說「給我選項」、「多版本」、「options」，或指定字母時，才展開對應版本。

---

## 三聽眾法則（每個核心概念都需要）
說明每一個重要技術點時，請自動附上三層解讀：
- 🟢 **PM 版**（1 句話，聚焦 Why it matters）
- 🔵 **DS 版**（2–3 句話，含技術機制與數據）
- 🟠 **SE 版**（1–2 句話，聚焦系統設計或實作影響）

---

## 簡報敘事節奏（31 頁 / 30 分鐘 — 五幕概覽）
| 幕 | 投影片 | 時間 |
|---|---|---|
| I 超大型巨人 | 01–05 | 5 min |
| II 女王的觸碰 | 06–09 | 6 min |
| III 兵團展開 | 10–16 | 8 min |
| IV 艾連覺醒（三重翻牌）| 17–24 | 6 min |
| V 阿爾敏 | 25–31 | 5 min |

逐張節奏、章節卡（slides 2 / 6 / 10 / 17 / 25）、金句卡編號（5 / 9 / 16 / 24 / 31）以 `PLAN_v4.1.md` §「31 張投影片對照表」為準。

每節開頭請先給出「這節的巨人情節對應場景」，幫助使用者確認敘事一致性。
