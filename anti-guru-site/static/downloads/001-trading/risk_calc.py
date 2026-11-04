#!/usr/bin/env python3
"""
risk_calc.py - the Appendix A cheat sheet as a tiny command-line tool.
The Anti-Guru Trading Manual (Field Manual #001).

Examples:
    python3 risk_calc.py size --account 1000 --risk 0.01 --stop-distance 2.50
    python3 risk_calc.py breakeven --rr 1.5 --cost-r 0.1
    python3 risk_calc.py drawdown --peak 1000 --now 800
    python3 risk_calc.py yearly-cost --trades 200 --cost 1.00 --account 1000

Standard library only. Made-up numbers in, plain numbers out.

Licence: CC BY-SA 4.0 - The Working-Class Trade Collective.
Not financial advice.
"""
import argparse


def position_size(account, risk_fraction, stop_distance):
    """S = (A x R) / D : dollars you will risk, divided by distance to your stop."""
    return (account * risk_fraction) / stop_distance


def breakeven_win_rate(reward_to_risk, cost_r=0.0):
    """W_BE = (1 + c) / (1 + R). With c = 0 this is 1 / (1 + R)."""
    return (1 + cost_r) / (1 + reward_to_risk)


def drawdown(peak, now):
    """D = (Peak - Now) / Peak."""
    return (peak - now) / peak


def gain_to_recover(dd):
    """D / (1 - D) : the gain you need to get back to even."""
    return dd / (1 - dd)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("size", help="position size")
    s.add_argument("--account", type=float, required=True)
    s.add_argument("--risk", type=float, default=0.01, help="fraction, 0.01 = 1%%")
    s.add_argument("--stop-distance", type=float, required=True, help="price distance from entry to stop")

    b = sub.add_parser("breakeven", help="break-even win rate")
    b.add_argument("--rr", type=float, required=True, help="reward-to-risk, e.g. 1.5")
    b.add_argument("--cost-r", type=float, default=0.0, help="all-in cost per trade in R")

    d = sub.add_parser("drawdown", help="drawdown and gain needed to get even")
    d.add_argument("--peak", type=float, required=True)
    d.add_argument("--now", type=float, required=True)

    y = sub.add_parser("yearly-cost", help="what the toll booth costs per year")
    y.add_argument("--trades", type=int, required=True)
    y.add_argument("--cost", type=float, required=True, help="all-in dollars per trade")
    y.add_argument("--account", type=float, required=True)

    a = ap.parse_args()

    if a.cmd == "size":
        print(f"Position size: {position_size(a.account, a.risk, a.stop_distance):.2f} units")
        print(f"Dollars at risk: {a.account * a.risk:.2f}")
    elif a.cmd == "breakeven":
        print(f"Break-even win rate: {breakeven_win_rate(a.rr, a.cost_r):.1%}")
    elif a.cmd == "drawdown":
        dd = drawdown(a.peak, a.now)
        print(f"Drawdown: {dd:.1%}")
        print(f"Gain needed to get even: {gain_to_recover(dd):.2%}")
    elif a.cmd == "yearly-cost":
        total = a.trades * a.cost
        print(f"Yearly cost: ${total:.2f} = {total / a.account:.1%} of the account")


if __name__ == "__main__":
    main()
