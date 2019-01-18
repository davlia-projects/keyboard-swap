from collections import deque, defaultdict as dd
from nltk.corpus import words
from time import time
from math import log
from pathlib import Path
import pickle

from common import *
from itertools import product

LCONST = 31.022801967573848 # lowest possible ngram score

def gen_cache(words, n):
    total_count = 0.0
    cache = {''.join(k): 1e-7 for k in product(*[colemak + ' '] * n)}
    for word in COLEMAK_WORDS:
        for ngram in roll(word, n):
            cache[ngram] += 1.0
            total_count += 1.0

    # Normalize
    for k in cache.keys():
        cache[k] /= total_count

    return cache

if Path(PICKLE_PATH).is_file():
    print("Cache found. Loading...")
    colemak_cache, qwerty_cache = pickle.load(open(PICKLE_PATH, "rb"))
else:
    print("Cache not found. Regenerating cache...")
    colemak_cache = gen_cache(COLEMAK_WORDS, NGRAMS)
    qwerty_cache = gen_cache(QWERTY_WORDS, NGRAMS)
    pickle.dump([colemak_cache, qwerty_cache], open(PICKLE_PATH, "wb"))

print("Starting.")

class Analyzer:
    def __init__(self):
        self.history = deque()
        self.max_history_len = 20
        self.keyboard = COLEMAK
        self.last_switch = time()

        self.ttl = 5
        self.cooldown = 5

        self.lowest_score = LCONST * (self.max_history_len + NGRAMS - 1)

    def register(self, key):
        if key == u"\u0008":
            # self.history.pop()
            pass
        else:
            self.history.append((key, time()))

        self._expire_history()

    def _expire_history(self):
        if len(self.history) == 0:
            return

        while len(self.history) > 0 and (time() - self.history[0][1] > self.ttl or len(self.history) > self.max_history_len):
            self.history.popleft()


    def current_keyboard(self):
        raw_word = ''.join(kp[0] for kp in self.history)
        colemak_word = ' ' * (self.max_history_len - len(self.history)) + raw_word
        qwerty_word = convert(colemak_word)

        cs = self._score(colemak_word, colemak_cache)
        qs = self._score(qwerty_word, qwerty_cache)
        print(cs, qs)
        if self._throttle(cs, qs):
            return "", self.keyboard

        if qs > cs:
            self.keyboard = QWERTY
            self.history = deque()
            return raw_word, QWERTY
        else:
            self.keyboard = COLEMAK
            self.history = deque()
            return raw_word, COLEMAK


    def _score(self, word, cache):
        score = 0.0
        for i, ngram in enumerate(roll(word, NGRAMS)):
            score += log(cache[ngram])
        normalized_score = 1.0 - (abs(score) / self.lowest_score)
        return normalized_score

    def _throttle(self, cs, qs):
        if cs < SIGNAL_THRESHOLD and qs < SIGNAL_THRESHOLD: # not enough of a signal
            return True

        if time() - self.last_switch < self.cooldown:
            return True

        self.last_switch = time()
        return False

