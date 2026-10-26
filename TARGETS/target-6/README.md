# Target 6 — OTP generator

## Artefactos
- `otp_capture.txt` — captura serial das OTPs esperadas até repetir, com os parâmetros do LCG recuperados e a próxima OTP prevista.
- Script: `code/target-6/otp_crack.py`.

## Resposta (placa 22, este boot)
- **Tentativas até repetir (período):** 1024.
- **Valor que repetiu:** 2779 (o 1.º valor, volta na tentativa 1025).
- **Próxima OTP prevista:** 2779 (o ciclo fecha).
- **Gerador recuperado:** X(n+1) = 3693 · X(n) mod 4096 (a=3693, c=0, m=4096), multiplicativo.

## Como se obteve
Entrar como Admin Alan leva ao fluxo do C&C. Dando a password do C&C e uma OTP errada, a placa revela a esperada ("Incorrect OTP, got X, was expecting N"). Capturando a sequência até repetir, recupera-se o LCG a partir dos dados.

Nota: um boot tem OTPs de paridade única, o que deixa 4 pares (a,c) possíveis para m=4096. Cruzando com um boot de paridade oposta, só (a=3693, c=0) serve para ambos: é o gerador verdadeiro (multiplicativo). O período depende da seed (ímpar → 1024, par → ≤512).
