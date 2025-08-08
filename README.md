# smart_trading_assistant_stage1
bot
# Smart Trading Assistant — Stage 1 (Read-only Monitor + Daily Report)

**目标**：提供一个最安全的 MVP（最小可行版本），只读 Binance 数据 → 计算波动率/ATR/健康检查 → 生成 Markdown 日报。  
**特点**：不会进行交易，不会修改账户，只做数据读取与分析。

---

## 功能
- ⛓️ **只读** Binance API 集成（无交易权限，无提现权限）
- 📈 从近期 K 线计算波动率 & ATR(14)
- 🚨 健康检查：价格是否超出区间、未成交网格比例（占位符）、DCA 触发次数（占位符）
- 📝 输出 Markdown 格式的日报，可直接粘贴到 Notion / Telegram
- 🤖 内置 GPT-5 提示词模板（可手动复制到 ChatGPT，Stage 2 再加自动调用）

---

## 快速开始

### 1. 准备环境
安装 Python 3.10 或 3.11（建议不要用 3.12+）。

### 2. 安装依赖
```bash
pip install -r requirements.txt
