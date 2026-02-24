import random
from .analyzer import MegaSenaAnalyzer

class MegaSenaSelector:
    def __init__(self, csv_path="data/megasena.csv"):
        self.analyzer = MegaSenaAnalyzer(csv_path)
        self.balls = list(range(1, 61))

    def weighted_pick(self, w_freq=1.0, w_rec=1.0, w_gap=1.0):
        freq = self.analyzer.frequency()
        rec = self.analyzer.recency()
        gap = self.analyzer.gap()

        max_freq = max(freq.values()) or 1
        max_rec = max(rec.values()) or 1
        max_gap = max(gap.values()) or 1

        weights = {}
        for b in self.balls:
            nf = freq[b] / max_freq
            nr = rec[b] / max_rec
            ng = gap[b] / max_gap

            score = nf * w_freq + ng * w_gap + nr * w_rec
            weights[b] = max(score, 0.0001)

        selected = []
        local_weights = weights.copy()

        for _ in range(6):
            total_w = sum(local_weights[b] for b in self.balls if b not in selected)
            r = random.uniform(0, total_w)
            upto = 0
            for b in self.balls:
                if b in selected:
                    continue
                w = local_weights[b]
                if upto + w >= r:
                    selected.append(b)
                    break
                upto += w

        selected.sort()
        return selected
