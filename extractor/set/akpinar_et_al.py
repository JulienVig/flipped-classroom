#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product
import numpy as np

from extractor.extractor import Extractor

from extractor.feature.total_clicks import TotalClicks
from extractor.feature.number_sessions import NumberSessions
from extractor.feature.count_ngrams import CountNGrams
from extractor.feature.sum_time import SumTime

'''
Akpinar, N. J., Ramdas, A., & Acar, U. (2020). Analyzing Student Strategies In Blended Courses Using Clickstream Data.
In Thirteenth International Conference on Educational Data Mining (EDM 2020).
'''

class AkpinarEtAl(Extractor):

    def __init__(self, name='base', vocab=None, ngram=3):
        super().__init__(name)
        self.name = 'akpinar_et_al'
        self.ngram = ngram
        self.perms = list(product(vocab, repeat=ngram))

    def get_labels(self):
        assert self.features is not None and self.perms is not None
        return [f.get_name() for f in self.features] + list(map(lambda perm: '(' + ", ".join(perm) + ')', self.perms))

    def __len__(self):
        assert self.features is not None and self.perms is not None
        return len(self.features) + len(self.perms)

    def extract_features(self, data, settings):
        self.features = [TotalClicks(data, settings),
                         NumberSessions(data, settings),
                         SumTime(data, {**settings, **{'mode':'video'}}),
                         SumTime(data, {**settings, **{'mode':'problem'}})]
        features = [f.compute() for f in self.features] + CountNGrams(data, {**settings, **{'perms': self.perms, 'ngram': self.ngram}}).compute()
        print(features)
        assert len(features) == self.__len__()
        return np.nan_to_num(features)