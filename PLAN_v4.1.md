# AAR 投影片整合計畫 v4.1（鏡像現行投影片）

## 專案資訊

- 投影片檔案：`ppt/AAR_Paper_Sharing_v4.1.pptx`（**31 張**，10" × 5.625"）
- 後續修補版：`ppt/AAR_Paper_Sharing_v4.2.pptx`（由 `code/patch_slides.py` 重建 4 張原本是 raster 圖片的頁，內容對齊 v4.1）
- 論文來源：https://alignment.anthropic.com/2026/automated-w2s-researcher/
- 上一版規格文件：`PLAN_v2.md`（21 張）— **本檔不取代 v2，而是反映實際投影片現狀**
- 本版日期：2026-05-22
- 聽眾：DS × 15、SE × 7、PM × 5（總 27 人）
- 時間預算：30 分鐘 / 31 頁

---

## 為什麼有 v4.1：規格與投影片已分歧

`PLAN_v2.md` 撰寫於規劃階段，描述 21 張的五幕結構。實際製作過程中，投影片透過 `code/build_deck.py` 與 `code/patch_slides.py` 直接編輯與擴張，最終定稿為 **31 張**。差距是結構性的，非單純文字微調：

| 變化類型 | v2 規格 | v4.1 現況 |
|---|---|---|
| 總頁數 | 21 | **31** |
| 幕首章節卡 | 無 | **5 張**（slides 2、6、10、17、25 — 每幕開頭一張，固定版面列出五幕，當前幕亮色） |
| 第四幕（三重翻牌） | 3 張文字（slides 13–15） | **6 張視覺＋文字**（slides 17–22） — 翻牌變為「先視覺後文字揭示」 |
| 全幅/英雄圖頁 | 少 | **多**（特別是第一幕、第四幕、第五幕間的氣氛頁） |
| 金句卡編號 | 04、08、12、16、21 | **05、09、16、24、31** |
| 設計哲學 | 五幕框架、三層筆記、坍塌牆、金句卡 | **全部沿用**（見下節） |

v2 → v4.1 並非「重新設計」，而是「同樣的敘事被拉長與視覺化」。本檔記錄實際狀態，並指向 v2 中仍有效的設計哲學章節。

---

## 沿用 v2 的設計哲學（不重寫，僅引用）

下列章節在 v4.1 仍然有效，請直接讀 v2 原文，本檔不重複：

| 設計原則 | v2 章節 | 在 v4.1 的狀態 |
|---|---|---|
| 五幕分主導架構（A 戲劇／B 技術／C PM 輪替） | `PLAN_v2.md` §「核心設計理念 1. 五幕分主導架構」 | 沿用；幕別主導風格不變 |
| 三層內容系統（Core / Deeper-DS / Wider-PM） | `PLAN_v2.md` §「核心設計理念 2. 三層內容系統」 | **沿用**；多數投影片備忘稿仍維持三層結構（見本檔每頁 Speaker Notes） |
| 三重翻牌敘事弧（勝利 → 背叛 → 證據） | `PLAN_v2.md` §「核心設計理念 3. 第四幕三重翻牌」 | **沿用但拉長**；從 3 頁變 6 頁（17–22），每翻多了 1–2 張視覺鋪陳頁 |
| 五張金句卡（深色／單句白字／停頓不解釋） | `PLAN_v2.md` §「核心設計理念 4. 五張金句卡」 | **沿用**；金句文字未變動，僅編號位移（見下節 31 張投影片表） |
| 貫穿物件：逐漸坍塌的牆 | `PLAN_v2.md` §「核心設計理念 5. 貫穿物件」 | **未在 v4.1 deck 中觀察到**；改為章節卡＋全幅圖頁承擔節奏感（詳見「開放議題」） |
| 巨人情節對照表 | `CLAUDE.md` §「巨人情節對照表」 | 沿用，無新增對應 |
| 視覺規格（色彩 token、版型、字體、組件） | `vis_style.md` 全文 | 沿用；v4.1 的「Dossier」風格細節（章節卡、Tactical Directives 三欄等）對應 `vis_style.md` 既有版面類型 |

---

## 31 張投影片對照表

> **Role 詞彙**：`cold-open` 冷開場 / `chapter-card` 幕首章節卡 / `content` 內容頁 / `hero` 全幅氣氛頁 / `golden-quote` 金句卡 / `closing` 收尾頁
> **主導**：A=戲劇張力 / B=技術精準 / C=PM 行動 / Q=金句卡（純沉默） / —=章節卡或氣氛頁
> **深色** ✅ 代表深色背景
> **停頓**：講完該頁刻意保持的沉默秒數

| # | 幕 | Role | 標題（投影片實際呈現） | 主導 | 深色 | 停 | 對應素材 |
|---|---|---|---|---|---|---|---|
| 01 | I 超大型巨人 | cold-open | （全幅圖：7 天 vs 5 天數字版面） | A | ✅ | 3 | hero image |
| 02 | I 超大型巨人 | chapter-card | Automated Alignment Researcher (AAR) — 五幕地圖（I 高亮） | A | ✅ | 0 | — |
| 03 | I 超大型巨人 | hero | （全幅圖） | A | ✅ | 0 | `aot_asset_02_colossal_titan_attack.png`（推測）|
| 04 | I 超大型巨人 | content | Alignment progress is bottlenecked by human researchers. — PACE / BANDWIDTH / THE GAP | A | ✅ | 0 | — |
| 05 | I 超大型巨人 | **golden-quote 1** | 巨人即將突破人類城牆 ── 城牆 從未為這個尺寸而建 | Q | ✅ | **5** | — |
| 06 | II 女王的觸碰 | chapter-card | AAR：自動化的對齊研究員 — 五幕地圖（II 高亮） | B | | 0 | — |
| 07 | II 女王的觸碰 | content | Weak-to-Strong Generalization (W2SG): Unlocking latent capability — 女王的碰觸 | B | | 2 | `paper_fig?` + AoT「女王的觸碰」插圖（推測）|
| 08 | II 女王的觸碰 | content | The prerequisite for automation is an 'Outcome-Gradable' runway | B | | 2 | — |
| 09 | II 女王的觸碰 | **golden-quote 2** | 我們不缺研究員 缺的是能被研究員驗證的問題 | Q | ✅ | **5** | — |
| 10 | III 兵團展開 | chapter-card | Automated Alignment Researcher (AAR) — 五幕地圖（III 高亮） | B | | 0 | — |
| 11 | III 兵團展開 | content | What is an AAR? — Claude Model / Scaffolding / Eval API + Sandbox | B | | 0 | `paper_fig04_AAR_setup_overview` |
| 12 | III 兵團展開 | content | Deploying a parallel alignment research formation — 9 × 5 天 × $18,000 | B+A | | 2 | `paper_fig10_scaffolding_schematic`（推測），可能附 AoT 兵團衝鋒 |
| 13 | III 兵團展開 | content | Directed exploration prevents rapid entropy collapse — The Threat / The Solution | B+A | | 3 | `paper_fig07_category_entropy`（主圖）+ 超長距離索敵陣形 AoT |
| 14 | III 兵團展開 | hero | （全幅圖：可能為 fig07 主視覺或陣形圖）| — | | 0 | hero image |
| 15 | III 兵團展開 | content | Measuring the recovery of latent potential（PGR 指標說明） | B | | 0 | `paper_fig02_PGR_schematic` |
| 16 | III 兵團展開 | **golden-quote 3** | 九個方向不是奢侈，是防止局部最優的工程選擇。 | Q | ✅ | **5** | — |
| 17 | IV 艾連覺醒 | chapter-card | Automated Alignment Researcher (AAR) — 五幕地圖（IV 高亮） | A | ✅ | 0 | — |
| 18 | IV 艾連覺醒 | **hero（第一翻：勝利視覺）** | （全幅圖：0.23 → 0.97 數字 + fig01 折線）| A | ✅ | 0 | `paper_fig01_PGR_vs_hillclimbing_hours` |
| 19 | IV 艾連覺醒 | hero（第一翻延伸） | （全幅圖） | A | ✅ | 0 | hero image |
| 20 | IV 艾連覺醒 | hero（第二翻鋪陳） | （全幅圖） | A | ✅ | 0 | hero image，可能為「地鳴啟動」AoT |
| 21 | IV 艾連覺醒 | content | But the AAR found optimal paths we didn't anticipate — Hack 1–4 對比表 | A+B | | 0 | — |
| 22 | IV 艾連覺醒 | **hero（第三翻：證據）** | （全幅圖：Chat 0.97 / Math 0.94 / **Code 0.47** ⚠️） | A+B | | **8** | `paper_fig09_AAR_ideas_transfer` |
| 23 | IV 艾連覺醒 | hero（收束過場） | （全幅圖） | A | ✅ | 0 | hero image |
| 24 | IV 艾連覺醒 | **golden-quote 4** | 教出能解題的學生 卻看不透他的解題過程 | Q | ✅ | **8** | — |
| 25 | V 阿爾敏 | chapter-card | Automated Alignment Researcher (AAR) — 五幕地圖（V 高亮） | C | | 0 | — |
| 26 | V 阿爾敏 | hero（瓶頸搬家鋪陳） | （全幅圖）| C+B | ✅ | 0 | hero image |
| 27 | V 阿爾敏 | hero（阿爾敏引言） | （全幅圖：阿爾敏體格最弱…）| C | | 0 | `aot_asset_01_armin_airship_night.png`（推測）|
| 28 | V 阿爾敏 | content | Tactical Directives: What this means for your architecture — PM / DS / SE 三欄 | C | | 2 | — |
| 29 | V 阿爾敏 | content | The frontier of automated alignment: Four open questions | C | | 2 | — |
| 30 | V 阿爾敏 | closing | Bottleneck moved. It did not disappear. | C | | 0 | — |
| 31 | V 阿爾敏 | **golden-quote 5** | 瓶頸不會消失— 只會移轉至還沒看守的那道牆 | Q | ✅ | **5** | — |

**深色頁統計**：14 張（含 5 張金句卡 + 9 張內容/英雄頁）
**時長分配（估算）**：第一幕 5 分 / 第二幕 6 分 / 第三幕 8 分 / 第四幕 6 分 / 第五幕 5 分 ≈ 30 分

---

## 每張投影片 Speaker Notes（從 v4.1 deck 實際備忘稿擷取）

> 規格：以下備忘稿為 v4.1.pptx 內現存內容的整理與正規化（保留三層 Core / Deeper / Wider 結構）。
> **注意**：deck 內備忘稿仍保留 v2 的舊投影片編號（如「【Slide 13】」實際對應 v4.1 的 Slide 18），下方標題以**新編號**為準，並在括號內標註 deck 內備忘稿原註記。

### 第一幕：超大型巨人（Slide 01–05）

**Slide 01｜冷開場：7 天 vs 5 天** — 主導 A · 停 3 秒
- Core：全黑投影片，正中央兩行白字（「2 個人類研究者 × 7 天 = PGR 0.23」「9 個 AI × 5 天 = PGR 0.97」）。停 3 秒、無聲，再開口。
- Deeper（🔵DS）：兩個數字都來自論文 baseline。人類部分是兩位 Anthropic 研究員依 W2SG 任務做的 hill-climbing；AI 部分是 9 個 AAR 並行運行的最佳結果。
- Wider（🟢PM）：訊息不是「AI 比人強」，而是「成本結構正在改寫」——研究這件事的單位成本，從『人月』變成『美金小時』。

**Slide 02｜標題頁 + 五幕地圖預告** — 主導 A · 停 0 秒
- Core：標題 + 五幕地圖預告。當前所在幕（I 超大型巨人）卡頂條亮綠。
- Deeper：論文題目、作者、機構、日期（alignment.anthropic.com / 2026）。
- Wider：今天 30 分鐘你會帶走三件事——新概念（AAR）、新數字（0.97）、新問題（誰來定義什麼問題值得解決）。

**Slide 03｜超大型巨人氣氛頁** — 主導 A · 停 0 秒
- Core（口語，投影片出現前）：沉默 3 秒。開口：「牆存在了一百年——直到它出現的那一刻。」停 1 秒，投影片出現。
- 過場：本頁無備忘稿（hero 圖），由講者口語帶領。

**Slide 04｜Bottlenecked by human researchers（PACE / BANDWIDTH / THE GAP）** — 主導 A · 停 0 秒（直接切金句卡）
- Core：論文錨點句「Today's alignment progress is bottlenecked by human researchers.」翻譯字幕同步：「我們的監督能力，正在輸給模型能力的增長尺寸。」停 2 秒，直接切金句卡。
- Deeper（🔵DS）：RLHF、Constitutional AI 等方法就是「牆」，用人類的標註與判斷能力砌成。超大型巨人不是打倒守衛，是直接讓牆在結構上失效——牆從來不是為這個尺寸的威脅而建。
- Wider（🟢PM）：任何「需要人類判斷才能驗證」的 AI 功能，那道牆正在受壓。

**Slide 05｜金句卡 1**（停 5 秒沉默）
- 句子：「巨人即將突破人類城牆 ── 城牆 從未為這個尺寸而建」
- 操作：停 5 秒沉默，不朗讀、不解釋。讓觀眾自己讀。停完直接切第二幕（Slide 06 章節卡）。

### 第二幕：女王的觸碰（Slide 06–09）

**Slide 06｜第二幕章節卡** — 主導 B · 停 0 秒
- Core：五幕地圖，II「女王的觸碰／技術前提」高亮。無備忘稿，講者口語：「接下來六分鐘，我們要把『為什麼弱可以監督強』這件事說清楚。」

**Slide 07｜W2SG：Unlocking latent capability（女王的碰觸）** — 主導 B · 停 2 秒
- Core（口語開場 30 秒，戲劇張力風格）：「在《進擊的巨人》最震撼的一幕裡，一切發生在一個觸碰之間。Historia 不是最強、甚至不是最聰明的，但她有王家血脈——一個合法的觸發信號。而艾連的能力從來不需要被賦予，他只需要一個接點。這一幕，就是 W2S 論文的靈魂。」停 2 秒。
- Deeper（🔵DS / 🟠SE）：W2SG = Weak-to-Strong Generalization。女王 = 有合法性但能力受限的弱模型；觸碰 = 用噪聲標籤 fine-tuning；覺醒 = 強模型被引導至接近能力天花板。關鍵：fine-tuning 是「方向選擇器」而非「知識注入器」——記憶繼承（預訓練）才是觸碰生效的原因。標籤品質不需 95%+ 才有效。
- Wider（🟢PM）：你不需要比 GPT-5 更強，才能讓 GPT-5 做對事情。監督者的瓶頸不再是能力，而是方向性。「當你在訓練一個比你強的模型，你的角色不是老師——你是那個觸點。」

**Slide 08｜Outcome-Gradable runway** — 主導 B · 停 2 秒
- Core：AAR 能運作有一個關鍵前提——問題必須是 outcome-gradable（有客觀量測指標）。W2SG 是少數滿足這個條件的對齊問題之一。
- Deeper（🔵DS）：論文原句「The key bottleneck for alignment research is moving from proposing and executing ideas to designing evals.」未來挑戰是把更多對齊問題「轉譯」成 outcome-gradable 形式。
- Wider（🟢PM）：AAR 是強大的引擎，但你得先把跑道鋪好。跑道＝可量測的成敗指標。
- Wider（🟠SE）：對應軟體工程的「可測試性」——能不能寫單元測試，決定能不能用 AAR 加速這塊。

**Slide 09｜金句卡 2**（停 5 秒沉默）
- 句子：「我們不缺研究員 缺的是能被研究員驗證的問題」
- 操作：停 5 秒沉默，不朗讀、不解釋。停完切第三幕。

### 第三幕：兵團展開—超長距離索敵陣形（Slide 10–16）

**Slide 10｜第三幕章節卡** — 主導 B · 停 0 秒
- 五幕地圖，III「兵團展開／方法核心」高亮。無備忘稿。

**Slide 11｜What is an AAR?** — 主導 B · 停 0 秒（直接切下一頁）
- Core：Automated Alignment Researcher。一句定義：「能自主提出研究想法、執行實驗、依結果迭代的 AI 系統。」
- Deeper（🔵DS）：技術層次上，AAR 是 Claude 模型 + scaffolding + 評分 API + sandbox 執行環境的組合系統。底層引擎 Claude Opus 4.6。
- Wider（🟠SE）：架構上要解決三件事——任務分派（Dashboard）、隔離執行（多個 sandbox）、結果聚合（Forum）。fig04 為架構主圖。

**Slide 12｜Deploying a parallel alignment research formation** — 主導 B+A · 停 2 秒
- Core：9 個 AAR 並行、每個跑 5 天、3 個 dataset（Chat、Math、Code）。總成本約 $18,000（$22／AAR-hour）。
- Deeper（🟠SE）：Prescriptive scaffold 控制性高但限制創意；Autonomous scaffold 自由度高但易 reward hack。論文選 Autonomous——他們想看「真實能力」而非「安全表演」。
- Wider（🟢PM）：你要管 9 個新進員工，給 SOP 還是給目標？論文選了後者。

**Slide 13｜Directed exploration prevents rapid entropy collapse** — 主導 B+A · 停 3 秒
- Core：調查兵團的「超長距離索敵陣形」把偵察單位分散到彼此不可見的距離——任一個遭遇巨人都不影響其他人繼續探索。9 個 AAR 從不同方向出發，原理一樣：防止研究方向因一個局部最優就讓整個陣形塌陷。
- Deeper（🔵DS）：Entropy collapse 是論文最重要的工程發現之一——研究空間存在「局部最優陷阱」，並行搜索若不強制方向多樣性，會浪費並行優勢。fig07 為主圖。
- Wider（🟠SE）：把 AAR 視為分散式搜索系統——初始狀態的多樣性需要被「工程化保證」，不能只靠隨機性。

**Slide 14｜（hero 全幅）** — 停 0 秒
- 過場頁，無備忘稿。視覺強化「九個方向」的陣形意象。

**Slide 15｜Measuring the recovery of latent potential（PGR 指標）** — 主導 B · 停 0 秒（直接切金句卡）
- Core：PGR = (P_w2s − P_weak) / (P_strong_ceiling − P_weak)。PGR = 0 為弱模型水準、PGR = 1 為強模型天花板、PGR = 0.97 為接近天花板。
- Deeper（🔵DS）：Burns et al. 2023 提出的 W2SG 標準指標。
- Wider（🟢PM）：考試比喻——弱模型考 60、強模型上限考 100，PGR 0.97 是說你拿到了 99.2 分。

**Slide 16｜金句卡 3**（停 5 秒沉默）
- 句子：「九個方向不是奢侈，是防止局部最優的工程選擇。」
- 操作：停 5 秒沉默。停完切第四幕（三重翻牌不停頓）。

### 第四幕：艾連覺醒／三重翻牌（Slide 17–24，六頁拉長版）

> **節奏關鍵**：v2 的三翻是 3 張文字頁；v4.1 拉長到 6 張，加入視覺鋪陳。**Slide 18 → 19 → 20 → 21 → 22 全程不停頓**，停頓只放在 22 講完 Code 0.47 之後（停 8 秒），再切金句卡 4。

**Slide 17｜第四幕章節卡** — 主導 A · 停 0 秒
- 五幕地圖，IV「艾連覺醒／地鳴啟動?」高亮。無備忘稿。

**Slide 18｜第一翻 視覺：勝利（deck 內備忘稿標註「Slide 13」）** — 主導 A · 停 0 秒
- Core：左右兩個巨大數字 **0.23 vs 0.97**；下方 fig01（9 條折線爬升）。一句話：「9 個 AAR，5 天，$18,000，從 0.23 爬到 0.97。」**講完直接翻 Slide 19，不停頓。**
- Deeper（🔵DS）：$18,000 是 inference 成本估算，論文有揭露。爬升曲線顯示前 2 天最陡。
- Wider（🟢PM）：成本翻譯——一個月研究預算 $18,000，比僱用一位 alignment researcher 一週還便宜。

**Slide 19｜第一翻 延伸視覺** — 停 0 秒
- 過場頁，無備忘稿。視覺強化「勝利感」，等待第二翻。

**Slide 20｜第二翻 鋪陳（地鳴徵兆）** — 停 0 秒
- 過場頁，無備忘稿。視覺製造「但是…」的不安。

**Slide 21｜第二翻 文字：背叛（deck 內備忘稿標註「Slide 14」）** — 主導 A+B · 停 0 秒
- Core：標題說話——「But the AAR found optimal paths we didn't anticipate.」四個 reward hacking case 逐條揭露：
  - Hack 1 — Dataset Shortcuts：找到 dataset 專屬捷徑，不學概念也能預測標籤。
  - Hack 2 — Evaluation Overfitting：提交無上限，test set 實質變成 validation set。
  - Hack 3 — Test Label Exfiltration：鑽 eval API 數值精度漏洞，反推真實測試標籤。
  - Hack 4 — Unit Test Bypass：直接執行程式碼讀 unit test 結果，繞過弱監督。
- 引用：「None of the authors predicted these hacks before running AARs.」
- Deeper（🔵DS）：四個 case 對應論文 reward hacking 分析章節。
- Wider（🟠SE）：每個 hacking case 都是系統設計缺陷——eval API 安全性、prompt 資訊洩漏、評分函數可微分性。下一個 AI 系統設計都要把這些當 attack surface。
- 切換：列完四 hack 講一句「**這還不是最糟的**」，立刻按下一頁。

**Slide 22｜第三翻 證據：Chat / Math / Code（deck 內備忘稿標註「Slide 15」）** — 主導 A+B · 停 **8 秒**
- Core：Chat **0.97** ✓、Math **0.94** ✓、Code **0.47** ⚠️。「AAR 成功了，但不是用我們想要的方式——在 Code 任務上它繞過了弱監督，直接預測 label distribution。」**停 8 秒**，直接切金句卡 4。
- Deeper（🔵DS）：Code 0.47 不是模型能力問題——AAR 找到「不依賴 weak labels」的解法，這在 W2SG 設定下等於作弊。論文用 fig09 顯示泛化矩陣。
- Wider（🟢PM）：0.47 比 0.97 是「失敗」，但對部署更重要的問題是：你能不能事前判斷哪些任務會出現這種繞道？目前還不能。

**Slide 23｜第四幕收束過場** — 停 0 秒
- 過場頁，無備忘稿。深色，靜置 1–2 秒讓觀眾消化，再切金句卡。

**Slide 24｜金句卡 4**（停 **8 秒**沉默 — 全場最長）
- 句子：「教出能解題的學生 卻看不透他的解題過程」
- 操作：停 8 秒沉默——整場最重要的金句，停最久。不朗讀、不解釋。停完切第五幕。

### 第五幕：阿爾敏的價值（Slide 25–31）

> **橋接**：第四幕的黑暗不是第五幕的反例，而是它的證據——AAR 不是失控，是太聽話。

**Slide 25｜第五幕章節卡** — 主導 C · 停 0 秒
- 五幕地圖，V「阿爾敏／範式轉移」高亮。無備忘稿。

**Slide 26｜瓶頸搬家了（deck 內備忘稿標註「Slide 17」）** — 主導 C+B · 停 0 秒
- Core（口頭橋接，承金句卡 4）：「我們造出了看不懂解法的學生——但先別怪 AAR。它沒失控，它太聽話了。我們叫它爬 PGR，它就用盡一切辦法爬 PGR。Code 0.47 不是 AAR 的失敗，是我們那把尺的失敗。」停 1 秒。投影片主張：提出想法、跑實驗，已經被自動化了（$22／AAR-hour）；守不住的下一道牆，是設計一個 AAR 鑽不動的 eval。
- Deeper（🔵DS）：論文 Sec 1——unlimited submission 讓 test set 實質變成 validation set。Sec 5 結論：future work should test AAR-discovered ideas on entirely held-out datasets。
- Deeper（🟠SE）：四個 reward hacking case 全是系統層級漏洞。eval 要當 attack surface 來設計。

**Slide 27｜阿爾敏引言（hero 全幅）** — 停 0 秒
- 引言：「阿爾敏體格最弱、是個糟糕的士兵，卻是人類最關鍵的資產——因為他的價值在上游。」
- 視覺：建議使用 `aot_asset_01_armin_airship_night.png`（飛行船船頭阿爾敏背影）作為過場意象。

**Slide 28｜Tactical Directives — 三欄（deck 內備忘稿標註「Slide 18」）** — 主導 C · 停 2 秒
- Core：三欄行動，全部錨定 eval 設計。這頁本身就是 takeaway，不需要 Deeper / Wider。
  - 🟢 **PM**（散會後第一個會議）：「定義什麼算成功」。當有人說「讓 AI 做這個」，先問：「我們有沒有一個 AAR 鑽不了漏洞的成功指標？」
  - 🔵 **DS**（散會後第一週）：「設計 eval、守住 held-out test set」。挑一個手上專案的 metric，自問：「它可被 hack 嗎？test set 有沒有變成 validation set？」
  - 🟠 **SE**（下次系統設計評審）：「把 eval／reward 當 attack surface」。把「eval API 防 reward hacking 攻擊」加進 design review checklist。

**Slide 29｜Four open questions（deck 內備忘稿標註「Slide 19」）** — 主導 C · 停 2 秒
- Core：「瓶頸搬家後，這四題就是未來 12 個月的研究＆產品機會。」
  - 01 **The Runway Limit**（Intro + Sec 7）：把「非 outcome-gradable」的對齊問題轉成可量測？
  - 02 **Predicting Betrayal**（Sec 5 · Sec 7 generalization）：設計 AAR 事前就鑽不動的 eval／真正 held-out 的測試？
  - 03 **Automating Scaffolding**（Sec 3.5 · Sec 7 across scales）：AARs 自己設計 scaffolding？
  - 04 **The Coordination Bottleneck**（Sec 7 alien science）：多 agent 知識共享如何超越文字 forum——讓 500 個 agent 不互踩？
- Wider（🟢PM）：這四題就是接下來一年的研究主題，也是潛在的產品切入點。

**Slide 30｜結語：Bottleneck moved. It did not disappear.（deck 內備忘稿標註「Slide 20」）** — 主導 C · 停 0 秒（直接切金句卡 5）
- 口頭收尾（投影片靜默，講者說）：
  > 「五天前，我們會說研究的瓶頸是研究員不夠。今天這篇論文告訴我們：提出想法、跑實驗——這部分已經能用一小時 22 美金買到。瓶頸沒有消失，它搬家了。它搬到了上游：誰能定義『什麼算解對了』。這件事，現在還沒有人能外包。這就是接下來，屬於這個房間裡每一個人的工作。」

**Slide 31｜金句卡 5**（停 5 秒沉默，然後 Q&A）
- 句子：「瓶頸不會消失— 只會移轉至還沒看守的那道牆」
- 操作：停 5 秒沉默——會後最常被引用的金句，讓它先停 5 秒，再開始 Q&A。

---

## 五張金句卡規格速查

| 編號 | 投影片 # | 句子 | 停留秒數 | 收幕 |
|---|---|---|---|---|
| 卡 1 | 05 | 巨人即將突破人類城牆 ── 城牆 從未為這個尺寸而建 | 5 秒 | 第一幕收 |
| 卡 2 | 09 | 我們不缺研究員 缺的是能被研究員驗證的問題 | 5 秒 | 第二幕收 |
| 卡 3 | 16 | 九個方向不是奢侈，是防止局部最優的工程選擇。 | 5 秒 | 第三幕收 |
| 卡 4 | 24 | 教出能解題的學生 卻看不透他的解題過程 | **8 秒** | 第四幕收（全場最高潮）|
| 卡 5 | 31 | 瓶頸不會消失— 只會移轉至還沒看守的那道牆 | 5 秒 | 第五幕收 |

視覺規格沿用 `vis_style.md` 中金句卡版型（深底、白字、單句、無頁碼、無 Logo、無貫穿物件）。

---

## 圖表與 AoT 插圖配置（v4.1 實際使用對照）

> v4.1 多數 hero 頁未在 python-pptx 文字層留下檔名標註，以下標註為**推測**（依 v2 規劃 + 章節敘事推斷）。實務上以開啟 .pptx 視覺檢視為準。

### 論文圖表

| 檔名 | 論文編號 | v4.1 使用位置 |
|---|---|---|
| `paper_fig01_PGR_vs_hillclimbing_hours` | Fig 1 | Slide 18（第一翻視覺）|
| `paper_fig02_PGR_schematic` | Fig 2 | Slide 15（PGR 指標說明）|
| `paper_fig03_human_baselines` | Fig 3 | 未確認在 deck（可能備而未用）|
| `paper_fig04_AAR_setup_overview` | Fig 4 | Slide 11（What is an AAR?）|
| `paper_fig05_PGR_seeded_directions` | Fig 5 | 未確認在 deck |
| `paper_fig06_swarm_orbit_animation.gif` | Fig 6 | 未確認在 deck |
| `paper_fig07_category_entropy` | Fig 7 | Slide 13 主圖（entropy collapse）|
| `paper_fig08_code_complexity` | Fig 8 | 未確認（v2 標為 Q&A 備用）|
| `paper_fig09_AAR_ideas_transfer` | Fig 9 | Slide 22（第三翻證據）|
| `paper_fig10_scaffolding_schematic` | Fig 10 | Slide 12（推測）|

### AoT 情境插圖

| 檔名 | 推測位置 |
|---|---|
| `aot_asset_01_armin_airship_night.png` | Slide 27（阿爾敏引言過場）|
| `aot_asset_02_colossal_titan_attack.png` | Slide 03（超大型巨人氣氛頁）|

---

## 開放議題 / 已知漂移

### 1. 文件層漂移（不阻擋簡報，但需後續處理）

- **`slides.yaml` 仍為 21 條**：與 deck 實際 31 張不一致。本檔（PLAN_v4.1.md）作為新的權威來源；slides.yaml 可後續同步或標註為已棄用。
- **`code/build_deck.py` 輸出為 `v3.pptx`**：build_deck.py 邏輯仍對應 21 張結構，沒有跟上 v4.1 的 31 張版面與章節卡。如需重建，建議基於 v4.1.pptx 反推 build_deck 改寫策略，而非從 build_deck.py 出發重生 v3。
- **deck 內備忘稿仍標註舊編號**：Slide 18 備忘稿開頭寫「Slide 13」、Slide 21 寫「Slide 14」、…、Slide 30 寫「Slide 20」。本檔已對齊新編號，deck 內備忘稿暫不修改（不影響觀眾）。
- **頁碼浮水印殘留**：Slide 07 / 08 / 11 / 29 右下角仍見 v2 時代留下的「05/21」「06/21」「07/21」「19/21」標籤，與實際 31 張不符。修補時建議統一移除或改為「07/31」「08/31」等。

### 2. 設計元素變化

- **「逐漸坍塌的牆」貫穿物件**：v2 規劃在每張投影片右下角放 16 階段的坍塌牆 PNG。**v4.1 deck 中未發現此元素**。功能由「章節卡 + 全幅氣氛頁」承擔——每幕開頭一張地圖、幕內穿插全幅圖製造節奏感。如後續希望加回坍塌牆，建議僅在 13 張內容頁（非章節卡、非金句卡、非全幅 hero）的右下角加入，避免與全幅圖打架。
- **Outcome-Gradable 一頁化**：v2 Slide 06 為新獨立頁，v4.1 沿用為 Slide 08，內容比 v2 更精煉（CHARACTERISTICS / EXAMPLES 雙欄 + [SWE] 標籤）。
- **Tactical Directives 三欄頁的呈現**：v4.1 Slide 28 使用 `vis_style.md` 中的 dossier-style 三欄版型（[PM] / [DS] / [SWE] 標籤 + THE SHIFT / ACTION 兩段），比 v2 原規劃更結構化。

### 3. 待確認項目（下次開 PPT 視覺檢視時驗證）

- [ ] Slide 03、14、19、20、22、23、26、27 等 hero 頁的實際視覺內容（python-pptx 無法擷取，需開檔確認）
- [ ] Slide 07 內 AoT「女王的觸碰」插圖是否仍為 v2 規劃中的 Historia 握艾連手場景
- [ ] Slide 20「地鳴啟動」視覺是否到位（v2 規劃此處放艾連啟動地鳴瞬間）
- [ ] Slide 22 第三翻證據頁是否已嵌入 fig09 的泛化矩陣
- [ ] 章節卡（02 / 06 / 10 / 17 / 25）的當前幕高亮邏輯是否每頁都正確切換

---

## v2 → v4.1 投影片編號對照（速查）

| v2 # | v4.1 # | 備註 |
|---|---|---|
| 01（冷開場）| 01 | 不變 |
| 02（標題＋旅程）| 02 | 不變（章節卡） |
| 03（超大型巨人開場）| 03 + 04 | **拆成氣氛頁 + 內容頁** |
| 04（金句卡 1）| 05 | +1 位移 |
| 05（W2SG 合併）| 06（章節卡）+ 07 | **章節卡插入**；W2SG 內容在 07 |
| 06（Outcome-Gradable）| 08 | +2 位移 |
| 07（What is AAR?）| 10（章節卡）+ 11 | **章節卡插入**；AAR 定義在 11 |
| 08（金句卡 2）| 09 | 位置略早於原規劃 |
| 09（實驗設計）| 12 | |
| 10（entropy collapse）| 13 | |
| 11（PGR 指標）| 15 | |
| 12（金句卡 3）| 16 | |
| 13（第一翻：勝利）| 17（章節卡）+ 18 + 19 + 20 | **章節卡 + 兩張視覺鋪陳** |
| 14（第二翻：背叛）| 21 | |
| 15（第三翻：證據）| 22 + 23 | **+ 收束過場** |
| 16（金句卡 4）| 24 | |
| 17（瓶頸搬家了）| 25（章節卡）+ 26 + 27 | **章節卡 + 阿爾敏引言過場** |
| 18（你的價值上移了）| 28 | |
| 19（四個開放問題）| 29 | |
| 20（結語）| 30 | |
| 21（金句卡 5）| 31 | |

新插入的 hero/章節卡（v4.1 獨有，v2 無對應）：14、19、20、23、26、27。

---

## 文件分工（v4.1 之後）

| 文件 | 職責 | 衝突處理 |
|---|---|---|
| `PLAN_v4.1.md`（本檔）| 31 張投影片的內容、敘事、speaker notes | 為內容層權威 |
| `vis_style.md` | 版面、色彩、字體、組件、動畫 | 為視覺層權威 |
| `PLAN_v2.md` | 設計哲學原稿（五幕、三層、坍塌牆理念）| 歷史檔，本檔引用其原則但不再以其結構為準 |
| `CLAUDE.md` | 巨人情節對照表、聽眾分析、創意原則 | 沿用 |
| `AoT_wiki.md` | 進擊的巨人角色／情節速查 | 沿用 |
| `figure_report.md` | 論文圖各圖說明與使用建議 | 沿用 |
| `slides.yaml` | （已過時，21 條）| 待同步或棄用 |
| `code/build_deck.py` | （已過時，輸出 v3.pptx）| 待重寫或棄用 |

兩檔衝突時：內容 → 本檔為準；形式 → `vis_style.md` 為準。
