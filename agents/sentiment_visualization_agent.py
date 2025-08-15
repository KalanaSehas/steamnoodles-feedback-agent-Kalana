import os
import re
from datetime import datetime, timedelta
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt

from utils.config import Config

class SentimentVisualizationAgent:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        os.makedirs(cfg.outputs_dir, exist_ok=True)

    @staticmethod
    def _parse_range(text: str):
        text = (text or "").strip().lower()
        today = datetime.now().date()
        if not text or text == "last 7 days":
            return today - timedelta(days=6), today
        # "YYYY-MM-DD to YYYY-MM-DD"
        if "to" in text:
            a, b = [s.strip() for s in text.split("to", 1)]
            return datetime.fromisoformat(a).date(), datetime.fromisoformat(b).date()
        # single date = that day
        try:
            d = datetime.fromisoformat(text).date()
            return d, d
        except Exception:
            # default
            return today - timedelta(days=6), today

    def _ensure_daily_counts(self, df: pd.DataFrame, start, end) -> pd.DataFrame:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df = df[(df["date"] >= start) & (df["date"] <= end)]
        if "sentiment" not in df.columns:
            # if no sentiment in CSV, assume neutral (will still show counts)
            df["sentiment"] = "neutral"
        pivot = (
            df.groupby(["date","sentiment"]).size().unstack(fill_value=0)
            .reindex(pd.date_range(start, end), fill_value=0)
        )
        pivot.index = pivot.index.date
        # Ensure all three columns exist
        for col in ["positive","negative","neutral"]:
            if col not in pivot.columns:
                pivot[col] = 0
        return pivot[["positive","negative","neutral"]]

    def plot(self, df: pd.DataFrame, date_prompt: str) -> str:
        start, end = self._parse_range(date_prompt)
        counts = self._ensure_daily_counts(df, start, end)

        plt.figure(figsize=(11,6))
        counts.plot(kind="bar", stacked=False)
        plt.title(f"SteamNoodles — Daily Sentiment Counts ({start} to {end})")
        plt.xlabel("Date")
        plt.ylabel("Number of Reviews")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        out_path = os.path.join(self.cfg.outputs_dir, "sentiment_plot.png")
        plt.savefig(out_path, dpi=150)
        plt.close()
        return out_path
