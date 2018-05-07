from tkinter import *
from tkinter import ttk

import speech_recognition as sr
import pyaudio
import wave
import math

from google.cloud import language_v1beta2
from google.cloud.language_v1beta2 import enums
from google.cloud.language_v1beta2 import types

import os

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("De-stract")
        canvas = Canvas(master, width=600, height=0, background="black")
        title = Label(master, text="De-stract", foreground="black", font=("Avenir", 72))
        title.grid()

        nb = ttk.Notebook(master)
        style = ttk.Style()

        style.theme_create("flatUI", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [180, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [30, 1], "background": "white"},
                "map": {"background": [("selected", "black")], "foreground": [("selected", "white")],
                        "expand": [("selected", [1, 1, 1, 0])]}},
            "TNotebook.Button": {
                "configure": {"padding": [30, 1], "background": "white"},
                "map": {"background": [("selected", "black")], "foreground": [("selected", "white")],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        style.theme_use("flatUI")

        page1 = ttk.Frame(nb, width=600, height=400)
        page2 = ttk.Frame(nb, width=600, height=400)
        nb.add(page1, text="Main")
        nb.add(page2, text="Sound Settings")

        slogan = Label(root, text="Digital Adderall").grid()

        Page1.createlist(master, page1)

        nb.grid()
        canvas.grid()


class Page1:
    def createlist(self, page):
        choices = Listbox(page, selectmode=SINGLE)
        begin = Button(page, text="Begin", font="Avenir", command=lambda: userchoice(choices),
                       background="black", foreground="white", highlightbackground="light grey")
        exit = Button(page, text="Exit", font="Avenir", command=quit, bg="black",
                      fg="#ffffff", highlightbackground="light grey")

        choices.insert(1, "Chemistry")
        choices.insert(2, "Physics")
        choices.insert(3, "Economics")
        choices.insert(4, "Biology")
        choices.insert(5, "History")
        choices.insert(6, "Math")

        choices.pack(side=TOP, pady=30)
        begin.pack()
        exit.pack()

        def userchoice(choices):
            thechoice = ''
            choice = choices.curselection()
            thechoice = choices.get(choice)
            print(thechoice)
            main('/Science/' + thechoice)



root = Tk()
window = MainWindow(root)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Shumpu/Downloads/google/My Project-455e0b88df87.json"


def classi(text):
    # print('1')
    language_client = language_v1beta2.LanguageServiceClient()

    # print('2')
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    # print('3')

    result = language_client.classify_text(document)
    # print(4)

    ffa = result.categories

    # print(ffa)

    ar = ['', '']

    counter = 0
    for category in ffa:
        ar[0] = category.name
        ar[1] = category.confidence
        # print(ar)
        break

    return ar


r = sr.Recognizer()


def record():

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "C:/Users/Shumpu/PycharmProjects/machine learning/tensorlfowstuff/audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


    audio = 'audio.wav'
    return audio


def play_sound():
    PyAudio = pyaudio.PyAudio  # initialize pyaudio

    # See https://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 16000  # number of frames per second/frameset.

    FREQUENCY = 500  # Hz, waves per second, 261.63=C4-note.
    LENGTH = 1  # seconds to play sound

    if FREQUENCY > BITRATE:
        BITRATE = FREQUENCY + 100

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''

    # generating wawes
    for x in range(NUMBEROFFRAMES):
        WAVEDATA = WAVEDATA + chr(int(math.sin(x / ((BITRATE / FREQUENCY) / math.pi)) * 127 + 128))

    for x in range(RESTFRAMES):
        WAVEDATA = WAVEDATA + chr(128)

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1),
                    channels=1,
                    rate=BITRATE,
                    output=True)

    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()
    p.terminate()


def longestSubstringFinder(topic, string2):
    answer = ""
    len1, len2 = len(topic), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and topic[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""

    if (
            topic.lower() == 'chemistry' or topic.lower() == 'physics' or topic.lower() == 'mathematics' or topic.lower() == 'biology') and string2.lower() == '/science/chemistry' or string2.lower() == '/science/biological sciences' or string2.lower() == '/science/physics' or string2.lower() == '/science/mathematics'  or string2.lower == '/science':
        return True
    else:
        return (len(answer) > 3)




# ----------------------------------------------------

def main(topic):
    on = True
    """print("Hello, you are using DeStract. To begin, please enter the category you are about to discuss: ")
    topic = input("Topic: ")
    print("Choose the interval of time passed in which you are off topic that it will sound the alarm: ")
    interval = int(input())"""
    listening = True
    while (on):
        win = Toplevel()
        # display message
        message = "De-stract is running..."
        Label(win, text=message).pack()

        def off():
            on = False
        Button(win, text='End Session', background="light green", foreground="black",
               command=off()).pack(side=TOP, pady=10)
        if not on:
            win.destroy()

        root.update()
        counter = 0
        while (listening):

            toParse = ''
            try:

                for f in range(3):
                    audio = record()

                    with sr.AudioFile(audio) as source:
                        audio = r.record(source)
                    asdf = r.recognize_google(audio)
                    toParse += asdf
                    print(toParse)
                    if(len(toParse) < 20):
                        f = 1

                # bee = classi(toParse)

                # asdf = r.recognize_google(audio)

                print(toParse)

                if len(toParse) < 20:
                    continue

                else:
                    print(toParse)
                    print(counter)
                    bee = classi(toParse)

                    print('category name: ', bee[0])
                    print('category confidence: ', bee[1], '\n')

                    if longestSubstringFinder(topic, bee[0]) == False:
                        counter += 1
                        print(counter)
                        continue
                    else:
                        counter=counter


            except:

                toParse += ''
                continue


            finally:

                #on = True
                print(counter)
                if counter >= 1:
                    print(counter)
                    play_sound()
                    print('You\'re off topic')
                    counter = 0
                    break


#if __name__ == "__main__":
root.mainloop()