# Target 7 - Final secret

## Artefactos
- `cc_connection.txt` - transcript da ligação ao C&C bem-sucedida (OTP aceite + linha do secret).

## Resposta (placa 22)
- **Secret final:** `calmvacationquiltmonkey`
- **Como os targets 5 e 6 se combinaram:** a ligação ao C&C exige duas coisas ao mesmo tempo, a password do C&C (recuperada no Target 5) e uma OTP válida. O Target 6 quebrou o gerador de OTP (LCG), o que permite prever a OTP esperada. Juntando as duas (password do T5 + OTP prevista do T6) a ligação é aceite e a placa devolve o secret.

## Como se obteve
Login como Admin Alan (Target 3) → fluxo do C&C → password do C&C (Target 5). No `OTP:`, enviou-se um dummy (0); a placa revelou a esperada (2826). O próximo OTP calcula-se com o gerador do Target 6: (3693 × 2826) mod 4096 = 3906. Enviou-se 3906 → aceite → secret.
