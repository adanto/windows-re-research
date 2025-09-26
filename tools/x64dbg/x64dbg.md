# x64dbg 

A lightweight, open-source Windows debugger for x86/x64 with a clean UI, strong scripting, and great plugins. Perfect for reversing, exploit dev, and dynamic malware triage when you want fast breakpoints, memory inspection, patching, and trace recording.


---

## Useful tips

* **EntryPoint early break:** Options → Events → “Entry breakpoint” to catch initial setup/TLS.
* **Module filtering:** Right-click in CPU → “Follow in Memory Map” → choose your module to avoid kernel32/ntdll noise.
* **Conditional BPs:** Right-click BP → “Edit” → Condition (e.g., `RIP==0x140012345 || RAX==0`).
* **Logging:** Use `log "text {RIP} {RAX}"` in scripts; check **Log** tab.
* **Symbols:** Load PDBs (if available) via Symbols → “Download Symbols.”

---

## Tracing (record + script)

x64dbg supports instruction tracing and saving to a `.trace64` file. This is useful to **reproduce control-flow**, **diff iterations**, and **debug anti-debug paths**. Below is a compact script inspired by the FLARE 2024 “Serpentine” style: it records execution and, when it detects a `TEST r/m64, r64` (`48 85` or `4D 85`), it **forces ZF** to explore a specific branch, logging each iteration.

### How to run

1. In x64dbg, open **Scripts** tab.
2. Paste the script, adjust the two `bp` addresses and the output path.
3. Set your initial breakpoints (e.g., first `hlt`, return from `ExecuteHandlerForException`).
4. Click **Run** in the Scripts tab.

```
// Tip: Be at the first HLT and have a BP at ExecuteHandlerForException return.

// --- Adjust these addresses to your target ---
bp 00007FF92B2F517D        // ExecuteHandlerForException (call rax)
bp 0000000140001649        // call cs:ch09_shellcode_01stLayer
// --------------------------------------------

run
run
run
StepInto

StartTraceRecording "C:\temp\serpentine.short.trace64"

$testCount = 0
pause

loop:
    // Trace until next TEST r/m64,r64 at RIP (opcode starts with 48 85 or 4D 85)
    TraceIntoConditional 2:[rip] == 0x854D | 2:[rip] == 0x8548, 20

    // Detect TEST
    cmp 2:[rip], 0x854D
    je detectedTest
    cmp 2:[rip], 0x8548
    jne continueLoop

detectedTest:
    // Execute the TEST instruction itself
    log "[*] Finishing iteration {testCount} @ {i:rip}"
    TraceIntoConditional 0, 1

    // Force ZF = 1 (bit 6 of RFLAGS)
    $iterFlags = RFLAGS
    log "[*] RFLAGS before: {RFLAGS}"
    or $iterFlags, 0x40
    RFLAGS = $iterFlags
    log "[*] RFLAGS after:  {RFLAGS}"

    inc $testCount

continueLoop:
    cmp $testCount, 6      // adjust or remove limit
    je finish
jmp loop

finish:
StopTraceRecording
```
