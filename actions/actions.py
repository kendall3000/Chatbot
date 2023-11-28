# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import wolframalpha
import json
import requests
from urllib.parse import urlencode

# Your API key from Wolfram Alpha
api_key = 'YWQRRR-93QVK98LEX'
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionSolveWolfram(Action):
    def name(self) -> Text:
        return "solve_wolfram"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, any]]:
        
        #dispatcher.utter_message
        # base_url = 'http://api.wolframalpha.com/v2/query?input='
        user_input = tracker.latest_message['text']
        # input_string = user_input.replace(' ', '+')
        # url = f'http://api.wolframalpha.com/v1/result?appid={api_key}&i={input_string}'
        # response = requests.get(url)
        # print(response.json())
        # dispatcher.utter_message(text=response)
  
        # App id obtained by the above steps 
        app_id = api_key 
        
        # Instance of wolf ram alpha  
        # client class 
        client = wolframalpha.Client(app_id) 
        
        # Stores the response from  
        # wolf ram alpha 
        res = client.query(user_input) 
        # Includes only text from the response 
        if res.success == True:
            answer = next(res.results).text
            dispatcher.utter_message(text=answer)
        else:
            answer = "I am not sure about that one. Sorry"
            dispatcher.utter_message(text=answer)
        return []
    

#name of class Action{name}
class ActionGetWiki(Action):
    #the name of the action, must match in domain.yml
    def name(self) -> Text:
        return "get_wiki"
    
    #the code for the custom action
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, any]]:
        #set title equal to entity
        query = tracker.latest_message['entities'][0]['value']
        api_url = "https://en.wikipedia.org/w/api.php"

        # API request parameters
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "exintro": "",
            "explaintext": "",
            "inprop": "url",
            "redirects": "1",
            "titles": query
        }

        # Encode parameters and make the API request
        url_params = urlencode(params)
        url = f"{api_url}?{url_params}"
        response = requests.get(url)
        data = response.json()

        # Extract page information
        page = next(iter(data["query"]["pages"].values()), None)

        if page and "missing" not in page:
            descrip = page["extract"][:200] 
            link = page["fullurl"]
            response = f'Hopefully this wikipedia page can help you out.\n{descrip}\nLink:\n{link}'
            #respond to user
            dispatcher.utter_message(text=response)
        else:
            response = 'Im sorry, I could not find anything.'
            #respond to user
            dispatcher.utter_message(text=response)
        return []
    
# name of class Action{name}
class ActionGetNews(Action):
    # this is just the name of the action, change it to match what you're doing
    def name(self) -> Text:
        return "get_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Assuming you have an entity named 'category' for the news category
        category = tracker.latest_message['entities'][0]['value']

        # News API key and endpoint
        api_key = '49ba5fd5bf1042e2a445ce9897c22b1d'
        endpoint = 'https://newsapi.org/v2/top-headlines'

        # API request parameters
        params = {
            'apiKey': api_key,
            'category': category,
            'country': 'us',  # country code can be changed as needed
        }

        # Make the API request
        try:
            response = requests.get(endpoint, params=params)
            data = response.json()

            # Extract relevant information from the API response
            if data['status'] == 'ok':
                articles = data['articles']
                if articles:
                    # Display the headline of the first news article
                    headline = articles[0]['title']
                    source = articles[0]['source']['name']
                    description = articles[0]['description']
                    link = articles[0]['url']
                    response = f"Here is the latest news in the {category} category from {source}:\n{headline}\n\n{description}\n\nLink: {link}"
                else:
                    response = f"No news available in the {category} category."
            else:
                response = f"Error: {data['message']}"

        except Exception as e:
            response = f"An error occurred: {str(e)}"

        # Send the response to the user
        dispatcher.utter_message(text=response)

        return []
    
class ActionGetWeather(Action):
    def name(self) -> Text:
        return "get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Assuming you have an entity named 'location' for the city name
        location = tracker.latest_message['entities'][0]['value']
        # print(tracker.latest_message['entities'])

        # Weatherstack API key and endpoint
        api_key = '86456a4395fe4fea7d63072313acd5f9'
        endpoint = 'http://api.weatherstack.com/current'

        # API request parameters
        params = {
            'access_key': api_key,
            'query': location,
            'units': 'f'
        }

        # Make the API request
        try:
            response = requests.get(endpoint, params=params)
            data = response.json()

            # Extract relevant information from the API response
            if 'error' in data:
                response = f"Error: {data['error']['info']}"
            else:
                temperature = data['current']['temperature']
                weather_description = data['current']['weather_descriptions'][0]
                response = f"The current temperature in {location} is {temperature}°F with {weather_description} conditions."

        except Exception as e:
            response = f"An error occurred: {str(e)}"

        # Send the response to the user
        dispatcher.utter_message(text=response)

        return []