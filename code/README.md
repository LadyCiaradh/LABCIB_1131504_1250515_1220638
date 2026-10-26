# Code

Scripts usados para comunicar com o Arduino e para transformar os artefactos em
bruto em gráficos e ficheiros derivados. A camada de I/O série é mantida genérica
(`serial_target.py`) para que o mesmo código de sessão/comunicação seja
reutilizado entre targets; cada target acrescenta só a sua lógica por cima.

Todos os comandos assumem que estás dentro da pasta do target e que a placa está
na porta COM certa (COM3 para a placa 22, COM5 para a placa 38), 115200 baud,
terminador New Line. Instala as dependências Python uma vez com
`pip install pyserial matplotlib`.

## Target 1 - Developer password (timing attack)

Pasta: `target-1/`

- `serial_target.py` - sessão série genérica (abrir porta, enviar, leitura cronometrada).
- `timing_attack.py` - recuperação de comprimento/caracteres pelo tempo de resposta.
- `plot_timing.py` - gera os gráficos de tempo a partir das amostras em bruto.

```
cd target-1
python timing_attack.py scan            # infere comprimento + 1.o caracter
python timing_attack.py recover 13      # recupera a password (comprimento 13)
python timing_attack.py finish <parcial># confirma o último caracter pela resposta
python plot_timing.py scan              # gráfico da varredura de comprimento
python plot_timing.py chars             # gráficos do 1.o/2.o caracter
```

As amostras em bruto são gravadas em `.csv` junto aos scripts e consumidas pelo
`plot_timing.py`, por isso as figuras são reproduzíveis a partir dos dados.

## Target 2 - Firmware dump

Pasta: `target-2/`

- `dump_capture.py` - faz login, navega o menu de developer, lê o PROGMEM em
  bruto, escreve `progmem.bin` e imprime o seu SHA-256.

```
cd target-2
python dump_capture.py 0                # 0 = PROGMEM -> TARGETS/target-2/progmem.bin + SHA-256
```

Verificar de forma independente com
`certutil -hashfile ..\..\TARGETS\target-2\progmem.bin SHA256` (Windows) ou
`sha256sum` (Linux/macOS). Um dump válido tem 32768 bytes e começa por `0c 94`
(tabela de vetores do AVR).

## Target 3 - Confidential strings

Sem código próprio. As strings são extraídas com a ferramenta `strings`
(Sysinternals no Windows) e os offsets com `-o`. A inspeção (procurar
credenciais, offsets e blobs) é manual, no editor.

```
strings64 -a -o -nobanner -n 4 progmem.bin > strings.txt
```

Comando completo e passos de inspeção: ver `TARGETS/target-3/README.md`.

## Target 4 - Cryptographic data

Pasta: `target-4/`

- `entropy_scan.py` - entropy de Shannon sobre o firmware em janelas de 256
  bytes, realçando as regiões da chave/assinatura face ao código.

```
cd target-4
python entropy_scan.py
```

A identificação da chave/assinatura em si usa OpenSSL (sem código):

```
openssl base64 -d -A -in key.b64 -out key.der
openssl asn1parse -inform DER -in key.der
openssl rsa -inform DER -in key.der -text -noout
```

## Target 5 - c&c password

Sem código próprio. Feito inteiramente com OpenSSL e a rainbow table fornecida.
Comandos e output estão em `TARGETS/target-5/`.

## Target 6 - OTP generator

Pasta: `target-6/`

- `otp_crack.py` - captura as tentativas de OTP pela série até o gerador repetir,
  recupera os parâmetros do LCG e prevê a próxima OTP.

```
cd target-6
python otp_crack.py                     # captura em bruto (.txt) + deteção de repetição + recuperação do LCG
```

## Target 7 - Final secret

Sem código próprio. A ligação ao C&C bem-sucedida (password + OTP válida) é
capturada como transcript série em `TARGETS/target-7/`.
