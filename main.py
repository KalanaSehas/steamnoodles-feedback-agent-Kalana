from utils.config import Config
from utils.data_loader import load_reviews_csv_or_sample
from agents.feedback_response_agent import FeedbackResponseAgent
from agents.sentiment_visualization_agent import SentimentVisualizationAgent

def run_feedback(agent: FeedbackResponseAgent):
    text = input("\nEnter a customer review: ").strip()
    result = agent.process(text)
    print(f"\nSentiment: {result['sentiment']}")
    print(f"Auto-reply: {result['response']}\n")

def run_plot(viz: SentimentVisualizationAgent, df):
    date_prompt = input("\nDate range (e.g., 'last 7 days' or '2025-08-01 to 2025-08-15'): ").strip()
    out = viz.plot(df, date_prompt)
    print(f"Plot saved to: {out}")

def main():
    cfg = Config()
    df = load_reviews_csv_or_sample(cfg.data_path)
    feedback_agent = FeedbackResponseAgent(cfg)
    viz_agent = SentimentVisualizationAgent(cfg)

    while True:
        print("""\n🍜 SteamNoodles — AgentX Mini Project
1) Feedback Response Agent
2) Sentiment Visualization Agent
3) Exit
""")
        choice = input("Choose: ").strip()
        if choice == "1":
            run_feedback(feedback_agent)
        elif choice == "2":
            run_plot(viz_agent, df)
        elif choice == "3":
            print("Bye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
