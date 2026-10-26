"""
Target 6 - crack do gerador de OTP.

Entra como Admin Alan, da a password do C&C e vai metendo OTPs invalidas.
A placa responde "Incorrect OTP, got X, was expecting N", ou seja revela a OTP
esperada em cada tentativa. Capturamos essa sequencia ate repetir (o periodo),
recuperamos o LCG a partir dos dados e prevemos a proxima OTP.

Uso: python otp_crack.py
Requisitos: pyserial. Ajustar PORT/BAUD em ../target-1/serial_target.py.
"""
import sys, os, re, math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "target-1"))
from serial_target import SerialTarget

ALAN = "alanimyirtjaawjwdkbzonruikuhxbmvsgykfvtkrirofdikmzvocg"   # admin -> fluxo C&C
CNC  = "cncazezuxmihjpgrddzjnemmyzajtwcyqufqqrqcrsoqhsdtnnwwa"    # password do C&C (Target 5)
DUMMY = "99999"   # fora do alcance 0-4095: nunca acerta, nunca liga
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                    "TARGETS", "target-6", "otp_capture.txt")


def crack_lcg(seq):
    """Recupera (a, c, m) de X(n+1)=(a*X(n)+c) mod m a partir da sequencia.

    Truque: para t = diferencas consecutivas, m divide sempre
    (t[i+1]*t[i-1] - t[i]^2). O gcd desses valores da um multiplo de m;
    dividimos por 2 ate dar o m certo. Depois testamos todos os 'a' (o 'c'
    fica determinado por c=(X1-a*X0) mod m). Um boot (paridade unica) admite
    varias solucoes; devolvemos a de menor c. Cruzar com um boot de paridade
    oposta confirma que a verdadeira e a=3693, c=0 (multiplicativo)."""
    t = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
    m = 0
    for i in range(1, len(t)-1):
        m = math.gcd(m, abs(t[i+1]*t[i-1] - t[i]*t[i]))
    while m >= 2:
        sols = []
        for a in range(m):
            c = (seq[1] - a*seq[0]) % m
            if (a*seq[1] + c) % m == seq[2] and all((a*seq[i]+c) % m == seq[i+1]
                                                    for i in range(len(seq)-1)):
                sols.append((a, c))
        if sols:
            sols.sort(key=lambda ac: ac[1])   # menor c = forma canonica
            return sols[0][0], sols[0][1], m
        m //= 2
    return None


def main():
    t = SerialTarget().open()
    seq, seen, lines = [], {}, []
    repeated = None
    try:
        t.read_until(["vending machine number"], timeout=8, idle=3)
        t.send_line(ALAN)
        t.read_until(["connecting to the c&c"], timeout=15, idle=4)
        t.read_until(["password:"], timeout=8, idle=3)
        t.send_line(CNC)
        t.read_until(["otp:"], timeout=8, idle=3)
        while True:
            t.send_line(DUMMY)
            chunk = t.read_until(["otp:"], timeout=6, idle=2)
            mo = re.search(r"was expecting (\d+)", chunk)
            if not mo:
                break
            y = int(mo.group(1))
            lines.append("tentativa %4d: was expecting %d" % (len(seq)+1, y))
            if y in seen:
                repeated = y
                break
            seen[y] = len(seq)
            seq.append(y)
            if len(seq) % 50 == 0:
                print("...capturadas %d OTPs" % len(seq))
    finally:
        t.close()

    period = len(seq) - seen[repeated] if repeated is not None else None
    res = crack_lcg(seq)

    with open(OUT, "w") as f:
        f.write("Target 6 - captura do gerador de OTP (boot atual)\n")
        f.write("=" * 50 + "\n\n")
        f.write("Captura das OTPs esperadas (OTP enviada = %s, sempre errada):\n\n" % DUMMY)
        f.write("\n".join(lines) + "\n\n")
        if repeated is not None:
            f.write("Primeiro valor a repetir: %d\n" % repeated)
            f.write("Tentativas ate repetir (periodo): %d\n\n" % period)
        if res:
            a, c, m = res
            nxt = (a*seq[-1] + c) % m
            f.write("Gerador recuperado (LCG):\n")
            f.write("  X(n+1) = (%d * X(n) + %d) mod %d\n" % (a, c, m))
            f.write("  a=%d  c=%d  m=%d\n\n" % (a, c, m))
            f.write("Ultima OTP capturada: %d\n" % seq[-1])
            f.write("Proxima OTP prevista: %d\n" % nxt)

    print("\nFeito. %d OTPs capturadas, periodo %s." % (len(seq), period))
    if res:
        print("LCG: a=%d c=%d m=%d | proxima OTP apos %d = %d"
              % (res[0], res[1], res[2], seq[-1], (res[0]*seq[-1]+res[1]) % res[2]))
    print("Gravado em %s" % OUT)


if __name__ == "__main__":
    main()
