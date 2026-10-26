# Target 1 - Timing attack (código)

Camada de I/O série separada da lógica do ataque, como o enunciado pede.

## Ficheiros
- `serial_target.py` - comunicação série + medição de tempo (reutilizável nos Targets 6 e 7). **Ajustar a secção CONFIG.**
- `timing_attack.py` - infere comprimento e recupera a password; grava os tempos em bruto em CSV.
- `plot_timing.py` - gera os gráficos a partir dos CSV.

## Pré-requisitos
```
pip install pyserial matplotlib
```

## Passos
1. Liga a placa por USB e descobre a porta (Windows: Gestor de Dispositivos → COMx).
2. Em `serial_target.py` ajusta `PORT`, `BAUD`, `SEND_TEMPLATE` e `RESPONSE_MARKERS` conforme o que a consola da **tua** placa mostra. Testa a ligação:
   ```
   python serial_target.py
   ```
   Deves ver a resposta a uma password errada.
3. Inferir o comprimento:
   ```
   python timing_attack.py length
   python plot_timing.py length
   ```
4. Recuperar a password (N = comprimento inferido):
   ```
   python timing_attack.py recover N
   python plot_timing.py chars
   ```

## Artefactos para TARGETS/target-1/
- `length_timing.csv`, `char_timing.csv` (dados brutos)
- `length_timing.png`, `char_timing_pos1.png`, `char_timing_pos2.png`
- Estes scripts (ou cópia)

Nota: regista a margem de tempo do caracter vencedor em cada posição (sai no output do `timing_attack.py recover`) e identifica a posição com menor margem.
