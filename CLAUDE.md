# CLAUDE.md — Exchange Handbook 交換生手冊

這份文件寫給在這個專案裡工作的 AI（Claude Code、Codex 等）。動手修改或新增內容前，請先完整讀完。

## 1. 專案目的

- 為中山大學（NSYSU）交換生整理一本「從申請到抵達後」的網頁手冊。
- 內容依交換的三個階段組織：
  - `apply`：申請期（選校、文件、語言門檻）
  - `pre-departure`：錄取後到出發前（與交換校對接：選課、住宿、簽證）
  - `arrival`：抵達後的日常（居留、開戶、交通、就醫）
- 本網站同時是期末專案「交換生全程 AI 助理」的 **RAG 知識庫**。每一頁都必須帶有完整的 front matter，段落要短、一段只講一件事，方便切段檢索。

## 2. 技術與部署

- 靜態網站，使用 GitHub Pages 內建的 **Jekyll**，不需要本機建置。
- 內容一律用 **Markdown** 撰寫；版型在 `_layouts/`，樣式只有 `assets/style.css` 一份。
- 首頁（`index.md`）用 Liquid 依 `type` 自動列出所有頁面，**新增頁面時不需要修改首頁**。
- 站內連結一律寫成 `{{ '/路徑/' | relative_url }}`，不要寫死網域。

## 3. 資料夾與命名

| 類型 | 放在 | 範本 | 檔名規則 | 範例 |
|---|---|---|---|---|
| 學校頁 `school` | `schools/` | `templates/school.md` | 學校英文名稱 kebab-case | `schools/sungkyunkwan-university.md` |
| 國家生活頁 `country` | `countries/` | `templates/country.md` | 國家英文名稱 kebab-case | `countries/south-korea.md` |
| 指南頁 `guide` | `guides/` | `templates/guide.md` | 主題英文 kebab-case | `guides/application-checklist.md` |

- 檔名只用小寫英文、數字與連字號 `-`，不要用中文或空白。
- 一校一檔、一國一檔；同一主題不要拆成兩頁。

## 4. Front matter（每頁必填）

```yaml
---
layout: entry
title: 頁面標題（學校頁用「中文名（原文名）」）
type: school | country | guide
stage: apply | pre-departure | arrival   # 指南頁可填多個，用陣列
country: KR                               # ISO 兩碼國碼；指南頁若不限國家填 ALL
summary: 一句話說明這頁在講什麼（會顯示在首頁卡片）
sources:
  - name: 來源名稱
    url: https://...
updated: YYYY-MM-DD
status: draft | verified
---
```

- `status` 預設為 `draft`。只有人工核對過所有來源後才能改成 `verified`，**AI 不可以自行改成 verified**。
- `updated` 填實際修改的日期。

## 5. 新增頁面的步驟

1. 從 `templates/` 複製對應範本到正確資料夾，照第 3 節命名。
2. 填寫 front matter 的每一個欄位。
3. **保留範本裡的所有二級標題（`##`），順序不要改**。沒有資料的章節保留標題，內容寫「待確認」。
4. 學校頁要在「相關頁面」連到該國的國家生活頁；國家頁若還不存在，就同時建立一份只有骨架的國家頁。
5. 不用改首頁，也不用改導覽列。

## 6. 內容與可信度規則（最重要）

- **每一項事實都要能對應到 `sources` 裡的一個來源。**
- 簽證、居留、費用、截止日、語言門檻這類高風險資訊，**沒有來源就寫「待確認」**，並在後面加上應該去哪裡查（例如「請查交換校國際處網站」）。**絕對不要憑印象補數字或日期。**
- 個人心得放在「心得與提醒」章節，用「（個人經驗）」標明，和官方資訊分開。
- 正文用繁體中文（台灣用語）；校名、課程名、機關名第一次出現時附原文。
- 一段不超過 4 句；條列優先於長段落。

## 7. 視覺風格

- 簡潔、像一本手冊：白底、單欄、最大寬度 760px，用卡片列出頁面。
- 三個階段各有固定的標籤顏色（定義在 `style.css` 的 `.stage-*`），不要新增顏色或字體。
- 不放裝飾圖片；需要圖片時放在 `assets/img/`，檔名同樣用 kebab-case，並附替代文字。

## 8. AI 修改時的限制

- 只動和這次任務有關的檔案；不要順手改寫其他頁面的內容。
- 不刪除任何頁面的 `sources`。
- 不新增 `_layouts/` 以外的版型，也不引入外部 CSS/JS 框架。
- 修改 `_layouts/` 或 `style.css` 前要先說明原因，因為會影響全站。
- 完成後，用一句話回報：新增或修改了哪些檔案，以及哪些欄位仍是「待確認」。
