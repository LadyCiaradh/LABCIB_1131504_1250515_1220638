# Target 2 — Dumped firmware

## Artefactos
- `progmem.bin` — dump cru do PROGMEM (32768 bytes).
- `SHA256SUMS.txt` — SHA-256 do dump.
- Script de captura: `code/target2/dump_capture.py`.

## Resposta (placa 22)
- **SHA-256 (PROGMEM):** `1c1405bab48356252c6671edc00d7d7f8e31981af30438fd0d0e60e8f31b1af2`
- **Tamanho:** 32768 bytes.
- **Offset da password de developer:** 18224 (tabela de credenciais do login).

## Verificar
`certutil -hashfile progmem.bin SHA256` (Windows) deve dar o mesmo SHA-256. Um segundo dump independente dá o mesmo hash, o que confirma uma captura completa.
