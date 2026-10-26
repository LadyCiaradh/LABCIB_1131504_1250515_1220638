# Code

Scripts used to talk to the Arduino and to turn raw artifacts into plots and derived files.

The serial I/O layer is kept generic (`serial_target.py`) so the same session/communication code is reused across targets; each target adds only its own logic on top.

All commands assume you are inside the target's folder and that the board is on the right COM port (COM3 for board 22, COM5 for board 38), 115200 baud, New Line ending. Install the Python deps once with `pip install pyserial matplotlib`.

## Target 1 - Developer Password (timing attack)

Path: [`target1/`](target1/)

- `serial_target.py` - generic serial session (open port, send, timed read).
- `timing_attack.py` - length/character recovery via response timing.
- `plot_timing.py` - builds the timing graphs from the raw samples.

```
cd target1
python timing_attack.py scan            # infer length + 1st character
python timing_attack.py recover 13      # recover full password (length 13)
python timing_attack.py finish <partial># confirm last character by response
python plot_timing.py scan              # length-scan graph
python plot_timing.py chars             # 1st/2nd character graphs
```

Raw samples are written as `.csv` next to the scripts and consumed by `plot_timing.py`, so the figures are reproducible from the data.

## Target 2 - Firmware Dump

Path: [`target2/`](target2/)

- `dump_capture.py` - logs in, navigates the dev menu, reads the raw PROGMEM, writes `progmem.bin` and prints its SHA-256.

```
cd target2
python dump_capture.py 0                # 0 = PROGMEM -> TARGETS/target-2/progmem.bin + SHA-256
```

Verify independently with `certutil -hashfile ..\..\TARGETS\target-2\progmem.bin SHA256` (Windows) or `sha256sum` (Linux/macOS). A valid dump is 32768 bytes and starts with `0c 94` (AVR vector table).

## Target 3 - Confidential Strings

Path: [`target3/`](target3/)

No custom build step: strings are extracted with the `strings` tool and offsets with `-o`.

```
strings64 -a -o -nobanner -n 4 progmem.bin > strings.txt
```

`find_offset.py` is a small helper to locate a string's byte offset directly in the binary (more reliable than eyeballing `strings.txt`):

```
cd target3
python find_offset.py progmem.bin danzhbmzndzdd
```

## Target 4 - Cryptographic Assets

Path: [`target4/`](target4/)

- `entropy_scan.py` - Shannon entropy over the firmware in 256-byte windows, highlighting the key/signature regions vs code.

```
cd target4
python entropy_scan.py progmem.bin
```

Key/signature identification itself uses OpenSSL (no code):

```
openssl base64 -d -A -in key.b64 -out key.der
openssl asn1parse -inform DER -in key.der
openssl rsa -inform DER -in key.der -text -noout
```

## Target 5 - C&C Password

No code. Done entirely with OpenSSL and the provided rainbow table. Commands and output are in `TARGETS/target-5/`.

## Target 6 - OTP Generator

Path: [`target6/`](target6/)

- `otp_capture.py` - captures the serial OTP attempts until the generator repeats and records the parameters.
- `otp_predict.py` - reproduces the recovered generator and prints the next expected value.

```
cd target6
python otp_capture.py                   # raw serial capture (.txt) + repeat detection
python otp_predict.py                   # next OTP from recovered parameters
```

## Target 7 - Final Secret

No code. The successful C&C connection (password + valid OTP) is captured as a serial transcript in `TARGETS/target-7/`.
