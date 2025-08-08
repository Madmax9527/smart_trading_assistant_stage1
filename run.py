import os, math, numpy as np, pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from tabulate import tabulate

# Bot 参数（示例）
BOTS = [
    {"symbol": "TRXUSDT", "type": "grid", "range": (0.1200, 0.1320), "grid_spacing_pct": 1.2, "grids": 20, "funds": 1000},
    {"symbol": "TONUSDT", "type": "dca",  "dca_drop_step_pct": 1.0, "dca_buy_amount": 7.5, "dca_max_steps": 8, "take_profit_rebound_pct": 2.0, "funds": 800},
    {"symbol": "BTCUSDT", "type": "grid", "range": (56000, 62000), "grid_spacing_pct": 1.5, "grids": 18, "funds": 1500},
    {"symbol": "ETHUSDT", "type": "trend_grid", "range": (2800, 3400), "grid_spacing_pct": 1.0, "grids": 22, "funds": 1200},
]

def synthetic_klines(symbol: str, hours: int = 24*30) -> pd.DataFrame:
    np.random.seed(abs(hash(symbol)) % 2**32)
    base = 1.0
    if symbol.startswith("BTC"): base = 60000
    elif symbol.startswith("ETH"): base = 3200
    elif symbol.startswith("TRX"): base = 0.125
    elif symbol.startswith("TON"): base = 6.5

    ts = [datetime.utcnow() - timedelta(hours=hours - i) for i in range(hours)]
    prices = [base]
    for _ in range(hours - 1):
        prices.append(prices[-1] * (1 + np.random.normal(0, 0.003)))
    prices = np.array(prices)

    high = prices * (1 + np.random.uniform(0, 0.002, size=hours))
    low  = prices * (1 - np.random.uniform(0, 0.002, size=hours))
    openp = prices * (1 + np.random.uniform(-0.001, 0.001, size=hours))
    closep = prices

    df = pd.DataFrame({
        "open_time": ts,
        "open": openp,
        "high": high,
        "low": low,
        "close": closep,
        "volume": np.random.uniform(100, 10000, size=hours),
    })
    return df

def atr(df: pd.DataFrame, period: int = 14) -> float:
    if df.empty: return 0.0
    high, low = df["high"], df["low"]
    prev_close = df["close"].shift(1)
    tr = pd.concat([(high - low).abs(), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    val = tr.rolling(period).mean().iloc[-1]
    return float(val) if pd.notna(val) else 0.0

def realized_vol(df: pd.DataFrame, bars: int) -> float:
    if len(df) < 2: return 0.0
    ret = df["close"].pct_change().dropna()
    return float(ret.tail(bars).std() * math.sqrt(bars))

def grid_out_of_range(price: float, low: float, high: float) -> bool:
    return price < low or price > high

def main():
    rows = []
    for bot in BOTS:
        df = synthetic_klines(bot["symbol"])
        last = float(df["close"].iloc[-1])
        m_atr = atr(df)
        vol7d  = realized_vol(df, 24*7)
        vol30d = realized_vol(df, 24*30)

        health = {}
        if bot["type"] == "grid":
            low, high = bot["range"]
            health["out_of_range"] = grid_out_of_range(last, low, high)
        elif bot["type"] == "dca":
            health["dca_triggers_used"] = 3  # 占位符

        rows.append({
            "Symbol": bot["symbol"],
            "Type": bot["type"],
            "Last": last,
            "ATR14": m_atr,
            "Vol7d": vol7d,
            "Vol30d": vol30d,
            "Range": bot.get("range"),
            "Grid%": bot.get("grid_spacing_pct"),
            "Grids": bot.get("grids"),
            "Health": health
        })

    md_lines = []
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    md_lines.append(f"# Daily Report — {ts}\n")
    md_lines.append("**Total Funds (self-reported)**: TBD\n")
    md_lines.append(tabulate(
        [[r["Symbol"], r["Type"], r["Last"], r["ATR14"], r["Vol7d"], r["Vol30d"], r["Range"], r["Grid%"], r["Grids"], r["Health"]] for r in rows],
        headers=["Symbol","Type","Last","ATR14","Vol7d","Vol30d","Range","Grid%","Grids","Health"],
        tablefmt="github", floatfmt=".6f"
    ))

    out_dir = Path("reports"); out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "latest_report.md"
    out_file.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Report generated at {out_file}")

if __name__ == "__main__":
    main()
