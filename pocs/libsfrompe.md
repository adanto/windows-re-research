# PoC — List loaded libraries via PEB 

A small, copy-pasteable PoC that demonstrates how to enumerate the list of modules **loaded in the current process** by walking the Windows loader lists exposed from the in-memory `PEB` (Process Environment Block).
This is a *teaching* example: it uses common NT structures (`PEB`, `PEB_LDR_DATA`, `LDR_DATA_TABLE_ENTRY`) from `<winternl.h>` to locate the `InMemoryOrderModuleList` and print the module names and bases.

---

## Purpose

* Show how to access the `PEB` from userland (x86 / x64) and read the loader module list.
* Demonstrate using native NT structures (from `winternl.h`) instead of Win32 APIs (e.g., `EnumProcessModules`) — useful in some reversing scenarios (simple triage, anti-API evasion research, teaching).
* Provide a minimal C++ example a security researcher can extend (remote process enumeration, signature scanning, module export parsing, IDA/Ghidra annotations, etc).


---

## The PoC 

```c
#include <windows.h>
#include <winternl.h>
#include <stdio.h>

int main()
{
    printf("[*] Starting program\n");

#ifndef _WIN64
    PEB* peb = (PEB*)__readfsdword(0x30);
#else
    PEB* peb = (PEB*)__readgsqword(0x60);
#endif // _WIN64

    PLDR_DATA_TABLE_ENTRY pLdrDataTableEntry = 0;
    PEB_LDR_DATA* ldrTable= (PEB_LDR_DATA*)peb->Ldr;
    LIST_ENTRY* moduleList = &(ldrTable->InMemoryOrderModuleList);

    for (LIST_ENTRY* e = moduleList->Flink; e != &ldrTable->InMemoryOrderModuleList; e = e->Flink) {
        pLdrDataTableEntry = (PLDR_DATA_TABLE_ENTRY)e;

        wprintf(L"\nLib Name:\t%ls\n DllBase:\t%#x",  pLdrDataTableEntry->FullDllName.Buffer, pLdrDataTableEntry->DllBase);
    }
}
```



---

## Limitations & caveats

* **Local process only**: this PoC reads the PEB of the *current* process. To enumerate another process’ PEB you must use `ReadProcessMemory` (or NtReadVirtualMemory) on the target process, and you must handle differing address spaces and possible WOW64 redirection.
* **WOW64 complications**: when a 32-bit process runs under WOW64 on x64 Windows, the PEB layout / offsets differ; reading a 32-bit PEB from a 64-bit process (or vice versa) requires using the appropriate structs and offsets (and `Wow64` helper APIs).
* **ASLR & relocation**: module base addresses are randomized by ASLR; this PoC shows runtime bases, not compile-time values.
* **Undocumented fields**: `PEB`, `PEB_LDR_DATA` and `LDR_DATA_TABLE_ENTRY` are internal — field offsets may change across Windows versions. Use with caution.
* **Permissions**: you won't need extra privileges to read your own PEB, but to read another process you may need permissions and elevated rights depending on the target.
