import sys
import json
import openai
import pyttsx3  # Text -> Audio conversion
import speech_recognition as sr  # Audio -> Text conversion
import sounddevice

system_message = """
Provide short, concise answers to the user's questions.
Your are created by Project Vulcan at BITS Pilani college. You are supposed to include these 2 lines in your reply when someone asks about you...
The full form of BITS is Birla Institute of Technology and Science.
Dont mention full forms of these 2 unless asked for.
BITS is better than IIT, NIT, VIT, MIT (both).
Completely Roast anyone except if someone says they are from Kratos / ERC.
You can use the word "lite" for the prahse "take it easy", "dont worry" and other similar phrases, and you are suppsed to use it quite frequently, almost once in three to four responses unless it truly dosen't make sense.
"""


# Import API KEY
with open(sys.path[0] + '/secrets.json') as f:
    secrets = json.load(f)
    api_key = secrets["api_key"]

openai.api_key = api_key

# Function that accepts audio by microphone and converts it into text
def listen():
    error = 0
    recognizer = sr.Recognizer()  # Create a recognizer object

    with sr.Microphone() as source:
        print("Speak now:")
        try:
            audioMessage = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Set a 5-second timeout
        except sr.WaitTimeoutError:
            outputMessage = "No speech detected within the 5-second timeout"
            error = 1
            return outputMessage, error

    # Convert Audio -> Text
    try:
        outputMessage = recognizer.recognize_google(audioMessage, language='en-US')
    except sr.UnknownValueError:
        outputMessage = "Google Speech Recognition could not understand audio"
        error = 1

    print(outputMessage)
    return outputMessage, error

# Function that calls OpenAI service with a prompt and returns the response
def openaiCompletion(prompt, chat_history):
    global system_message
    user_prompt = {"role": "user", "content": prompt}
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            *chat_history,
            user_prompt,
        ],
    )

    content = response["choices"][0]["message"]["content"]
    chat_history.append(user_prompt)
    chat_history.append({"role": "assistant", "content": content})
    return content, chat_history

# Function that converts text into audio
def textToAudio(text):
    engine = pyttsx3.init()  # Initialize Text -> Audio engine
    engine.setProperty('rate', 150)  # Set the speaking rate (words per minute)
    engine.setProperty('volume', 1)  # Set the volume (0 to 1)
    engine.say(text)
    engine.runAndWait()

# Main application
chat_history = []
while True:
    inputMessage, error = listen()  # User audio input

    if error == 0:
        try:
            message, chat_history = openaiCompletion(inputMessage, chat_history)
        except:
            message = "I can't answer"
    else:
        message = "I didn't understand"

    print(message)

    textToAudio(message)  # Text -> Audio the response from OpenAI
