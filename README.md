# Windows Research — Notes & Tools

A curated collection of Windows internals notes, malware reversing tips, and small PoCs aimed at reverse engineers.  
It may also include longer, book-style documents created during my learning process on specific topics or techniques.  

This repository serves as a personal, fast-access notebook for day-to-day malware analysis, Windows internals, and reversing.  
Instead of hundreds of scattered bookmarks or a massive text file, it centralizes concise notes, reference links, and code snippets for quick Ctrl+F access.  

The goal is simplicity and practicality — short entries, precise pointers, and ready-to-use references.  

All documentation is based on open-source material and libraries, curated and condensed (sometimes with the help of AI tools) to provide clear descriptions of techniques and defensive insights.


## Quick Index


  - **Docs**
    - [Basic Structs Cheat-Sheet](./docs/structs.md)
  - **PoCs**
    - [Basic InMemoryOrderModuleList](./pocs/libsfrompe.md)
    - [NOP Slide](./pocs/nopslide.md)
    - [Input blob Builder](./pocs/blobbuilder.md)
    - [Shellcode Launcher](./pocs/shellcodelauncher.md)
  - **Tools & Tips**
    - [IDA](./tools/ida/ida.md)
    - [Frida](./tools/frida/frida.md)
    - [x64dbg](./tools/x64dbg/x64dbg.md)
    - [Speakeasy](./tools/speakeasy.md)

## Long-form guides

- **WinLow — Windows Exploitation & Internals (WIP)** — a companion, hands-on reference that bridges Windows internals with exploitation and detection. Lab-friendly notes, redacted PoCs and hunting playbooks; actively maintained. https://github.com/adanto/winlow

### Internals Basics

  - **Part 1 – Fundamentals**
      - [Introduction](https://github.com/adanto/winlow/tree/main/part1/01-introduction.md)
      - [Processes & Threads](https://github.com/adanto/winlow/tree/main/part1/02-processes-threads.md)
      - [Windows Loader & Image Activation](https://github.com/adanto/winlow/tree/main/part1/03-loader-image-activation.md)
      - [Memory & Virtual Address Space](https://github.com/adanto/winlow/tree/main/part1/04-memory-vas.md)
      - [Object Manager & Handles](https://github.com/adanto/winlow/tree/main/part1/05-object-manager-handles.md)
      - [Syscalls & the NTAPI Boundary](https://github.com/adanto/winlow/tree/main/part1/06-syscalls-ntapi.md)
      - [Scheduling, APCs & Callback Surfaces](https://github.com/adanto/winlow/tree/main/part1/07-apcs-callbacks.md)
      - [IPC (ALPC, RPC, COM, Pipes)](https://github.com/adanto/winlow/tree/main/part1/08-ipc.md)
  - **Part 2 – Exploitation Mitigations**
      - [DEP / NX / W^X](https://github.com/adanto/winlow/tree/main/part2/01-dep-nx-wx.md)
      - [ASLR / KASLR](https://github.com/adanto/winlow/tree/main/part2/02-aslr-kaslr.md)
      - [Compiler & Hardware CFI: CFG, CET (Shadow Stack/IBT)](https://github.com/adanto/winlow/tree/main/part2/03-cfg-cet.md)
      - [Trust & Integrity: Secure Boot, WDAC/App Control, Code Integrity, PatchGuard, VBS/HVCI, PPL](https://github.com/adanto/winlow/tree/main/part2/04-trust-integrity-stack.md)
      - [Compiler & EH Hardening (/GS, SafeSEH/SEHOP history, EHCONT)](https://github.com/adanto/winlow/tree/main/part2/05-compiler-eh-hardening.md)
  - **Part 3 – Anti-Reversing & Evasion**
      - [Anti-Debugging](https://github.com/adanto/winlow/tree/main/part3/01-anti-debugging.md)
      - [Anti-Disassembly](https://github.com/adanto/winlow/tree/main/part3/02-anti-disassembly.md)
      - [Sandbox & VM Evasion](https://github.com/adanto/winlow/tree/main/part3/03-sandbox-vm-evasion.md)
      - [Process Injection & Hooking](https://github.com/adanto/winlow/tree/main/part3/04-injection-hooking.md)
      - [AMSI & Script Host Internals](https://github.com/adanto/winlow/tree/main/part3/05-amsi-script-host.md)
      - [Telemetry Tampering & Unhooking (ETW, Direct Syscalls)](https://github.com/adanto/winlow/tree/main/part3/06-telemetry-tampering.md)
      - [Rootkits & Bootkits](https://github.com/adanto/winlow/tree/main/part3/07-rootkits-bootkits.md)
  - **Part 4 – Practical Exploitation**
      - [Buffer Overflows](https://github.com/adanto/winlow/tree/main/part4/01-buffer-overflows.md)
      - [Use-After-Free & Type Confusion](https://github.com/adanto/winlow/tree/main/part4/02-uaf-type-confusion.md)
      - [ROP & JOP](https://github.com/adanto/winlow/tree/main/part4/03-rop-jop.md)
      - [Shellcoding](https://github.com/adanto/winlow/tree/main/part4/04-shellcoding.md)
      - [Fuzzing & Exploit Development](https://github.com/adanto/winlow/tree/main/part4/05-fuzzing-exploit-dev.md)
      - [Kernel Exploitation Primer](https://github.com/adanto/winlow/tree/main/part4/06-kernel-exploitation-primer.md)
  - **Part 5 – Detection & Countermeasures**
      - [Windows Eventing & ETW Playbook](https://github.com/adanto/winlow/tree/main/part5/01-etw-playbook.md)
      - [Telemetry & Hunting](https://github.com/adanto/winlow/tree/main/part5/02-telemetry-hunting.md)
      - [EDR & AV Evasion](https://github.com/adanto/winlow/tree/main/part5/03-edr-av-evasion.md)
