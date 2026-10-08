# Target 7 — Secret final

Junta Target 5 (password c&c) e Target 6 (OTP **deste** boot). Se reiniciares a placa, o OTP do Target 6 deixa de servir — volta a medir o gerador.

## 1. Ligação C&C
- [ ] Consola série na **mesma** placa
- [ ] Usar credenciais e OTP obtidos nos alvos 5 e 6, conforme o menu/protocolo que observarem
- [ ] Capturar a sessão **inteira** até aparecer a linha do secret

## 2. Artefactos (obrigatório)
- [ ] Transcript serial completo
- [ ] Tem de se ver: OTP aceite **e** a linha do secret final

## 3. Responder no README da raiz
- [ ] Como os alvos 5 e 6 se combinaram para ligar

## 4. `secrets.csv`
- [ ] Secret final
- [ ] Rever a linha completa: ID, Dan, Alan, c&c, secret, MD5, SHA-256 PROGMEM — tudo da mesma placa

## 5. Antes do ZIP
- [ ] `TARGETS/AI-DISCLOSURE.md` preenchido
- [ ] README da raiz sem TODOs pendentes
- [ ] Cada `target-n/` com artefactos reais (não só este passo a passo)
