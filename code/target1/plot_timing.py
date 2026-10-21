"""
Gera os graficos do timing attack a partir dos CSV brutos (Target 1).
Reproduz as figuras exigidas pelo enunciado (1a e 2a letra) a partir dos dados.

Uso:
    python plot_timing.py length     -> grafico tempo medio vs comprimento
    python plot_timing.py chars      -> grafico por caracter (posicoes 0 e 1)

Requisitos: pip install matplotlib
"""

import sys
import csv
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt

LEN_CSV = "length_timing.csv"
POS_CSV = "char_timing.csv"


def plot_length():
    data = defaultdict(list)
    with open(LEN_CSV) as f:
        for r in csv.DictReader(f):
            data[int(r["length"])].append(int(r["elapsed_ns"]))
    xs = sorted(data)
    ys = [statistics.mean(data[x]) / 1e6 for x in xs]
    plt.figure()
    plt.bar(xs, ys)
    plt.xlabel("Comprimento testado")
    plt.ylabel("Tempo medio de resposta (ms)")
    plt.title("Target 1 - inferencia do comprimento")
    plt.savefig("length_timing.png", dpi=150, bbox_inches="tight")
    print("length_timing.png")


def plot_char(position):
    data = defaultdict(list)
    with open(POS_CSV) as f:
        for r in csv.DictReader(f):
            if int(r["position"]) == position:
                data[r["candidate_char"]].append(int(r["elapsed_ns"]))
    chars = sorted(data)
    ys = [min(data[c]) / 1e6 for c in chars]   # minimo: coerente com a decisao do ataque
    plt.figure(figsize=(9, 3))
    plt.bar(chars, ys)
    plt.xlabel("Caracter candidato")
    plt.ylabel("Tempo minimo (ms)")
    plt.title(f"Target 1 - posicao {position + 1}")
    plt.savefig(f"char_timing_pos{position + 1}.png", dpi=150, bbox_inches="tight")
    print(f"char_timing_pos{position + 1}.png")


def plot_scan():
    from collections import defaultdict
    data = defaultdict(lambda: defaultdict(list))
    with open("scan_pos0.csv") as f:
        for r in csv.DictReader(f):
            data[int(r["length"])][r["candidate_char"]].append(int(r["elapsed_ns"]))
    lengths = sorted(data)
    gaps = []
    for L in lengths:
        mins = sorted((min(v) for v in data[L].values()), reverse=True)
        gaps.append((mins[0] - mins[1]) / 1e6)
    plt.figure()
    plt.bar(lengths, gaps)
    plt.xlabel("Comprimento testado")
    plt.ylabel("Separacao do melhor caracter (ms)")
    plt.title("Target 1 - varredura comprimento x 1o caracter")
    plt.savefig("scan_gap.png", dpi=150, bbox_inches="tight")
    print("scan_gap.png")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("length", "chars", "scan"):
        print(__doc__)
        return
    if sys.argv[1] == "length":
        plot_length()
    elif sys.argv[1] == "scan":
        plot_scan()
    else:
        plot_char(0)   # 1a letra
        plot_char(1)   # 2a letra


if __name__ == "__main__":
    main()
