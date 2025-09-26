# Windows RE — Useful Structures (cheat-sheet)

A compact, copy-ready Markdown page linking the most common and useful Windows structures for reversing (IDA / Ghidra). Short descriptions, quick links to authoritative docs, and tiny usage tips so you can jump straight from an IDB to the structure you need.

---

## How to use this page

* Use the name to search in your IDA type libraries (`Shift+F11`) or apply as a manual struct (`N` or `M`) in the Structures window.

---

## Quick reference table

| Structure                                                             |                                                                                                                                                                    What it is / Why care | Common doc / link                                                                                                                                                                                    |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **IMAGE_DOS_HEADER**                                                  |                                                                                               DOS header at file start (`e_magic == 'MZ'`). First thing to check when triaging PE files. | Microsoft / PE docs (see PE spec)                                                                                                                                                                    |
| **IMAGE_NT_HEADERS**                                                  |                                                           PE header (NT headers) — contains FileHeader and OptionalHeader; essential to parse sections, entry point and characteristics. | [https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_nt_headers32](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_nt_headers32)                       |
| **IMAGE_FILE_HEADER**                                                 |                                                                       Part of NT_HEADERS — machine, number of sections, characteristics. Useful to quickly identify target architecture. | (see PE docs above)                                                                                                                                                                                  |
| **IMAGE_OPTIONAL_HEADER32 / IMAGE_OPTIONAL_HEADER64**                 |                                                                           Optional header (entry point, image base, section alignment, data directories). Critical for mapping behavior. | [https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_optional_header32](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_optional_header32)             |
| **IMAGE_DATA_DIRECTORY**                                              |                                                                         Points to important PE tables (Export, Import, Resource, TLS, CLI, etc.). Use to find exports/imports/TLS/Certs. | [https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_data_directory](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_data_directory)                   |
| **IMAGE_EXPORT_DIRECTORY**                                            |                                                                                                            Export table layout — useful when resolving ordinals/exports inside a module. | [http://pinvoke.net/default.aspx/Structures.IMAGE_EXPORT_DIRECTORY](http://pinvoke.net/default.aspx/Structures.IMAGE_EXPORT_DIRECTORY)                                                               |
| **IMAGE_IMPORT_DESCRIPTOR**                                           |                                                                                                                   Import table entries — where imported DLL names and thunk arrays live. | (PE docs / analyzer references)                                                                                                                                                                      |
| **IMAGE_TLS_DIRECTORY**                                               |                                                                                               TLS callbacks — often abused by malware for early run code. Look for `.tls` and callbacks. | (PE docs / MS links)                                                                                                                                                                                 |
| **IMAGE_RESOURCE_DIRECTORY**                                          |                                                                                                     Structure that describes resources (.rsrc) — icons, dialogs, manifest, version info. | (PE docs)                                                                                                                                                                                            |
| **PEB (Process Environment Block)**                                   | In-memory process struct with pointers to process parameters, loader data, image base, etc. Frequently used in userland RE to iterate loaded modules or find command line / environment. | [https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb](https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb)                                         |
| **PEB_LDR_DATA**                                                      |                                                        Loader lists (InLoadOrderModuleList, InMemoryOrderModuleList). Use to enumerate modules without APIs (anti-API evasion analysis). | [https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb_ldr_data](https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb_ldr_data)                       |
| **LDR_DATA_TABLE_ENTRY**                                              |                                                       Single module entry inside loader lists — contains BaseDllName, FullDllName, DllBase, SizeOfImage. Use to map modules and exports. | [https://www.geoffchappell.com/studies/windows/km/ntoskrnl/inc/api/ntldr/ldr_data_table_entry.htm](https://www.geoffchappell.com/studies/windows/km/ntoskrnl/inc/api/ntldr/ldr_data_table_entry.htm) |
| **TEB (Thread Environment Block)**                                    |                      Per-thread structure (stack limits, thread id, TLS slots, last error, TEB->ProcessEnvironmentBlock pointer). Useful for thread-local insights and stack inspection. | [https://en.wikipedia.org/wiki/Win32_Thread_Information_Block](https://en.wikipedia.org/wiki/Win32_Thread_Information_Block)                                                                         |
| **CONTEXT**                                                           |           Thread context structure used by `GetThreadContext`/`SetThreadContext` and debuggers. Essential for register/state dumps and to craft stolen thread or remote thread payloads. | (Win32 docs)                                                                                                                                                                                         |
| **UNICODE_STRING / ANSI_STRING**                                      |                                                           Classic Windows string descriptors used everywhere in NT APIs and many kernel/user structures (Length, MaximumLength, Buffer). | (Win32/NT docs)                                                                                                                                                                                      |
| **OBJECT_ATTRIBUTES**                                                 |                                                 Kernel/user structure used with many native APIs (`NtCreateFile`, `NtOpenKey`, etc.). Useful when reading syscall-level calls in traces. | (NT docs)                                                                                                                                                                                            |
| **IO_STATUS_BLOCK**                                                   |                                                         Standard structure for many I/O native calls (status code, information). Seen in DeviceIoControl / NtDeviceIoControlFile traces. | (NT docs)                                                                                                                                                                                            |
| **FILE_STANDARD_INFORMATION / FILE_BASIC_INFORMATION**                |                                                                       File metadata structures returned by native file queries — helpful for forensic timestamps and attribute analysis. | (NT docs)                                                                                                                                                                                            |
| **EPROCESS**                                                          |                                    Kernel structure representing a process in NT kernel. Used when analysing drivers or kernel memory to find process lists, token pointers and handles. | (kernel internals references)                                                                                                                                                                        |
| **ETHREAD**                                                           |                                                                        Kernel per-thread structure — scheduling state, thread id, APC queues. Useful for kernel RE and rootkit analysis. | (kernel internals references)                                                                                                                                                                        |
| **KTHREAD / KPROCESS**                                                |                                                                                                                Lower-level kernel scheduling structures — used in deep kernel debugging. | (kernel references)                                                                                                                                                                                  |
| **DRIVER_OBJECT / DEVICE_OBJECT**                                     |                                                                       Kernel driver related structures — entry points, device name, dispatch routines. Essential when reversing drivers. | (ntddk docs)                                                                                                                                                                                         |
| **MODULE / RTL structures (RTL_BALANCED_NODE, RTL_HASH_TABLE, etc.)** |                                                             Generic RTL structures used across the kernel and userland runtimes — useful to decode internal containers and linked lists. | (internal docs / blogs)                                                                                                                                                                              |

---

## Calling conventions (short)

* `__cdecl` — default x86 C: caller cleans stack, return in `EAX`.
* `__stdcall` — callee cleans stack, return in `EAX`.
* `__fastcall` — x86 variants use registers (`ECX`, `EDX`) for first args (implementation dependent).
* **Microsoft x64** — first 4 integer/pointer args in `RCX, RDX, R8, R9`; caller allocates 32-byte shadow space; additional args on stack. See calling convention notes. 

Reference: x86-64 calling conventions. (See wiki / MS docs.)

(When reversing, annotate calling convention on functions to get parameter names and types in the decompiler.)

---

## Magic numbers & file signatures

Sometimes quick triage needs a magic-number scan (e.g., DOC/CFBF signature `D0CF11E0A1B11AE1` for old Office formats). Check a short list of common file signatures when a blob looks like a document / archive. Useful when unpacking staged payloads or hidden resources.

* Compound File Binary Format (CFBF): `D0 CF 11 E0 A1 B1 1A E1` — old Office files.
* PDF: `%PDF-`.
* ZIP: `PK\x03\x04`.
* EXE: `MZ` followed by `PE\0\0` at `e_lfanew`.

Further lists: file signature references / magic numbers (see Wikipedia's list of file signatures).

---

## Practical IDA / RE tips

* **Load type libraries**: `ntapi`, `ntapi64_win7`, `ntddk64_win7` in IDA to get many of the above structures available as typed structs. 
* **Structs → Create**: copy field names (e.g., `PEB`, `PEB_LDR_DATA`, `LDR_DATA_TABLE_ENTRY`) and apply them to memory addresses when you spot the data (e.g., PEB pointer in `gs:60h` on x64).
* **Annotate imports/exports**: use `IMAGE_EXPORT_DIRECTORY`, `IMAGE_IMPORT_DESCRIPTOR` to resolve function names and annotate call sites.
* **Use FLIRT sigs**: helps resolve runtime libraries quickly (`Shift+F5`). 


