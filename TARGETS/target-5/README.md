# Target 5 — c&c password

## Artefactos
- `hash.json` — hash MD5 recuperado da assinatura (bloco decriptado com a chave privada).
- `rainbow_lookup.txt` — linha da rainbow table que corresponde ao MD5 (password + hash).
- `openssl_transcript.txt` — registo dos comandos openssl (decriptação) e do lookup.

## Resposta (placa 22)
- **MD5 recuperado da assinatura:** `e07fcd7e6951d04659c4a8debe8e63de`
- **Password do c&c:** `cncazezuxmihjpgrddzjnemmyzajtwcyqufqqrqcrsoqhsdtnnwwa`
- **Porque chega uma rainbow table curta:** as passwords do c&c vêm de um conjunto pequeno e conhecido (prefixo `cnc`, comprimento fixo) e o MD5 não tem salt; basta pré-calcular as candidatas.

## Como se obteve
A "assinatura" (`sig.bin` do T4) não abre como assinatura (chave pública dá lixo); abre como bloco encriptado, com a chave privada:
`openssl pkeyutl -decrypt -inkey ../target-4/key.der -keyform DER -in ../target-4/sig.bin`.
O resultado é um JSON com o MD5, que se procura na coluna de hashes do `Rainbowtablee.txt`.
