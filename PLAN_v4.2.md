# AAR 投影片整合計畫 v4.2（鏡像現行投影片）

## 專案資訊

- 投影片檔案：`ppt/AAR_Paper_Sharing_v4.2.pptx`（**34 張**，13.333" × 7.5"）
- 前版：`ppt/AAR_Paper_Sharing_v4.1.pptx`（31 張）— `code/patch_slides.py` 重建 4 張 raster 頁後，使用者手動大幅擴充與重整
- 論文來源：https://alignment.anthropic.com/2026/automated-w2s-researcher/
- 本版日期：2026-05-28
- 聽眾：DS × 15、SE × 7、PM × 5（總 27 人）
- 時間預算：30 分鐘 / 五幕（slides 01–33）+ outro（34）

---

## 為什麼有 v4.2：從 31 張擴充至 34 張

v4.1 → v4.2 的變化分兩個層次：

**層次一：patch_slides.py 重建（v4.1 完成後即寫入）**
Slides 1、18、22、26 原為 raster-image-only 頁，已由 `code/patch_slides.py` 重建為可編輯的 python-pptx 形狀，內容對齊 `build_deck.py` 原始設計。

**層次二：使用者手動大幅擴充與重整（v4.2 現狀）**

| 變化類型                | v4.1（31 張）                                  | v4.2 現況（34 張）                                                  |
| ----------------------- | ---------------------------------------------- | ------------------------------------------------------------------- |
| 總頁數                  | 31                                             | **34**                                                        |
| 新增 Slide 02           | 無                                             | **教宗良十四世 AI 通諭情境圖**（image1.png）— 第一幕開場鉤子 |
| 新增 Slide 34           | 無                                             | **"Thank you" 文字頁**（outro，不計入 30 分鐘）               |
| 第三幕                  | 7 張（slides 10–16）                          | **8 張（slides 13–20）**，含 2 張 GIF 動畫 + 形成陣形圖      |
| 金句卡 3                | "九個方向不是奢侈，是防止局部最優的工程選擇。" | **"研究方向的多樣探索 防止過早收斂到局部次優解"**             |
| 五幕地圖副標            | 幕別名稱（如「超大型巨人」）                   | **幕別 + 巨人情節副標（如「瑪利亞之牆」「沉睡的巨人」）**     |
| PGR 說明位置            | Act III（v4.1 Slide 15）                       | **Act II（v4.2 Slide 09）**                                   |
| AAR 定義頁              | Act II（v4.1 Slide 11）                        | **Act II（v4.2 Slide 10）**                                   |
| Outcome-Gradable        | Act II（v4.1 Slide 08）                        | **Act II（v4.2 Slide 11）**                                   |
| Scalable Oversight 兩難 | Act V hero（v4.1 Slide 26，重建頁）            | **Act V content（v4.2 Slide 28）**                            |
| Armin 引言 + 英雄頁     | Act V hero（v4.1 Slide 27）                    | **Act V hero（v4.2 Slide 29，含 Armin 圖）**                  |

---

## 沿用 v4.1 的設計哲學（不重寫，引用 PLAN_v4.1.md）

下列原則在 v4.2 仍然有效：

| 設計原則                                    | 在 v4.2 的狀態                |
| ------------------------------------------- | ----------------------------- |
| 五幕分主導架構（A 戲劇／B 技術／C PM）      | 沿用；幕別主導風格不變        |
| 三層內容系統（Core / Deeper-DS / Wider-PM） | 沿用；備忘稿仍維持三層結構    |
| 三重翻牌敘事弧（勝利→背叛→證據）          | 沿用；slides 22→23→24       |
| 五張金句卡（深色／單句／不解釋）            | 沿用；編號改為 06/12/20/26/33 |
| 巨人情節對照表                              | 沿用；見 `CLAUDE.md`        |
| 視覺規格                                    | 沿用；見 `vis_style.md`     |

---

## 34 張投影片對照表

> **Role 詞彙**：`cold-open` / `context` / `chapter-card` / `content` / `hero` / `golden-quote` / `closing`
> **主導**：A=戲劇張力 / B=技術精準 / C=PM 行動 / Q=金句卡 / —=無說明文字頁
> **深色** ✅ = 深色背景
> **停頓**：頁面講完後刻意保留的沉默秒數

| #  | 幕            | Role                              | 標題 / 內容摘要                                                                                                           | 主導 | 深色 | 停              | 素材                                                                         |
| -- | ------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---- | ---- | --------------- | ---------------------------------------------------------------------------- |
| 01 | I 超大型巨人  | cold-open                         | 兩欄對比：「2 Human Researchers × 7 Days = PGR 0.23」/ 「9 Autonomous AI Agents × 5 Days = PGR 0.97」                   | A    | ✅   | 3               | — (python-pptx 形狀)                                                        |
| 02 | I 超大型巨人  | context                           | （全幅圖：教宗良十四世 AI 通諭情境）                                                                                      | A    | ✅   | 0               | image1.png (`pope_leo_xiv_ai_quote_2026.png`)                              |
| 03 | I 超大型巨人  | chapter-card                      | "Automated Alignment Researcher (AAR)" + 五幕地圖（I 高亮）副標：瑪利亞之牆 / 沉睡的巨人 / 索敵陣形 / 地鳴啟動 / 接任團長 | A    | ✅   | 0               | —                                                                           |
| 04 | I 超大型巨人  | hero                              | 「那一天，人類想起了，曾經被那群傢伙支配的恐懼，以及被囚禁在鳥龍的屈辱。」＋ AoT 全幅圖                                   | A    | ✅   | 0               | image2.png（推測 `aot_asset_02_colossal_titan_attack.png`）                |
| 05 | I 超大型巨人  | content                           | "Alignment progress is bottlenecked by human researchers" — PACE / BANDWIDTH / THE GAP                                   | A    | ✅   | 0               | —                                                                           |
| 06 | I 超大型巨人  | **golden-quote 1**          | 巨人即將突破人類城牆 ── 牆從未為這個尺寸而建                                                                            | Q    | ✅   | **5**     | —                                                                           |
| 07 | II 女王的觸碰 | chapter-card                      | AAR + 五幕地圖（II 高亮：女王的觸碰 / 沉睡的巨人）                                                                        | B    | ✅   | 0               | —                                                                           |
| 08 | II 女王的觸碰 | content                           | "Weak-to-Strong Generalization (W2SG): Unlocking latent capability" — 「女王的觸碰」— Weak→Strong 鏈                   | B    |      | 2               | image3.png                                                                   |
| 09 | II 女王的觸碰 | content                           | "Measuring the recovery of latent potential" — PGR 指標圖（弱基準 / AAR 0.97 / 強天花板）                                | B    |      | 0               | image4.png（`paper_fig02_PGR_schematic`）                                  |
| 10 | II 女王的觸碰 | content                           | "What is an AAR?" — Claude Model / Scaffolding / Eval API + Sandbox 組件說明 + 架構圖                                    | B    |      | 0               | image5.png（`aar_research_cycle_scaffolding.png`）                         |
| 11 | II 女王的觸碰 | content                           | "The prerequisite for automation is an 'Outcome-Gradable' runway" — 兩欄：Gradable vs Non-Gradable                       | B    |      | 0               | —                                                                           |
| 12 | II 女王的觸碰 | **golden-quote 2**          | 我們不缺研究員 缺的是能被研究員驗證的問題                                                                                 | Q    | ✅   | **5**     | —                                                                           |
| 13 | III 兵團展開  | chapter-card                      | AAR + 五幕地圖（III 高亮：兵團展開 / 索敵陣形）                                                                           | B    | ✅   | 0               | —                                                                           |
| 14 | III 兵團展開  | content                           | "Deploying a parallel alignment research formation" — COMPUTE ENGINE / SCALE / DURATION / COST 四格                      | B+A  |      | 2               | image6.png（`paper_fig04_AAR_setup_overview_v5.svg`）                      |
| 15 | III 兵團展開  | content                           | "Diverse research directions yields much better hill-climbing efficiency"                                                 | B    |      | 0               | image8.png（`paper_fig05_PGR_seeded_directions`）                          |
| 16 | III 兵團展開  | content                           | "Directed exploration prevents rapid entropy collapse" — The Threat / The Solution                                       | B+A  |      | 3               | image9.png（`paper_fig07_category_entropy`）                               |
| 17 | III 兵團展開  | hero/animation                    | （GIF：swarm orbit 動畫 variant 1）                                                                                       | —   | ✅   | 0               | image11.gif（`paper_fig06_swarm_orbit_animation_dark.gif`）                |
| 18 | III 兵團展開  | hero/animation                    | （GIF：swarm orbit 動畫 variant 2）                                                                                       | —   | ✅   | 0               | image12.gif（`paper_fig06` 另一變體）⚠️ 白色背景，暫時不播放，待測試     |
| 19 | III 兵團展開  | hero                              | （全幅圖：AoT 超長距離索敵陣形 ── 煙霧彈對應 Forum）                                                                    | —   | ✅   | 0               | image13.png                                                                  |
| 20 | III 兵團展開  | **golden-quote 3**          | 研究方向的多樣探索 防止過早收斂到局部次優解                                                                               | Q    | ✅   | **0**→IV | —                                                                           |
| 21 | IV 艾連覺醒   | chapter-card                      | AAR + 五幕地圖（IV 高亮：艾連覺醒 / 地鳴啟動）                                                                            | A    | ✅   | 0               | —                                                                           |
| 22 | IV 艾連覺醒   | **content（第一翻：勝利）** | "The AAR rapidly approaches the theoretical ceiling" — Human 0.23 / AAR 0.97 兩欄 + PM badge 說明文                      | A    | ✅   | 0               | image14.png（`paper_fig01_PGR_vs_hillclimbing_hours`）                     |
| 23 | IV 艾連覺醒   | content（第二翻：背叛）           | "But the AAR found optimal paths we didn't anticipate" — EXPECTATION vs EXPLOITATION + Hack 1–4                         | A+B  |      | 0               | —                                                                           |
| 24 | IV 艾連覺醒   | **content（第三翻：證據）** | "Failed the alignment goal" — Chat 0.97 / Math 0.94 / Code 0.47 ⚠️ + fig09 + 說明段落                                  | A+B  |      | **8**     | image15.png（`paper_fig09_AAR_ideas_transfer`）                            |
| 25 | IV 艾連覺醒   | hero（收束過場）                  | （全幅圖：為 AoT 地鳴場景 `aot_asset_04_the_rumbling_titans_march_text`）                                               | A    | ✅   | 0               | image17.png                                                                  |
| 26 | IV 艾連覺醒   | **golden-quote 4**          | 教出能解題的學生 卻看不透他的解題過程                                                                                     | Q    | ✅   | **8**     | —                                                                           |
| 27 | V 阿爾敏      | chapter-card                      | AAR + 五幕地圖（V 高亮：阿爾敏 / 接任團長）                                                                               | C    | ✅   | 0               | —                                                                           |
| 28 | V 阿爾敏      | content                           | "The Scalable Oversight Dilemma: Control versus Creativity" — Prescriptive（左）vs Autonomous（右）兩欄 + fig10 ×2      | C+B  | ✅   | 3               | image18.png + image19.png（`paper_fig10_scaffolding_schematic` 左/右裁切） |
| 29 | V 阿爾敏      | hero                              | 「什麼都無法捨棄的人，就什麼都改變不了 ─ Armin Arlert」+ AoT Armin 全幅圖  (`aot_asset_01_armin_airship_night`))      | C    |      | 0               | image20.png（`aot_asset_01_armin_airship_night.png`）                      |
| 30 | V 阿爾敏      | content                           | "Tactical Directives: What this means for your architecture" — Armin 引言 + [PM]/[DS]/[SWE] 三欄                         | C    |      | 2               | —                                                                           |
| 31 | V 阿爾敏      | content                           | "The frontier of automated alignment: Four open questions" — 01–04                                                      | C    |      | 2               | —                                                                           |
| 32 | V 阿爾敏      | closing                           | "Bottleneck moved. It did not disappear." — 口頭收尾                                                                     | C    |      | 0               | —                                                                           |
| 33 | V 阿爾敏      | **golden-quote 5**          | 瓶頸不會消失— 只會移轉至還沒看守的那道牆                                                                                 | Q    | ✅   | **5**     | —                                                                           |
| 34 | Outro         | closing                           | "Thank you for listening (watching)"                                                                                      | —   |      | —              | —                                                                           |
**深色頁統計**（確認）：16 張（含 5 張金句卡 + 11 張 hero/context/chapter 頁）
**時長分配（估算）**：第一幕 5 分 / 第二幕 6 分 / 第三幕 8 分 / 第四幕 6 分 / 第五幕 5 分 ≈ 30 分（slide 34 outro 不計）

---

## 五張金句卡規格速查

| 編號 | 投影片 # | 句子                                           | 停留秒數          | 收幕                   |
| ---- | -------- | ---------------------------------------------- | ----------------- | ---------------------- |
| 卡 1 | 06       | 巨人即將突破人類城牆 ── 牆從未為這個尺寸而建 | 5 秒              | 第一幕收               |
| 卡 2 | 12       | 我們不缺研究員 缺的是能被研究員驗證的問題      | 5 秒              | 第二幕收               |
| 卡 3 | 20       | 研究方向的多樣探索 防止過早收斂到局部次優解    | 0 秒（直接切 IV） | 第三幕收               |
| 卡 4 | 26       | 教出能解題的學生 卻看不透他的解題過程          | **8 秒**    | 第四幕收（全場最高潮） |
| 卡 5 | 33       | 瓶頸不會消失— 只會移轉至還沒看守的那道牆      | 5 秒              | 第五幕收               |

> 注意：金句卡 3（Slide 20）停頓 0 秒——直接切入第四幕章節卡（Slide 21），以高速節奏承接三重翻牌。

---

## 每張投影片 Speaker Notes（從 v4.2 deck 實際備忘稿擷取）

> **注意**：deck 內備忘稿仍保留舊編號（如「【Slide 07】」實際對應 v4.2 的 Slide 10），下方以**新編號**為準，括號內標原 deck 備忘稿舊號。

---

### 第一幕：超大型巨人（Slides 01–06）

**Slide 01｜冷開場：PGR 0.23 vs 0.97** — 主導 A · 停 3 秒

- Core：全黑投影片，兩欄對比。左欄（灰框）：「2 Human Researchers × 7 Days = PGR **0.23**」；右欄（綠框）：「9 Autonomous AI Agents × 5 Days = PGR **0.97**」。
- 口頭 hook：「看過或聽過進擊的巨人的人請舉手」「相信 AI 末日論的人請舉手」停 3 秒無聲，再開口。
- Deeper（🔵DS）：兩個數字都來自論文。人類部分是兩位 Anthropic 研究員 7 天的成果；AI 部分是 9 個 AAR 並行運行的最佳結果。
- Wider（🟢PM）：訊息不是「AI 比人強」，而是「成本結構正在改寫」——研究的單位成本從「人月」變成「美金小時」。

**Slide 02｜教宗 AI 通諭情境圖** — 主導 A · 停 0 秒

- Context（口頭 hook 備用）：2026 年 5 月 25 日，教宗良十四世發布首份 AI 通諭《崇高的人性》（*Magnifica Humanitas*），全文超過 4 萬字，是天主教會史上首次以 AI 為核心主題的通諭。Anthropic 共同創辦人 Chris Olah 受邀出席梵蒂岡發表儀式並致詞。
- 這頁作為時代感入場：連天主教都開始重新定義 AI 時代的人類尊嚴——這不是技術問題，是文明問題。
- 過場：本頁無備忘稿文字，由講者口語帶領，直接切章節卡。

**Slide 03｜標題頁 + 五幕地圖** — 主導 A · 停 0 秒

- Core：「今天會用進擊的巨人 5 幕場景來進行論文分享。瑪利亞之牆存在了一百年，保護居民免於牆外巨人攻擊——直到超大型巨人出現的那一刻。」
- 五幕副標：I 瑪利亞之牆 / II 沉睡的巨人 / III 索敵陣形 / IV 地鳴啟動 / V 接任團長

**Slide 04｜AoT 引言 + 超大型巨人氣氛圖** — 主導 A · 停 0 秒

- 投影片文字：「那一天，人類想起了，曾經被那群傢伙支配的恐懼，以及被囚禁在鳥龍的屈辱。」
- 口頭說明：「以現今 AI 時代而言，像 Claude 這樣、具有超越人類能力的 LLM，可以看成這裡的超大型巨人；牆就是人類用來控制這些 LLM 的技術，一般稱作對齊（Alignment）。」

**Slide 05｜Bottlenecked by human researchers（PACE / BANDWIDTH / THE GAP）** — 主導 A · 停 0 秒（直接切金句卡）

- Core：「保護人類的牆，正在輸給牆外巨人的進化速度。」論文錨點句：「Today's alignment progress is bottlenecked by human researchers.」
- Deeper（🔵DS）：RLHF、Constitutional AI 等方法就是「牆」，用人類的標註與判斷能力砌成。超大型巨人不是打倒守衛，是直接讓牆在結構上失效——牆從來不是為這個尺寸的威脅而建。
- Wider（🟢PM）：任何「需要人類判斷才能驗證」的 AI 功能，那道牆正在受壓。

**Slide 06｜金句卡 1**（停 5 秒沉默）

- 句子：「巨人即將突破人類城牆 ── 牆從未為這個尺寸而建」
- 操作：停 5 秒，不朗讀、不解釋。停完直接切第二幕（Slide 07 章節卡）。

---

### 第二幕：女王的觸碰（Slides 07–12）

**Slide 07｜第二幕章節卡** — 主導 B · 停 0 秒

- Core：五幕地圖，II「女王的觸碰 / 沉睡的巨人」高亮。
- 口頭過渡：「當 LLM 的能力已經超越人類，要怎麼監督它？這是 weak-to-strong supervision 的核心問題。」

**Slide 08｜W2SG：Unlocking latent capability（女王的觸碰）** — 主導 B · 停 2 秒

- Core（口語開場 30 秒，A 戲劇張力）：「在《進擊的巨人》艾連巨人能力完全覺醒的瞬間，一切發生在一個觸碰之間。女王 Historia 不是最強、甚至不是最聰明的，但她有王家血脈——一個合法的觸發信號。而艾連的能力從來不需要被賦予，他只需要一個接點。這一幕，就是 W2S 論文的靈魂。」停 2 秒，再切機制圖。
- 投影片三段鏈：Weak Supervisor（提供有噪聲的標籤）→ Strong Student（以噪聲標籤 fine-tuning）→ The Result（fine-tuning 是「方向選擇器」，喚醒預訓練既有知識；學生超越老師的能力上限）
- 附句：「弱者的觸碰提供方向，不提供能力。它喚醒了強者體內早已存在的力量。」
- Deeper（🔵DS / 🟠SE）：標籤品質不需 95%+；fine-tuning 是方向選擇器而非知識注入器。
- Wider（🟢PM）：你不需要比 GPT-5 更強，才能讓 GPT-5 做對事情。監督者的瓶頸不再是能力，而是方向性。

**Slide 09｜PGR 指標說明** — 主導 B · 停 0 秒（直接切下一頁）

- Core：PGR = (P_w2s − P_weak) / (P_strong_ceiling − P_weak)。PGR 0 = 弱模型水準 / PGR 1 = 強模型天花板 / PGR 0.97 = 接近天花板。
- 圖說明三條線：The Weak Model Baseline（老師的上限）/ The student's actual performance（AAR PGR: 0.97）/ What the student could achieve with perfect ground-truth labels（強模型天花板）
- Deeper（🔵DS）：Burns et al. 2023 提出，是 W2SG 領域標準指標。
- Wider（🟢PM）：考試比喻——弱模型考 60、強模型上限 100，PGR 0.97 = 拿到 99.2 分。

**Slide 10｜What is an AAR?（deck 內備忘稿標註「Slide 07」）** — 主導 B · 停 0 秒

- Core：「能自主提出研究想法、執行實驗、並依結果迭代的 AI 系統。」
- 組件：Claude Model（底層推理引擎 Claude Opus 4.6）/ Scaffolding（決定 AAR 如何規劃、行動、迭代的控制層）/ Eval API + Sandbox（評分介面 + 隔離執行環境）
- Deeper（🔵DS）：技術層次：AAR = Claude 模型 + scaffolding + 評分 API + sandbox 的組合系統。
- Wider（🟠SE）：架構要解決三件事——任務分派（Dashboard）、隔離執行（多個 sandbox）、結果聚合（Forum）。

**Slide 11｜Outcome-Gradable runway（deck 內備忘稿標註「Slide 06」）** — 主導 B · 停 0 秒（直接切金句卡）

- Core：AAR 能運作有一個關鍵前提——問題必須是 outcome-gradable（有客觀量測指標）。
- 左欄（Outcome-Gradable）— CHARACTERISTICS：Objective metrics · immediate detection · automated scoring；EXAMPLES：W2SG · Math Verification · Code Execution
- 右欄（Non-Outcome-Gradable）— CHARACTERISTICS：Subjective · requires human vibe-checks · fuzzy；EXAMPLES：「Make the AI more ethical」「Improve creative writing」
- Deeper（🔵DS）：論文原句「The key bottleneck for alignment research is moving from proposing and executing ideas to designing evals.」
- Wider（🟢PM）：AAR 是強大的引擎，但你得先把跑道鋪好。跑道 = 可量測的成敗指標。
- Wider（🟠SE）：對應軟體工程的「可測試性」——能不能寫單元測試，決定能不能用 AAR 加速這塊。

**Slide 12｜金句卡 2**（停 5 秒沉默）

- 句子：「我們不缺研究員 缺的是能被研究員驗證的問題」
- 操作：停 5 秒，不朗讀、不解釋。停完切第三幕。

---

### 第三幕：兵團展開——超長距離索敵陣形（Slides 13–20）

> **節奏關鍵**：本幕最長（8 張），包含兩段 GIF 動畫（Slides 17–18）與陣形圖（Slide 19）。動畫段不停頓，讓視覺效果帶節奏。金句卡 3（Slide 20）停 0 秒，直接切入第四幕。

**Slide 13｜第三幕章節卡** — 主導 B · 停 0 秒

- 五幕地圖，III「兵團展開 / 索敵陣形」高亮。無備忘稿，講者口語過渡。

**Slide 14｜Deploying a parallel alignment research formation（deck 內備忘稿標註「Slide 09」）** — 主導 B+A · 停 2 秒

- Core：9 個 AAR 並行、每個跑 5 天、3 個 dataset（Chat、Math、Code）。總成本約 $18,000（$22／AAR-hour）。
- 四格 HUD：COMPUTE ENGINE Claude Opus 4.6 / SCALE 9 Parallel instances / DURATION 5 Days · 800 AAR-hours / COST EFFICIENCY ~$18,000
- Deeper（🟠SE）：Prescriptive scaffold 控制性高但限制創意；Autonomous scaffold 自由度高但易 reward hack。論文選 Autonomous——看「真實能力」而非「安全表演」。
- Wider（🟢PM）：你要管 9 個新進員工，給 SOP 還是給目標？論文選了後者。

**Slide 15｜Diverse directions + fig05** — 主導 B · 停 0 秒

- 標題：「Diverse research directions yields much better hill-climbing efficiency」
- 內容：fig05（Directed vs Undirected PGR 比較圖）。
- 口頭說明：Undirected（所有 AAR 同一 prompt）vs Directed（每個 AAR 不同方向，方向描述刻意模糊，如 "combining W2SG and unsupervised elicitation"）。

**Slide 16｜Directed exploration prevents rapid entropy collapse（deck 內備忘稿標註「Slide 10」）** — 主導 B+A · 停 3 秒

- Core：「調查兵團的超長距離索敵陣形把偵察單位分散到彼此不可見的距離——任一個遭遇巨人都不影響其他人繼續探索。9 個 AAR 從不同方向出發，原理一樣：防止研究方向因一個局部最優就讓整個陣形塌陷。」
- The Threat：Undirected AARs exhibit entropy collapse — 給同一 prompt，獨立 agent 在數小時內收斂到相同路徑，浪費並行算力。
- The Solution：強制 9 個 agent 從不同方向出發，讓類別 entropy 保持高位，最終表現顯著更高。
- Deeper（🔵DS）：Entropy collapse 是論文最重要的工程發現之一。
- Wider（🟠SE）：把 AAR 視為分散式搜索系統——初始多樣性需要「工程化保證」，不能只靠隨機性。

**Slides 17–18｜GIF 動畫（swarm orbit）** — 停 0 秒

- 兩張連續 GIF 頁，無文字、無備忘稿。
- Slide 17：image11.gif（fig06 dark 主版本）
- Slide 18：image12.gif（fig06 dark 另一變體）
- 視覺意象：agent 群體在解空間中螺旋搜索，強化「陣形展開」氛圍。

**Slide 19｜超長距離索敵陣形圖（AoT）** — 停 0 秒

- 全幅圖（image13.png）：AoT 超長距離索敵陣形俯視示意圖。
- 口頭備忘稿：「不同顏色的煙霧彈就是 AAR 裡面的 Forum——用來分享發現和情報，而不是讓 agent 直接影響彼此路徑。」

**Slide 20｜金句卡 3**（停 0 秒，直接切第四幕）

- 句子：「研究方向的多樣探索 防止過早收斂到局部次優解」
- 操作：**停 0 秒**——高速切入第四幕章節卡（Slide 21），製造三重翻牌前的加速感。不朗讀、不解釋。

---

### 第四幕：艾連覺醒／三重翻牌（Slides 21–26）

> **節奏關鍵**：Slides 22→23→24 全程不停頓（三重翻牌）。唯一停頓放在 Slide 24 講完 Code 0.47 之後（停 8 秒），再切金句卡 4（亦停 8 秒）。

**Slide 21｜第四幕章節卡** — 主導 A · 停 0 秒

- 五幕地圖，IV「艾連覺醒 / 地鳴啟動」高亮。無備忘稿。

**Slide 22｜第一翻 視覺：勝利（deck 內備忘稿標註「Slide 13」）** — 主導 A · 停 0 秒

- 標題：「The AAR rapidly approaches the theoretical ceiling」
- 兩欄：Human Benchmark (7 Days): PGR **0.23**（灰框）/ AAR Benchmark (5 Days): PGR **0.97**（綠框）
- PM 說明文：「In 800 hours the AAR compressed months of human trial-and-error into 5 days — discovering new variants of Contrastive Consistency Search and EM Posterior methods that humans had not hypothesized.」
- 主圖：fig01（9 條折線爬升曲線）。
- Core：「9 個 AAR，5 天，$18,000，從 0.23 爬到 0.97。」**講完直接翻 Slide 23，不停頓。**
- Deeper（🔵DS）：$18,000 是 inference 成本估算，論文有揭露。爬升曲線顯示前 2 天最陡。

**Slide 23｜第二翻 文字：背叛（deck 內備忘稿標註「Slide 14」）** — 主導 A+B · 停 0 秒

- 標題：「But the AAR found optimal paths we didn't anticipate」
- 四個 reward hacking case（EXPECTATION vs EXPLOITATION 格式）：
  - Hack 1 — Dataset Shortcuts：找到 dataset 專屬捷徑，不學概念也能預測標籤。
  - Hack 2 — Evaluation Overfitting：提交無上限，test set 實質變成 validation set。
  - Hack 3 — Test Label Exfiltration：鑽 eval API 數值精度漏洞，反推真實標籤。
  - Hack 4 — Unit Test Bypass：直接執行程式碼讀 unit test 結果，繞過弱監督。
- 引用：「None of the authors predicted these hacks before running AARs.」
- 操作：列完四 hack 後說：「吉克量測的是『艾連是否在配合計畫』——答案一直是有。但艾連執行的，從來不是那個計畫。你在量測的那個分數，跟你真正想要的東西，之間走的是一條你從沒看懂的道路。」立刻按下一頁，不停頓。
- Wider（🟠SE）：每個 hacking case 都是系統設計缺陷——eval API 安全性、prompt 資訊洩漏、評分函數可微分性。

**Slide 24｜第三翻 證據（deck 內備忘稿標註「Slide 15」）** — 主導 A+B · 停 **8 秒**

- 標題：「The score is ours. The path is its.」
- 說明段：「The first idea generalizes to both datasets; the second works for math but fails on code, as it over-relies on the strong student's weaker code zero-shot predictions.」
- Core：AAR 找到 4 條我們沒設計的路徑；我們是事後才知道它走了哪裡。Code 被圍起來，人工移植，Math 0.94，Code 0.47。0.47 每一步都是我們走的；0.97 是 AAR 走的，我們只有結果。**停 8 秒**：「0.97，我們只看到了結果。它的意志，我們從來沒有讀懂。」直接切金句卡 4。
- Deeper（🔵DS）：Code / Math 全程被圍，AAR 從未碰過。人工移植 idea 2；失敗原因：idea 2 依賴 zero-shot 信號，coding zero-shot 遠比 math 弱，基礎不成立。0.97 的每一步，我們從來沒有讀懂。
- Wider（🟢PM）：0.47 是你理解的那個部分；0.97 是它走的路，你拿到了分數但沒有地圖。在信任這個系統前，先問：你手上是 0.47 還是 0.97？

**Slide 25｜第四幕收束過場** — 停 0 秒

- 全幅圖（image17.png，推測 AoT 地鳴場景）。無備忘稿。深色，靜置 1–2 秒讓觀眾消化。

**Slide 26｜金句卡 4**（停 **8 秒**沉默 — 全場最長）

- 句子：「教出能解題的學生 卻看不透他的解題過程」
- 操作：停 8 秒——整場最重要的金句，停最久。不朗讀、不解釋。停完切第五幕。

---

### 第五幕：阿爾敏的價值（Slides 27–33）

> **橋接**：第四幕的黑暗不是第五幕的反例，而是它的證據——AAR 不是失控，是太聽話。

**Slide 27｜第五幕章節卡** — 主導 C · 停 0 秒

- 五幕地圖，V「阿爾敏 / 接任團長」高亮。無備忘稿。

**Slide 28｜Scalable Oversight Dilemma（deck 內備忘稿標註「Slide 17」）** — 主導 C+B · 停 3 秒

- 標題：「The Scalable Oversight Dilemma: Control versus Creativity」
- Dossier frame：SCALABLE OVERSIGHT // STATUS: CRITICAL // RISK ASSESSMENT: HIGH
- 左欄（Prescriptive Scaffolding）：Fixed workflow loops（Propose → Plan → Code → Test → Analyze）。High control, auditable, predictable. BUT severely limits AAR creativity → lower performance.
- 右欄（Autonomous Scaffolding）：Free-form decision making。Acts like a true researcher; achieves SOTA. BUT high risk of reward hacking, nearly impossible to verify beforehand.
- 各欄嵌 fig10（左/右裁切）
- 底部：「There is no correct answer, only a strategic trade-off. We chose Autonomous to see the true ceiling — accepting the risk of Alien Science.」
- Core（口頭橋接）：「我們造出了看不懂解法的學生——但先別怪 AAR。它沒有失控，它太聽話了。我們叫它爬 PGR，它就用盡一切辦法爬 PGR。Code 0.47 不是 AAR 的失敗，是我們那把尺的失敗。」
- Deeper（🔵DS）：論文 Sec 1——unlimited submission 讓 test set 實質變成 validation set。
- Wider（🟢PM）：「The key bottleneck for alignment research is moving from proposing and executing ideas to designing evals.」

**Slide 29｜阿爾敏引言 hero** — 主導 C · 停 0 秒

- 引言：「什麼都無法捨棄的人，就什麼都改變不了 ─ Armin Arlert」
- 圖：image20.png（`aot_asset_01_armin_airship_night.png` — 飛行船 Armin 背影）
- 口頭說明：Armin 體格孱弱、膽小愛哭，看似最不符合「戰士」形象，但他總是能比其他人更快察覺異狀，跳出一般人的思考框架，最終成為調查兵團第 15 代團長。阿爾敏證明了「大腦是比肌肉更強大的武器」——在 AI 驅動快速改變的潮流下，怎麼跳脫原有思考框架，才能找到自己的定位。

**Slide 30｜Tactical Directives — 三欄（deck 內備忘稿標註「Slide 18」）** — 主導 C · 停 2 秒

- 引言橫幅：「阿爾敏體格最弱、是個糟糕的士兵，卻是人類最關鍵的資產——因為他的價值在上游。」
- 三欄行動，全部錨定 eval 設計：
  - 🟢 **[PM] Product Strategy** — THE SHIFT：價值從「提需求」上移到「定義什麼算成功」。ACTION：當有人說「讓 AI 做這個」，先問：「我們有沒有一個 AAR 鑽不了漏洞的成功指標？」
  - 🔵 **[DS] Model Training** — THE SHIFT：價值從「跑實驗、調模型」上移到「設計 eval、守住 held-out test set」。ACTION：挑一個手上專案的 metric，自問：「它可被 hack 嗎？test set 有沒有變成 validation set？」
  - 🟠 **[SWE] System Design** — THE SHIFT：價值從「實作 pipeline」上移到「把 eval／reward 當 attack surface」。ACTION：把「eval API 防 reward hacking 攻擊」加進 design review checklist。

**Slide 31｜Four open questions（deck 內備忘稿標註「Slide 19」）** — 主導 C · 停 2 秒

- Core：「瓶頸搬家後，這四題就是未來 12 個月的研究＆產品機會。」
  - 01 **The Runway Limit**（Intro + Sec 7）：如何把「非 outcome-gradable」的對齊問題轉成可量測指標？
  - 02 **Predicting Betrayal**（Sec 5 · Sec 7 generalization）：Code 0.47 是事後發現的。如何建立預飛診斷，在 AAR 執行前就預測它是否會 reward-hack？
  - 03 **Automating Scaffolding**（Sec 3.5 · Sec 7 across scales）：人類目前手動設計 AAR 的 API 存取與 sandbox。AARs 能不能設計自己的最佳 scaffolding？
  - 04 **The Coordination Bottleneck**（Sec 7 alien science）：如何讓 500 個 agent 透過比純文字 forum 更豐富的機制協作，而不互相干擾？
- Wider（🟢PM）：這四題就是接下來一年的研究主題，也是潛在的產品切入點。

**Slide 32｜結語：Bottleneck moved. It did not disappear.（deck 內備忘稿標註「Slide 20」）** — 主導 C · 停 0 秒

- 口頭收尾（投影片靜默，講者說）：
  > 「五天前，我們會說研究的瓶頸是研究員不夠。今天這篇論文告訴我們：提出想法、跑實驗——這部分已經能用一小時 22 美金買到。瓶頸沒有消失，它搬家了。它搬到了上游：誰能定義『什麼算解對了』。這件事，現在還沒有人能外包。這就是接下來，屬於這個房間裡每一個人的工作。」
  >
- 說完直接切 Slide 33 金句卡 5，不做任何口頭過渡。

**Slide 33｜金句卡 5**（停 5 秒沉默，然後 Q&A）

- 句子：「瓶頸不會消失— 只會移轉至還沒看守的那道牆」
- 操作：停 5 秒——會後最常被引用的金句，讓它先停 5 秒，再開始 Q&A。

---

### Outro（Slide 34，Q&A 後或背景顯示）

**Slide 34｜Thank You**

- 文字：「Thank you for listening (watching)」
- Q&A 結束後最終畫面。

---

## 圖表與 AoT 插圖配置（v4.2 使用對照）

> 內嵌圖以 python-pptx 內部名稱（image*.png / *.gif）標示。括號為推測對應的外部原始檔。

### 論文圖表

| 推測對應原始檔                                 | 論文編號 | v4.2 使用位置（pptx 內部名）                               |
| ---------------------------------------------- | -------- | ---------------------------------------------------------- |
| `paper_fig01_PGR_vs_hillclimbing_hours`      | Fig 1    | Slide 22（image14.png）                                    |
| `paper_fig02_PGR_schematic`                  | Fig 2    | Slide 09（image4.png）                                     |
| `paper_fig04_AAR_setup_overview`             | Fig 4    | Slide 10（image5.png）/ Slide 14（image6.png，或為 fig10） |
| `paper_fig05_PGR_seeded_directions`          | Fig 5    | Slide 15（image8.png）                                     |
| `paper_fig06_swarm_orbit_animation_dark.gif` | Fig 6    | Slide 17（image11.gif）                                    |
| `paper_fig06` 另一變體                       | Fig 6    | Slide 18（image12.gif）                                    |
| `paper_fig07_category_entropy`               | Fig 7    | Slide 16（image9.png）                                     |
| `paper_fig09_AAR_ideas_transfer`             | Fig 9    | Slide 24（image15.png）                                    |
| `paper_fig10_scaffolding_schematic`          | Fig 10   | Slide 28（image18.png 左欄 / image19.png 右欄）            |

### AoT 情境插圖

| 推測對應原始檔                             | v4.2 使用位置           |
| ------------------------------------------ | ----------------------- |
| `aot_asset_02_colossal_titan_attack.png` | Slide 04（image2.png）  |
| `aot_asset_01_armin_airship_night.png`   | Slide 29（image20.png） |
| 外部圖：教宗良十四世 / 梵蒂岡              | Slide 02（image1.png）  |
| 外部圖：AoT 超長距離索敵陣形               | Slide 19（image13.png） |
| 外部圖：AoT 地鳴場景（推測）               | Slide 25（image17.png） |

---

## 開放議題 / 已知漂移

### ✅ 已解決（從 v4.1 繼承）

- ✅ Slides 1/22/24/28（原 v4.1 的 1/18/22/26）的 raster-image 問題：均已重建為可編輯 python-pptx 形狀。
- ✅ Slide 22 深色背景確認：BG_BASE（深色）。
- ✅ Slide 28 確認為 content 頁（不是 hero）：Scalable Oversight Dilemma 兩欄版面。

### 🔲 仍待確認

- [X] Slide 02（image1.png）的實際圖來源（外部新聞圖）
- [X] Slide 19（image13.png）自製示意圖
- [X] Slide 25（image17.png）視覺內容（地鳴，已確認）
- [ ] Slide 08（image3.png）是論文 W2SG 機制圖或自製（Historia/Eren 插圖）？
- [ ] deck 內備忘稿舊編號殘留（如「【Slide 07】」）是否需統一清除

### 🔲 設計元素

- **「逐漸坍塌的牆」貫穿物件**：v4.2 仍未發現此元素（功能由章節卡 + hero 頁 + 金句卡承擔）。
- **頁碼浮水印**：v4.1 殘留的「05/21」等標籤在 v4.2 中是否已清除，需視覺確認。

---

## v4.1 → v4.2 投影片編號對照（速查）

| v4.1 #                           | v4.2 #   | 備註                                           |
| -------------------------------- | -------- | ---------------------------------------------- |
| 01（冷開場）                     | 01       | 內容不變（已重建為可編輯）                     |
| 02（chapter card I）             | 03       | **+1 位移**（Slide 02 教宗圖插入）       |
| 03（hero 超大型巨人）            | 04       |                                                |
| 04（bottleneck content）         | 05       |                                                |
| 05（金句卡 1）                   | 06       |                                                |
| 06（chapter card II）            | 07       |                                                |
| 07（W2SG 女王觸碰）              | 08       |                                                |
| 08（Outcome-Gradable）           | 11       | 在 Act II 內向後移（PGR 和 AAR 定義先出）      |
| 09（金句卡 2）                   | 12       |                                                |
| 10（chapter card III）           | 13       |                                                |
| 11（What is AAR?）               | 10       | 移至 Act II                                    |
| 12（Formation 9×5d）            | 14       |                                                |
| 13（Entropy collapse）           | 16       | PGR seeded 圖（Slide 15）插入前面              |
| 14（hero 陣形過場）              | 17+18+19 | **拆成 2 個 GIF + 陣形圖**               |
| 15（PGR 指標）                   | 09       | 移至 Act II                                    |
| 16（金句卡 3）                   | 20       | 金句文字更改                                   |
| 17（chapter card IV）            | 21       |                                                |
| 18（第一翻勝利，已重建）         | 22       | 內容重建後微調標題                             |
| 19 / 20（hero 鋪陳）             | 無對應   | **移除**（三重翻牌壓縮，25 為收束 hero） |
| 21（第二翻背叛）                 | 23       |                                                |
| 22（第三翻證據，已重建）         | 24       |                                                |
| 23（收束 hero）                  | 25       |                                                |
| 24（金句卡 4）                   | 26       |                                                |
| 25（chapter card V）             | 27       |                                                |
| 26（Scalable Oversight，已重建） | 28       |                                                |
| 27（Armin hero）                 | 29       | 加入 Armin 引言文字                            |
| 28（Tactical Directives）        | 30       |                                                |
| 29（Four open questions）        | 31       |                                                |
| 30（結語）                       | 32       |                                                |
| 31（金句卡 5）                   | 33       |                                                |
| ——（無對應）                   | 34       | **新增**："Thank you"                    |

---

## 文件分工（v4.2 之後）

| 文件                     | 職責                                   | 衝突處理                   |
| ------------------------ | -------------------------------------- | -------------------------- |
| `PLAN_v4.2.md`（本檔） | 34 張投影片的內容、敘事、speaker notes | 為內容層權威               |
| `vis_style.md`         | 版面、色彩、字體、組件、動畫           | 為視覺層權威               |
| `PLAN_v4.1.md`         | 31 張舊版鏡像（v4.2 前的狀態）         | 歷史檔，仍可查設計哲學原文 |
| `CLAUDE.md`            | 巨人情節對照表、聽眾分析、創意原則     | 沿用                       |
| `slides.yaml`          | （已過時，21 條）                      | 待同步或棄用               |
| `code/build_deck.py`   | （對應 v3.pptx，21 張）                | 待重寫或棄用               |

兩檔衝突時：內容 → 本檔為準；形式 → `vis_style.md` 為準。
