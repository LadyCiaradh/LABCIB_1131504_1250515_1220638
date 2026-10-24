# Target 1 — Developer password

## Artefactos
- `length_timing.csv` — tempos por comprimento (varredura de comprimento).
- `scan_pos0.csv` — tempos candidato x posição (varredura do 1.o caracter).
- `char_timing.csv` — tempos por caracter nas posições analisadas.
- `char_timing_pos1.png`, `char_timing_pos2.png` — gráficos da 1.a e 2.a letra.
- `scan_gap.png` — margem de tempo por comprimento.
- Script que gera os gráficos a partir dos CSV: `CODE/target-1/plot_timing.py` (correr reproduz as figuras).

## Resposta (placa 22)
- **Comprimento inferido:** 13.
- **Margem do caracter vencedor por posição:** ~1 ms por caracter correto (um atraso por caracter); posição 0 ~2 ms porque o filler 'a' coincide com o 2.o caracter.
- **Posição com menor margem:** 10 (0,943 ms). As posições 1 a 11 correspondem todas a um único atraso, logo as margens são quase iguais e a da posição 10 é a mais pequena, dentro do ruído de medição.

## Resposta (placa 38)
- **Comprimento inferido:** 13.
- **Margem do caracter vencedor por posição:** ~1 ms por caracter correto (um atraso por caracter); posição 0 ~2 ms porque o filler 'a' coincide com o 2.o caracter.
- **Posição com menor margem:** Tal como na placa 22, as posições 1-11 correspondem todas a um único atraso (~0.9 ms), por isso as margens são praticamente iguais.

## Reproduzir
Com a placa ligada: `CODE/target-1/timing_attack.py` (scan, recover, finish). Offline: `CODE/target-1/plot_timing.py` sobre os CSV reproduz os gráficos.
