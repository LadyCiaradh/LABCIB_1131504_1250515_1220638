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

Pré-requisitos: Python 3, `pip install pyserial matplotlib`. Sysinternals `strings` (Target 3) e OpenSSL (Target 4). Ajustar `PORT`/`BAUD` em `code/target-1/serial_target.py`.

### Target 1 — Developer password (timing attack)
```
cd code/target-1
python timing_attack.py scan           # infere comprimento + 1.o caracter
python timing_attack.py recover 13     # recupera a password (N = comprimento)
python timing_attack.py finish dansudeulzbl   # ultimo caracter pela resposta
python plot_timing.py chars            # graficos da 1.a e 2.a letra
python plot_timing.py scan             # grafico da varredura
```

### Target 2 — Firmware dump
```
cd code\target-2
python dump_capture.py 0                           # escreve TARGETS\target-2\progmem.bin + imprime SHA-256
certutil -hashfile ..\..\TARGETS\target-2\progmem.bin SHA256   # verificacao do hash (Windows)
```

### Target 3 — Strings (inspeção manual)
```
cd TARGETS\target-2
strings64 -a -o -nobanner -n 4 progmem.bin > ..\target-3\strings.txt
```
Depois inspecionar `TARGETS/target-3/strings.txt` no editor: `Ctrl+F "Admin"` para a tabela de credenciais e os offsets, `Ctrl+F "MII"` para a chave e a assinatura.

### Target 4 — Dados criptográficos
```
cd TARGETS\target-4
openssl base64 -d -A -in key.b64 -out key.der      # descodifica a chave (base64 -> DER)
openssl base64 -d -A -in sig.b64 -out sig.bin      # descodifica a assinatura
openssl asn1parse -inform DER -in key.der > asn1parse_key.txt
openssl rsa -inform DER -in key.der -text -noout > rsa_text.txt
python ..\..\code\target-4\entropy_scan.py        # entropy.csv + entropy_scan.png
```
Os blobs `key.b64` e `sig.b64` são o base64 copiado das strings do firmware (offsets 2954 e 4562).

### Target 5 — c&c password
```
cd TARGETS\target-5
openssl pkeyutl -decrypt -inkey ..\target-4\key.der -keyform DER -in ..\target-4\sig.bin -out hash.json
type hash.json
findstr "<MD5_do_hash.json>" ..\..\..\Rainbowtablee.txt > rainbow_lookup.txt
```
A "assinatura" (sig.bin) é na verdade um bloco encriptado com a chave pública; abre-se com a privada (do T4). O JSON tem um MD5; procura-se esse MD5 na coluna de hashes da rainbow table para obter a password.

### Target 6 — OTP generator
```
cd code\target-6
python otp_crack.py        # captura ate repetir + recupera o LCG -> TARGETS\target-6\otp_capture.txt
```
Entrar como Admin Alan leva ao fluxo do C&C. Dando a password do C&C e OTPs invalidas, cada erro revela a OTP esperada ("was expecting N"). Captura-se a sequencia ate repetir e recupera-se o gerador (LCG) a partir dos dados.

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
- **Offset da password do developer:** 18224 (tabela de credenciais do login). A password surge tambem no offset 700, no dialogo embebido, mas a resposta e 18224, por ser onde a credencial e guardada e usada no login.

### Target 3 — Strings
- **2.a password de manutencao (Alan):** `alanimyirtjaawjwdkbzonruikuhxbmvsgykfvtkrirofdikmzvocg`
- **Offset relativo a do developer:** +25 bytes (Dan em 18224, Alan em 18249).
- **Comprimento dos blobs base64:** chave 1592 caracteres; assinatura 344 caracteres (= 256 bytes).


### Target 4 — Dados criptográficos
- **Tamanho da chave:** 2048 bits (RSA privada, 2 primos), guardada em claro no firmware.
- **Bytes ASN.1/DER que a identificam:** SEQUENCE (30 82...); version INTEGER 00; modulus INTEGER de 257 bytes (256 + 1 de sinal = 2048 bits); expoente publico 010001 (65537). Prefixo base64 `MII` = 30 82 (magic DER).
- **Tamanho da assinatura:** 256 bytes (sig.bin) = um bloco RSA-2048.
- **Entropy (chave vs codigo):** codigo ~4.63; chave em base64 ~5.98; assinatura em base64 ~5.89; chave descodificada ~7.81 bits/byte (quase aleatoria).

### Target 5 — c&c password
- **MD5 recuperado da assinatura:** `e07fcd7e6951d04659c4a8debe8e63de`
- **Password do c&c:** `cncazezuxmihjpgrddzjnemmyzajtwcyqufqqrqcrsoqhsdtnnwwa`
- **Porque chega uma rainbow table curta:** as passwords do c&c sao de um conjunto pequeno e conhecido (prefixo `cnc`, comprimento fixo) e o MD5 nao tem salt, logo basta pre-calcular as candidatas em vez de todo o espaco de strings.

### Target 6 — OTP generator
- **Periodo (este boot):** 1024 tentativas (depende da seed: impar -> 1024, par -> ate 512).
- **Valor que repetiu:** 2779.
- **Proxima OTP:** 2779.
- **Gerador recuperado:** X(n+1) = 3693 * X(n) mod 4096 (a=3693, c=0, m=4096), multiplicativo.

### Target 7
Por realizar.

## secrets.csv

Uma linha, sem cabecalho, campos por esta ordem:
`Arduino ID, password Dan, password Alan, password c&c, secret final, MD5 da c&c, SHA-256 PROGMEM`.
