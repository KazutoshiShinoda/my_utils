import math
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.font_manager._rebuild()
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.axisbelow'] = True

from ..data import Statistics


bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

def plot_reliability(confidences, scores, title='Reliability', xlabel='Confidence', ylabel='Score', show=True, output_file=None):
    """Plot Reliability Diagram
    See Figure 1 of 'On Calibration of Modern Neural Networks' for details

    `len(confidences) == len(scores)` should be True

    Params:
        confidences: list of confidence on data_i
        scores: list of score on data_i
    """
    assert len(confidences) == len(scores)
    lowerbound2stat = {i: Statistics() for i in bins[:-1]}
    for c, s in zip(confidences, scores):
        lb = round(math.floor(c * 10) * 0.1, 1)
        lowerbound2stat[lb].update_dict({'score': s})

    counts = [lowerbound2stat[lb].global_update for lb in bins[:-1]]
    mean_scores = [lowerbound2stat[lb].mean()['score'] if lowerbound2stat[lb].global_update > 0 else 0 for lb in bins[:-1]]
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111)
    ax.grid(color='gray', linestyle='dotted', linewidth=2)
    ax.bar(bins[:-1], mean_scores, align='edge', width=0.1, color='b', linewidth=1, edgecolor='black')
    ax.patch.set_facecolor('#f8f8f8')
    plt.title(title, fontsize=22, fontweight="bold")
    plt.xlabel(xlabel, fontsize=18)
    plt.ylabel(ylabel, fontsize=18)
    ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.0)
    plt.tick_params(labelsize=18)
    if show:
        plt.show()
    if output_file is not None:
        fig.savefig(output_file)

def calibration_error(confidences, scores, type=''):
    assert len(confidences) == len(scores)
    if type == 'ece':
        lowerbound2stat = {i: Statistics() for i in bins[:-1]}
        for c, s in zip(confidences, scores):
            lb = round(math.floor(c * 10) * 0.1, 1)
            lowerbound2stat[lb].update_dict{'score': s, 'conf': c}
        counts = [lowerbound2stat[lb].global_update for lb in bins[:-1]]
        mean_values = [lowerbound2stat[lb].mean() if lowerbound2stat[lb].global_update > 0 else 0 for lb in bins[:-1]]
        errors = [np.abs(v['score'] - v['conf']) for v in mean_values]
        ece = 0
        n = sum(counts)
        for count, error in zip(counts, errors):
            ece += count * error / n
        return np.abs(np.array(confidences) - np.array(scores)).sum()
    elif type == 'mce':
        return np.max(np.array(confidences) - np.array(scores))
    else:
        raise ValueError(f"type: {type} is not implemented.")
