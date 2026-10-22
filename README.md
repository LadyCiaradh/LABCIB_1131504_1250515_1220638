# Embedded Lab — Submission

- **Team:** 1131504, 1250515, 1220638
- **Arduino identification number:** 22 (das placas atribuídas, 38 e 22)
- **ZIP name (on delivery):** `1131504_1250515_1220638.zip`

Enunciado: [Part I](embedded-lab-part-01.md) · [Part II](embedded-lab-part-02.md)
Relatório detalhado (com figuras e evidências): `Relatorio_Embedded_Lab_1131504_1250515_1220638.docx`

## Estrutura

- `code/` — scripts usados (ferramentas), por target.
- `TARGETS/` — evidências por target (`target-<n>/`), `secrets.csv` e `AI-DISCLOSURE.md`.

## Como correr o código

Pré-requisitos: Python 3, `pip install pyserial matplotlib`. Sysinternals `strings` (para o Target 3). Ajustar `PORT`/`BAUD` em `code/target1/serial_target.py`.

### Target 1 — Developer password (timing attack)
```
cd code/target1
python timing_attack.py scan           # infere comprimento + 1.o caracter
python timing_attack.py recover 13     # recupera a password (N = comprimento)
python timing_attack.py finish dansudeulzbl   # ultimo caracter pela resposta
python plot_timing.py chars            # graficos da 1.a e 2.a letra
python plot_timing.py scan             # grafico da varredura
```

### Target 2 — Firmware dump
```
cd code/target2
python dump_capture.py 0               # PROGMEM -> progmem.bin + SHA-256
certutil -hashfile progmem.bin SHA256  # verificacao do hash (Windows)
```

### Target 3 — Strings (inspeção manual)
```
cd TARGETS\target-2
strings64 -a -o -nobanner -n 4 progmem.bin > ..\target-3\strings.txt
```
Depois inspecionar `TARGETS/target-3/strings.txt` no editor: `Ctrl+F "Admin"` para a tabela de credenciais e os offsets, `Ctrl+F "MII"` para a chave e a assinatura.

## Respostas (placa 22)

### Target 1 — Developer password
- **Metodo:** timing attack a consola serie. A validacao para no 1.o caracter errado, logo quanto mais caracteres certos, mais tempo demora. Inferimos primeiro o comprimento (varredura comprimento x 1.o caracter) e depois caracter a caracter, escolhendo o de maior tempo (minimo de 60 amostras).
- **Password (Dan):** `dansudeulzblj`
- **Comprimento:** 13
- **Margem por posicao:** ~1 ms (um atraso por caracter correto); posicao 0 ~2 ms (o filler 'a' coincide com o 2.o caracter).
- **Menor margem:** posicao 10 (0,943 ms), dentro do ruido por ser um unico atraso como as restantes.

### Target 2 — Firmware
- **SHA-256 (PROGMEM):** `1c1405bab48356252c6671edc00d7d7f8e31981af30438fd0d0e60e8f31b1af2`
- **Tamanho:** 32768 bytes
- **Offset da password do developer:** 700 (dialogo embebido) e 18224 (tabela de credenciais do login).

### Target 3 — Strings
- **2.a password de manutencao (Alan):** `alanimyirtjaawjwdkbzonruikuhxbmvsgykfvtkrirofdikmzvocg`
- **Offset relativo a do developer:** +25 bytes (Dan em 18224, Alan em 18249).
- **Comprimento dos blobs base64:** chave 1592 caracteres; assinatura 344 caracteres (= 256 bytes).


### Targets 4–7
Por realizar.

## secrets.csv

Uma linha, sem cabecalho, campos por esta ordem:
`Arduino ID, password Dan, password Alan, password c&c, secret final, MD5 da c&c, SHA-256 PROGMEM`.
