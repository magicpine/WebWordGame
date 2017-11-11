# data_utils.py - part of the WordGame - by Paul Barry.
# email: paul.barry@itcarlow.ie

import pickle
import os


PICKLE = 'scores.pickle'


def add_to_scores(name, score) -> None:
    """Add the name and its associated score to the pickle."""
    scores = []
    if not os.path.exists(PICKLE):
        with open(PICKLE, 'wb') as scoresf:
            pickle.dump(scores, scoresf)
    else:
        with open(PICKLE, 'rb') as scoresf:
            scores = pickle.load(scoresf)
    scores.append((score, name))  # Note the ordering here.
    with open(PICKLE, 'wb') as scoresf:
        pickle.dump(scores, scoresf)


def get_sorted_leaderboard() -> list:
    """Return a sorted list of tuples - this is the leaderboard."""
    with open(PICKLE, 'rb') as scoresf:
        return sorted(pickle.load(scoresf))
