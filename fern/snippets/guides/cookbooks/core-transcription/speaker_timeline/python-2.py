import matplotlib.pyplot as plt

def plot_speaker_timeline(utterances):
    fig, ax = plt.subplots(figsize=(12, 4))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    speaker_colors = {}

    for utterance in utterances:
        start = utterance.start / 60000 # in minutes
        end = utterance.end / 60000 # in minutes
        speaker = utterance.speaker

        if speaker not in speaker_colors:
            speaker_colors[speaker] = colors[len(speaker_colors) % len(colors)] # set a colour for each new speaker

        ax.barh(speaker, end - start, left=start, color=speaker_colors[speaker], height=0.4) # create horizontal bar plot

    ax.set_xlabel('Time (mins)')
    ax.set_ylabel('Speakers')
    ax.set_title('Speaker Timeline')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()
