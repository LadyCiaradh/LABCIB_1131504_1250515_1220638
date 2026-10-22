# Target 3 — Confidential strings

## Artefactos
- `strings.txt` — output completo do `strings` (formato `offset:texto`).
- `annotated_assets.md` — lista anotada dos assets e porque são relevantes.

## Resposta (placa 22)
- **2.a password de manutenção (Alan):** `alanimyirtjaawjwdkbzonruikuhxbmvsgykfvtkrirofdikmzvocg`
- **Offset relativo à password de developer:** +25 bytes (Dan em 18224, Alan em 18249).
- **Comprimento dos blobs base64:** chave 1592 caracteres; assinatura 344 (= 256 bytes).

## Gerar
```
cd TARGETS\target-2
strings64 -a -o -nobanner -n 4 progmem.bin > ..\target-3\strings.txt
```
Depois inspecionar `strings.txt`: `Ctrl+F "Admin"` para as credenciais e offsets, `Ctrl+F "MII"` para a chave e a assinatura.
