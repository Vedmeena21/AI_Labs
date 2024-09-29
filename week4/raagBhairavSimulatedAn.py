!pip install pydub -q

import random
import math
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import io
import IPython.display as ipd

class RaagBhairav:
    def __init__(self):
        self.name = 'Bhairav'
        # swar. represents lower octave swar, swar' represents upper octave swar
        self.aaroh = ["S", "r", "G", "m", "P", "d", "N", "S'"]
        self.avaroh = ["S'", "N", "d", "P", "m", "G", "r", "S"]
        self.vadi = "d"
        self.samvadi = "r"
        self.pakad = (
            ("S", "G", "m", "P", "d", "P"),
            ("P", "d", "m", "P"),
            ("d", "d", "N", "N", "S'", "r'", "S'"),
            ("r", "G", "m", "P", "m", "G", "r", "S"),
            ("d", "P", "m", "G", "r", "S")
        )
        self.sargam = {
            "sthai": "S d P P d m P m G r G r G m P m G r r S N. S r r S d. d. N. S G r G m P m G r r S",
            "antra": "P P d d N S' d N S' d d N S' r' S' N d d P m G m P d r' S' d d P S' N d d P m G r r S S d P P d m P m G r"
        }
        self.lakshan_geet = {
            "sthai": "S r G r S N. S r S d N. N. S S S G m m m m r r r G r G m m m r S S",
            "antra": "P P d d N N S' S' S' S' N S' r' r' m' m' r' S' S' S' r' S' d P G m G m P d P P d N S' S' r' S' N d N d P m G m"
        }
        self.wt = {
            "S": 9, "r": 8, "G": 7, "m": 7, "P": 8, "d": 10, "N": 6,
            "S'": 6, "r'": 4, "m'": 3, "N.": 4, "d.": 3, "S'": 2
        }

def parse_notation(n):
    p = []
    i = 0
    while i < len(n):
        if i + 1 < len(n) and n[i + 1] in ["'", ".", ")"]:
            p.append(n[i:i + 2])
            i += 2
        elif n[i] == "(":
            j = n.index(")", i)
            p.append(tuple(n[i + 1:j].split()))
            i = j + 1
        elif n[i] == "-":
            if p:
                p.append(p[-1])
            i += 1
        elif n[i] != " ":
            p.append(n[i])
            i += 1
        else:
            i += 1
    return p

def generate_melody(raag, length):
    melody = []
    while len(melody) < length:
        if random.random() < 0.5:
            phrase = random.choice(raag.pakad)
            melody.extend(phrase)
        else:
            phrase = random.choice([raag.sargam["sthai"], raag.sargam["antra"], raag.lakshan_geet["sthai"], raag.lakshan_geet["antra"]])
            parsed = parse_notation(phrase)
            start = random.randint(0, len(parsed) - 1)
            end = min(start + length - len(melody), len(parsed))
            melody.extend(parsed[start:end])
    return melody[:length]

def calculate_adherence(melody, raag):
    score = 0

    for pakad_phrase in raag.pakad:
        pakad_count = sum(1 for i in range(len(melody) - len(pakad_phrase) + 1)
                          if melody[i:i + len(pakad_phrase)] == list(pakad_phrase))
        score -= pakad_count * 30

    vadi_count = melody.count(raag.vadi)
    samvadi_count = melody.count(raag.samvadi)
    score -= vadi_count * 15
    score -= samvadi_count * 10

    if any(melody.count(note) > vadi_count for note in set(melody)):
        score += 50

    if len([note for note in set(melody) if melody.count(note) > samvadi_count]) > 1:
        score += 30

    for source in [raag.sargam, raag.lakshan_geet]:
        for part in ["sthai", "antra"]:
            parsed = parse_notation(source[part])
            for i in range(len(melody) - 3):
                if melody[i:i + 4] in [parsed[j:j + 4] for j in range(len(parsed) - 3)]:
                    score -= 20

    for note in melody:
        if note not in raag.aaroh and note not in raag.avaroh:
            score += 100

    for i in range(len(melody) - 2):
        if melody[i:i + 3] in [raag.aaroh[j:j + 3] for j in range(len(raag.aaroh) - 2)] or \
           melody[i:i + 3] in [raag.avaroh[j:j + 3] for j in range(len(raag.avaroh) - 2)]:
            score -= 5

    return score

def get_neighbor(melody, raag):
    new_melody = melody.copy()
    index = random.randint(0, len(melody) - 1)
    if random.random() < 0.5:
        pakad_phrase = random.choice(raag.pakad)
        new_melody[index:index] = pakad_phrase
        if len(new_melody) > len(melody):
            new_melody = new_melody[:len(melody)]
    else:
        new_note = random.choices(
            raag.aaroh + raag.avaroh,
            weights=[raag.wt.get(s, 1) for s in raag.aaroh + raag.avaroh],
            k=1
        )[0]
        new_melody[index] = new_note
    return new_melody

def simulated_annealing(raag, initial_temp=100, cooling_rate=0.995, melody_length=64):
    current_melody = generate_melody(raag, melody_length)
    current_score = calculate_adherence(current_melody, raag)
    best_melody = current_melody
    best_score = current_score
    temp = initial_temp

    while temp > 1:
        neighbor = get_neighbor(current_melody, raag)
        neighbor_score = calculate_adherence(neighbor, raag)

        if neighbor_score < current_score or random.random() < math.exp((current_score - neighbor_score) / temp):
            current_melody = neighbor
            current_score = neighbor_score

        if current_score < best_score:
            best_melody = current_melody
            best_score = current_score

        temp *= cooling_rate

    return best_melody, best_score

def format_melody(melody):
    formatted = []
    for i, note in enumerate(melody):
        if i % 4 == 0 and i != 0:
            formatted.append("|")
        if i % 16 == 0:
            formatted.append("\n")
        formatted.append(str(note))
    formatted.append("|")
    return " ".join(formatted)

def melody_to_audio(melody, tempo=120, sample_rate=44100):
    note_frequencies = {
        "S": 261.63, "r": 277.18, "R": 293.66, "g": 311.13, "G": 329.63,
        "m": 349.23, "M": 369.99, "P": 392.00, "d": 415.30, "D": 440.00,
        "n": 466.16, "N": 493.88, "S'": 523.25
    }

    beat_duration = 60000 / tempo

    audio = AudioSegment.silent(duration=0)

    for note in melody:
        if note in note_frequencies:
            frequency = note_frequencies[note]
            sine_wave = Sine(frequency).to_audio_segment(duration=beat_duration)
            audio += sine_wave
        elif note == "-":
            audio += AudioSegment.silent(duration=beat_duration)

    samples = np.array(audio.get_array_of_samples())

    samples = samples / np.max(np.abs(samples))

    return samples, sample_rate

def save_audio(samples, sample_rate, filename="melody.wav"):
    audio_data = (samples * 32767).astype(np.int16)
    audio = AudioSegment(
        audio_data.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio_data.dtype.itemsize,
        channels=1
    )
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    return buffer

if __name__ == "__main__":
    bhairav = RaagBhairav()
    best_melody, best_adherence_score = simulated_annealing(bhairav)
    print("Generated Melody in Teental:")
    print(format_melody(best_melody))
    print(f"Raag Adherence Score: {best_adherence_score}") # lesser score is better(less than -1700 works best)
    samples, sample_rate = melody_to_audio(best_melody)
    audio_buffer = save_audio(samples, sample_rate)
    display(ipd.Audio(audio_buffer.getvalue(), rate=sample_rate))
