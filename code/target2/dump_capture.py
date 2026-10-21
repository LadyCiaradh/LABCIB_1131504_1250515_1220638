"""
Captura RAW (binaria) do dump de memoria pela consola de developer (Target 2).

O dump sai em bytes crus pela serie (nao em hex), por isso lemos bytes e
gravamos um .bin sem descodificar. Capturamos exatamente o tamanho da regiao
e enviamos Enter para parar.

Reutiliza a camada serie do Target 1.

Uso:
    python dump_capture.py 0   -> PROGMEM (firmware)  [default]
    python dump_capture.py 1   -> EEPROM
    python dump_capture.py 2   -> SRAM

Saidas: <regiao>.bin (dados), <regiao>_raw.bin (captura completa), e imprime
o tamanho e o SHA-256.
"""

import sys, os, time, hashlib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "target1"))
from serial_target import SerialTarget

PASSWORD = "dansudeulzblj"
REGIONS = {"0": ("PROGMEM", 32768), "1": ("EEPROM", 1024), "2": ("SRAM", 36864)}
HEADER = b"Press Enter to stop"


def main():
    region = sys.argv[1] if len(sys.argv) > 1 else "0"
    if region not in REGIONS:
        print("Regiao invalida (0/1/2)."); return
    name, size = REGIONS[region]

    t = SerialTarget().open()   # abrir a porta reinicia o Nano
    try:
        # login
        t.read_until(["enter password"], timeout=5, idle=2.0)
        t.send_line(PASSWORD)
        t.read_until(["development menu"], timeout=12, idle=3.0)
        # [1] Dump -> escolher regiao
        t.send_line("1")
        t.read_until(["memory location to print"], timeout=5, idle=2.0)
        print(f"A capturar {name} ({size} bytes)...")
        t.send_line(region)

        # ler bytes crus ate ter o cabecalho + 'size' bytes de dados
        raw = b""
        t_end = time.perf_counter() + 180
        while time.perf_counter() < t_end:
            c = t.ser.read(2048)
            if c:
                raw += c
                h = raw.find(HEADER)
                if h != -1:
                    nl = raw.find(b"\n", h)
                    if nl != -1 and (len(raw) - (nl + 1)) >= size:
                        break
        t.send_line("")   # Enter para parar o dump

        h = raw.find(HEADER); nl = raw.find(b"\n", h)
        data = raw[nl + 1: nl + 1 + size]
        with open(f"{name.lower()}.bin", "wb") as f:
            f.write(data)
        with open(f"{name.lower()}_raw.bin", "wb") as f:
            f.write(raw)
        print(f"{name.lower()}.bin  bytes={len(data)}  (esperado {size})")
        print(f"SHA-256: {hashlib.sha256(data).hexdigest()}")
    finally:
        t.close()


if __name__ == "__main__":
    main()
