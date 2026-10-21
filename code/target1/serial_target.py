"""
Camada de comunicacao serie com o alvo (Target 1).
Isola a I/O serie para que a logica do ataque nao dependa do protocolo.
Reutilizavel nos Targets 6 e 7.

Mede o tempo ate ao PRIMEIRO byte da resposta (latencia da validacao) e
limpa o resto da resposta sem o cronometrar, para cada tentativa ser rapida.

Requisitos: pip install pyserial
"""

import time
import serial  # pyserial


# ===================== CONFIG (ajustada a placa 22) =====================
PORT = "COM3"          # placa 22 (Arduino Nano)
BAUD = 115200          # confirmado no Serial Monitor
READ_TIMEOUT = 0.8     # segundos max a aguardar a resposta

# A consola usa "New Line", logo a password termina com \n.
SEND_TEMPLATE = "{pw}\n"

# Marca que indica que o ciclo terminou e a placa voltou a pedir password.
# Serve para limpar o buffer entre tentativas (fora da zona cronometrada).
PROMPT_MARKER = b"enter password"
# ========================================================================


class SerialTarget:
    def __init__(self, port=PORT, baud=BAUD, read_timeout=READ_TIMEOUT):
        self.port = port
        self.baud = baud
        self.read_timeout = read_timeout
        self.ser = None

    def open(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=0.02)
        time.sleep(2.0)          # o Nano reinicia ao abrir a porta
        self._flush()
        return self

    def close(self):
        if self.ser:
            self.ser.close()

    def _flush(self):
        n = self.ser.in_waiting
        if n:
            self.ser.read(n)

    def _drain_until(self, marker, timeout=0.5):
        """Le e descarta ate ver 'marker' (ou esgotar timeout). Nao cronometrado."""
        buf = b""
        t_end = time.perf_counter() + timeout
        while time.perf_counter() < t_end:
            c = self.ser.read(64)
            if c:
                buf += c
                if marker in buf.lower():
                    break
        return buf

    def time_attempt(self, password):
        """Envia uma password e mede o tempo ate ao PRIMEIRO byte de resposta.
        Devolve (elapsed_ns, primeiro_byte). O resto da resposta e o novo
        prompt sao drenados sem contar para o tempo."""
        self._flush()
        payload = SEND_TEMPLATE.format(pw=password).encode()
        t0 = time.perf_counter_ns()
        self.ser.write(payload)
        self.ser.flush()
        first = b""
        t_end = time.perf_counter() + self.read_timeout
        while time.perf_counter() < t_end:
            b = self.ser.read(1)
            if b:
                first = b
                break
        t1 = time.perf_counter_ns()
        # limpa o resto (Login failure + novo prompt) para a proxima tentativa
        self._drain_until(PROMPT_MARKER)
        return (t1 - t0), first

    def submit(self, password):
        """Envia uma password e devolve a resposta completa (texto).
        Util para distinguir sucesso de "Login failure" sem cronometrar."""
        self._flush()
        self.ser.write(SEND_TEMPLATE.format(pw=password).encode())
        self.ser.flush()
        buf = b""
        t_end = time.perf_counter() + 0.6
        while time.perf_counter() < t_end:
            c = self.ser.read(128)
            if c:
                buf += c
                t_end = time.perf_counter() + 0.25   # estende enquanto houver dados
        return buf.decode(errors="replace")



if __name__ == "__main__":
    t = SerialTarget().open()
    try:
        for _ in range(5):
            dt, first = t.time_attempt("zzzzz")
            print(f"1o byte em {dt/1e6:7.3f} ms  (byte={first})")
    finally:
        t.close()
