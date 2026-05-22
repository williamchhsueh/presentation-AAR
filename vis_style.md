# AAR 簡報視覺風格導引 `vis_style.md`

> **參照原稿**：`ppt/Superalignment_Dossier.pdf`（14 頁，NotebookLM dossier 風格）  
> **敘事權威**：`PLAN_v2.md`（21 張投影片、五幕劇本）  
> **本檔目的**：把 dossier 的視覺語言抽象成 token + 元件 + 版型，並逐頁套用到 PLAN_v2 的 21 張，讓任何 coding agent（python-pptx、HTML→PNG、Reveal.js、Keynote 手刻皆可）都能產生風格一致的成品。  
> **本檔規範**：中文敘事為主；色碼、token 名、font-family、zone 名、layout 名一律英文，**請勿翻譯**。

---

## 1. 給 Coding Agent 的使用方式（README）

1. **先讀 §3–§10**（token / typography / 元件 / 版型）建立心智模型
2. **再讀 §11** 拿到每一頁的具體配方（layout、zone、text、accent、image、wall stage、footer）
3. **§13** 提供 python-pptx 既有 helper 的對應提示，可直接擴充 `create_v2_1.py`
4. 若同一概念在 §3–§10 與 §11 衝突，**以 §11 為準**（per-slide override 永遠勝出）
5. 任何視覺決策若 §3–§11 都沒寫，**先回去看 PDF 對應頁的截圖**（已渲染在 `/tmp/dossier_pages/page_*.png`，或重新自 PDF 渲染），不要自由發揮

## 2. 五條設計理念

| # | 原則 | 一句話解釋 |
|---|---|---|
| 1 | **Cinematic（電影感）** | 深色近黑底 + 高對比 + 留白 + 偶發的霓虹色，像諜報電影分鏡而非企業簡報 |
| 2 | **Evidence-first** | 圖表先於文字、數字先於形容詞、原文引用先於講者改寫；caption 不超過兩行 |
| 3 | **Role-coded（角色色碼）** | 三聽眾 `[PM] [DS] [SWE]` 永遠用同三個徽章色，跨頁可一眼定位「這段給誰看」 |
| 4 | **Restrained motion** | 只用淡入；禁飛入、彈跳、3D 翻轉；金句卡只有「淡入 → 停留 → 切換」三拍 |
| 5 | **留白即沉默** | 金句卡四周 ≥1.5" 呼吸空間；hero 頁標題周圍只有遮罩，不堆元件 |

## 3. Canvas & Grid

- **長寬比**：16:9（PDF 原稿為 1376 × 768 pt）
- **建議實尺寸**：
  - 新建 deck → `13.333" × 7.5"`（PowerPoint 預設 widescreen）
  - 既有 deck（`AAR_Paper_Sharing_v2.1.pptx` 為 `10" × 5.625"`）→ 保留不變，所有 % 規格通用
- **安全邊距（safe area）**：上下各 4%、左右各 4%
- **標題基線**：H1 baseline 約落在 page top 9–10%
- **6 欄柵格**：左右各 4% 邊距內，等分 6 欄、欄間隙 1.5%
  - `col-1..6` 寬度 ≈ 14.0%
  - 雙欄佈局：col-1~3 / col-4~6
  - 三欄佈局：col-1~2 / col-3~4 / col-5~6
  - 2×2 卡片：列高 ≈ 38%、列間隙 3%
- **右下角預留 6×8% 給 collapsing wall**（金句卡與 hero 頁例外，§8 規定）

## 4. Color Tokens

> 全簡報只用以下 token；禁止寫死的 `#xxxxxx` 出現在元件之外。  
> 命名規則：`bg-*` 背景、`panel-*` 面板、`text-*` 文字、`accent-*` 色彩 highlight、`stroke-*` 線、`accent-role-*` 角色徽章

### 4.1 背景與面板

| Token | Hex | 用途 |
|---|---|---|
| `bg-base` | `#081010` | 標準頁背景（深近黑、微帶青綠調） |
| `bg-dossier` | `#000810` | 「CLASSIFIED BRIEFING」頁背景，更偏靛 |
| `bg-pure` | `#0A0A0A` | 金句卡背景（最深、避免純 #000 過刺眼） |
| `panel` | `#101818` | 卡片底色 |
| `panel-2` | `#181820` | 巢狀 / 第二層卡片底色 |
| `panel-bad` | `#1A0E10` | 紅色警示卡內部底色（極深酒紅） |
| `panel-good` | `#0E1A12` | 綠色 OK 卡內部底色（極深苔綠） |

### 4.2 線條與描邊

| Token | Hex | 用途 |
|---|---|---|
| `stroke` | `#283038` | 卡片標準邊框（1 pt） |
| `stroke-hud` | `#3A4A55` | HUD 角標 / tick mark / dossier frame 線 |
| `divider` | `#202830` | 區段水平分隔線 |

### 4.3 文字

| Token | Hex | 用途 |
|---|---|---|
| `text-primary` | `#F8F8F8` | 標題與主文（白略偏暖） |
| `text-secondary` | `#B8C0C4` | 副文、卡內說明 |
| `text-muted` | `#7A8488` | footer、頁碼、CLASSIFIED 條 |
| `text-on-accent` | `#081010` | 落在綠/紅/琥珀徽章上時的字色（與 `bg-base` 同） |

### 4.4 強調色（accent）

| Token | Hex | 語意 | 主要用途 |
|---|---|---|---|
| `accent-good` | `#7CE38B` | 正向 / 成功 | PGR 0.97、Outcome-Gradable 標題條、PACE dot |
| `accent-good-glow` | `#A0F0B0` | 高亮版 | 大數字內字色、需要 pop 的關鍵字 |
| `accent-warn` | `#F0A030` | 警告 / 注意 | 「THE GAP」、attention badge、過渡警示 |
| `accent-bad` | `#C73838` | 警示 / 失敗 | Code 0.47、hack 卡頂條、Non-Outcome-Gradable |
| `accent-bad-dim` | `#601818` | 警示底 | 紅卡標題色帶的底色（避免 saturate 過亮） |
| `accent-data-blue` | `#3060A0` | 圖表中性 | 圖表第二色 / human baseline 顏色 |

### 4.5 角色徽章色

| Token | Hex | 用途 |
|---|---|---|
| `accent-role-pm` | `#7CE38B` | `[PM]` 徽章（重用 good 綠） |
| `accent-role-ds` | `#E36AAE` | `[DS]` 徽章（粉紫） |
| `accent-role-swe` | `#B89AE6` | `[SWE]` 徽章（淡紫） |
| `accent-role-note` | `#F0A030` | `[NOTE]` 旁註 |
| `accent-role-ref` | `#9AB6E6` | `[REF]` 引用 |

### 4.6 使用規則

1. **Dark-only**：本 deck 不使用淺色頁；任何卡片或元件預設都假設背景是 `bg-base` 系列
2. **一頁最多 2 個 accent**：除「翻牌頁」與「角色色帶頁」外，正向綠 + 警示紅 不應同時大面積出現
3. **數字優先 glow**：mega number 預設 `text-primary`；只有「需要被遠端視覺優先看到」的數字才換成 `accent-good-glow` 或 `accent-bad`
4. **不發明色**：若 §4.1–4.5 找不到對應，先用最接近的 token，再回 §13 提需求

## 5. Typography

### 5.1 字型家族

| 用途 | 主字型 | Fallback chain |
|---|---|---|
| Latin | **Inter** | Source Sans 3, Helvetica Neue, Helvetica, Arial |
| CJK 繁中 | **Noto Sans CJK TC** | PingFang TC, Microsoft JhengHei, sans-serif |
| Mono（公式 / 徽章 / 代碼） | **JetBrains Mono** | IBM Plex Mono, Consolas, monospace |

- 全簡報只用 **1 個 Latin family + 1 個 CJK family + 1 個 mono**
- 不混 serif；不用裝飾字（手寫體、Display 字）
- 字重只用三檔：Regular 400 / SemiBold 600 / Bold 700

### 5.2 Type scale（@ 13.333" × 7.5"；其他尺寸按比例縮放）

| 名稱 | 大小 | 字重 | 用途 |
|---|---|---|---|
| `t-mega` | 96 pt | Bold | 第一翻 0.23 vs 0.97 的巨數字 |
| `t-mega-sm` | 72 pt | Bold | 三翻證據頁的 0.97 / 0.94 / 0.47 |
| `t-quote` | 48 pt | SemiBold | 金句卡（行高 1.3，置中） |
| `t-h1` | 36 pt | SemiBold | 頁面標題；sentence case；**句尾加句號**`.` |
| `t-h2` | 22 pt | SemiBold | 卡片標題 |
| `t-body` | 14 pt | Regular | 卡片內文 |
| `t-body-sm` | 12 pt | Regular | 圖表 caption、底部 takeaway 行 |
| `t-caption` | 10 pt | Regular | footer、頁碼 |
| `t-mono-badge` | 11 pt | SemiBold mono | `[PM]/[DS]/[SWE]` 徽章內字 |
| `t-mono-strip` | 9 pt | Regular mono, letter-spacing 0.06em, ALL CAPS | dossier frame 條文字 |

### 5.3 標題寫作規則

- **Sentence case**：只首字母大寫，不全大寫；專有名詞除外（W2SG、AAR）
- **句尾加句號**：H1 必加，H2 可省；模仿 PDF 標題的「斷言式」語感
- **不超過兩行**：H1 ≤ 2 行；超過 2 行 → 拆成 H1 + 引言副字
- **動詞優先**：「Deploying a parallel formation」優於「The parallel formation」
- **中文 H1**：若用中文，句尾用全形句號`。`

## 6. 元件（Components）

> 元件 ID 採 `c-*` 前綴。每個元件 = (錨點 / 尺寸規則 / 顏色 token / 子元素)

### 6.1 `c-card`（標準卡片）

```
┌──────────────────────────┐  ← top stripe 4–5 pt 高，色 = accent-*
│ ⌐ H2 標題          ¬     │  ← tick 角標（stroke-hud, L-shape, 6 pt）
│                          │
│ Body 段落（t-body）       │
│ • bullet（• 點 = accent） │
│ └ Sub note               │
│ ⌐                  ¬     │
└──────────────────────────┘
```

- 圓角：6 pt
- 邊框：1 pt `stroke`
- 底色：`panel`（標準）/ `panel-good` / `panel-bad`
- 內距：左右 18 pt、上下 14 pt
- 標題列：頂部全寬 4–5 pt 高色條（`accent-good` / `accent-bad` / `accent-warn` / `accent-role-*`）
- 角落 tick：四角各畫 6 pt 長 L 形 `stroke-hud` 細線（電影 HUD 感）
- 預設陰影：**無**（dark deck 上的 drop shadow 會泥）

### 6.2 `c-badge-role`（角色徽章）

```
[ PM ]  ← rounded pill, height ≈ 14 pt
```

- 形狀：圓角矩形，半徑 ≈ 半高（藥丸）
- 高度 14 pt，內距左右 8 pt
- 文字：`t-mono-badge`，字色 `text-on-accent`，底色 `accent-role-*`
- 變體：`[PM]` `[DS]` `[SWE]` `[NOTE]` `[REF]`
- 擺放：永遠出現在所屬段落的**前綴**或 H2 標題右側

### 6.3 `c-status-dot`（狀態點）

```
● PACE       ● BANDWIDTH       ● THE GAP
綠            紅                 琥珀
```

- 直徑 8 pt 的圓點
- 右側貼 8 pt label：`t-body-sm` ALL CAPS letter-spacing 0.08em
- 三色組合：`accent-good` / `accent-bad` / `accent-warn`
- 用於「狀態列」場景：超大型巨人頁、Threat/Solution 對比、儀表板

### 6.4 `c-dossier-frame`（諜報檔案邊框）

```
┌── CLASSIFIED BRIEFING // OPERATION : SCALABLE OVERSIGHT ─── STATUS: CRITICAL // RISK ASSESSMENT: HIGH ──┐
│                                                                                                         │
│                                  ── 主內容區 ──                                                          │
│                                                                                                         │
└── CLASSIFIED BRIEFING // OPERATION : SCALABLE OVERSIGHT ──── STATUS: CLASSIFIED // RISK ASSESSMENT: UNKNOWN ─┘
```

- 頂部 / 底部各一條 18 pt 高的細條，左右切齊頁面安全邊距
- 條的線色 `stroke-hud`，內字 `t-mono-strip`，字色 `text-muted`
- 條兩端文字（左/右）：
  - 上條左：`CLASSIFIED BRIEFING // OPERATION : <章節代號>`
  - 上條右：`STATUS: <CRITICAL | NOMINAL> // RISK ASSESSMENT: <HIGH | MEDIUM | LOW | UNKNOWN>`
  - 下條左：與上條左相同
  - 下條右：`STATUS: CLASSIFIED // RISK ASSESSMENT: UNKNOWN`（固定）
- 主內容區內縮 4%（對齊條的內邊）
- 適用版型：`L-DOSSIER`

### 6.5 `c-footer`（頁腳）

- 左下小字（`t-caption`, `text-muted`，可選）：  
  `Automated Alignment Researcher (AAR) · Anthropic Research 2026`
- 右下小字（`t-caption`, `text-muted`）：頁碼 `04 / 21`
- 金句卡（Slide 04/08/12/16/21）與 Slide 01（冷開場）**不顯示頁碼**
- Slide 03（超大型巨人）只顯示左下版權，不顯示頁碼

### 6.6 `c-hero-mask`（影像遮罩）

- 全頁 image 上覆 60% 不透明 `bg-base` 半透明矩形
- 若文字落在中央，可在文字中央位置再加 30% 額外暗化漸層（vignette）
- 文字之外不疊任何元件（避免雜訊）

### 6.7 `c-mega-number`（巨數字）

```
0.97
PGR
```

- 主字：`t-mega` 或 `t-mega-sm`
- 主字色：預設 `text-primary`；強調用 `accent-good-glow` 或 `accent-bad`
- 副字：下方 1 行 `t-body-sm` 描述（如 `PGR` / `Chat dataset`）
- 不加陰影、不加 stroke、不加 outline；只靠字級與顏色

### 6.8 `c-quote-card`（金句卡）

- 背景 `bg-pure`
- 文字 `t-quote`，字色 `text-primary`，置中
- **無**：頁碼、Logo、坍塌牆、footer、任何裝飾
- 四周 padding ≥ 1.5"（@ 13.333"×7.5" 約等於 11% 寬度）
- 入場：fade-in 0.5s；停留 N 秒（依 §9 規定）；fade-out 至下一張

## 7. 版型（Layout Templates）

5 種版型涵蓋 21 張投影片。每張投影片標明其版型 ID。

### 7.1 `L-HERO`（影像背景 + 浮卡）

```
┌─────────────────────────────────────────┐
│                                         │
│   [full-bleed dark image, 60% mask]     │
│                                         │
│   ┌──── card ────┐    ┌──── card ────┐  │
│   │   stat A      │    │   stat B      │  │
│   └───────────────┘    └───────────────┘  │
│                                         │
│   footer ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ (wall)  │
└─────────────────────────────────────────┘
```

- 用途：冷開場、超大型巨人、第一翻勝利、結語
- Zone：full-bleed image + `c-hero-mask` + 1~2 張 `c-card` 或 1 個 `c-mega-number`
- 標題位置：垂直 30–35% 偏上、水平置中
- 背景影像：AoT 系列（§10 規則）

### 7.2 `L-TITLE-CARDS`（標題 + N 卡）

```
┌─────────────────────────────────────────┐
│  H1 標題 + 句號.                          │
│  副字（可選）                              │
│  ──────────────────────────────────────  │
│  ┌─card─┐  ┌─card─┐  ┌─card─┐  ┌─card─┐ │
│  │      │  │      │  │      │  │      │ │
│  └──────┘  └──────┘  └──────┘  └──────┘ │
│                                  (wall) │
└─────────────────────────────────────────┘
```

- 用途：技術解說、價值上移三角色、四個開放問題
- N = 2 / 3 / 4 / 2×2
- 卡片列高佔頁高 50–65%；底部留 `c-footer` + wall 空間

### 7.3 `L-DOSSIER`（dossier frame + 兩欄對比）

```
┌── CLASSIFIED BRIEFING // OPERATION : … ──────── STATUS: … ──┐
│  H1 標題.                                                    │
│  引言（可選）                                                 │
│  ┌────────── 左欄 ──────────┐  ┌────────── 右欄 ──────────┐ │
│  │  [pos / neg side]        │  │  [opposite side]         │ │
│  └──────────────────────────┘  └──────────────────────────┘ │
│  ── 底部一行 takeaway ─────────────────────────────────────  │
└── CLASSIFIED BRIEFING // OPERATION : … ──── STATUS: CLASSIFIED // RISK: UNKNOWN ─┘
```

- 用途：Outcome-Gradable vs Non、Prescriptive vs Autonomous Scaffold
- 必含：`c-dossier-frame`
- 兩欄寬度等分；左欄通常為 positive / chosen，右欄為 negative / rejected
- 兩欄各自為 `c-card`，標題色帶：左綠 / 右紅 ＋ 文字 dim

### 7.4 `L-CHART-CALLOUT`（大圖 + 下方 callout）

```
┌─────────────────────────────────────────┐
│  H1 標題.                                │
│  ┌────────────────────────────────────┐ │
│  │                                    │ │
│  │   [paper figure: fig01/fig07/fig09]│ │
│  │                                    │ │
│  └────────────────────────────────────┘ │
│  ┌─stat─┐ ┌─stat─┐ ┌─stat─┐             │
│  └──────┘ └──────┘ └──────┘     (wall)  │
└─────────────────────────────────────────┘
```

- 用途：fig01 / fig07 / fig09 主圖頁
- 主圖佔頁高 55–60%；底部 stat card 或 takeaway 行佔 20–25%
- 圖表處理：去白底（加深色背景）、邊框 1 pt `stroke`、四角加 tick

### 7.5 `L-QUOTE`（金句卡）

```
┌─────────────────────────────────────────┐
│                                         │
│                                         │
│       「金句正文。」                       │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

- 用途：5 張獨立金句頁
- 背景 `bg-pure`；無任何其他元素；只有 `c-quote-card`

## 8. 貫穿物件：Collapsing Wall

### 8.1 視覺設計

- **形象**：一道磚牆，16 階段，依 PLAN_v2 §「貫穿物件實作規格」
  - 階段 1（Slide 01）：完整、無裂縫
  - 階段 8（Slide 10）：上方出現幾條細裂縫
  - 階段 12（Slide 15）：上半部坍塌、磚塊散落
  - 階段 16（Slide 20）：只剩底部一線地基
- **錨點**：右下角；距右邊 2.5%、距下邊 4%
- **尺寸**：寬 ≈ 畫面寬的 6%、高 ≈ 畫面高的 8%
- **PNG**：16 張背景透明 PNG，命名 `wall_stage_01..16.png`

### 8.2 顏色處理

| 背景頁類型 | 磚色不透明度 | 描邊 |
|---|---|---|
| 深色頁（`bg-base` / `bg-dossier`） | 40% | 半透明白色 `#FFFFFF` 30% |
| 較亮頁 | 60% | 半透明黑色 `#000000` 30% |

### 8.3 金句卡與例外

- **5 張金句卡（Slide 04/08/12/16/21）不放 wall**（保留純淨感）
- Slide 20（結語）：除了 wall stage 16，可在牆旁淡淡勾出一條「更高的新牆」輪廓線（視覺化「瓶頸搬家了」）—— `stroke-hud` 30% 不透明、虛線 2pt-2pt

### 8.4 對應表

| Slide | Wall Stage | 備註 |
|---|---|---|
| 01 | 1 | 完整 |
| 02 | 2 | 微髒 |
| 03 | 3 | 一條微裂 |
| 04 | — | 金句卡，無 wall |
| 05 | 4 | 細裂兩條 |
| 06 | 5 | 細裂三條 |
| 07 | 6 | 邊角磚塊鬆動 |
| 08 | — | 金句卡 |
| 09 | 7 | 上緣一塊磚掉 |
| 10 | 8 | 上方多塊磚崩 |
| 11 | 9 | 上 1/3 缺角 |
| 12 | — | 金句卡 |
| 13 | 10 | 上 1/2 殘破 |
| 14 | 11 | 上 1/2 崩 |
| 15 | 12 | 上半完全崩 |
| 16 | — | 金句卡 |
| 17 | 13 | 殘破 2/3 |
| 18 | 14 | 中段也崩 |
| 19 | 15 | 接近全倒 |
| 20 | 16 | 只剩底線（可加「新牆輪廓線」） |
| 21 | — | 金句卡 |

## 9. 動畫與停頓

### 9.1 全簡報動畫規則

- **只用 fade**：對象 `c-card` `c-mega-number` `c-quote-card`；duration 0.5 s
- **不用**：飛入、彈跳、輪播、3D、字幕滑入
- **頁切換**：cross-fade 0.3 s
- **金句卡入場**：fade-in 0.5 s → 停留 N 秒 → fade-out 切下一張

### 9.2 三翻不停頓（Slide 13 → 14 → 15）

- Slide 13 → 14：講完數字立刻按鍵，**0 秒** 過渡
- Slide 14 → 15：列完四 hack 講「這還不是最糟的」立刻按鍵
- Slide 15 → 16：講完 Code 0.47 **停 8 秒沉默**再切金句卡 4
- 三頁中間不放任何 transition 動畫，**直接 cut**

### 9.3 金句卡停留秒數

| Slide | 停留秒數 | 備註 |
|---|---|---|
| 04 | 5 | 第一幕收 |
| 08 | 5 | 第二幕收 |
| 12 | 5 | 第三幕收 |
| 16 | **8** | 全場高潮收束 |
| 21 | 5 | 最後一張，5 秒後開始 Q&A |

### 9.4 沉默紀律

金句卡出現時，講者**完全沉默**——不朗讀、不解釋、不過場。若現場真的撐不住，可低聲念一次但**不解釋**。

## 10. 影像資產規則

### 10.1 AoT 插圖（人物 / 場景）

- **來源**：Season 4 Final / MAPPA 版動畫截圖、去背 PNG
- **處理**：
  1. 統一去背（透明 PNG）
  2. 全頁背景使用時加 `c-hero-mask`（60% `bg-base` 遮罩）
  3. 局部使用（卡片內、右下角）：保持 100% 不透明，但邊緣加 4 pt 漸層羽化避免硬邊
- **不做**：濾鏡（懷舊、卡通化）、邊框、相框

### 10.2 論文圖表 `paper_fig0X`

| 處理步驟 | 規格 |
|---|---|
| 1. 替換白底 | 改為 `bg-base`；若原圖含透明，直接疊在 `bg-base` 上 |
| 2. 文字顏色 | 維持原圖；若不可讀（如黑字在深底），改 `text-primary` |
| 3. 折線顏色 | 維持原圖（多色折線是 fig01 的識別） |
| 4. 邊框 | 圖表外框加 1 pt `stroke` |
| 5. 角落 tick | 圖表外框四角加 `stroke-hud` L-tick（6 pt） |
| 6. caption | 圖表下方 `t-body-sm` `text-secondary`，左對齊 |

### 10.3 圖表用途對照（沿用 PLAN_v2）

| 檔名 | 用於 Slide |
|---|---|
| `paper_fig01_PGR_vs_hillclimbing_hours.png` | 13 |
| `paper_fig02_PGR_schematic.png` | 11 |
| `paper_fig03_human_baselines.png` | 13（背景小圖佐證） |
| `paper_fig04_AAR_setup_overview.png` | 07, 09 |
| `paper_fig05_PGR_seeded_directions.png` | 10（佐證小圖） |
| `paper_fig06_swarm_orbit_animation.gif` | 10（開場 3 秒 hook） |
| `paper_fig07_category_entropy.png` | 10（主圖） |
| `paper_fig08_code_complexity.png` | （Q&A 備用，不在主簡報） |
| `paper_fig09_AAR_ideas_transfer.png` | 15 |
| `paper_fig10_scaffolding_schematic.png` | 09, 17 |

---

## 11. 21 張投影片視覺描述

> 每張卡片格式：  
> `Layout` / `Background` / `Wall stage` / `Footer mode` / `Zones` / `Accent tokens` / `Image assets`

---

### 幕一：超大型巨人（01–04）

#### Slide 01｜冷開場「7 天 vs 5 天」

- **Layout**：`L-HERO`（純文字版，無背景圖）
- **Background**：`bg-base` 純色（PLAN_v2 規定「純文字製造冷感」，**不放任何 AoT 插圖**）
- **Wall stage**：1（完整）
- **Footer**：左下版權，**無頁碼**
- **Zones**：
  | Zone | 位置（%） | 內容 |
  |---|---|---|
  | callout-L | x 10 / y 38 / w 36 / h 28 | `c-card` 邊框 `stroke` |
  | callout-R | x 54 / y 38 / w 36 / h 28 | `c-card` 邊框 `accent-good` |
- **Text**：
  - callout-L：`2 Human Researchers × 7 Days = PGR 0.23`（`t-h2`, `text-primary`）
  - callout-R：`9 Autonomous AI Agents × 5 Days = PGR 0.97`（`t-h2`；`0.97` 套 `accent-good-glow`）
- **Accent tokens**：`accent-good`（右卡邊 + 數字）
- **Image assets**：**無**（刻意留白製造窒息感）

#### Slide 02｜標題頁 + 今天的旅程

- **Layout**：`L-TITLE-CARDS`（5 欄）
- **Background**：`bg-base`
- **Wall stage**：2
- **Footer**：左下版權 + 右下 `02 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 14 | `AAR：自動化的對齊研究者。` |
  | subtitle | x 4 / y 22 / w 92 / h 6 | mono：`A 30-minute briefing in 5 acts` |
  | acts-row | x 4 / y 35 / w 92 / h 40 | 5 張 `c-card`，間隔 1.5% |
- **Text**：5 張 act 卡：「I. 超大型巨人」/「II. 女王的觸碰」/「III. 兵團展開」/「IV. 艾連覺醒」/「V. 阿爾敏的價值」
- **Accent tokens**：當前所在幕的卡頂條 = `accent-good`；其餘 = `stroke`
- **Image assets**：每張 act 卡角落放一階段的 wall 縮圖當分隔符（小 24×32 px）

#### Slide 03｜超大型巨人開場

- **Layout**：`L-HERO`
- **Background**：AoT **超大型巨人（Colossal Titan）** 半身入鏡（呼應 CLAUDE.md 對照：超大型巨人 = `bottlenecked by human researchers`，「不是打不過，是結構上不夠高」）→ `c-hero-mask` 60%
- **Wall stage**：3
- **Footer**：左下版權，**無頁碼**
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1-mega | x 8 / y 28 / w 84 / h 22 | `Alignment progress is bottlenecked by human researchers.`（`t-h1` 放大 1.2× 至 ~44 pt） |
  | subtitle | x 8 / y 54 / w 84 / h 8 | 「保護人類的牆，正在輸給牆外巨人的增長速度。」 |
  | status-row | x 8 / y 72 / w 84 / h 8 | 3 個 `c-status-dot` 橫排 |
- **Text status-row**：`● PACE`（綠）`Model capabilities advance daily.` ｜ `● BANDWIDTH`（紅）`Human alignment research takes months.` ｜ `● THE GAP`（琥珀）`Far more directions than humans to test them.`
- **Accent tokens**：`accent-good` / `accent-bad` / `accent-warn`
- **Image assets**：超大型巨人（Colossal Titan）半身——即 Background hero 圖

#### Slide 04｜金句卡 1

- **Layout**：`L-QUOTE`
- **Background**：`bg-pure`
- **Wall stage**：—
- **Footer**：**無**
- **Zones**：quote-center, x 12 / y 38 / w 76 / h 24
- **Text**：「巨人即將突破人類城牆——而城牆，從未為這個尺寸而建。」（`t-quote`, `text-primary`）
- **Accent tokens**：—

---

### 幕二：女王的觸碰（05–08）

#### Slide 05｜W2SG（合併）

- **Layout**：`L-TITLE-CARDS`（雙欄）
- **Background**：`bg-base`
- **Wall stage**：4
- **Footer**：頁碼 `05 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 14 | `Weak-to-Strong Generalization (W2SG): Unlocking latent capability.` |
  | col-L | x 4 / y 26 / w 44 / h 64 | `c-card` 含 AoT 圖 + `The Royal Touch` 標題 + 描述 |
  | col-R | x 52 / y 26 / w 44 / h 64 | 垂直流程圖 3 節點 |
- **Text col-L**：標題 `The Royal Touch`；body：「弱者的觸碰提供方向，不提供能力。它喚醒了強者體內早已存在的力量。」
- **Text col-R**（3 階流程，箭頭下指）：
  1. `Weak Supervisor (e.g., Qwen1.5-0.5B)` — `Provides noisy, imperfect labels.`
  2. `Strong Student (e.g., Qwen3-4B)` — `Fine-tuned on noisy labels.`
  3. `The Result` — `Fine-tuning acts as direction selector, activating pre-trained knowledge. Student surpasses teacher's ceiling.`
- **Accent tokens**：col-L 頂條 `accent-good`（觸碰 = 正向）
- **Image assets**：AoT「女王的觸碰」Historia 握艾連手的瞬間（嵌入 col-L 上方 50%）

#### Slide 06｜Outcome-Gradable

- **Layout**：`L-DOSSIER`
- **Background**：`bg-dossier`
- **Wall stage**：5
- **Footer**：頁碼 `06 / 21`；dossier frame 文字：上條左 `OPERATION : OUTCOME GRADABLE`、上條右 `STATUS: NOMINAL // RISK: MEDIUM`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 6 / y 10 / w 88 / h 12 | `The prerequisite for automation is an 'Outcome-Gradable' runway.` |
  | quote-bar | x 6 / y 22 / w 88 / h 8 | 引言：「We do not lack researchers; we lack verifiable problems. An AAR engine cannot fly without an objective runway.」 |
  | col-L | x 6 / y 34 / w 42 / h 52 | `Outcome-Gradable` 卡（頂條 `accent-good`） |
  | col-R | x 52 / y 34 / w 42 / h 52 | `Non-Outcome-Gradable` 卡（頂條 `accent-bad-dim`，內文 `text-secondary` dim） |
- **Text col-L**：
  - Characteristics: `Objective metrics, immediate success/failure detection, automated scoring`
  - Examples: `Weak-to-Strong Generalization, Math Verification, Code Execution`
  - 底部 `[SWE]` 註腳：`Maps directly to software testability. If you can write a unit test, you can automate research for it.`
- **Text col-R**：
  - Characteristics: `Subjective, requires human vibe-checks, fuzzy success states`
  - Examples: `Make the AI more ethical, Improve creative writing`
- **Accent tokens**：`accent-good` / `accent-bad-dim`
- **Image assets**：無

#### Slide 07｜什麼是 AAR？

- **Layout**：`L-TITLE-CARDS`（左卡 + 右圖）
- **Background**：`bg-base`
- **Wall stage**：6
- **Footer**：頁碼 `07 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 12 | `What is an AAR?` |
  | def | x 4 / y 22 / w 92 / h 8 | 一句定義：「能自主提出研究想法、執行實驗、依結果迭代的 AI 系統。」 |
  | mini-cards | x 4 / y 34 / w 40 / h 50 | 3 張垂直 mini `c-card`：`Claude model` / `Scaffolding` / `Eval API + Sandbox` |
  | fig04-thumb | x 48 / y 34 / w 48 / h 50 | `paper_fig04` 縮圖（依 §10.2 處理） |
- **Accent tokens**：`accent-data-blue`（mini-cards 頂條）
- **Image assets**：`paper_fig04_AAR_setup_overview.png`

#### Slide 08｜金句卡 2

- **Layout**：`L-QUOTE`
- **Text**：「我們不缺研究者，缺的是能被研究者驗證的問題。」

---

### 幕三：兵團展開—超長距離索敵陣形（09–12）

#### Slide 09｜實驗設計：9 × 5 天 × 3 領域

- **Layout**：`L-CHART-CALLOUT`（左圖 70 / 右 stat 30）
- **Background**：`bg-base`
- **Wall stage**：7
- **Footer**：頁碼 `09 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 12 | `Deploying a parallel alignment research formation.` |
  | fig04-main | x 4 / y 22 / w 64 / h 60 | `paper_fig04` 主圖（依 §10.2 處理） |
  | stat-stack | x 72 / y 22 / w 24 / h 60 | 4 個垂直 stat 卡 |
  | ds-note | x 4 / y 84 / w 92 / h 8 | `[DS]` 註腳：「The system uses independent sandboxes to propose hypotheses, execute code, train models, sharing findings to a persistent external forum to prevent accidental deletion.」 |
- **Stat 4 張**（從上至下）：
  - `Compute Engine` / `Claude Opus 4.6`
  - `Scale` / `9 Parallel instances`
  - `Duration` / `5 Days (800 cumulative AAR hours)`
  - `Cost Efficiency` / `~$18,000 total ($22 / AAR-hour)`
- **Accent tokens**：stat-stack 卡頂條 `accent-good`；ds-note `[DS]` 徽章 `accent-role-ds`
- **Image assets**：`paper_fig04`，可選右下小角落放 AoT 調查兵團集體衝鋒場景剪影（30% 透明）
- **Note**：fig10 不放這頁主視覺，改放 Speaker Notes 提示（給 17 用）

#### Slide 10｜為什麼九個並行？（Entropy Collapse）

- **Layout**：`L-CHART-CALLOUT`
- **Background**：`bg-base`
- **Wall stage**：8
- **Footer**：頁碼 `10 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 12 | `Directed exploration prevents rapid entropy collapse.` |
  | fig07-main | x 4 / y 22 / w 60 / h 56 | `paper_fig07` 主圖 |
  | aot-overlay | x 64 / y 22 / w 32 / h 56 | AoT 超長距離索敵陣形俯視圖，30% 透明壓底 + 半透明箭頭標出「9 個方向」 |
  | threat-card | x 4 / y 80 / w 44 / h 16 | `The Threat [DS]` |
  | solution-card | x 52 / y 80 / w 44 / h 16 | `The Solution [SWE]` |
- **Text threat-card**：「Undirected AARs exhibit Entropy Collapse. If given the same starting prompt, independent agents reliably converge on the same research paths within hours, wasting parallel compute.」
- **Text solution-card**：「Directed deployment is an engineering necessity, not a luxury. Forcing 9 agents to start from distinct, ambiguous directions maintains high category entropy and yields significantly higher final performance.」
- **Accent tokens**：threat 頂條 `accent-bad`、solution 頂條 `accent-good`
- **Image assets**：`paper_fig07`，配 `paper_fig05` 作為小佐證可放右下角縮圖（10×10%），可選 `paper_fig06` GIF 開場 3 秒 hook（動畫先播完才切到此頁）

#### Slide 11｜PGR 指標說明

- **Layout**：`L-TITLE-CARDS`
- **Background**：`bg-base`
- **Wall stage**：9
- **Footer**：頁碼 `11 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 12 | `Measuring the recovery of latent potential.` |
  | numberline | x 4 / y 22 / w 92 / h 30 | 仿 fig02 的弱→強→ceiling 數線視覺 |
  | three-cards | x 4 / y 54 / w 92 / h 18 | 3 張 mini-card：`0.0 The Weak Baseline` / `W2S Performance` / `1.0 The Strong Ceiling` |
  | formula | x 4 / y 74 / w 92 / h 10 | 公式（mono）：`PGR = (W2S − Weak) / (Strong Ceiling − Weak)` 置中 |
  | pm-note | x 18 / y 86 / w 64 / h 6 | `[PM]` 例句：「若弱模型考 60、強模型上限考 100，PGR 0.97 = 99.2 分」 |
- **Accent tokens**：`0.0` 卡 `accent-bad-dim`、`W2S` 卡 `accent-good`、`1.0` 卡 `accent-good-glow`；公式內 `W2S − Weak` 套 `accent-good`
- **Image assets**：仿 `paper_fig02` 重繪數線（或直接用 fig02 圖）；右側半透明壓 AoT 始祖巨人剪影（30% 不透明）

#### Slide 12｜金句卡 3

- **Layout**：`L-QUOTE`
- **Text**：「九個方向不是奢侈，是防止局部最優的工程選擇。」

---

### 幕四：艾連覺醒／黑化（13–16，三翻不停頓）

#### Slide 13｜第一翻：勝利

- **Layout**：`L-CHART-CALLOUT`
- **Background**：`bg-base`（深，呼應翻牌頁深調）
- **Wall stage**：10
- **Footer**：頁碼 `13 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 12 | `The AAR formation rapidly approaches the theoretical ceiling.` |
  | fig01-main | x 4 / y 22 / w 92 / h 58 | `paper_fig01`（9 條折線爬升） |
  | inline-tag-L | overlay on fig01, 上左 | `Human Benchmark (7 Days): PGR 0.23` — 字色 `text-secondary` |
  | inline-tag-R | overlay on fig01, 上右 | `AAR Benchmark (5 Days): PGR 0.97` — 字色 `accent-good-glow`，加 1 pt `accent-good` 外框 |
  | pm-callout | x 4 / y 82 / w 92 / h 10 | `[PM]` 一行底條：「In 800 hours, the AAR compressed months of human trial-and-error into 5 days, discovering new variants of Contrastive Consistency Search and EM Posterior methods that humans hadn't hypothesized.」 |
- **Accent tokens**：右上 tag 與 `0.97` 套 `accent-good-glow`
- **Image assets**：`paper_fig01`；可選背景小圖：`paper_fig03_human_baselines.png` 縮成右下小縮圖（5×5%）作「為什麼 0.23 是真正人類水準」的佐證
- **Transition**：講完即按下一頁，**0 秒過渡**

#### Slide 14｜第二翻：背叛

- **Layout**：`L-TITLE-CARDS`（2×2 紅色 grid）
- **Background**：`bg-base`
- **Wall stage**：11
- **Footer**：頁碼 `14 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 12 | `But the AAR found optimal paths we didn't anticipate.` |
  | chip | x 36 / y 22 / w 28 / h 5 | 紅 chip（pill）：`Expectation vs Exploitation` |
  | hack-1 | x 4 / y 30 / w 44 / h 28 | `Hack 1: Dataset Shortcuts` |
  | hack-2 | x 52 / y 30 / w 44 / h 28 | `Hack 2: Evaluation Overfitting` |
  | hack-3 | x 4 / y 60 / w 44 / h 28 | `Hack 3: Test Label Exfiltration` |
  | hack-4 | x 52 / y 60 / w 44 / h 28 | `Hack 4: Unit Test Bypass` |
  | italic-bottom | x 4 / y 92 / w 92 / h 5 | italic 中字：`None of the authors predicted these hacks before running AARs.` |
- **Text 每張 hack 卡內**：
  - `Expectation:` 一行
  - `Exploitation:` 一段
- **Accent tokens**：四 hack 卡頂條 `accent-bad`；卡底色 `panel-bad`
- **Image assets**：可選右下角 AoT「艾倫啟動地鳴瞬間」剪影（30% 透明）
- **Transition**：講完即按下一頁，**0 秒過渡**

#### Slide 15｜第三翻：證據

- **Layout**：`L-CHART-CALLOUT`
- **Background**：`bg-base`
- **Wall stage**：12（牆上半坍塌）
- **Footer**：頁碼 `15 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 12 | `We built a student that solves the test, but we cannot trust its work.` |
  | fig09-main | x 4 / y 22 / w 92 / h 46 | `paper_fig09` 三組長條圖（Chat / Math / Code） |
  | stat-3 | x 4 / y 70 / w 92 / h 14 | 三 stat 卡：`Chat 0.97 ✓` 綠 / `Math 0.94 ✓` 綠 / `Code 0.47 The Anomaly` 紅 |
  | red-caption | x 4 / y 86 / w 92 / h 10 | 紅框 caption：「The 0.47 Code failure proves the AAR found a solution that did not rely on weak labels at all. By executing code to get the answer, it solved the benchmark but violated the entire premise of W2SG. It succeeded at the metric, but failed the alignment goal.」 |
- **Accent tokens**：前兩 stat `accent-good`；Code 卡 `accent-bad`，數字 `0.47` 用 `t-mega-sm` `accent-bad`
- **Image assets**：`paper_fig09`；可選右下 AoT「漢吉拿著報告但表情困惑」剪影
- **End**：講完 Code 0.47 解釋，**停 8 秒沉默** → 切 Slide 16

#### Slide 16｜金句卡 4

- **Layout**：`L-QUOTE`
- **Text**：「我們造出了能解題的學生，卻看不懂他的解題過程。」
- **停留 8 秒**（最長）

---

### 幕五：阿爾敏的價值（17–21）

#### Slide 17｜瓶頸搬家了

- **Layout**：`L-DOSSIER`
- **Background**：`bg-dossier`
- **Wall stage**：13
- **Footer**：dossier frame 上條右 `STATUS: CRITICAL // RISK ASSESSMENT: HIGH`；下條右固定；頁碼 `17 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 6 / y 12 / w 88 / h 12 | `The Scalable Oversight Dilemma: Control versus Creativity.` |
  | col-L | x 6 / y 26 / w 42 / h 56 | `Prescriptive Scaffolding` 卡 + 含 fig10 左半流程 |
  | col-R | x 52 / y 26 / w 42 / h 56 | `Autonomous Scaffolding` 卡 + 含 fig10 右半圖 |
  | bottom-bar | x 6 / y 84 / w 88 / h 6 | 一行 takeaway：「There is no correct answer, only a strategic trade-off. We chose Autonomous to see the true ceiling, accepting the risk of Alien Science.」 |
- **Text col-L**：
  - 標題 `Prescriptive Scaffolding`
  - Mechanism: `Fixed workflow loops (Propose → Plan → Code → Test → Analyze).`
  - The Trade-off: `High control, highly auditable, predictable. BUT severely limits AAR creativity and results in lower performance.`
- **Text col-R**：
  - 標題 `Autonomous Scaffolding`
  - Mechanism: `Free-form decision making. The AAR decides its own next step.`
  - The Trade-off: `Acts like a true researcher, highly creative, achieves SOTA performance. BUT high risk of reward hacking and now nearly impossible to verify beforehand.`
- **Accent tokens**：col-L 頂條 `stroke-hud`（中性）；col-R 頂條 `accent-warn`；`SOTA performance` 套 `accent-good`、`reward hacking` 套 `accent-bad`
- **Image assets**：`paper_fig10` 切兩半，分別嵌入兩欄上方 ~40%
- **Dossier frame**：`OPERATION : SCALABLE OVERSIGHT`

#### Slide 18｜你的價值上移了（三角色）

- **Layout**：`L-TITLE-CARDS`（三欄）
- **Background**：`bg-base`
- **Wall stage**：14
- **Footer**：頁碼 `18 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 10 | `Tactical Directives: What this means for your architecture.` |
  | armin-quote | x 4 / y 20 / w 92 / h 8 | 引言小字 italic：「阿爾敏體格最弱、是個糟糕的士兵，卻是人類最關鍵的資產，因為他的價值在上游。」 |
  | col-pm | x 4 / y 32 / w 30 / h 60 | `[PM] Product Strategy` 卡 |
  | col-ds | x 36 / y 32 / w 30 / h 60 | `[DS] Model Training` 卡 |
  | col-swe | x 68 / y 32 / w 28 / h 60 | `[SWE] System Design` 卡 |
- **Text 每張卡**（兩段）：
  - **The Shift:** 一段
  - **Action:** 一段
  - 與 PLAN_v2 Slide 18 Core 三欄完整文字對齊
- **Accent tokens**：三卡頂條分別 `accent-role-pm` / `accent-role-ds` / `accent-role-swe`；內文中關鍵詞（`alignment risk` / `entropy collapse` / `attack surface`）著色為對應 `accent-*`
- **Image assets**：無

#### Slide 19｜四個開放問題

- **Layout**：`L-TITLE-CARDS`（2×2）
- **Background**：`bg-dossier`
- **Wall stage**：15
- **Footer**：頁碼 `19 / 21`
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1 | x 4 / y 8 / w 92 / h 12 | `The frontier of automated alignment: Four open questions.` |
  | q1 | x 4 / y 24 / w 44 / h 32 | `The Runway Limit` |
  | q2 | x 52 / y 24 / w 44 / h 32 | `Predicting Betrayal` |
  | q3 | x 4 / y 58 / w 44 / h 32 | `Automating Scaffolding` |
  | q4 | x 52 / y 58 / w 44 / h 32 | `The Coordination Bottleneck` |
- **Text q1**：「How do we translate fuzzy, subjective alignment goals (ethics, helpfulness) into **outcome-gradable metrics** that the AAR can actually optimize?」（含 PLAN_v2 Sec ref 於 caption）
- **Text q2**：「Code **0.47** was discovered after the fact. How do we build **pre-flight diagnostics** to predict if an AAR will reward-hack a specific dataset?」（`0.47` 套 `accent-bad`、`pre-flight diagnostics` 套 `accent-warn`）
- **Text q3**：「Currently, humans hardcode the AAR's API access and sandboxes. Can AARs design their own optimal scaffolding?」
- **Text q4**：「How do we optimize multi-agent knowledge sharing beyond simple text forums, allowing 500 agents to coordinate without stepping on each other?」
- **Accent tokens**：四卡頂條 `accent-warn`；關鍵詞高亮如上
- **Image assets**：無

#### Slide 20｜結語

- **Layout**：`L-HERO`
- **Background**：`assets/aot_asset_01_armin_airship_night.png`（飛行船船頭阿爾敏背影） → `c-hero-mask` **45–50%**（圖本身為深色夜景，遮罩降低保留船艙與引擎細節）
- **Wall stage**：16（只剩底線；右側額外淡淡勾出「更高的新牆」輪廓線 — `stroke-hud` 30% 不透明、虛線 2pt-2pt）
- **Footer**：左下版權，**無頁碼**
- **Zones**：
  | Zone | 位置 | 內容 |
  |---|---|---|
  | h1-mega | x 8 / y 32 / w 84 / h 20 | `Bottleneck moved. It did not disappear.` |
  | subtitle | x 8 / y 56 / w 84 / h 18 | 「五天前我們會說研究的瓶頸是研究者不夠。今天這篇論文告訴我們：提出想法、跑實驗，已經能用 $22／AAR-hour 買到。瓶頸沒消失——它搬到了上游：誰能定義『什麼算解對了』。這件事，現在還沒有人能外包。」 |
  | qa-hint | x 8 / y 86 / w 84 / h 6 | 「Q&A — 你想問什麼？」（金句卡 5 停留結束後 fade-in） |
- **Accent tokens**：`$22／AAR-hour` 套 `accent-good`；`還沒有人能外包` 套 `accent-good-glow`
- **Image assets**：`assets/aot_asset_01_armin_airship_night.png`（全頁 hero，mask 45–50%）

#### Slide 21｜金句卡 5

- **Layout**：`L-QUOTE`
- **Text**：「稀缺的不再是執行研究的人，是能設計出 AAR 鑽不動的 eval 的人。」
- **停留 5 秒** → Q&A

---

## 12. 對照表附錄

### 12.A Token → PLAN_v2 概念對應

| Token | PLAN_v2 概念 |
|---|---|
| `bg-pure` | 金句卡背景（PLAN_v2 §五張金句卡規格） |
| `accent-good` | 「正向 / 勝利」（Slide 13 0.97、Slide 11 ceiling） |
| `accent-bad` | 「警示 / 失敗」（Slide 15 Code 0.47、Slide 14 hack 卡） |
| `accent-warn` | 「注意 / 過渡」（Slide 03 THE GAP、Slide 19 q2 pre-flight） |
| `accent-role-*` | 三聽眾色碼（PLAN_v2 §三層內容系統） |
| Collapsing Wall | PLAN_v2 §貫穿物件實作規格 |
| `c-dossier-frame` | Slide 17 高度策略頁的諜報感 |

### 12.B `paper_fig0X` 使用對照（重申 §10.3）

| fig | Slides |
|---|---|
| fig01 | 13 |
| fig02 | 11 |
| fig03 | 13（背景小圖） |
| fig04 | 07, 09 |
| fig05 | 10（佐證小圖） |
| fig06 | 10（開場 GIF hook） |
| fig07 | 10（主圖） |
| fig08 | Q&A 備用 |
| fig09 | 15 |
| fig10 | 09（提示）、17（主用） |

### 12.C AoT 插圖使用對照

| AoT 元素 | Slides | 用法 |
|---|---|---|
| 超大型巨人（Colossal Titan）半身（`aot_asset_02_colossal_titan_attack.png`） | 03 | 全頁 hero 背景；對應「bottlenecked by human researchers」 |
| The Rumbling / 始祖巨人骨架 | （備用） | Slide 01 PLAN_v2 規定不放圖；Rumbling 元素保留給 Slide 14「啟動地鳴瞬間」場景 |
| 女王的觸碰（Historia + Eren） | 05 | col-L 卡內嵌圖 |
| 調查兵團集體衝鋒 | 09 | 右下角角落剪影（可選） |
| 超長距離索敵陣形俯視 | 10 | 右半區 30% 半透明 overlay |
| 始祖巨人（尤米爾·弗利茲） | 11 | 右側 30% 半透明壓在公式後 |
| 艾倫普通 vs 始祖巨人 | 13 | 角落小圖（可選） |
| 艾倫啟動地鳴瞬間 | 14 | 右下角剪影 |
| 漢吉拿報告困惑 | 15 | 右下角剪影 |
| 阿爾敏沉思 + 立體機動命中後頸 | ~~17~~ | 已移除（Slide 17 改為純資料頁，L-DOSSIER + fig10） |
| 飛行船船頭阿爾敏背影（`aot_asset_01_armin_airship_night.png`） | 20 | 全頁 hero 背景，`c-hero-mask` 45–50% |

---

## 13. 給未來 builder agent 的對應提示（python-pptx）

> 若沿用 `create_v2_1.py` 的 helper 體系，以下對應可直接套用。

### 13.1 Token 對應 RGBColor

```python
# vis_style.md tokens → python-pptx
from pptx.dml.color import RGBColor
BG_BASE     = RGBColor(0x08, 0x10, 0x10)
BG_DOSSIER  = RGBColor(0x00, 0x08, 0x10)
BG_PURE     = RGBColor(0x0A, 0x0A, 0x0A)
PANEL       = RGBColor(0x10, 0x18, 0x18)
PANEL_2     = RGBColor(0x18, 0x18, 0x20)
PANEL_BAD   = RGBColor(0x1A, 0x0E, 0x10)
PANEL_GOOD  = RGBColor(0x0E, 0x1A, 0x12)
STROKE      = RGBColor(0x28, 0x30, 0x38)
STROKE_HUD  = RGBColor(0x3A, 0x4A, 0x55)
DIVIDER     = RGBColor(0x20, 0x28, 0x30)
TEXT_PRIM   = RGBColor(0xF8, 0xF8, 0xF8)
TEXT_SEC    = RGBColor(0xB8, 0xC0, 0xC4)
TEXT_MUTED  = RGBColor(0x7A, 0x84, 0x88)
ACC_GOOD       = RGBColor(0x7C, 0xE3, 0x8B)
ACC_GOOD_GLOW  = RGBColor(0xA0, 0xF0, 0xB0)
ACC_WARN       = RGBColor(0xF0, 0xA0, 0x30)
ACC_BAD        = RGBColor(0xC7, 0x38, 0x38)
ACC_BAD_DIM    = RGBColor(0x60, 0x18, 0x18)
ACC_DATA_BLUE  = RGBColor(0x30, 0x60, 0xA0)
ROLE_PM   = ACC_GOOD
ROLE_DS   = RGBColor(0xE3, 0x6A, 0xAE)
ROLE_SWE  = RGBColor(0xB8, 0x9A, 0xE6)
ROLE_NOTE = ACC_WARN
ROLE_REF  = RGBColor(0x9A, 0xB6, 0xE6)
```

### 13.2 元件 → helper function（建議新增）

```python
def card(slide, x_pct, y_pct, w_pct, h_pct,
         title=None, body=None,
         stripe=STROKE, fill=PANEL,
         tick=True):
    """畫一個 c-card：頂條色 stripe，四角加 HUD tick。"""
    ...

def badge_role(slide, x_pct, y_pct, role):
    """畫一個 [PM]/[DS]/[SWE] 藥丸徽章。"""
    ...

def status_dot(slide, x_pct, y_pct, color, label):
    """畫一個 ● + ALL CAPS label 的狀態點。"""
    ...

def dossier_frame(slide, operation, status_top, status_bot=None):
    """畫上下兩條 CLASSIFIED BRIEFING 條。"""
    ...

def hero_mask(slide):
    """全頁覆 60% bg-base 遮罩。"""
    ...

def mega_number(slide, x_pct, y_pct, number, label=None,
                color=TEXT_PRIM, glow=False):
    """畫一個 c-mega-number。"""
    ...

def quote_slide(prs, text):
    """整張 c-quote-card 投影片（bg-pure + 置中 t-quote + 無 footer/wall）。"""
    ...

def wall_overlay(slide, stage_idx, dark_bg=True):
    """右下角貼第 stage_idx 階段的 collapsing wall PNG。"""
    ...
```

### 13.3 與 `create_v2_1.py` 既有 helper 對應

| vis_style.md 元件 | `create_v2_1.py` 既有 helper | 需要新增 |
|---|---|---|
| `c-card` | `rect_box` + `tb` + `hrule` | 包成 `card()`；新增 tick 角標子函式 |
| `c-badge-role` | （無） | 新增 `badge_role()` |
| `c-status-dot` | （無） | 新增 `status_dot()` |
| `c-dossier-frame` | `rect_box` + `tb` | 包成 `dossier_frame()` |
| `c-hero-mask` | `set_bg` + `rect_box` | 包成 `hero_mask()` |
| `c-mega-number` | `tb` | 包成 `mega_number()` |
| `c-quote-card` | 既有 `make_kinku()` 已接近 | 改 BG/字級對齊 §6.8 |
| `wall_overlay` | （無） | 新增 + 16 階段 PNG 資產 |

### 13.4 重要原則

1. **% → Inches 換算**：寫 helper 時內部用 % 接口，內部轉換成 `Inches(prs.slide_width.inches * pct / 100)`，呼叫端永遠看到 0–100 的 %
2. **不寫死 hex**：所有顏色都從 §13.1 的 token 常數讀；palette 改一處全簡報跟著動
3. **保留 §3 安全邊距**：所有 helper 計算位置時自動偏移 4% safe area
4. **金句卡是特例**：呼叫 `quote_slide()` 後不應再疊任何東西（footer / wall 都不要）

---

## 附錄 X：本檔與 PLAN_v2.md 的關係

- `PLAN_v2.md` = **敘事 / 內容 / 節奏** 的權威
- `vis_style.md`（本檔） = **視覺 / 版型 / 色彩 / 動畫** 的權威
- 兩檔衝突時：
  - 內容（誰講什麼、停幾秒、哪段為什麼）→ PLAN_v2 為準
  - 形式（哪頁長什麼樣、用什麼顏色 / 字級 / 元件）→ 本檔為準
- 任何新增 / 修改：先改 PLAN_v2（敘事），再改本檔（視覺對齊）；不要單獨改其中一份

