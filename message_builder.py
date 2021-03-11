#! /usr/bin/env python3
import os
from gtts import gTTS

try:
    os.mkdir("audio")
except FileExistsError:
    pass

os.chdir("audio")

chords = ["C", "A", "G", "E", "D", "Am", "Em", "Dm"]
chords_pronunciation_dict = {"C" : "C", "A" : "A", "G" : "G", "E" : "E", "D" : "D", "Am" : "Ay minor", "Em" : "E minor", "Dm" : "D minor"}



bpm_choice = "Please enter a number in the range of 1 to 300, to set the beats per minute for your training session!"
audio = gTTS(bpm_choice)
audio.save("bpm_choice.mp3")

bpm_failure = "Unfortunately that didn't work! Did you use a number in the specified range? Please try again!"
audio = gTTS(bpm_failure)
audio.save("bpm_failure.mp3")

welcome = "Welcome to the chord trainer! You can end it at anytime using control c!"
audio = gTTS(welcome)
audio.save("welcome.mp3")

good_bye = "Good bye and thanks for playing!"
audio = gTTS(good_bye)
audio.save("good_bye.mp3")

critical_failure = "Critical failure encountered, will terminate program now!"
audio = gTTS(critical_failure)
audio.save("critical_failure.mp3")


for chord_from in chords:
    for chord_to in chords:
        audio = gTTS("Now play chord {}, and after that {}".format(chords_pronunciation_dict[chord_from], chords_pronunciation_dict[chord_to]))
        audio.save("from_{}_to_{}.mp3".format(chords_pronunciation_dict[chord_from], chords_pronunciation_dict[chord_to]))


