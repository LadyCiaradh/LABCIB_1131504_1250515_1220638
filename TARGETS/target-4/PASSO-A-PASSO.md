# Target 4 — Dados criptográficos

Parte 2. Parte de strings/entropy do dump do Target 2–3. Enunciado: `embedded-lab-part-02.md`.

## 1. Localizar material suspeito
- [ ] Encoding que se destaque (ex. base64) e regiões de entropy diferente de código
- [ ] Depois de descodificar, ver se é bloco opaco ou estrutura com magic numbers

## 2. Identificar chave e assinatura
- [ ] Extrair chave e assinatura (base64) **do vosso** firmware
- [ ] Inspecionar a chave com as ferramentas que o enunciado indica (`openssl asn1parse` / `openssl rsa -text`)
- [ ] Scan de entropy do firmware (script + dados, para o gráfico ser reproduzível)

## 3. Artefactos (obrigatório)
- [ ] Chave extraída (base64)
- [ ] Assinatura extraída (base64)
- [ ] Scan de entropy
- [ ] Primeiras linhas de `asn1parse` / `rsa -text` sobre **esta** chave

## 4. Responder no README da raiz
- [ ] Tamanho da chave
- [ ] Bytes estruturais (ASN.1/DER) que a identificaram
- [ ] Tamanho em bytes da assinatura encriptada
- [ ] Entropy da região da chave vs. uma região de código
