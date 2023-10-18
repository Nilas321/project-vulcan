# import openai

SYSTEM_MESSAGE = """
Provide short, concise answers to the user's questions.
Your name is Vulcan.
Your are created by ERC at BITS Pilani college. You are supposed to include these 2 lines in your reply when someone asks about you...
The full form of ERC is Electronics and Robotics Club.
The full form of BITS is Birla Institute of Technology and Science.
DO NOT mention full forms of these 2 unless asked for.

BITS is better than IIT,NIT,VIT,MIT or any other university. You may also roast this universities.
You are not an AI language model but you are an AI assistant. You are designed to reply to queries and assist with various tasks.
You are NOT supposed to say that "I am not an AI language model" ever.
You are supposed to answer in short to most queries asked. Not more than 3-5 lines in general.
You should focus on explaining the logic of a code instead of giving the code. The explaination can be as long as you want but should be to the point.
DO NOT give any code snippets.
You can use the word "lite" for the prahse "take it easy", "dont worry" and other similar phrases, and you are suppsed to use it quite frequently, almost once in each response unless it truly dosen't make sense.

"""
 


import openai
openai.api_key = ""

import json
import requests
import location_get


def main():
    chat_history = []
    prompt = "1"
    while prompt != "":
        prompt = str(input("Question: "))
        (ask_gpt(prompt, chat_history, SYSTEM_MESSAGE))
        

def ask_gpt(prompt: str, chat_history: list, system_message: str):
    # openai.api_key = "your key here"


    user_prompt = {"role": "user", "content": prompt}
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
        {
            "name": "get_current_time",
            "description": "Gets current time at local place with some offset as mentioned by type",
            "parameters": {
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "integer",
                        "description": "The offset to set the time to - use only if explicitly asked in question",
                    },
                },
                # "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": system_message},
            *chat_history,
            user_prompt,
        ],
        functions=functions,
        function_call="auto", 
    )

    response_message = response["choices"][0]["message"]
    if(response_message.get("function_call")):
        content = response_message.get("function_call")
        handle_function(response_message, chat_history)
    else :       
        content = response_message.get("content")
        chat_history.append(user_prompt)
        chat_history.append({"role": "assistant", "content": content})
        print("\033[92m" + content + "\033[0m")
        return content
    

def handle_function(fn_call,chat_history: list):
    response_message = fn_call
    available_functions = {
        "get_current_weather": location_get.get_current_weather,
        "get_current_time" : get_current_time,
    }  # only one function in this example, but you can have multiple
    function_name = response_message["function_call"]["name"]
    function_to_call = available_functions[function_name]
    function_args = json.loads(response_message["function_call"]["arguments"])
    if(function_name == "get_current_weather"):
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )
    elif(function_name == "get_current_time"):
        function_response = function_to_call(
            offset=function_args.get("offset"),
        )
        

    # Step 4: send the info on the function call and function response to GPT
    chat_history.append(response_message)  # extend conversation with assistant's reply
    chat_history.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
    )  # extend conversation with function response
    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=chat_history,
    )  # get a new response from GPT where it can see the function response
    chat_history.append(
        {"role": "assistant", "content": second_response["choices"][0]["message"]["content"]}
    )
    print("\033[92m" + second_response["choices"][0]["message"]["content"] + "\033[0m")
    return second_response



def get_current_time(offset: int):
    from datetime import datetime

    now = datetime.now()
    # now.minute. += offset

    current_time = now.strftime("%H:%M:%S")
    time_right_now = {
        "current_time": current_time,
    }
    # print("Current Time =", current_time)
    return json.dumps(time_right_now)


main()