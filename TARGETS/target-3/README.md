# Target 3 - Confidential Strings

## Artefactos
- `strings-22.txt` - output completo do `strings` do dump PROGMEM da placa 22 (formato `offset:texto`, offsets em decimal).
- `strings-38.txt` - o mesmo para a placa 38.

## Como gerar
```
cd TARGETS\target-2
strings64 -accepteula -a -o -nobanner -n 4 progmem.bin > ..\target-3\strings-22.txt
strings64 -accepteula -a -o -nobanner -n 4 progmem-38.bin > ..\target-3\strings-38.txt
```
Depois inspecionar os ficheiros:
- `Ctrl+F "Admin"` para a tabela de credenciais.
- `Ctrl+F "MII"` para a chave privada.
- `Ctrl+F "signature"` para a assinatura (a linha a seguir à chave).
- `Ctrl+F "DEVELOPMENT"` para o menu de debug e as strings aleatórias que o antecedem.

Convenção de offsets: para os blobs base64 indica-se o offset do início do blob, não o da linha do diálogo. Os prefixos `Dan: The key "` (14 caracteres) e `Dan: The very secret signature. "` (33 caracteres) explicam a diferença em relação ao offset mostrado pelo `strings`.

---

## Resposta (placa 22)
- **Password de manutenção (Alan):** `alanimyirtjaawjwdkbzonruikuhxbmvsgykfvtkrirofdikmzvocg` (offset 18249, 54 caracteres)
- **Offset relativo à password de developer:** +25 bytes (Dan em 18224, Alan em 18249)
- **Comprimento dos blobs base64:** chave RSA 1592 caracteres (offset 2968, = 1193 bytes); assinatura 344 caracteres (offset 4595, = 256 bytes)

### Credenciais (tabela em ~18210–18328)
Tabela de utilizadores com rótulo + password, separados por terminador nulo. É a fonte mais crítica, porque dá acesso direto à consola sem precisar de side-channel.
- 18210 `Developer Dan` - rótulo da conta de developer.
- 18224 `dansudeulzblj` - password do developer (Dan), 13 caracteres. É a mesma que foi recuperada por timing no Target 1, o que confirma o ataque. Aparece também em 700, dentro do diálogo embebido (fuga duplicada).
- 18238 `Admin Alan` - rótulo da conta de manutenção/admin.
- 18249 `alanimyirtjaawjwdkbzonruikuhxbmvsgykfvtkrirofdikmzvocg` - password de manutenção (Alan), 54 caracteres. Fica +25 bytes depois da do Dan (13 caracteres + nulo = 14; `Admin Alan` + nulo = 11). Em claro no firmware. Por timing seria muito mais demorada de recuperar.
- 18304 `fxsvtywolkdwxdzntueuhlref` - 25 caracteres, logo após a password do Alan (18249 + 54 + nulo). Sem rótulo. Não existe equivalente na placa 38.

### Candidatas a credenciais (não rotuladas)
Strings com o mesmo alfabeto das passwords, fora da tabela, imediatamente antes do menu de desenvolvimento. Existem nas duas placas na mesma posição estrutural.
- 17470 `papnmrmhkzvuwcteqqmwarzzlmnwgjpldhsddedpefbdufqgaajjn` - 53 caracteres. Offset relativo ao Dan: −754.
- 17524 `lrxabzgyvhdabvgnpnizynp` - 23 caracteres, contígua à anterior (17470 + 53 + nulo). Offset relativo ao Dan: −700.

Nenhuma destas strings está associada a um utilizador. A validar por tentativa de login na consola (`Logged in as ...` identifica a conta).

### Material criptográfico (Targets 4 e 5)
Chave privada e assinatura hardcoded no firmware. Quem as extrai pode fazer-se passar pelo dispositivo perante o C&C. Contraria diretamente o que o Alan pede no diálogo ("They cannot be hardcoded").
- 2968 Chave privada RSA em base64 (`MIIEpQIBAAKCAQEA...`). 1592 caracteres → 1193 bytes DER (PKCS#1, cabeçalho `MIIEpQ` = SEQUENCE de 0x4A5 + 4 bytes). Chave RSA-2048.
- 4595 Assinatura em base64 (`JFSvf6ww...`). 344 caracteres → 256 bytes, o tamanho exato de uma assinatura RSA-2048.

### Consola / login / dump
Revelam o fluxo de autenticação e a funcionalidade de dump usada no Target 2.
- 17736 `Password: `, 17747 `Wrong password`, 18042 `Enter password for vending machine number `, 18088 `Logged in as `, 18102 `Login failure`. As respostas distintas para sucesso e falha são consistentes com o timing leak explorado no Target 1.
- 17956 `Press Enter to stop`, 17977 `Dumping Interrupted`, 17998 `Dumping Interrupted %d %d` (format string com os índices onde o dump parou), 18025 `Finished dumping` - mensagens do dump.

### Menu de desenvolvimento
Menu de debug que permite listar e despejar regiões de memória. Foi o vetor usado no Target 2 e não devia existir em firmware de produção.
- 17569 `Current memory locations`, 17610 `Unacceptable index`, 17629 `MEMORY LOCATION TO PRINT`, 17654 `DEVELOPMENT MENU`, 17671 `List Memory locations`, 17693 `Dump Memory location`.
- 18116 `PROGMEM: Flash memory for large data`, 18153 `EEPROM: Memory for data storage`, 18185 `SRAM: Memory for runtime` - regiões disponíveis para dump. Indica que a EEPROM e a SRAM também podem ser extraídas.

### C&C (Targets 5/6/7)
Mostram que o dispositivo comunica com um C&C autenticado por OTP e que existe um secret final.
- 17714 `Connecting to the C&C`, 17762 `OTP: `, 17768 `Incorrect OTP, got `, 17788 `, was expecting `. A mensagem de erro revela o OTP esperado, o que é uma fuga de informação.
- 17805 `CONGRATULATIONS! You have successfully connected to the C&C`, 17865 `Here is the final secret: ` - objetivo final.
- 17892 `TODO: Replace this with actual connection to C&C` - indica que a ligação é simulada localmente, por isso a validação acontece no próprio firmware.
- 17941 `Signed-By: Dan` - associa a assinatura ao developer.

### Diálogo Dan/Alan (~105–5417)
Conversa embebida (deixada em comentário/string, como o próprio Alan critica em 5181) que explica o esquema chave privada + assinatura + nonce (OTP) para ligar ao C&C. Contém a password do Dan (700) e os dois blobs base64.
- 1972 / 5036 - o nonce é gerado por uma função "in-house" e tem de ser aleatório. Sugere um gerador fraco ou previsível, alvo provável para prever o OTP.
- 4941 - "I don't see "Signed-By" anywhere.... Oooh, maybe thats the secret part". Liga a string `Signed-By: Dan` (17941) à mensagem assinada.

---

## Resposta (placa 38)
- **Password de manutenção (Alan):** `alanyangksdbajomxyrtbbtfkiicwyqybmbwigdyecluhrdbfymgdf` (offset 18247, 54 caracteres)
- **Offset relativo à password de developer:** +25 bytes (Dan em 18222, Alan em 18247)
- **Comprimento dos blobs base64:** chave RSA 1588 caracteres (offset 2968, = 1191 bytes); assinatura 344 caracteres (offset 4591, = 256 bytes)

### Credenciais (tabela em ~18208–18300)
Tabela de utilizadores com rótulo + password, separados por terminador nulo. É a fonte mais crítica, porque dá acesso direto à consola sem precisar de side-channel.
- 18208 `Developer Dan` - rótulo da conta de developer.
- 18222 `danzhbmzndzdd` - password do developer (Dan), 13 caracteres. É a mesma que foi recuperada por timing no Target 1, o que confirma o ataque. Aparece também em 700, dentro do diálogo embebido (fuga duplicada).
- 18236 `Admin Alan` - rótulo da conta de manutenção/admin.
- 18247 `alanyangksdbajomxyrtbbtfkiicwyqybmbwigdyecluhrdbfymgdf` - password de manutenção (Alan), 54 caracteres. Fica +25 bytes depois da do Dan (13 caracteres + nulo = 14; `Admin Alan` + nulo = 11). Em claro no firmware. Por timing seria muito mais demorada de recuperar.
- Depois da password do Alan não há mais strings até 32549 (ao contrário da placa 22).

### Candidatas a credenciais (não rotuladas)
Strings com o mesmo alfabeto das passwords, fora da tabela, imediatamente antes do menu de desenvolvimento.
- 17466 `paprycaoepjwblfbmqawpmpbldupjerribjwqvuuvwdbvfkjrrmce` - 53 caracteres. Offset relativo ao Dan: −756.
- 17520 `erccvmlrxabztavmnznarggvz` - 25 caracteres, contígua à anterior (17466 + 53 + nulo). Offset relativo ao Dan: −702.

Nenhuma destas strings está associada a um utilizador. A validar por tentativa de login na consola (`Logged in as ...` identifica a conta).

### Material criptográfico (Targets 4 e 5)
Chave privada e assinatura hardcoded no firmware. Quem as extrai pode fazer-se passar pelo dispositivo perante o C&C. Contraria diretamente o que o Alan pede no diálogo ("They cannot be hardcoded").
- 2968 Chave privada RSA em base64 (`MIIEowIBAAKCAQEA...`). 1588 caracteres → 1191 bytes DER (PKCS#1, cabeçalho `MIIEow` = SEQUENCE de 0x4A3 + 4 bytes). Chave RSA-2048.
- 4591 Assinatura em base64 (`Y0ZME+yj...`). 344 caracteres → 256 bytes, o tamanho exato de uma assinatura RSA-2048.

### Consola / login / dump
Revelam o fluxo de autenticação e a funcionalidade de dump usada no Target 2.
- 17734 `Password: `, 17745 `Wrong password`, 18040 `Enter password for vending machine number `, 18086 `Logged in as `, 18100 `Login failure`. As respostas distintas para sucesso e falha são consistentes com o timing leak explorado no Target 1.
- 17954 `Press Enter to stop`, 17975 `Dumping Interrupted`, 17996 `Dumping Interrupted %d %d` (format string com os índices onde o dump parou), 18023 `Finished dumping` - mensagens do dump.

### Menu de desenvolvimento
Menu de debug que permite listar e despejar regiões de memória. Foi o vetor usado no Target 2 e não devia existir em firmware de produção.
- 17567 `Current memory locations`, 17608 `Unacceptable index`, 17627 `MEMORY LOCATION TO PRINT`, 17652 `DEVELOPMENT MENU`, 17669 `List Memory locations`, 17691 `Dump Memory location`.
- 18114 `PROGMEM: Flash memory for large data`, 18151 `EEPROM: Memory for data storage`, 18183 `SRAM: Memory for runtime` - regiões disponíveis para dump. Indica que a EEPROM e a SRAM também podem ser extraídas.

### C&C (Targets 5/6/7)
Mostram que o dispositivo comunica com um C&C autenticado por OTP e que existe um secret final.
- 17712 `Connecting to the C&C`, 17760 `OTP: `, 17766 `Incorrect OTP, got `, 17786 `, was expecting `. A mensagem de erro revela o OTP esperado, o que é uma fuga de informação.
- 17803 `CONGRATULATIONS! You have successfully connected to the C&C`, 17863 `Here is the final secret: ` - objetivo final.
- 17890 `TODO: Replace this with actual connection to C&C` - indica que a ligação é simulada localmente, por isso a validação acontece no próprio firmware.
- 17939 `Signed-By: Dan` - associa a assinatura ao developer.

### Diálogo Dan/Alan (~105–5413)
Conversa embebida (deixada em comentário/string, como o próprio Alan critica em 5177) que explica o esquema chave privada + assinatura + nonce (OTP) para ligar ao C&C. Contém a password do Dan (700) e os dois blobs base64.
- 1972 / 5032 - o nonce é gerado por uma função "in-house" e tem de ser aleatório. Sugere um gerador fraco ou previsível, alvo provável para prever o OTP.
- 4937 - "I don't see "Signed-By" anywhere.... Oooh, maybe thats the secret part". Liga a string `Signed-By: Dan` (17939) à mensagem assinada.
