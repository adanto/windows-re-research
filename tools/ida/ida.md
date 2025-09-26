# IDA Pro

A short reference for using **IDA Pro** and IDAPython for interactive reversing and lightweight debugging automation.

---

## Links
- IDA tips & tricks: https://hex-rays.com/blog/tag/idatips  
- IDA keyboard shortcuts / configuration: https://docs.hex-rays.com/user-guide/configuration/shortcuts

---

## Signatures (Shift+F5)
These FLIRT signature packs are the minimal ones I keep for faster VC/MFC/runtime recognition:

- `msmfc64`  
- `vc32rtf`  
- `vc32seh`  
- `vc32ucrt`  
- `vc64rtf`  
- `vc64seh`  
- `vc64ucrt`  

> Apply via **Shift+F5** in IDA (or `Options → Load file → FLIRT signatures`).

---

## Libraries (Shift+F11)

Useful library files to load for improved function recognition (userland & kernel):

- `ntapi`  
- `ntapi64_win7`  
- `ntddk64_win7`  *(useful when analysing kernel drivers)*  
- `mssdk64_win7` *(often loaded automatically)*

> Load via **Shift+F11** (or `Options → Load library file (tilib)`).

---

## plugins 

A short list of useful IDA plugins and utilities (links + one-line descriptions) you can add to your `docs/IDA.md` page.


* **Base debugging plugin** — Base IDA plugin to launch a debugging program: ([GitHub][6])

* **Shellcode Hashes** — Helps identify and resolve common string/hash patterns used by shellcode (precomputed hash DB + IDA script to match). Useful when reversing raw shellcode or unpacked payloads. ([GitHub][1])

* **Diaphora** — A mature program-diffing plugin for IDA (binary diffing between two IDBs). Great for finding patches, regressions, or differences between versions. Actively maintained on GitHub. ([GitHub][2])

* **ComIDA** — Finds and annotates COM usage (GUIDs, CoCreateInstance/QI sites) to improve decompilation and make COM-heavy modules easier to read. See the plugin repo and a Hex-Rays “plugin focus” writeup. ([GitHub][3])

* **capa / Capa Explorer (IDA plugin)** — Integrates Mandiant’s capa into IDA so you can discover capabilities (high-level behaviour matches) inside the database and author new rules from IDA context. Very helpful for triage and focusing RE efforts. ([GitHub][4])
 
* **hashdb** — Integrates the OALabs HashDB service into IDA, allowing quick resolution of custom API hash functions to their original strings. Useful when analyzing malware that obfuscates API calls or strings with non-standard hashing algorithms. Provides right-click lookups from IDA and supports collaboration by contributing new hashes. ([GitHub][8])


---

## Utility: creating `.idt` / `.ids` files (create IDT)

* **What it is:** `.idt` (and compressed `.ids`) files map API ordinals and export positions to names so IDA can resolve imports/ordinals and annotate code automatically.
* **How to create them:** There are small scripts and community posts showing how to generate `.idt` files from MS libraries / PDBs (examples and historical tooling linked below). Useful when analysing obscure or trimmed system libraries. 
* On the wild case in which they needed to recreate these tables at [harfanglab.io][7] to reverse engineering .NET AOT apps


[1]: https://github.com/mandiant/flare-ida
[2]: https://github.com/joxeankoret/diaphora
[3]: https://github.com/airbus-cert/comida
[4]: https://github.com/mandiant/capa
[5]: https://www.hexacorn.com/blog/2016/04/22/creating-idtids-files-for-ida-from-ms-libraries-with-symbols/
[6]: /tools/ida/idaScriptBase.py
[7]: https://harfanglab.io/insidethelab/reverse-engineering-ida-pro-aot-net/
[8]: https://github.com/OALabs/hashdb-ida