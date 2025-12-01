# AI 協助撰寫 Git Commit Message

作為「AI × Git × VSCode」整合實作。



---

## 學習目標



學員完成後可以：

1. 理解為什麼企業在意「好的 commit message」，以及它與維護性的關係。

2. 會使用 ChatGPT / OpenWebUI，從 Git diff 自動產生 commit message。

3. 了解三個成熟度等級：

   - Level 1：Basic – 一句話說清楚「做了什麼」。

   - Level 2：Conventional Commit + Why – 說清楚「做了什麼」與「為什麼」。

   - Level 3：Enterprise – Summary + Change Detail + Root Cause + Impact。

4. 熟悉 VSCode × Git × AI 的操作路徑：Diff → Prompt → Commit。



---

## 課程流程建議



### Part A：動機與反例



1. 打開 `範例檔案/ex_bad_commit_messages.txt`，讓學員看到常見壞例子，例如：

   - `fix bug`

   - `update code`

   - `temp change`



2. 學員討論：

   - 三個月後回頭看這些 commit，能不能知道改了什麼、為什麼改？

   - 新人接手專案時，只看到這些 commit 會有多痛苦？



3. 收斂重點：

   - 好的 commit message 能提升：

     - 問題發生時的回溯速度（快速找到哪一次改壞的）。

     - 維護溝通效率（新同仁看歷史就能理解演進）。

   - 今天會示範如何用 AI 大幅簡化 commit 訊息撰寫的負擔。



---



### Part B：Level 1 – Basic Commit



目標：讓 AI 幫忙把 diff 轉成「清楚的一行文字」。



- 範例檔案：`範例檔案/ex1_diff_bugfix.patch`  

- 情境：修正 log parser 取 latency_ms 時沒有正確轉成整數，導致統計錯誤。



示範步驟：

1. 在 VSCode 中打開對應檔案，讓學員先用肉眼讀 diff。

2. 示範如何從 VSCode 取得 diff：

   - 左側 Source Control → 點選檔案 → 檢視差異。

   - 或在 Terminal 執行 `git diff`。

3. 將 diff 貼到 ChatGPT / OpenWebUI。  

   使用 Prompt：`Prompt 檔案/basic_commit_message.md`。

4. 展示 AI 可能產出的範例，例如：

   - `fix(parser): correctly parse latency_ms as integer`



說明重點：

- Level 1 的最低標準：  

  一句話說清楚「這次 commit 主要改了什麼」，比 `fix bug` 好太多。

- 讓學員實際操作：

  - 各自對 ex1 的 diff 跑一次 Prompt，複製 AI 結果貼回 VSCode commit 欄位。



---

### Part C：Level 2 – Conventional Commit + Why



目標：導入更正式、適合團隊協作的規範。



- 範例檔案：`範例檔案/ex2_diff_refactor.patch`  

- 情境：將 log parser 中重複的 parsing 邏輯抽成共用 function。



示範步驟：

1. 說明 diff 的性質：  

   這類修改是「重構」（refactor），不是新功能，也不是 bug fix。

2. 將 diff 貼給 ChatGPT / OpenWebUI。  

   使用 Prompt：`Prompt 檔案/conventional_commit.md`。

3. 觀察 AI 回覆範例（概念）：

   - 第一行：`refactor(log-parser): extract latency parsing into helper function`

   - 第二行 Why：例如  

     `Why: reduce duplicated code and make it easier to extend validation later.`



說明重點：

- Conventional Commits 基本型式：

  - `type(scope): summary`

  - type 可用：`feat`、`fix`、`refactor`、`docs`…等。



- 建議團隊平常至少用到 Level 2：

  - type 讓 Git log 易於快速掃描。

  - Why 讓未來的閱讀者理解「當時的設計考量」。



---

### Part D：Level 3 – Enterprise Commit



目標：示範「給 Code Review / 大型專案管理」時的高資訊量 commit。



- 範例檔案：`範例檔案/ex3_diff_feature.patch`  

- 情境：新增 recommend 模型錯誤率的告警規則。



示範步驟：

1. 將 diff 貼給 ChatGPT / OpenWebUI。  

   使用 Prompt：`Prompt 檔案/enterprise_commit_history.md`。

2. 觀察 AI 產出的結構，預期包含：

   - Summary（一行）

   - [Change Detail]：Before / After

   - [Root Cause]

   - [Impact / Risk]

   - [Reviewer Notes]



3. 解釋這種 commit 在下列情境尤其有價值：

   - 重大 bug 修正

   - 影響 SLO / 告警／安全邏輯的改動

   - 功能拆解、重構專案時的關鍵節點



---



## 小結：Diff → Prompt → Commit 的標準路徑



1. 在 VSCode 取得清楚的 diff（盡量一個 commit 解決一件事情）。

2. 把 diff 丟給 AI，依需求選擇對應 Prompt：

   - 練習或小修改：Level 1。

   - 團隊日常開發：Level 2。

   - 關鍵變更：Level 3。

3. 將 AI 回覆的文字貼回 VSCode，完成 commit。



---

## 建議課後練習



1. 請學員在自己的專案中挑 2～3 次實際修改：

   - 至少寫一個 Level 2 commit。

   - 至少寫一次 Level 3 commit（例如修 bug 或改 SLO）。

2. 將產生的 commit message 貼到內部群組，互相 review。

