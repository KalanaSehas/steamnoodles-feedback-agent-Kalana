import os
import pandas as pd
from datetime import datetime, timedelta
import random

def _generate_sample_df(days: int = 30, per_day: int = 10) -> pd.DataFrame:
    pos = [
        "Amazing noodles and super friendly staff!",
        "Broth was rich and delicious. Loved it!",
        "Quick service, tasty dumplings.",
        "Great value; will come again.",
        "Generous portions; very flavorful."
    ]
    neg = [
        "Soup arrived cold; order was late.",
        "Staff seemed rude and inattentive.",
        "Noodles overcooked and bland.",
        "Long wait and wrong order.",
        "Too salty and place wasn't clean."
    ]
    neu = [
        "Decent food; average experience.",
        "Okay portion size. Nothing special.",
        "Menu has variety but could improve.",
        "Not bad, not great either.",
        "Fine for a quick meal."
    ]
    sentiments = ["positive","negative","neutral"]
    pool = {"positive": pos, "negative": neg, "neutral": neu}

    today = datetime.now().date()
    rows = []
    for d in range(days):
        date = today - timedelta(days=d)
        for _ in range(per_day):
            s = random.choice(sentiments)
            rows.append({
                "date": date.isoformat(),
                "text": random.choice(pool[s]),
                "sentiment": s,
            })
    return pd.DataFrame(rows)

def load_reviews_csv_or_sample(path: str) -> pd.DataFrame:
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Ensure columns exist
        required = {"date","text"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"CSV missing required columns: {missing}")
        # If sentiment column absent, leave it to agent to compute
        return df
    # Generate sample if missing
    df = _generate_sample_df()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return df
