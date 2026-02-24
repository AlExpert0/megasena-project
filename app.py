from engine.selector import MegaSenaSelector

def main():
    print("Mega-Sena Predictor")
    print("--------------------")

    selector = MegaSenaSelector(csv_path="data/megasena.csv")

    picks = selector.weighted_pick(
        w_freq=1.2,
        w_rec=1.0,
        w_gap=0.8
    )

    print("Your predicted numbers:", picks)

if __name__ == "__main__":
    main()
