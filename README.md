# Async Service Monitor

比較「循序（同步）」與「非同步」兩種 HTTP 請求方式效能差異的小型網站可用性檢查工具。

專案針對一組網站清單，分別以同步與非同步方式發送請求，並量測每個網站的回應延遲與整體耗時，最後透過命令列或 Streamlit 網頁介面呈現比較結果。

## 功能特色

- **同步檢查**：使用 `httpx2.Client`，依序逐一請求每個網址。
- **非同步檢查**：使用 `httpx2.AsyncClient` 搭配 `asyncio.gather`，同時發送所有請求。
- **狀態與延遲紀錄**：記錄每個網址的 HTTP 狀態碼與回應時間。
- **例外處理**：逾時顯示 `TIMEOUT`，其他連線錯誤顯示 `ERROR`。
- **Streamlit 介面**：一鍵執行比較，並以表格、進度條與加速倍數視覺化結果。
- **集中設定**：網址清單與逾時時間統一在 `config.py` 管理。

## 專案結構

```
.
├── async_check.py      # 非同步檢查（可單獨執行）
├── sync_check.py       # 同步檢查（可單獨執行）
├── streamlit_app.py    # Streamlit 網頁介面，同時比較兩種方式
├── config.py           # 網址清單與逾時設定
└── requirements.txt    # 相依套件
```

## 環境需求

- Python 3.9 以上（程式使用了 `str.removeprefix`）
- 相依套件：`httpx2`、`streamlit`

## 安裝

```bash
# 建議先建立虛擬環境
python -m venv venv
source venv/bin/activate      # Windows：venv\Scripts\activate

# 安裝相依套件
pip install -r requirements.txt
```

## 使用方式

### 1. 命令列執行

同步版本：

```bash
python sync_check.py
```

非同步版本：

```bash
python async_check.py
```

輸出範例：

```
URL                              STATUS    LATENCY
----------------------------------------------------
https://github.com                  200    0.2574 s
https://www.python.org/             200    0.4400 s
...
Total: 2.0944 s
```

### 2. Streamlit 網頁介面

```bash
streamlit run streamlit_app.py
```

開啟瀏覽器後點擊 **Run Comparison**，程式會先執行同步檢查，再執行非同步檢查，並顯示：

- 各網站在兩種模式下的延遲（毫秒）
- 兩種模式的總耗時
- 執行時間進度條比較
- 加速倍數（Speedup = 同步總耗時 ÷ 非同步總耗時）

## 設定

編輯 `config.py` 即可調整檢查目標與逾時：

```python
URLS = [
    "https://github.com",
    "https://www.python.org/",
    "https://www.cloudflare.com",
    "https://www.google.com/",
    "https://www.youtube.com/",
    "https://www.bilibili.com/",
]

TIMEOUT = 3.0   # 單次請求逾時秒數
```

## 運作原理

| 項目 | 同步 (`sync_check.py`) | 非同步 (`async_check.py`) |
| --- | --- | --- |
| 用戶端 | `httpx2.Client` | `httpx2.AsyncClient` |
| 執行方式 | `for` 迴圈依序請求 | `asyncio.gather` 並行請求 |
| 總耗時 | 約等於各請求耗時的**總和** | 約等於**最慢那一個**請求的耗時 |

網路請求大部分時間都在等待伺服器回應（I/O 等待）。同步版本在等待時無法做其他事；非同步版本則能在等待期間同時處理其他請求，因此網址越多，差距通常越明顯。

## 注意事項

- 實際數值會受網路環境、DNS 快取、連線建立成本與目標網站狀態影響，每次執行結果不會完全相同。
- 在部分網路環境下，某些網站（例如 Google、YouTube、Bilibili）可能逾時或無法連線，狀態會顯示為 `TIMEOUT` 或 `ERROR`。
- 逾時或連線失敗的請求，其延遲時間仍會計入統計。
- Streamlit 介面中，同步檢查先於非同步檢查執行，第一輪可能包含較多連線暖身成本，多執行幾次比較更具參考性。

## 授權

本專案僅供學習與練習使用。
