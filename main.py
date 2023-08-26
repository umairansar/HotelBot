from ChatBot.conversation_flow import ConversationFlow
from ChatBot.IntentRecognizer.intent_model import IntentModel

def main():
    intent_model = IntentModel()
    conversation = ConversationFlow(intent_model)
    conversation.start_conversation()

if __name__ == "__main__":
    print("in main")
    main()