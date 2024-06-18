import librosa
import numpy as np
import matplotlib.pyplot as plt

def calculate_bpm(audio_path):
    try:
        # Load the audio file
        y, sr = librosa.load(audio_path, sr=22050)  # Load with a fixed sample rate
        print(f"Audio loaded: y shape = {y.shape}, sample rate = {sr}")

        # Get the onset envelope
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        
        # Perform beat tracking
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, start_bpm=150, tightness=100)
        print(f"Beat tracking performed: tempo = {tempo}, beats length = {len(beats)}")

        # Get the times of the beats
        beat_times = librosa.frames_to_time(beats, sr=sr)
        print(f"Beat times calculated: beat times length = {len(beat_times)}")

        # Plot the onset envelope and the beat tracking
        plt.figure()
        plt.plot(librosa.times_like(onset_env, sr=sr), onset_env, label='Onset strength')
        plt.vlines(beat_times, 0, onset_env.max(), color='r', alpha=0.75, linestyle='--', label='Beats')
        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('Onset strength')
        plt.title('Onset Strength and Beat Tracking')
        plt.show()

        return tempo, beat_times
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Example usage
audio_path = 'audio2.mp3'  # Ensure this path points to your actual audio file
bpm, beat_times = calculate_bpm(audio_path)
if bpm is not None and beat_times is not None:
    if isinstance(bpm, np.ndarray):
        bpm = bpm[0]  # Assuming tempo is a 1-element array
    print(f"Estimated BPM: {bpm:.2f}")
    print("Beat times:", beat_times)
else:
    print("Failed to calculate BPM and beat times.")
