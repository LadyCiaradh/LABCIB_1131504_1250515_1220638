# Divulgação de utilização de IA

- Team (student IDs): Diogo Gomes (1131504), Gabriel Costa (1250515), Joana Soares (1220638)
- Assigned Arduino ID: 22 & 38

## Ferramentas utilizadas

- Cursor (Grok): scaffold inicial de `TARGETS/` e do README de submissão.
- Claude (Anthropic): apoio no desenvolvimento e depuração do código e na
  estruturação do relatório, ao longo dos Targets 1 a 7.

## Para que foi usada cada ferramenta

- Compreender a estrutura do trabalho e os entregáveis exigidos.
- Target 1: ajuda a escrever e afinar os scripts em `code/target-1/` (camada série,
  motor do timing attack, medição por mínimo, medição até ao primeiro byte,
  varredura comprimento+caracter) e a interpretar os tempos obtidos.
- Target 2: ajuda a escrever e depurar `code/target-2/dump_capture.py` (captura em
  bruto do PROGMEM e cálculo do SHA-256).
- Target 3: orientação sobre o método de inspeção de strings com a ferramenta
  `strings` e redação da secção correspondente do relatório.
- Target 4: ajuda na extração dos blobs base64, nos comandos `openssl`
  (asn1parse, rsa -text) e no script de entropy (`code/target-4/entropy_scan.py`).
- Target 5: apoio na decriptação da assinatura com `openssl pkeyutl` e no lookup
  do MD5 na rainbow table.
- Target 6: apoio no desenvolvimento do script `code/target-6/otp_crack.py`
  (captura das OTPs e recuperação dos parâmetros do LCG).
- Target 7: apoio na combinação da password do C&C com a OTP prevista para
  estabelecer a ligação ao C&C.
- Redação e organização do relatório (metodologia, resultados, análise).

## Targets / secções envolvidas

- Scaffolding de submissão (README, `TARGETS/`).
- Targets 1 a 7 (código, comandos, evidências e redação).

## Confirmação

Confirmamos que os artefactos sob `TARGETS/` foram produzidos pela nossa equipa,
nas placas Arduino atribuídas (ID 22 e ID 38). As medições de tempo, os dados
brutos, o dump do firmware, as strings e o material criptográfico foram obtidos
nas nossas placas. Compreendemos que o uso de IA não declarado ou deturpado é uma
violação de integridade académica.
