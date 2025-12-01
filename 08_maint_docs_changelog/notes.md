學員完成後可以：

理解為什麼企業需要「Changelog」與「維護紀錄（Maintenance Note）」。
知道如何從 Git diff / commit log 中，讓 AI 自動整理：
對外或對 PM 的版本變更說明（Changelog）。
給 SRE / 維運同仁看的維護紀錄（Maintenance Note）。
熟悉一條實務流程：
從 VSCode / Git 取得 diff 或 commit 記錄
貼給 ChatGPT / OpenWebUI 套用 Prompt
將輸出文件存到 docs/ 或 repo 中。
二、課程延續與重點
前一個模組（07_git_commit_ai）學員已經學過：

如何用 AI 針對「單一 commit」產生高品質 commit message。
本模組要處理的是：

一個版本可能有數十個 commit。
PM / 維運 / 管理階層不會看 commit log， 他們需要的是「整理好的版本說明」。
核心比喻：

commit message = 點（event）
changelog / maintenance note = 線（story）
三、Part A：動機說明與案例導入
先請學員思考幾個問題：

產品發一個新版本時，PM 需要什麼文件？
SRE / 維運需要什麼資訊才能安心佈署？
一個月後要追溯「這版到底動了什麼」時，要看什麼？
打開範例檔案：範例檔案/maint_note_example.md
示範一份「寫得還算像樣」的維護紀錄，感受內容結構，通常包含：

版本範圍
主要變更
風險與注意事項
佈署前後檢查步驟
回滾（rollback）注意事項
收斂重點：

這類文件如果靠工程師手寫，很花時間，也很容易遺漏。
本單元要示範如何用 AI 讓這種文件從「很痛」變成「很快」。
四、Part B：Step by Step 修改程式並產生 .diff
此段是示範「實際修改程式 → 產生 diff → 存成檔案」的流程，
最終得到 範例檔案/release_changes_v1.2.3.diff。

B.1 修改第一支程式（mobile_log_metrics_manual.py）
在 VSCode 中開啟檔案：

05_log_ai_analytics/3_Python/mobile_log_metrics_manual.py

找到原本解析 latency_ms 的程式區塊（示意）：

if "AIInference" in line and "latency_ms=" in line:
    parts = line.split("latency_ms=")
    if len(parts) > 1:
        right = parts[1]
        num_str = ""
        for ch in right:
            if ch.isdigit():
                num_str += ch
            else:
                break
        if num_str:
            asr_latencies.append(int(num_str))
將其改成較穩健版本（加入 try/except 與逗號處理）：
if "AIInference" in line and "latency_ms=" in line:
    try:
        parts = line.split("latency_ms=")
        right = parts[1].split()[0]
        num_str = right.replace(",", "")
        latency = int(num_str)
        asr_latencies.append(latency)
    except (IndexError, ValueError):
        # ignore malformed latency
        continue
     4.存檔，但先不要 commit。
B.2 修改第二支程式（scheduled_log_alert_manual.py）
開啟檔案：

06_scheduled_log_alert/3_Python/scheduled_log_alert_manual.py

在 check_abnormal() 裡面，原本程式只有 asr_p95 的判斷：

if acfg.get("enabled") and summary["asr_p95"] is not None:
    if summary["asr_p95"] > acfg.get("max_p95_ms", 200):
        triggered["asr_p95"] = summary["asr_p95"]
在這段下面新增一個 recommend 模型錯誤率的告警規則：

rcfg = alerts_cfg.get("recommend_error_rate", {})
if rcfg.get("enabled"):
    err_rate = summary.get("recommend_error_rate")
    if err_rate is not None and err_rate > rcfg.get("max_error_rate", 0.05):
        triggered["recommend_error_rate"] = err_rate
存檔，仍然先不要 commit。

B.3 產生這次版本的 diff 檔案
在 VSCode 底部開啟 Terminal（PowerShell 或 bash 均可）。

確認目前在專案根目錄，例如：

C:\Users\xxx\realtek-ai-dev-training>
執行指令：

git diff > 08_maint_docs_changelog/範例檔案/release_changes_v1.2.3.diff
回到 VSCode 檔案總管，開啟：

08_maint_docs_changelog/範例檔案/release_changes_v1.2.3.diff

就可以看到這次版本的所有程式變更內容。

這一步老師先 demo 一次，
之後請學員自己再做一次，確認都知道如何產生 diff 檔案。


五、Part C：從 diff 產生 Changelog
使用範例檔案：範例檔案/release_changes_v1.2.3.diff

在 VSCode 開啟 release_changes_v1.2.3.diff，學員快速瀏覽：

新增了 recommend 模型錯誤率告警。

修正 asr-small-v1 latency 解析邏輯。

了解這些改動在系統上的意義。

在瀏覽器開啟 ChatGPT 或 OpenWebUI。

將 Prompt 檔案/changelog_from_diff.md 的內容貼到 AI，
接著在最後貼上整份 release_changes_v1.2.3.diff。

示範讓 AI 產生類似結構的 changelog：

版本標題與日期，例如：

v1.2.3 – 2025-11-30

Added / Changed / Fixed 三段列表。

每一點都是「自然語言」說明，不再是程式碼片段。

將 AI 的輸出貼回 VSCode，存成一個新檔案，例如：

docs/changelog_v1.2.3.md

或在 CHANGELOG.md 增加一節「v1.2.3」。

收斂說明：

日常開發 → 只要維持「寫好 commit message」即可（呼應 07 模組）。

發版時 → 把這一版的 diff 丟給 AI，整理成對 PM / 對客戶的 changelog。

兼顧技術正確性與非工程師可讀性。

六、Part D：從 commit 歷史產生維護紀錄
此段聚焦「給維運 / SRE 看的文件」。

在專案中示範 Git 指令（老師 demo）：

例如只抓這一版範圍的 commit：

git log v1.2.2..v1.2.3 --oneline
或手動選取需要的 commit 訊息，複製到剪貼簿。

將這段 commit 記錄貼給 AI，使用：

Prompt 檔案/maintenance_note_from_commits.md

要求 AI 產生「給維運同仁看的維護紀錄」，格式包含：

本次維護範圍概述（Scope）

重要變更列表

佈署前檢查項目

佈署後驗證步驟

回滾（rollback）注意事項

將 AI 生成內容貼回 VSCode，存成：

docs/maintenance_2025-11-30.md

或公司既有慣例路徑，例如 maint_notes/maint_2025-11-30_v1.2.3.md。

學員思考：

維護紀錄的主要讀者不是原開發者，而是：

之後的維運工程師

未來半年內要接手的人

AI 非常擅長「摘要、重述、重組」：

只要 commit message 寫得好，就可以大量節省這類文件撰寫時間。

七、Part E：與 07 模組的整合流程
完整實務流程可以是：

開發階段：

每次 commit 都用 07 模組教的 Prompt 寫清楚訊息。

發版前：

用 git diff 產生本版變更 → 套用 changelog_from_diff.md → 產出 changelog。

用 git log 取得本版 commit → 套用 maintenance_note_from_commits.md → 產出維護紀錄。

最後可以再做一個「Release v1.2.3」的總結 commit：

將 changelog / 維護紀錄的檔名寫在 commit message 裡，方便日後追溯。

八、本模組重點回顧
commit message 解決「當下這一次」的溝通。

changelog / maintenance note 解決「一整版」的溝通。

AI 非常擅長把：

細節 → 摘要

程式碼 → 自然語言

多次 commit → 一篇故事

核心價值：
讓 AI 把工程師平常的開發痕跡，轉換成「對人類友善的維護文件」。

