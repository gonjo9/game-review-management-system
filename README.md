# 遊戲評論管理系統

## 專案概述

這是一個遊戲評論管理系統，用戶可以上傳遊戲和評論、查看評論和比較不同遊戲的評價。

## 使用的技術

- **MySQL**：資料庫儲存和管理
- **wxPython**：圖形用戶介面框架

## 實現的功能

### 核心功能
- **用戶管理**：新增和管理用戶資訊
- **遊戲管理**：新增遊戲並設定多個標籤
- **評論系統**：為遊戲新增評分和評論
- **標籤系統**：動態管理遊戲標籤

### 查詢和比較功能
- **查看所有資料**：瀏覽用戶、遊戲和評論
- **按標籤搜尋遊戲**：根據標籤篩選遊戲
- **平均評分排序**：查看按平均評分排序的遊戲列表
- **遊戲評論詳情**：雙擊查看遊戲的所有評論和詳細資訊

## 資料庫架構

- **USERS**：user_id, username, gender, age
- **GAMES**：game_id, title, developer
- **TAGS**：tag_id, tag_name
- **GAMETAGS**：game_id, tag_id
- **REVIEWS**：review_id, user_id, game_id, rating, comment, added_date
