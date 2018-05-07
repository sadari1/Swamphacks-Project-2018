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

theChoice = ''


class Window:
    def __init__(self, master):
        self.master = master
        master.title("De-stract")
        canvas = Canvas(master, width=800, height=0, background="black")
        title = Label(master, text="De-stract", foreground="black", font=("Avenir", 72))
        title.grid()

        nb = ttk.Notebook(master)
        style = ttk.Style()

        style.theme_create("yummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [290, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [30, 1], "background": "white"},
                "map": {"background": [("selected", "black")], "foreground": [("selected", "white")],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        style.theme_use("yummy")

        page1 = ttk.Frame(nb, width=800, height=600)
        page2 = ttk.Frame(nb, width=800, height=600)
        nb.add(page1, text="Main")
        nb.add(page2, text="Sound Settings")

        slogan = Label(root, text="Gucci Gang").grid()

        choices = Listbox(page1, selectmode=SINGLE)
        choiceButton = Button(page1, text="Begin", command=lambda: userChoice(choices))
        quitButton = Button(page1, text="Exit", command=quit)

        def userChoice(choices):
            choice = choices.curselection()
            for i in choice:
                print(choices.get(i))
                theChoice = choices.get(i)
            main('/Science/' + theChoice)
            win = Toplevel()
            # display message
            message = "Dstract is running!"
            Label(win, text=message).pack()
            Button(win, text='End Session', command=win.destroy).pack()

        choices.insert(1, "Chemistry")
        choices.insert(2, "Physics")
        choices.insert(3, "Economics")
        choices.insert(4, "Biology")
        choices.insert(5, "History")
        choices.insert(6, "Math")

        choices.pack()
        choiceButton.pack()
        quitButton.pack()

        nb.grid()
        canvas.grid()


root = Tk()
window = Window(root)

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
    RECORD_SECONDS = 15
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

    FREQUENCY = 1000  # Hz, waves per second, 261.63=C4-note.
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
        for j in range(len2):
            lcs_temp = 0
            match = ''
            while ((i + lcs_temp < len1) and (j + lcs_temp < len2) and topic[i + lcs_temp] == string2[j + lcs_temp]):
                match += string2[j + lcs_temp]
                lcs_temp += 1
            if (len(match) > len(answer)):
                answer = match


    if (
            topic.lower() == 'chemistry' or topic.lower() == 'physics' or topic.lower() == 'biology') and string2.lower() == '/science/chemistry' or string2.lower() == '/science/biological sciences' or string2.lower() == '/science/physics' or string2.lower == '/science':
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

        counter = 0
        while (listening):

            toParse = ''
            try:

                for f in range(2):
               # while len(toParse) < 20:
                    audio = record()

                    with sr.AudioFile(audio) as source:
                        audio = r.record(source)
                    asdf = r.recognize_google(audio)
                    toParse += ' ' + asdf + ' '
                    print(toParse)

                # bee = classi(toParse)

                # asdf = r.recognize_google(audio)

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

                on = True
                print(counter)
                if counter >= 1:
                    print(counter)
                    play_sound()
                    print('Youre off topic')
                    counter = 0
                    break


#if __name__ == "__main__":
root.mainloop()