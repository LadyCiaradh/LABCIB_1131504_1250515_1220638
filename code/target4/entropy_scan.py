"""
Entropy scan do firmware (Target 4).

Calcula a entropy de Shannon em janelas deslizantes sobre o PROGMEM e mostra
que a zona dos blobs base64 (chave + assinatura) se destaca do codigo.
O codigo tem entropy baixa; os dados criptograficos (mesmo em base64) sobem.

Le:      ../../TARGETS/target-2/progmem.bin
Escreve: ../../TARGETS/target-4/entropy.csv e entropy_scan.png

Uso: python entropy_scan.py
Requisitos: pip install matplotlib
"""
import os, csv, math
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "TARGETS", "target-2", "progmem.bin"))
OUT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "TARGETS", "target-4"))

WINDOW = 256
STEP = 64

KEY_OFF, KEY_LEN = 2954, 1592      # chave base64 (offsets do Target 3)
SIG_OFF, SIG_LEN = 4562, 344       # assinatura base64
CODE_OFF, CODE_LEN = 512, 1592     # regiao de codigo (opcodes AVR) para comparar


def entropy(block):
    if not block:
        return 0.0
    counts = [0] * 256
    for b in block:
        counts[b] += 1
    n = len(block)
    h = 0.0
    for c in counts:
        if c:
            p = c / n
            h -= p * math.log2(p)
    return h


def main():
    data = open(BIN, "rb").read()
    rows = []
    off = 0
    while off + WINDOW <= len(data):
        rows.append((off, entropy(data[off:off + WINDOW])))
        off += STEP
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "entropy.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["offset", "entropy_bits_per_byte"])
        for o, h in rows:
            w.writerow([o, f"{h:.4f}"])

    ek = entropy(data[KEY_OFF:KEY_OFF + KEY_LEN])
    es = entropy(data[SIG_OFF:SIG_OFF + SIG_LEN])
    ec = entropy(data[CODE_OFF:CODE_OFF + CODE_LEN])
    print(f"Entropy codigo (offset {CODE_OFF}):               {ec:.2f} bits/byte")
    print(f"Entropy chave em base64 (offset {KEY_OFF}):       {ek:.2f} bits/byte")
    print(f"Entropy assinatura em base64 (offset {SIG_OFF}):  {es:.2f} bits/byte")
    der_path = os.path.join(OUT, "key.der")
    if os.path.exists(der_path):
        der = open(der_path, "rb").read()
        print(f"Entropy chave DESCODIFICADA (DER, {len(der)} B):  {entropy(der):.2f} bits/byte")

    xs = [r[0] for r in rows]
    ys = [r[1] for r in rows]
    plt.figure(figsize=(10, 3))
    plt.plot(xs, ys, linewidth=0.8)
    plt.axvspan(KEY_OFF, KEY_OFF + KEY_LEN, color="orange", alpha=0.35, label="chave base64")
    plt.axvspan(SIG_OFF, SIG_OFF + SIG_LEN, color="red", alpha=0.35, label="assinatura base64")
    plt.xlabel("Offset no PROGMEM (bytes)")
    plt.ylabel("Entropy (bits/byte)")
    plt.title("Target 4 - Entropy do firmware (janela de 256 bytes)")
    plt.legend(loc="lower right", fontsize=8)
    plt.ylim(0, 8)
    plt.savefig(os.path.join(OUT, "entropy_scan.png"), dpi=150, bbox_inches="tight")
    print("->", os.path.join(OUT, "entropy_scan.png"))


if __name__ == "__main__":
    main()
