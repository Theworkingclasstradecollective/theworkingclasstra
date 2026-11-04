#!/usr/bin/env python3
"""
workout_volume.py - the "Volume Formula" and "Spike Ratio" from chapter 3 of
The Anti-Guru Fitness Manual (Field Manual #002).

    V = L x reps x sets x M        (M = seconds per rep / 2, capped at 2)
    Holds: reps in a hold = seconds held / 2
    Spike ratio = this week's V / your 4-week average
    Highest safe week = 1.10 x your 4-week average
    Deload week = 60% of your peak V

Usage:
    python3 workout_volume.py session session.csv
    python3 workout_volume.py spike --last4 300 320 310 330 --planned 316.5

session.csv columns: move, L, reps, sets, seconds_per_rep
For a hold, leave seconds_per_rep empty and put the seconds held in "reps"
(it is halved for you; M is 1).

Standard library only. V compares you with your own past, not with strangers.
Note: the book rounds each line to one decimal before adding (105.5 in the
worked example); this script adds the exact values (105.45 -> prints 105.4).

Licence: CC BY-SA 4.0 - The Working-Class Strength Collective.
General education, not medical advice.
"""
import argparse
import csv


def tempo_multiplier(seconds_per_rep):
    return min(seconds_per_rep / 2, 2.0)


def line_volume(L, reps, sets, seconds_per_rep=None):
    if seconds_per_rep is None:  # a hold
        return L * (reps / 2) * sets
    return L * reps * sets * tempo_multiplier(seconds_per_rep)


def spike_ratio(planned, last4):
    return planned / (sum(last4) / len(last4))


def colour(ratio):
    if ratio <= 1.10:
        return "GREEN - train as planned."
    if ratio <= 1.30:
        return "AMBER - hold at last week's V. No rung changes."
    return "RED - cut sets by one third. No new moves."


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("session", help="add up V for one session")
    s.add_argument("csv_file")

    k = sub.add_parser("spike", help="spike ratio for a planned week")
    k.add_argument("--last4", type=float, nargs="+", required=True)
    k.add_argument("--planned", type=float, required=True)

    a = ap.parse_args()

    if a.cmd == "session":
        total = 0.0
        sets_total = 0
        with open(a.csv_file, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                spr = (row.get("seconds_per_rep") or "").strip()
                v = line_volume(
                    float(row["L"]),
                    float(row["reps"]),
                    int(row["sets"]),
                    float(spr) if spr else None,
                )
                total += v
                sets_total += int(row["sets"])
                print(f"{row['move']:<36} V = {v:6.1f}")
        print("-" * 46)
        print(f"{'Session V':<36}     {total:6.1f}")
        print(f"Sets: {sets_total}")
    else:
        avg = sum(a.last4) / len(a.last4)
        ratio = spike_ratio(a.planned, a.last4)
        print(f"4-week average: {avg:.1f}")
        print(f"Highest safe week (1.10x): {1.10 * avg:.1f}")
        print(f"Spike ratio: {ratio:.2f}  ->  {colour(ratio)}")
        print(f"Deload week (60% of your highest recent week, {max(a.last4):.0f}): {0.6 * max(a.last4):.1f}")


if __name__ == "__main__":
    main()
