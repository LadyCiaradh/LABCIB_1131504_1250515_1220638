# Target 1 — Password de developer

Usa **uma** placa de cada vez (38 ou 22). Anota o ID físico. Não faças Upload de sketches.

Detalhe do método: enunciado em `embedded-lab-part-01.md` (TARGET 1). O código fica em `code/`; aqui só a evidência.

## 1. Sessão série
- [ ] USB, porta COM, Serial Monitor (115200; se lixo, 9600)
- [ ] Reset: texto inicial / prompt
- [ ] Password errada: resposta do dispositivo
- [ ] Guardar um extracto da sessão (opcional, útil para o relatório)

## 2. Trabalho do alvo
- [ ] Seguir o enunciado para inferir a password (o texto aponta para diferenças de tempo na validação; comprimento antes do resto; `a-z`, máx. 20)
- [ ] Implementar **vocês** a medição e a comunicação série em `code/`
- [ ] Repetir amostras o suficiente para o gráfico não ser ruído de uma única tentativa

## 3. Artefactos (obrigatório)
- [ ] Ficheiro de dados brutos: carácter candidato × posição × amostras
- [ ] Script que **reproduz** os gráficos a partir desse ficheiro
- [ ] Gráficos da 1.ª e 2.ª letras (se usarem timing)

Gráfico sem CSV + script = 0 neste alvo.

## 4. Responder no README da raiz
- [ ] Como inferiram a password
- [ ] Comprimento
- [ ] Margem do carácter vencedor em cada posição
- [ ] Posição com **menor** margem e porquê

## 5. `secrets.csv`
- [ ] Campo Arduino ID
- [ ] Password do Dan (developer), quando tiverem a certeza nesta placa
