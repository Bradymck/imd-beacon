#!/usr/bin/env python3
"""Exact committee-capture risk for SPEC.md section 5.1. Offline, standard library only.

Binomial (large population) by default; pass --pool M --adversarial A for the exact
hypergeometric case from a real registry snapshot.

Usage:
  python3 -I scripts/committee_risk.py                        # reproduce the spec table
  python3 -I scripts/committee_risk.py --pool 900 --adversarial 300 --n 256 --t 129
"""
import argparse
from fractions import Fraction
from math import comb


def binomial_tail(n, c, p):
    p = Fraction(p).limit_denominator(10**6)
    return sum(comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(c, n + 1))


def hypergeometric_tail(pool, adversarial, n, c):
    return Fraction(sum(comb(adversarial, k) * comb(pool - adversarial, n - k) for k in range(c, n + 1)), comb(pool, n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int)
    ap.add_argument("--t", type=int)
    ap.add_argument("--pool", type=int, help="eligible registered seats M")
    ap.add_argument("--adversarial", type=int, help="adversarial seats A")
    a = ap.parse_args()
    if a.pool is not None:
        n, t = a.n or 256, a.t or 129
        sign = hypergeometric_tail(a.pool, a.adversarial, n, t)
        block = hypergeometric_tail(a.pool, a.adversarial, n, n - t + 1)
        print(f"M={a.pool} A={a.adversarial} N={n} t={t}: sign {float(sign):.6g}  block {float(block):.6g}")
        return
    print(f"{'N/t':>8} {'p':>5} {'Pr[X>=t] sign':>16} {'Pr[X>=N-t+1] block':>20}")
    for n, t in [(64, 43), (64, 33), (128, 65), (256, 129)]:
        for p in (0.10, 0.20, 0.33, 0.40):
            print(f"{n:>4}/{t:<3} {p:>5.2f} {float(binomial_tail(n, t, p)):>16.6g} {float(binomial_tail(n, n - t + 1, p)):>20.6g}")


if __name__ == "__main__":
    main()
