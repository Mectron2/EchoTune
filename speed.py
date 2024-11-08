from pydub import AudioSegment
import time
from datetime import timedelta

def pitch(input, output, speed):
    start = time.time()
    sound = AudioSegment.from_file(input, format="wav")
    new_sample_rate = int(sound.frame_rate * speed)
    hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    hipitch_sound = hipitch_sound.set_frame_rate(44100)
    hipitch_sound.export(output, format="wav")
    end = time.time()
    return timedelta(seconds=end - start)