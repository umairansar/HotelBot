import json
import random
import os
import requests
from configs import API_URL, Recommend, RecommendByRating, RecommendByName, RecommendByArea, ScheduleCall, Email

class ConversationFlow:
    def __init__(self, intent_model):
        
        #Init customer info
        self.customer_name = None
        self.customer_email = None
        self.customer_phone = None
        self.hotels = None
        self.jump_from_intent = None
        self.user_input
        
        #load bots phrases to reply
        self.conversation_texts = self.load_conversation_texts()
        
        #load conversation terminators
        self.exit_keywords = self.conversation_texts["bye_keywords"]
        
        #Load Intent Recognition Model
        self.intent_model = intent_model
                
        
    def load_conversation_texts(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(script_directory, "conversation_phrases.json")
        with open(json_file_path, "r") as file:
            return json.load(file)
    
    def exit_if_bye():
        if any(keyword in user_input for keyword in self.exit_keywords):
                print("Bot: Thank you for chatting with me. Have a great day!")
                exit 
    
    def say(self, message, variable=None):
        reply = random.choice(self.conversation_texts[message])
        if variable != None:
            reply = reply.format(place_holder=variable)
        return print(reply)

    def start_conversation(self):
        self.say("greeting")
        self.customer_name = input("You: ")
        self.say("intro", self.customer_name)
        self.user_input = input("You: ").lower()
        self.exit_if_bye()
        self.handle_recommendation(self.user_input)

    def handle_recommendation(self, user_input):
        intent = self.intent_model.predict(user_input)

        if intent == "book_hotel":
            self.reserve_book(intent)
            self.handle_travel_suggestion(user_input)
        elif intent == "travel_suggestion":
            self.travel_suggestion(intent, user_input)
            self.handle_travel_suggestion(user_input)
        elif intent == "make_call":
            self.schedule(intent, user_input)
            self.jump_from_intent = intent
        elif intent == "confirm_reservation":
            self.reserve_book(intent)
            self.handle_travel_suggestion(user_input)
            
    def travel_suggestion(self, intent, user_input):
        self.say("recommend_prompt")
        search_entities = NER(self.user_input)
            
        if (search_entities.Contains("Name")):
            self.say("name_recommend")
            self.hotels = self.make_api_call(RecommendByName)
        elif (search_entities.Contains("Area")):
            self.say("area_recommend")
            self.hotels = self.make_api_call(RecommendByArea)
        elif (search_entities.Contains("Rating")):
            self.say("rating_recommend")
            self.hotels = self.make_api_call(RecommendByRating)
        else:
            self.say("general_recommend")
            self.hotels = self.make_api_call(Recommend)
        
        print(self.hotels)   
        self.user_input = input("You: ").lower()
        self.jump_from_intent = intent  
        
    def reserve_book(self, intent):
        if (self.jump_from_intent == "travel_suggestion"):
                self.say("reserve_hotel")
                self.jump_from_intent = intent
        else:
            self.say("not_understand")
        
        self.user_input = input("You: ").lower()   
        
    def schedule(self, user_input):
        if "email" in user_input:
            self.make_api_call(Email)
        elif "call" in user_input:
            self.make_api_call(ScheduleCall)
            
        self.say("exit_thank_you")     

    def make_api_call(endpoint, data=None):
        try:
            url = f"{API_URL}{endpoint}"
            response = requests.post(url+data if data != None else '')

            if response.status_code == 200:
                data = response.json()
                print(data)
                
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)