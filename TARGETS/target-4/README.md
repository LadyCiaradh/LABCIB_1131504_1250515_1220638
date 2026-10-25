# Target 4 - Cryptographic data

## Artefactos
- `key.b64`, `sig.b64` - chave e assinatura em base64, copiadas das strings do firmware (offsets 2954 e 4562).
- `key.der`, `sig.bin` - versões binárias (base64 descodificado com `openssl base64 -d -A`).
- `asn1parse_key.txt` - saída de `openssl asn1parse` sobre a chave.
- `rsa_text.txt` - saída de `openssl rsa -text` sobre a chave.
- `entropy.csv`, `entropy_scan.png` - scan de entropy do firmware (`code/target-4/entropy_scan.py`).

## Resposta (placa 22)
- **Comprimento dos blobs base64:** chave 1592 caracteres; assinatura 344 (= 256 bytes).
- **Tamanho da chave:** 2048 bits (RSA privada, 2 primos).
- **Bytes ASN.1/DER que a identificam:** SEQUENCE (30 82...); version INTEGER 00; modulus de 257 bytes (= 2048 bits); expoente 010001 (65537). Prefixo base64 `MII` = 30 82.
- **Tamanho da assinatura:** 256 bytes (bloco RSA-2048).
- **Entropy chave vs código:** código ~4.63; chave base64 ~5.98; chave descodificada ~7.81 bits/byte.

## Reproduzir
Ver a secção Target 4 no README raiz (descodificação com openssl + `entropy_scan.py`).
