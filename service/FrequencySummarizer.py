from collections import defaultdict
from heapq import nlargest

from domain.TechArticlesConstants import TECH_LABEL, NON_TECH_LABEL, ENGLISH_STOP_WORDS


class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = ENGLISH_STOP_WORDS

    @staticmethod
    def get_word_frequencies(training_data):
        word_frequencies = {TECH_LABEL: defaultdict(int), NON_TECH_LABEL: defaultdict(int)}
        for label in training_data:
            for article_url in training_data[label]:
                if len(training_data[label][article_url][0]) > 0:
                    raw_frequencies = FrequencySummarizer().extract_raw_frequencies(training_data[label][article_url])
                    for word in raw_frequencies:
                        word_frequencies[label][word] += raw_frequencies[word]
        return word_frequencies

    def extract_features(self, article_content, n, custom_stop_words=None):
        self._freq = self._compute_frequencies(article_content, custom_stop_words)
        if n < 0:
            return nlargest(len(self._freq_keys()), self._freq, key=self._freq.get)
        else:
            return nlargest(n, self._freq, key=self._freq.get)

    def extract_raw_frequencies(self, article):
        freq = defaultdict(int)
        for word in (word for word in article.split() if word not in self._stopwords):
            freq[word] += 1
        return freq

    def _compute_frequencies(self, article_content, custom_stop_words=None):
        freq = defaultdict(int)
        stop_words = (
            set(self._stopwords) if custom_stop_words is None else set(custom_stop_words).union(self._stopwords))
        for word in (word for word in article_content.split() if word not in stop_words):
            freq[word] += 1
        m = float(max(freq.values()))
        for word in list(freq.keys()):
            freq[word] = freq[word] / m
            if freq[word] >= self._max_cut or freq[word] <= self._min_cut:
                del freq[word]
        return freq

