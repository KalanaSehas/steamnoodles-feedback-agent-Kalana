import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "").strip() or None
        self.model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.temperature = float(os.getenv("TEMPERATURE", "0.2"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "128"))
        self.data_path = os.getenv("DATA_PATH", "data/steamnoodles_reviews.csv")
        self.outputs_dir = os.getenv("OUTPUTS_DIR", "outputs")
        os.makedirs(self.outputs_dir, exist_ok=True)
