# Embedded Lab — Submission

- **Team:** 1131504, 1250515, 1220638
- **Arduino identification number:** Arduino 38 e 22
- **ZIP name (on delivery):** `1131504_1250515_1220638.zip`

Lab statements: [Part I](embedded-lab-part-01.md) · [Part II](embedded-lab-part-02.md)

Fill in every **TODO** below from *this team's assigned board*. Plots and conclusions must be reproducible from the files under `TARGETS/`.

---

## How to run the code

Scripts live in [`code/`](code/). Replace the commands once each tool exists.

### Target 1 — timing measurements and plots

```text
TODO: how to connect to the board, invoke the measurement tool, and generate plots from TARGETS/target-1/
```

### Target 2 — firmware dump

```text
TODO: how the dump was obtained and how SHA-256 of each binary is computed
```

### Target 3 — strings

```text
TODO: command used to produce TARGETS/target-3/strings.txt
```

### Target 4 — cryptographic assets

```text
TODO: openssl / entropy commands used
```

### Target 5 — c&c password

```text
TODO: openssl decrypt + rainbow-table lookup
```

### Target 6 — OTP generator

```text
TODO: how the serial capture was taken and how the next OTP is reproduced
```

### Target 7 — C&C session

```text
TODO: how the successful C&C connection was performed (password + OTP)
```

---

## Secrets (`TARGETS/secrets.csv`)

Single CSV line, no header, fields in this order:

1. Arduino ID
2. Dan's password
3. Alan's password
4. c&c password
5. Final secret
6. c&c password MD5 (hash recovered from the decrypted signature)
7. PROGMEM firmware SHA-256

Current file: [`TARGETS/secrets.csv`](TARGETS/secrets.csv)

---

## Answers (all assignment questions)

### Target 1 — Developer password

**How did you infer the password?** TODO

**If a timing attack:** plots of the first and second letters — [`TARGETS/target-1/`](TARGETS/target-1/)  
**If not:** how long did it take to crack? TODO

**Answer this (from *your* board).**

- Inferred length: TODO
- Timing margin of the winning character at each position: TODO
- Position with the *smallest* margin, and why: TODO

**Required artifacts:** raw timing data (candidate × position × samples) and the script that builds the plots.

---

### Target 2 — Dumped firmware

**Answer this (from *your* board).**

- SHA-256 of the PROGMEM dump: TODO
- Byte length of the PROGMEM dump: TODO
- Offset where the developer password appears: TODO

**Required artifacts:** dumped binaries plus SHA-256 of each, under [`TARGETS/target-2/`](TARGETS/target-2/).

---

### Target 3 — Confidential strings

**Relevant strings and why they matter:** TODO (see annotated list in [`TARGETS/target-3/`](TARGETS/target-3/))

**Answer this (from *your* board).**

- Second maintenance password: TODO
- Byte offset relative to the developer password: TODO
- Length of the base64 blobs: TODO

**Required artifacts:** full `strings` output and annotated asset list.

---

### Target 4 — Cryptographic data

**Answer this (from *your* board).**

- Key size: TODO
- Structural (ASN.1/DER) bytes that identified the key: TODO
- Encrypted signature size (bytes): TODO
- Key-region entropy vs a code region: TODO

**Required artifacts:** extracted key and signature (base64), firmware entropy scan, first lines of `openssl asn1parse` / `openssl rsa -text`.

---

### Target 5 — c&c password

**Answer this (from *your* board).**

- MD5 recovered from the decrypted signature: TODO
- Recovered c&c password: TODO
- Why a *short* rainbow table is enough: TODO

**Required artifacts:** decrypted `hash` file, openssl decrypt transcript, rainbow-table lookup result.

---

### Target 6 — OTP generator

**Answer this (from *your* board).**

- Attempts until the generator repeated (this boot): TODO
- Value that repeated: TODO
- Next OTP the generator will produce: TODO

**Required artifacts:** raw serial capture showing the repeat (`.txt`), recovered generator parameters, reproduction of the next expected value.

---

### Target 7 — Final secret

**Answer this (from *your* board).**

- How targets 5 and 6 combined to connect: TODO

**Required artifacts:** full serial transcript of the successful C&C connection (OTP accepted + final-secret line).

---

## File map

| Path | Role |
| --- | --- |
| [`code/`](code/) | Scripts used to talk to the board and process artifacts |
| [`TARGETS/secrets.csv`](TARGETS/secrets.csv) | One-line secrets for grading |
| [`TARGETS/AI-DISCLOSURE.md`](TARGETS/AI-DISCLOSURE.md) | Mandatory AI-use disclosure |
| [`TARGETS/target-1/`](TARGETS/target-1/) … [`target-7/`](TARGETS/target-7/) | Per-target proof-of-work |

Noteworthy / unexpected observations: TODO
