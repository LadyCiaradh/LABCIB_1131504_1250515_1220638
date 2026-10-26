# Embedded Lab - Entrega

- **Team:** 1131504 Diogo Gomes, 1250515 Gabriel Costa, 1220638 Joana Soares
- **Arduino identification number:** 22 e 38
- **ZIP name (on delivery):** `1131504_1250515_1220638.zip`

Enunciado: [Parte I](embedded-lab-part-01.md) · [Parte II](embedded-lab-part-02.md)
Relatório detalhado (com figuras e evidências): `Relatório_Embedded_Lab_1131504_1250515_1220638.pdf`

## Estrutura

- `code/` - scripts usados (ferramentas), por target.
- `TARGETS/` - evidências por target (`target-<n>/`), `secrets.csv` e `AI-DISCLOSURE.md`.

## Como correr o código

Pré-requisitos: Python 3, `pip install pyserial matplotlib`. Sysinternals `strings` (Target 3) e OpenSSL (Target 4). Ajustar `PORT`/`BAUD` em `code/target-1/serial_target.py`.

### Target 1 - Developer password (timing attack)
```
cd code/target-1
python timing_attack.py scan           # infere comprimento + 1.o caracter
python timing_attack.py recover 13     # recupera a password (N = comprimento)
python timing_attack.py finish dansudeulzbl   # ultimo caracter pela resposta
python plot_timing.py chars            # graficos da 1.a e 2.a letra
python plot_timing.py scan             # grafico da varredura
```

### Target 2 - Firmware dump
```
cd code\target-2
python dump_capture.py 0                           # escreve TARGETS\target-2\progmem.bin + imprime SHA-256
certutil -hashfile ..\..\TARGETS\target-2\progmem.bin SHA256   # verificacao do hash (Windows)
```

### Target 3 - Strings (inspeção manual)
```
cd TARGETS\target-2
strings64 -a -o -nobanner -n 4 progmem.bin > ..\target-3\strings-22.txt
```
Depois inspecionar `TARGETS/target-3/strings-22.txt` no editor: `Ctrl+F "Admin"` para a tabela de credenciais e os offsets, `Ctrl+F "MII"` para a chave e a assinatura.

### Target 4 - Dados criptográficos
```
cd TARGETS\target-4
openssl base64 -d -A -in key.b64 -out key.der      # descodifica a chave (base64 -> DER)
openssl base64 -d -A -in sig.b64 -out sig.bin      # descodifica a assinatura
openssl asn1parse -inform DER -in key.der > asn1parse_key.txt
openssl rsa -inform DER -in key.der -text -noout > rsa_text.txt
python ..\..\code\target-4\entropy_scan.py        # entropy.csv + entropy_scan.png
```
Os blobs key.b64 e sig.b64 são o base64 copiado das strings do firmware (linhas em 2954 e 4562; os blobs começam em 2968 e 4595, depois do prefixo do diálogo).

### Target 5 - c&c password
```
cd TARGETS\target-5
openssl pkeyutl -decrypt -inkey ..\target-4\key.der -keyform DER -in ..\target-4\sig.bin -out hash.json
type hash.json
findstr "<MD5_do_hash.json>" ..\..\..\Rainbowtablee.txt > rainbow_lookup.txt
```
A "assinatura" (sig.bin) é na verdade um bloco encriptado com a chave pública; abre-se com a privada (do T4). O JSON tem um MD5; procura-se esse MD5 na coluna de hashes da rainbow table para obter a password.

### Target 6 - OTP generator
```
cd code\target-6
python otp_crack.py        # captura ate repetir + recupera o LCG -> TARGETS\target-6\otp_capture.txt
```
Entrar como Admin Alan leva ao fluxo do C&C. Dando a password do C&C e OTPs invalidas, cada erro revela a OTP esperada ("was expecting N"). Captura-se a sequencia ate repetir e recupera-se o gerador (LCG) a partir dos dados.

### Target 7 - OTP generator

A ligação ao C&C exige duas coisas ao mesmo tempo, a password do C&C (recuperada no Target 5) e uma OTP válida. O Target 6 quebrou o gerador de OTP, por isso conseguimos prever a OTP esperada.
