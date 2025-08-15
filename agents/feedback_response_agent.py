from typing import Optional, Dict
from utils.config import Config

# LangChain imports
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

class RuleBasedSentiment:
    POS = ["good","great","amazing","excellent","awesome","tasty","love","delicious","friendly","fast","rich","flavorful"]
    NEG = ["bad","terrible","awful","disgusting","slow","hate","cold","rude","worst","dirty","overcooked","bland","late"]

    @classmethod
    def classify(cls, text: str) -> str:
        t = text.lower()
        pos = sum(w in t for w in cls.POS)
        neg = sum(w in t for w in cls.NEG)
        if pos > neg: return "positive"
        if neg > pos: return "negative"
        return "neutral"

    @staticmethod
    def response(text: str, sentiment: str) -> str:
        if sentiment == "positive":
            return ("Thanks so much for the kind words! We're thrilled you enjoyed your visit. "
                    "Can't wait to welcome you back to SteamNoodles 🍜")
        if sentiment == "negative":
            return ("We're sorry your experience fell short. Please DM us with more details so we can make it right — "
                    "your feedback genuinely helps us improve.")
        return ("Thanks for sharing your thoughts. We appreciate your feedback and "
                "will keep working to serve you better.")

class FeedbackResponseAgent:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.llm = None
        if cfg.openai_api_key:
            try:
                self.llm = ChatOpenAI(
                    api_key=cfg.openai_api_key,
                    model=cfg.model_name,
                    temperature=cfg.temperature,
                    max_tokens=cfg.max_tokens,
                )
            except Exception:
                self.llm = None

        self.cls_prompt = PromptTemplate.from_template(
            "Classify the sentiment of this restaurant review as exactly one token from "
            "'positive', 'negative', or 'neutral'. Review: {review}"
        )
        self.reply_prompt = PromptTemplate.from_template(
            "You are SteamNoodles' support agent. The review sentiment is {sentiment}. "
            "Write a short, polite, context-aware reply (max 2 sentences) to this review: {review}"
        )
        self.parser = StrOutputParser()

    def _classify_with_llm(self, review: str) -> Optional[str]:
        if not self.llm:
            return None
        chain = self.cls_prompt | self.llm | self.parser
        out = chain.invoke({"review": review}).strip().lower()
        if out in {"positive","negative","neutral"}:
            return out
        return None

    def _reply_with_llm(self, review: str, sentiment: str) -> Optional[str]:
        if not self.llm:
            return None
        chain = self.reply_prompt | self.llm | self.parser
        out = chain.invoke({"review": review, "sentiment": sentiment}).strip()
        return out or None

    def process(self, review: str) -> Dict[str, str]:
        review = (review or "").strip()
        if not review:
            return {"sentiment": "neutral", "response": "Thanks for reaching out to us."}

        # Try LLM classification then fallback
        sentiment = self._classify_with_llm(review) or RuleBasedSentiment.classify(review)
        # Try LLM reply then fallback
        response = self._reply_with_llm(review, sentiment) or RuleBasedSentiment.response(review, sentiment)
        return {"sentiment": sentiment, "response": response}
