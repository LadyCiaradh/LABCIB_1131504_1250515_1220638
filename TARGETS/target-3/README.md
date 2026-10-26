# Target 3 - Confidential strings

## Artefactos
- `strings.txt` - output completo do `strings` (formato `offset:texto`).
- `annotated_assets.md` - lista anotada dos assets e porque são relevantes.

## Resposta (placa 22)
Fonte: `progmem.bin` (dump PROGMEM do Target 2, 32768 bytes). Offsets em decimal.
Output completo em `strings.txt`.

### Credenciais (tabela em ~18210–18329)
- 18210 `Developer Dan` - rótulo.
- 18224 `dansudeulzblj` - password do developer (Dan), 13 caracteres. Aparece também em 700 (no diálogo embebido).
- 18238 `Admin Alan` - rótulo.
- 18249 `alanimyirtjaawjwdkbzonruikuhxbmvsgykfvtkrirofdikmzvocg` - Password de manutenção (Alan), 54 caracteres. Fica 25 bytes depois da do Dan.
- 18304 `fxsvtywolkdwxdzntueuhlref` - string de 25 caracteres, por identificar (possível relação com o secret final; a confirmar nos targets seguintes).

### Material criptográfico (Targets 4 e 5)
- 2954 Chave privada RSA em base64 (`MIIEpQIBAAKCAQEA...`). 1592 caracteres → 1193 bytes DER (PKCS#1). Chave RSA-2048.
- 4562 Assinatura em base64 (`JFSvf6ww...`). 344 caracteres → 256 bytes. Compatível com assinatura RSA-2048.

### Consola / login / dump
- 17736 `Password: `, 17747 `Wrong password`, 18042 `Enter password for vending machine number `, 18088 `Logged in as `, 18102 `Login failure`.
- 17956 `Press Enter to stop`, 17977/17998 `Dumping Interrupted`, 18025 `Finished dumping` - mensagens do menu de dump.

### C&C (Targets 5/6/7)
- 17714 `Connecting to the C&C`, 17762 `OTP: `, 17768 `Incorrect OTP, got `, 17788 `, was expecting `, 17805 `CONGRATULATIONS! You have successfully connected to the C&C`, 17865 `Here is the final secret: `, 17941 `Signed-By: Dan`.

### Diálogo Dan/Alan (105–5470)
Conversa que explica a necessidade de chave privada + assinatura + nonce (OTP) para ligar ao C&C de forma segura. Pistas para os targets seguintes.

## Resposta (placa 38)
- **Password de manutenção (Alan):** `alanyangksdbajomxyrtbbtfkiicwyqybmbwigdyecluhrdbfymgdf`
- **Offset relativo à password de developer:** +25 bytes (Dan em 18222, Alan em 18247).

## Gerar
```
cd TARGETS\target-2
strings64 -a -o -nobanner -n 4 progmem.bin > ..\target-3\strings.txt
```
Depois inspecionar `strings.txt`: `Ctrl+F "Admin"` para as credenciais e offsets, `Ctrl+F "MII"` para a chave e a assinatura.
