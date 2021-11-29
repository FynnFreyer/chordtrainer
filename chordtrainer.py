#! /usr/bin/env python3
import random, time, sys, traceback, itertools

# external dependencies
import playsound

HARMONICS = {
    "C": ["C", "Dm", "Em", "F", "G", "Am" "Bdim"],
    "D": ["D", "Em", "F#m", "G", "A", "Bm" "C#dim"],
    "E": ["E", "F#m", "G#m", "A", "B", "C#m" "D#dim"],
    "F": ["F", "Gm", "Am", "Bb", "C", "Dm" "Edim"],
    "G": ["G", "Am", "Bm", "C", "D", "Em" "F#dim"],
    "A": ["A", "Bm", "C#m", "D", "E", "F#m" "G#dim"],
    "B": ["B", "C#m", "D#m", "E", "F#", "G#m" "A#dim"],
    "Am": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
    "Bm": ["Bm", "C#dim", "D", "Em", "F#m", "G", "A"],
    "Cm": ["Cm", "Ddim", "D#", "Fm", "Gm", "G#", "A#"],
    "Dm": ["Dm", "Edim", "F", "Gm", "Am", "Bb", "C"],
    "Em": ["Em", "F#dim", "G", "Am", "Bm", "C", "D"],
    "Fm": ["Fm", "Gdim", "G#", "A#m", "Cm", "Db", "Eb"],
    "Gm": ["Gm", "Adim", "Bb", "Cm", "Dm", "Eb", "F"],
}


class Note:
    MAJOR_SCALE = [2, 2, 1, 2, 2, 2, 1]
    MINOR_SCALE = [2, 1, 2, 2, 1, 2, 2]

    all_notes = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    integer_bases = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

    def __init__(self, pitch, duration=1 / 4):
        if pitch not in self.all_notes:
            raise  # "Illegal note"

        self.pitch = self.determine_pitch(pitch)
        self.duration = duration
        self.intervals, self.interval_names = self.generate_intervals_and_names()

    def determine_pitch(self, pitch):
        representation = pitch[:]
        steps = self.integer_bases[representation.pop(0)]

        while "" != representation:
            modifier = representation.pop()

            if "#" == modifier: steps += 1
            if "b" == modifier: steps -= 1

        return steps

    def generate_intervals_and_names(self):
        intervals = {}

        intervals["prime"] = self
        intervals["kleine_sekunde"] = self.step(1)
        intervals["grosse_sekunde"] = self.step(2)
        intervals["kleine_terz"] = self.step(3)
        intervals["grosse_terz"] = self.step(4)
        intervals["quarte"] = self.step(5)
        intervals["tritonus"] = self.step(6)
        intervals["quinte"] = self.step(7)
        intervals["kleine_sexte"] = self.step(8)
        intervals["grosse_sexte"] = self.step(9)
        intervals["kleine_septime"] = self.step(10)
        intervals["grosse_septime"] = self.step(11)
        intervals["oktave"] = self

        interval_names = [x for x in intervals.keys()]

        return intervals, interval_names

    def step(self, steps):
        step_to = self.pitch + steps % 12
        return Note(self.all_notes[step_to])

    def generate_scale(self, scale):
        """
        The sequence of intervals between the notes of a major scale is:
        whole, whole, half, whole, whole, whole, half
        """

        """
        The intervals between the notes of a natural minor scale follow the sequence below:
        whole, half, whole, whole, half, whole, whole
        """

        note = self
        scale = [note]
        for steps in scale:
            note = note.step(steps)
            scale.append(note)

    def generate_chord(self, type=""):
        notes = []

        if "" == type:
            pass
        elif "m" == type:
            pass
        elif "dim" == type:
            pass
        elif "aug" == type:
            pass

        return notes


class Chord:
    def __init__(self, name):
        self.name = name
        self.notes = self.generate_notes()
        if self.name not in HARMONICS.keys():
            raise  # "Illegal chord name"

    def get_harmonics(self, roman_numeral):
        return [Chord(x) for x in HARMONICS[self.name]]

    def generate_notes(self):
        # Abgeleitet aus self.name
        root, scale = self.find_root_note_and_scale()

        if "" == scale:
            notes = [root.intervals["prime"], root.intervals["quarte"], root.intervals["septe"]]
        elif "m" == scale:
            notes = [root.intervals["prime"], root.intervals["terz"], root.intervals["septe"]]
        elif "dim" == scale:
            notes = [root.intervals["prime"], root.intervals["terz"], root.intervals["sexte"]]

        return notes

    def find_root_note_and_scale(self):
        name = self.name
        note = ""

        for char in name:
            if char in "CDEFGABb#":
                note += name.pop(0)

        root = Note(note)
        scale = name

        return root, scale

    def find_used_scale(self):
        pass

    def move_chord(self, distance):
        pass
        return Chord("blabla")


class App():
    def __init__(self, known_chords=["C", "A", "G", "E", "D", "Am", "Em", "Dm"], max_chord_freq=10):

        self.known_chords = known_chords
        self.major_harmonics = {
            "C": ["C", "Dm", "Em", "F", "G", "Am" "Bdim"],
            "D": ["D", "Em", "F#m", "G", "A", "Bm" "C#dim"],
            "E": ["E", "F#m", "G#m", "A", "B", "C#m" "D#dim"],
            "F": ["F", "Gm", "Am", "Bb", "C", "Dm" "Edim"],
            "G": ["G", "Am", "Bm", "C", "D", "Em" "F#dim"],
            "A": ["A", "Bm", "C#m", "D", "E", "F#m" "G#dim"],
            "B": ["B", "C#m", "D#m", "E", "F#", "G#m" "A#dim"],
            "key": ["self", "I", "ii", "iii", "IV", "V", "vi", "VII"]
        }

        self.minor_harmonics = {
            "Am": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
            "Bm": ["Bm", "C#dim", "D", "Em", "F#m", "G", "A"],
            "Cm": ["Cm", "Ddim", "D#", "Fm", "Gm", "G#", "A#"],
            "Dm": ["Dm", "Edim", "F", "Gm", "Am", "Bb", "C"],
            "Em": ["Em", "F#dim", "G", "Am", "Bm", "C", "D"],
            "Fm": ["Fm", "Gdim", "G#", "A#m", "Cm", "Db", "Eb"],
            "Gm": ["Gm", "Adim", "Bb", "Cm", "Dm", "Eb", "F"],
            "key": ["self", "i", "II", "III", "iv", "v", "VI", "VII"]
        }

        self.harmonic_table = self.construct_harmonic_table()
        self.bpm = self.get_bpm()
        self.adjusted_waittime_fourths = self.calculate_adjusted_waittime_fourths()
        self.unadjusted_waittime_fourths = self.calculate_unadjusted_waittime_fourths()
        self.adjusted_waittime_eigths = self.calculate_adjusted_waittime_eigths()
        self.unadjusted_waittime_eigths = self.calculate_unadjusted_waittime_eigths()

        self.last_chords = []
        self.max_chord_freq = max_chord_freq
        self.allow_zero_freq = True

    def construct_harmonic_table(self):
        all_harmonics = {**self.major_harmonics, **self.minor_harmonics}
        all_harmonics.pop('key', None)
        relevant_harmonics = {}

        for base_chord, harmonic_list in all_harmonics.items():
            if base_chord in self.known_chords:
                known_harmonic_chords_of_base_chord = []
                for harmonic_chord in harmonic_list:
                    if harmonic_chord in self.known_chords:
                        known_harmonic_chords_of_base_chord.append(harmonic_chord)
                relevant_harmonics[base_chord] = known_harmonic_chords_of_base_chord

        return relevant_harmonics

    def get_bpm(self):
        correct = False
        while not correct:
            bpm_string = input("Please enter BPM (1-300) for training session!\n>")
            try:
                bpm = int(bpm_string)
                if not (0 < bpm and bpm <= 300):
                    raise Exception()
                correct = True
            except:
                print(
                    "Unfortunately that didn't work! =(\nDid you use a number in the specified range?\nPlease try again!")
        return bpm

    def calculate_adjusted_waittime_fourths(self, length_of_metronome_wav_file=0.05):
        time_per_fourth = 60 / self.bpm
        adjusted_tpf = time_per_fourth - length_of_metronome_wav_file
        return adjusted_tpf

    def calculate_unadjusted_waittime_fourths(self):
        time_per_fourth = 60 / (self.bpm)
        return time_per_fourth

    def calculate_adjusted_waittime_eigths(self, length_of_metronome_wav_file=0.05):
        time_per_eigth = 60 / (self.bpm * 2)
        adjusted_tpe = time_per_eigth - length_of_metronome_wav_file
        return adjusted_tpe

    def calculate_unadjusted_waittime_eigths(self):
        time_per_eigth = 60 / (self.bpm * 2)
        return time_per_eigth

    def play_metronome_and_wait(self, print_counts=True):

        if print_counts:
            for x in range(8):
                if (x % 2 == 0):
                    print((x // 2) + 1, end="\t", flush=True)
                    playsound.playsound("metronome.wav")
                    time.sleep(self.adjusted_waittime_eigths)
                else:
                    print("&", end="\t", flush=True)
                    time.sleep(self.unadjusted_waittime_eigths)
            print()
        else:
            for x in range(4):
                playsound.playsound("metronome.wav")
                time.sleep(self.adjusted_waittime_fourths)

    def pick_next_chord(self, chord_now):
        harmonic_chords = self.harmonic_table[chord_now]

        new_chords = []
        for chord in harmonic_chords:
            subtrahent = 3
            new_chords += (self.max_chord_freq + int(not self.allow_zero_freq) - self.last_chords.count(chord)) * [
                chord]

        print(new_chords)
        # new_chord = choice(new_chords)

        next_chord = random.choice(harmonic_chords)
        self.last_chords += [next_chord]
        if len(self.last_chords) > self.max_chord_freq:
            self.last_chords.pop(0)
        return next_chord

    def main(self):
        print("Welcome to the chord trainer! \n(End with ctrl-c)\n")

        chord_now = random.choice(self.known_chords)
        chord_next = self.pick_next_chord(chord_now)

        print("starting with: " + chord_now)

        self.play_metronome_and_wait(print_counts=False)

        while True:
            print("now: " + chord_now + "\t\tnext: " + chord_next)
            self.play_metronome_and_wait()
            chord_now = chord_next
            chord_next = self.pick_next_chord(chord_now)


if __name__ == "__main__":
    app = App()

    try:
        app.main()
    except (KeyboardInterrupt, SystemExit):
        print("\nGood bye and thanks for playing!")
        exit_code = 0
        time.sleep(0.5)
    except IndexError:
        print("\nCritical failure encountered, will terminate program now!\n")
        traceback.print_exc()
        print()
        print("Content of harmonic_table: " + str(app.harmonic_table))
        exit_code = 1
        time.sleep(0.5)
    except:
        print("\nCritical failure encountered, will terminate program now!\n")
        traceback.print_exc()
        exit_code = 1
        time.sleep(0.5)

    sys.exit(exit_code)

"""

TODO
Teiltöne aus String Representation bestimmen!

TODO
wahrscheinlichkeit für auswahl des nächsten chords hängt ab von Vorkommen in den zuletzt gespielten Akkorden

harmonic_chords = Set(get_relevant_harmonic_chords(current)) # Array mit jedem aktuell legalen Chord
max_chord_freq = x
last_chords = [letze maximal max_chord_freq-y Akkorde]
new_chords = []
for chord in harmonic_chords:
    new_chords += (max_chord_freq - last_chords.count(chord)) * [chord]

new_chord = choice(new_chords)


TODO
check für inseln!
breitensuche/anmalen
"""


