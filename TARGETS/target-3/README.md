# Target 3 - Confidential strings

## Artefactos
- `strings.txt` - output completo do `strings` (formato `offset:texto`).
- `annotated_assets.md` - lista anotada dos assets e porque são relevantes.

## Resposta (placa 22)
- **Password de manutenção (Alan):** `alanimyirtjaawjwdkbzonruikuhxbmvsgykfvtkrirofdikmzvocg`
- **Offset relativo à password de developer:** +25 bytes (Dan em 18224, Alan em 18249).

## Resposta (placa 38)
- **Password de manutenção (Alan):** `alanyangksdbajomxyrtbbtfkiicwyqybmbwigdyecluhrdbfymgdf`
- **Offset relativo à password de developer:** +25 bytes (Dan em 18222, Alan em 18247).

## Gerar
```
cd TARGETS\target-2
strings64 -a -o -nobanner -n 4 progmem.bin > ..\target-3\strings.txt
```
Depois inspecionar `strings.txt`: `Ctrl+F "Admin"` para as credenciais e offsets, `Ctrl+F "MII"` para a chave e a assinatura.
