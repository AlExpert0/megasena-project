import pandas as pd

class MegaSenaAnalyzer:
    def __init__(self, csv_path="data/megasena.csv"):
        self.df = pd.read_csv(csv_path)
        self.balls = list(range(1, 61))

    def frequency(self):
        freq = {b: 0 for b in self.balls}
        for _, row in self.df.iterrows():
            for col in ["b1", "b2", "b3", "b4", "b5", "b6"]:
                freq[int(row[col])] += 1
        return freq

    def recency(self):
        rec = {b: None for b in self.balls}
        total = len(self.df)

        for idx, (_, row) in enumerate(self.df.iloc[::-1].iterrows(), start=1):
            for col in ["b1", "b2", "b3", "b4", "b5", "b6"]:
                ball = int(row[col])
                if rec[ball] is None:
                    rec[ball] = idx

        for b in self.balls:
            if rec[b] is None:
                rec[b] = total + 1

        return rec

    def gap(self):
        last_seen = {b: None for b in self.balls}
        total = len(self.df)

        for i, (_, row) in enumerate(self.df.iterrows()):
            draw_index = i + 1
            for col in ["b1", "b2", "b3", "b4", "b5", "b6"]:
                ball = int(row[col])
                last_seen[ball] = draw_index

        gap = {}
        for b in self.balls:
            if last_seen[b] is None:
                gap[b] = total
            else:
                gap[b] = total - last_seen[b]

        return gap
