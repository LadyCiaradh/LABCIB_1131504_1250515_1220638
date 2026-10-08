# Target 2 — Dump do firmware

Só depois do Target 1 (consola de desenvolvimento acessível **nesta** placa).

## 1. Obter os binários
- [ ] Usar a consola já autenticada; o enunciado diz que ela pode ajudar a obter o firmware
- [ ] Guardar cada dump **sem** o alterar
- [ ] **Não** voltar a gravar firmware na placa

## 2. Artefactos (obrigatório)
- [ ] Ficheiros binários dumpados nesta pasta
- [ ] SHA-256 de **cada** ficheiro (lista de checksums)

## 3. Responder no README da raiz
- [ ] SHA-256 do dump PROGMEM
- [ ] Tamanho em bytes desse dump
- [ ] Offset onde aparece a password de developer

## 4. `secrets.csv`
- [ ] Campo PROGMEM firmware SHA-256 (tem de bater com o dump desta pasta)
