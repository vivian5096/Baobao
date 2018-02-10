import pyaudio
import wave
import numpy as np
#import matplotlib.pyplot as plt
#from scipy.fftpack import fft
import speech_recognition as sr
from preprocesslexicon import lexdict

def listening(babymem):
    # Define variables for recording audio
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = "file1.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    print("recording...")
    frames = []

    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
    #nframes = np.frombuffer(data,dtype=np.int16) / 2**15

    #loud = len([*filter(lambda x: x >= 0.04, nframes)]) > 2
    #plt.plot(nframes)
    #plt.show()
    #print(loud)

    #fft_out = fft(nframes)
    #plt.plot(np.abs(fft_out))


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save file for analysis later
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # Speech recognition using pocketsphinx
    r = sr.Recognizer()
    with sr.AudioFile("file1.wav") as source:
        audio = r.record(source)  # read the entire audio file

    try:
        playerspeech = r.recognize_sphinx(audio)
#        print("Sphinx thinks you said " + playerspeech)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    # Evaluate the value in the player's response, and save words in baby's
    # memory
    playerspeech = playerspeech.split(' ')
    speechvalue = 0
    for i in range(len(playerspeech)):
        word = playerspeech[i]
        if babymem.get(word) == None:
            babymem[word] = 1
        else:
            babymem[word] += 1
        values = lexdict.get(word,[0,0])
        speechvalue += values[0]*values[1]
    speechvalue = 1/(1+np.exp(-speechvalue))

    return [speechvalue, babymem]

if  __name__ == "__main__":
    a,b = listening({})
    print(a,b)
