import speech_recognition as sr
import pyaudio
import wave
import math

from google.cloud import language_v1beta2
from google.cloud.language_v1beta2 import enums
from google.cloud.language_v1beta2 import types




import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Shumpu/Downloads/google/My Project-455e0b88df87.json"



on = True

#'''credentials="AIzaSyD3g1LoWHLAzpZ44phjhuSHGbi-ng1A7NQ"'''
#AIzaSyD3g1LoWHLAzpZ44phjhuSHGbi-ng1A7NQ
#credentials="AIzaSyC0ueTFpiKw40rXgZaWJyle_dW_t3sddnU"
def classi(text):
   # print('1')
    language_client = language_v1beta2.LanguageServiceClient()

   # print('2')
    document = types.Document(content=text, type = enums.Document.Type.PLAIN_TEXT)
   # print('3')

    result = language_client.classify_text(document)
   # print(4)


    ffa = result.categories

    #print(ffa)

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

def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""

    if (topic.lower() == 'chemistry' or topic.lower() == 'physics' or topic.lower() == 'biology') and string2.lower()=='/science/chemistry' or string2.lower()=='/science/biology' or string2.lower()=='/science/physics' or string2.lower =='/science':
        return True
    else:
        return (len(answer) > 5)




#----------------------------------------------------

print("Hello, you are using DeStract. To begin, please enter the category you are about to discuss: ")
topic = input("Topic: ")

print("Choose the interval of time passed in which you are off topic that it will sound the alarm: ")
interval = int(input())


listening = True

while(on):



    counter = 0
    while(listening):

        toParse = ''
        try:


            for f in range(3):
                audio = record()

                with sr.AudioFile(audio) as source:


                    audio = r.record(source)
                asdf = r.recognize_google(audio)
                toParse += asdf

            # bee = classi(toParse)


            #asdf = r.recognize_google(audio)

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
                    if counter > 0:
                        counter -=1


        except:

            toParse += ''
            continue


        finally:

            on = True
            thing = interval / 30
            print(thing)
            print(counter)
            if counter >= thing:
                print(counter)
                play_sound()
                counter = 0
                break
