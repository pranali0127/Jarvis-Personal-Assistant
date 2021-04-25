import pyttsx3
import datetime
import speech_recognition as sr
import audiomath
import wikipedia
import webbrowser
import os
import random
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# print(voices)

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('your_mail','your_password')
    server.sendmail('your_mail',to,content)
    server.close()



# Microphone from speech recognition library is not working on my system
# it showing me error " Could not find PyAudio; check installation "
# that's why i am using audiomath. i find this solution from stackoverflow.

class DuckTypedMicrophone(sr.AudioSource):  # descent from AudioSource is required purely to pass an assertion in Recognizer.listen()
    def __init__(self, device=None, chunkSeconds=1024 / 44100.0):  # 1024 samples at 44100 Hz is about 23 ms
        self.recorder = None
        self.device = device
        self.chunkSeconds = chunkSeconds

    def __enter__(self):
        self.nSamplesRead = 0
        self.recorder = audiomath.Recorder(audiomath.Sound(5, nChannels=1), loop=True, device=self.device)
        # Attributes required by Recognizer.listen():
        self.CHUNK = audiomath.SecondsToSamples(self.chunkSeconds, self.recorder.fs, int)
        self.SAMPLE_RATE = int(self.recorder.fs)
        self.SAMPLE_WIDTH = self.recorder.sound.nbytes
        return self

    def __exit__(self, *blx):
        self.recorder.Stop()
        self.recorder = None

    def read(self, nSamples):
        sampleArray = self.recorder.ReadSamples(self.nSamplesRead, nSamples)
        self.nSamplesRead += nSamples
        return self.recorder.sound.dat2str(sampleArray)

    @property
    def stream(
            self):  # attribute must be present to pass an assertion in Recognizer.listen(), and its value must have a .read() method
        return self if self.recorder else None


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    #speak("Jarvis is Starting")
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Hi,Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hi,Good Afternoon")
    else:
        speak("Hi,Good Evening")
    speak("I am Jarvis. Please tell me how may I help you")


def takeCommand():
    # it takes microphone input from the user and returns string output
    r = sr.Recognizer()
    '''
    you can use following code if you didn't get any error
        with sr.Microphone() as sourse:
        print("Listening.... ")
        r.pause_threshold = 1
        audio = r.listen(sourse)
    '''
    with DuckTypedMicrophone() as sourse:
        print("Listening.... ")
        r.pause_threshold = 1
        audio = r.listen(sourse)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please....")
        return "None"
    return query


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        # logic to execute user commands
        if 'wikipedia' in query:
            speak('Searching wikipedia')
            query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            #print(results)
            speak(results)
        elif 'youtube' in query:
            speak("Okay, opening youtube")
            webbrowser.open("https://www.youtube.com/")
        elif 'google classroom' in query:
            speak("Okay, opening google classroom")
            webbrowser.open("https://classroom.google.com/u/2/h")
        elif 'linkedin' in query:
            speak("Okay, opening linkedin")
            webbrowser.open("https://www.linkedin.com/feed/")
        elif 'pinterest' in query:
            speak("Okay, opening pinterest")
            webbrowser.open("https://www.pinterest.ca/")
        elif 'google' in query:
            speak("Okay, opening google")
            webbrowser.open("https://www.google.com/")

        elif 'music' in query:
            speak("Okay, playing your favorite music")

            music_dir = 'C:\\Users\\PRIYAMATE\\music'
            songs = os.listdir(music_dir)
            song_index = random.randint(0,len(songs))
            os.startfile(os.path.join(music_dir,songs[song_index]))
            print(f"Currently playing : {songs[song_index]}\n")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time now is {strTime}")
        elif 'open code' in query:
            code_path = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.3.2\\bin\\pycharm64.exe"
            os.startfile(code_path)
        elif 'email to Pranali' in query:
            try:
                speak("what should i say?")
                content = takeCommand()
                to = "receiver's_mail@gmail.com"
                sendEmail(to,content)
                speak("Email send to Pranali")
            except Exception as e:
                print(e)
                speak("Sorry meri dost Pranali, I am not able to send this Email")
        elif 'quit' in query:
            speak("Okay")
            speak("This is jarvis signing off!! Have a Good day")
            exit()




