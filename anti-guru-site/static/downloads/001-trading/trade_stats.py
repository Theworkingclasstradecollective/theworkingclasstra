#!/usr/bin/env python3
"""
trade_stats.py - the "After 50 trades, work out:" table from Appendix E,
The Anti-Guru Trading Manual (Field Manual #001).

Usage:
    python3 trade_stats.py trade-log-50.csv

Reads a CSV with the columns: trade_no, date, direction, planned_r,
realized_r, rules_followed (Y/N), running_total_r. Empty rows are ignored.
Standard library only. No network. No tracking.

Licence: CC BY-SA 4.0 - The Working-Class Trade Collective.
Not financial advice. Test everything in demo mode for 100 trades first.
"""
import csv
import sys


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not (row.get("realized_r") or "").strip():
                continue  # blank line in the log
            rows.append(
                {
                    "r": float(row["realized_r"]),
                    "ok": (row.get("rules_followed") or "").strip().upper() == "Y",
                }
            )
    return rows


def expectancy(results):
    """(win rate x avg win) - (loss rate x avg loss), all in R."""
    n = len(results)
    if n == 0:
        return 0.0
    wins = [r for r in results if r > 0]
    losses = [-r for r in results if r < 0]
    win_rate = len(wins) / n
    loss_rate = len(losses) / n
    avg_win = sum(wins) / len(wins) if wins else 0.0
    avg_loss = sum(losses) / len(losses) if losses else 0.0
    return win_rate * avg_win - loss_rate * avg_loss


def worst_streak(results):
    worst = run = 0
    for r in results:
        run = run + 1 if r < 0 else 0
        worst = max(worst, run)
    return worst


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    trades = load(sys.argv[1])
    if not trades:
        sys.exit("No completed trades found in the log yet. Keep logging.")

    results = [t["r"] for t in trades]
    n = len(results)
    wins = [r for r in results if r > 0]
    losses = [-r for r in results if r < 0]

    print(f"Trades logged ........ {n}")
    if n < 100:
        print(f"  (the book says 100 before you judge anything; you have {n})")
    print(f"Win rate ............. {len(wins) / n:.1%}")
    print(f"Average win (R) ...... {sum(wins) / len(wins):.2f}" if wins else "Average win (R) ...... n/a")
    print(f"Average loss (R) ..... {sum(losses) / len(losses):.2f}" if losses else "Average loss (R) ..... n/a")
    print(f"Expectancy (R) ....... {expectancy(results):+.3f}")
    print(f"Worst losing streak .. {worst_streak(results)}")
    print(f"Compliance ........... {sum(t['ok'] for t in trades) / n:.1%}")
    print(f"Running total (R) .... {sum(results):+.2f}")

    # Remove the biggest win and redo it. Luck hides in one trade.
    if wins:
        trimmed = results.copy()
        trimmed.remove(max(results))
        print(f"Expectancy without your best trade (R) .. {expectancy(trimmed):+.3f}")


if __name__ == "__main__":
    main()
