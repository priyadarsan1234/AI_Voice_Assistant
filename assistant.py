import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import webbrowser
import csv
import wikipedia

listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def store_name(name):
    try:
        with open('user_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', name])
    except Exception as e:
        print(e)
        talk("Sorry, I couldn't store your name.")


def get_stored_name():
    try:
        with open('user_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == 'Name':
                    return row[1]
    except FileNotFoundError:
        return None


def store_address(address):
    try:
        with open('user_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Address', address])
    except Exception as e:
        print(e)
        talk("Sorry, I couldn't store your address.")


def delete_name():
    try:
        with open('user_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', ''])
        talk("Your name has been deleted from my memory.")
    except Exception as e:
        print(e)
        talk("Sorry, I couldn't delete your name.")


def delete_address():
    try:
        with open('user_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Address', ''])
        talk("Your address has been deleted from my memory.")
    except Exception as e:
        print(e)
        talk("Sorry, I couldn't delete your address.")


def change_name():
    talk("Sure, what should I call you now?")
    new_name = take_command()
    if new_name:
        store_name(new_name)
        talk(f"Got it. I'll now call you {new_name}.")


def change_address():
    talk("Sure, what is your new address?")
    new_address = take_command()
    if new_address:
        store_address(new_address)
        talk("Got it. Your address has been updated.")


def get_stored_address():
    try:
        with open('user_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == 'Address':
                    return row[1]
    except FileNotFoundError:
        return None


def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command(timeout=5):
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        voice = listener.listen(source, timeout=timeout)

    try:
        command = listener.recognize_google(voice).lower()
        print('User:', command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print(f"Sorry, there was an error with the request. {e}")
        return ""
    except sr.WaitTimeoutError:
        print("Listening timeout reached.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(search_url)


def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        talk(result)
    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:5])
        talk(f"There are multiple options for {query}. They include: {options}")
    except wikipedia.exceptions.PageError:
        talk("Sorry, I couldn't find any information on that topic.")


def run_assistant():
    talk("Hello! I'm your voice assistant. What can I do for you?")
    
    stored_name = get_stored_name()
    if stored_name:
        talk(f"Welcome back, {stored_name}!")
    else:
        talk("I don't seem to have your name. What should I call you?")
        name_command = take_command()
        store_name(name_command)
        talk("Got it. I'll remember your name.")

    stored_address= get_stored_address()
    if stored_address:
        pass
    else:
        talk("I don't seem to have your Address. Tell Your Address?")
        address_command = take_command()
        store_address(address_command)
        talk("Got it. I'll remember your address.")

    while True:
        command = take_command()
        if 'play' in command:
            search_query = command.replace('play', '')
            talk(f"Playing {search_query} on YouTube")
            pywhatkit.playonyt(search_query)
        elif 'morning' in command:
            talk("Good morning, sir")
        elif 'afternoon' in command:
            talk("Good afternoon")
        elif 'hello' in command:
            talk("Hello ")
        elif 'night' in command:
            talk("Good Night sir")
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The current time is {time}")
        elif 'search for' in command:
            query = command.replace('search for', '')
            talk(f"Searching for {query} on Google")
            search_google(query)
        elif 'my name' in command:
            stored_name = get_stored_name()
            if stored_name:
                talk(f"Your name is {stored_name}")
            else:
                talk("I don't seem to have your name stored.")
        elif 'delete name' in command:
            delete_name()
        elif 'change name' in command:
            change_name()
        elif 'my address' in command:
            stored_address = get_stored_address()
            if stored_address:
                talk(f"Your address is {stored_address}")
            else:
                talk("I don't seem to have your address stored.")
        elif 'delete address' in command:
            delete_address()
        elif 'Create address' in command:
            talk("Tail Me Your Address")
            address_command = take_command()
            store_address(address_command)
            talk("Got it. I'll remember your address.")
        elif 'change address' in command:
            change_address()
        elif 'thank' in command:
            talk("Thank you Have A Nice Day Sir")
        elif 'exit' in command:
            talk("Exiting. Goodbye!")
            break
        elif 'search Wikipedia for' in command:
            query = command.replace('search Wikipedia for', '')
            talk(f"Searching Wikipedia for {query}")
            search_wikipedia(query)
        else:
            talk("Sorry, I didn't catch that. Please try again.")
run_assistant()