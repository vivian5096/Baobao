import myRecorder as mR
import wave
import numpy as np
import speech_recognition as sr
from preprocesslexicon import lexdict

WAVE_OUTPUT_FILENAME = "file1.wav"

def listening(babymem, rec):
    # Save file for analysis later
    data = rec.get_buffer()
    #print(rec.get_buffer(True))
    if data == None:
        print('no data')
        return(0,babymem)

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(rec.channels)
    waveFile.setsampwidth(rec.p.get_sample_size(rec.format))
    waveFile.setframerate(rec.rate)
    waveFile.writeframes(data)
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
        return(0,babymem)
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        return(0,babymem)

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
    rec = mR.Recorder(num_chunk = 100)
    rec.stream_init()

    for i in range(50):
        a,b = listening({},rec)
        print(a,b)

    del rec
