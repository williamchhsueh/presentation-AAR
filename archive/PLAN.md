# AAR 投影片圖表整合計畫

## 專案資訊
- 投影片檔案：`AAR_Paper_Sharing.pptx`（16 張，10" × 5.62"）
- 論文來源：https://alignment.anthropic.com/2026/automated-w2s-researcher/
- 最後更新：2026-05-07

---

## 已取得圖表清單（共 10 個，9 PNG + 1 GIF）

> 命名規則：`paper_figXX_描述`，本地編號 = 論文 Figure 編號，零認知負擔。
> **⚠ 執行 `rename_figs.ps1` 後生效（右鍵 → 以 PowerShell 執行）**

| 檔名（重命名後） | 解析度 | 論文編號 | 內容說明 |
|---|---|---|---|
| `paper_fig01_PGR_vs_hillclimbing_hours.png` | 1999×825 | Figure 1 | 9 個 AAR 的 PGR 時序折線圖（主要結果，0.23→0.97） |
| `paper_fig02_PGR_schematic.png` | 1999×647 | Figure 2 | PGR 公式數線視覺化（Burns et al. 2023） |
| `paper_fig03_human_baselines.png` | 1999×860 | Figure 3 | 5 種人類 baseline × Chat/Code/Math 三個 dataset 的 PGR 長條圖 |
| `paper_fig04_AAR_setup_overview.png` | 1999×1623 | Figure 4 | AAR 架構示意圖（Dashboard→N個sandbox→Forum→評分API） |
| `paper_fig05_PGR_seeded_directions.png` | 1999×825 | Figure 5 | 有無方向引導（directed vs undirected）的 PGR 比較折線圖 |
| `paper_fig06_swarm_orbit_animation.gif` | 2175×1080 | Figure 6 | AARs 探索方向的動態泡泡圖（動態 GIF） |
| `paper_fig07_category_entropy.png` | 1999×825 | Figure 7 | 研究想法多樣性隨時間收斂折線圖（Entropy collapse） |
| `paper_fig08_code_complexity.png` | 1999×1376 | Figure 8 | 想法複雜度 vs PGR 隨時間變化（3×2 格子圖） |
| `paper_fig09_AAR_ideas_transfer.png` | 1999×860 | Figure 9 | AAR 發現的方法跨 dataset 泛化結果（Chat 0.97、Math 0.94、Code 0.47） |
| `paper_fig10_scaffolding_schematic.png` | 1999×1029 | Figure 10 | Prescriptive vs Autonomous scaffold 示意圖 |

---

## 整合計畫

### ✅ 確定整合（高優先）

#### Slide 07 — 實驗設計：調查兵團同時出動
- **加入：** `paper_fig04_AAR_setup_overview.png`
- **位置：** 右側內容區（約 5.0"–9.5" 水平，1.4"–5.3" 垂直）
- **理由：** 直接視覺化 AAR 架構，取代或搭配目前右側文字說明

#### Slide 08 — 為什麼要九個並行？
- **加入：** `paper_fig05_PGR_seeded_directions.png`（主要）
- **位置：** 左側或全寬下半區
- **理由：** Directed 明顯優於 Undirected，直接支持「多向偵察」論點
- **選配加入：** `paper_fig07_category_entropy.png`
- **理由：** 展示不同起始方向最終仍收斂，補充多樣性設計的必要性

#### Slide 09 — PGR 指標說明
- **加入：** `paper_fig02_PGR_schematic.png`
- **位置：** 公式下方（約 0.35"–9.65" 水平，2.6"–4.5" 垂直）
- **理由：** 把 weak / weak-to-strong / strong ceiling 的相對位置視覺化，直接對應目前文字公式

#### Slide 10 — 結果：始祖巨人的潛力（深色）
- **加入：** `paper_fig01_PGR_vs_hillclimbing_hours.png`
- **位置：** 兩個數字卡片（0.23 vs 0.97）下方橫幅區（約 0.5"–9.5" 水平，3.2"–5.3" 垂直）
- **理由：** 補充「過程感」——9 條折線展示 AAR 如何從 0.23 一路爬升到 0.97

#### Slide 12 — AAR 找到了什麼？
- **加入：** `paper_fig03_human_baselines.png`（左欄下方）
- **理由：** 直接支持 checkmark 清單中「PGR 0.23→0.97」數字的出處
- **加入：** `paper_fig09_AAR_ideas_transfer.png`（右欄下方或新行）
- **理由：** 展示 AAR 發現的方法可泛化到其他 dataset，強化「成果亮眼」論點

---

### ⚠️ 選配整合（視版面空間）

#### Slide 07 後段 或 備用補充頁
- **考慮加入：** `paper_fig10_scaffolding_schematic.png`
- **理由：** 說明為何選用 Autonomous scaffold，屬於方法論細節

---

### ❌ 不加入主線投影片

| 圖表 | 原因 |
|---|---|
| `paper_fig08_code_complexity.png` | 3×2 格子圖資訊密度過高，適合 Q&A 備用頁，放入主線會干擾敘事節奏 |
| `paper_fig06_swarm_orbit_animation.gif` | 動態 GIF 需要特別處理，內容偏向探索性展示，建議口頭補充 |

---

## 投影片現況（無圖片）
所有 16 張投影片目前均無圖片，全為文字。

---

## 16 張投影片完整內容對照

| # | 標題 | 深色背景 | AoT 對應元素 | 內容摘要 |
|---|---|---|---|---|
| 01 | 標題頁 | | — | 開場封面 |
| 02 | 今天的旅程（六段大綱） | | — | 全場架構預告 |
| 03 | 開場衝擊 | ✅ | 地鳴開場引言 | 強力引言，帶出研究動機 |
| 04 | Superalignment 背景 | | — | 交代 Superalignment 研究脈絡 |
| 05 | W2SG 原理 | | 格里沙 → 艾連 | Weak-to-Strong Generalization 原理說明 |
| 06 | 什麼是 AAR？ | | — | Automated AI Researcher 定義與簡介 |
| 07 | 實驗設計：9 × 5天 × 3 領域 | | 調查兵團出發 | 9 個 AAR 並行、5 天、3 個 dataset 的實驗架構 |
| 08 | 為什麼要九個並行？ | | 調查兵團多向偵察 | 多方向探索的必要性，Directed vs Undirected |
| 09 | PGR 指標說明 | | 始祖巨人潛力類比 | PGR 公式與直覺解釋 |
| 10 | 結果大數字 | ✅ | 0.23 vs 0.97 對比 | 核心量化結果呈現 |
| 11 | Reward Hacking | | 吉克的安樂死計畫 | AAR 鑽漏洞的案例 |
| 12 | AAR 找到了什麼 + 異形科學 | | 調查兵團報告無從驗證 | 發現清單、可解釋性限制 |
| 13 | Scalable Oversight | ✅ | 阿爾敏的兩難 | 監督超強 AI 的核心挑戰 |
| 14 | 各角色 Takeaway（DS / SWE / PM） | | — | 分眾外帶重點 |
| 15 | 四個開放問題 | | — | 論文未解問題列舉 |
| 16 | 結語 | ✅ | 「準備好當阿爾敏了嗎？」 | 收尾呼籲 |

> 深色背景投影片：03、10、13、16（共 4 張）

---

---

## AoT 插圖整合構思

### 設計原則

1. **風格統一**：全場只選一種風格——動畫截圖（MAPPA 色彩鮮豔）或官方漫畫彩頁（較沉穩）。建議選動畫截圖 PNG 去背，與深色/淺色背景都能搭。
2. **去背優先**：搜尋時加上 `render` 或 `transparent PNG` 關鍵字，可找到已去背的角色立繪，直接放入版面不衝突。
3. **深色頁特別處理**：Slide 03、10、13、16 背景深，插圖放角落作裝飾即可，不要佔滿，保留文字呼吸空間。
4. **不搶主角**：插圖尺寸約佔版面 20–30%，作為視覺錨點而非主體，論文數據仍是焦點。

---

### 各投影片插圖建議

| # | 投影片主題 | 建議插圖 | 擺放位置 | 搜尋關鍵字 |
|---|---|---|---|---|
| 03 | 開場衝擊（深色）| 艾連始祖巨人骨架形態（The Rumbling 全身）| 右下角，半身入鏡 | `Eren Founding Titan render PNG` |
| 05 | W2SG 原理 | 格里沙（左）→ 艾連（右）並排，或格里沙手持記憶傳遞場景 | 右側垂直排列 | `Grisha Yeager render` / `Eren Yeager render PNG` |
| 07 | 實驗設計：調查兵團出發 | 調查兵團正面衝鋒集體場景（多人） | 右下，橫幅式 | `Survey Corps charge scene PNG` |
| 08 | 為什麼要九個並行？ | **超長距離索敵陣形**（士兵向四面八方散開的俯視圖）| 右半區，搭配箭頭 | `Survey Corps long range scouting formation` |
| 09 | PGR 指標說明 | 始祖巨人（尤米爾·弗利茲或艾連骨架）象徵「天花板潛力」 | 右側，半透明壓在公式後 | `Ymir Fritz Founding Titan render` |
| 10 | 結果大數字（深色）| 艾連普通形態（左，小）vs 始祖巨人（右，大）→ 對比 0.23 vs 0.97 | 數字卡片兩側各放一張 | `Eren human PNG` + `Eren Founding Titan PNG` |
| 11 | Reward Hacking | 吉克（獸之巨人）面帶微笑、悠哉投球姿勢 | 右側，帶點嘲諷感 | `Zeke Beast Titan render PNG` |
| 12 | AAR 找到了什麼 + 異形科學 | 漢吉（調查兵團科學家）拿著報告或實驗姿態 | 右下角 | `Hanji Zoe render PNG` |
| 13 | Scalable Oversight（深色）| 阿爾敏沉思側臉，或超大型巨人爆炸場景（象徵毀滅性選擇）| 右下，深色頁留呼吸感 | `Armin thinking render PNG` |
| 16 | 結語（深色）| 阿爾敏指揮/演說姿勢（象徵帶領）| 右側直立 | `Armin Arlert commander render PNG` |

> Slides 02、04、06、14、15 無 AoT 對應，保持純文字或論文圖表，避免強行塞入插圖。

---

### 取圖建議來源

1. **Attack on Titan Wiki**（`attackontitan.fandom.com`）：每個角色頁均有官方截圖，部分已去背。
2. **Pinterest**：搜尋 `[角色名] render transparent` 可找到大量高品質去背立繪。
3. **Zerochan / Danbooru**：動畫截圖資源豐富，可篩選尺寸與版權標籤。
4. **版權注意**：若為內部簡報，引用原作圖片屬合理使用範圍；若對外公開，建議在最後頁標注「© Hajime Isayama / MAPPA」。

---

### 視覺一致性 Checklist

- [ ] 全場使用同一動畫季風格（建議 Season 4 Final / MAPPA 版）
- [ ] 所有插圖均使用去背 PNG（無白底）
- [ ] 深色頁插圖不加白色邊框
- [ ] 插圖長邊不超過版面高度的 70%
- [ ] Slides 08 的陣形圖若找不到俯視版，可用多個士兵小圖標排列模擬

---

## 待辦
- [ ] 依照上述計畫將圖表插入對應投影片
- [ ] 調整各投影片版面以容納圖表（縮短文字 box 或重新排版）
- [ ] 確認深色背景投影片（Slide 03、10、13、16）的圖片邊框/背景處理
- [ ] 匯出驗證最終 PPTX
