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

## Long reading documentation

  - **Internals Basics**
    - Part 1 – Fundamentals
        - Introduction
        - Processes & Threads
        - Windows Loader & Image Activation
        - Memory & Virtual Address Space
        - Object Manager & Handles
        - Syscalls & the NTAPI Boundary
        - Scheduling, APCs & Callback Surfaces
        - IPC (ALPC, RPC, COM, Pipes)
    - Part 2 – Exploitation Mitigations
        - DEP / NX / W^X
        - ASLR / KASLR
        - Compiler & Hardware CFI: CFG, CET (Shadow Stack/IBT)
        - Trust & Integrity: Secure Boot, WDAC/App Control, Code Integrity, PatchGuard, VBS/HVCI, PPL
        - Compiler & EH Hardening (/GS, SafeSEH/SEHOP history, EHCONT)
    - Part 3 – Anti-Reversing & Evasion
        - Anti-Debugging
        - Anti-Disassembly
        - Sandbox & VM Evasion
        - Process Injection & Hooking
        - AMSI & Script Host Internals
        - Telemetry Tampering & Unhooking (ETW, Direct Syscalls)
        - Rootkits & Bootkits
    - Part 4 – Practical Exploitation
        - Buffer Overflows
        - Use-After-Free & Type Confusion
        - ROP & JOP
        - Shellcoding
        - Fuzzing & Exploit Development
        - Kernel Exploitation Primer
    - Part 5 – Detection & Countermeasures
        - Windows Eventing & ETW Playbook
        - Telemetry & Hunting
        - EDR & AV Evasion
        - Case Studies
        - Malware Capability Triage: YARA/CAPA/Sigma



