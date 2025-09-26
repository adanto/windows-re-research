# SystemInformer: PHNT 

Short summary: **PHNT** is a collection of modern, community-maintained Windows headers that expose the NT-internals types, enums and APIs (PEB/TEB, NTSTATUS, native syscall prototypes, RTL structures, etc.) in a safe, consistent and versioned way. For security researchers and PoC authors it’s invaluable because it lets you *compile against the same hidden structures you read and modify at runtime* instead of reinventing fragile struct layouts, magic offsets, or hand-rolled typedefs.

---

# PHNT — what it is

PHNT (short for *Public Headers for NT internals*) provides:

* Carefully defined Windows NT types (PEB, TEB, RTL structures) with correct packing and conditional compilation for x86/x64.
* Prototypes for undocumented or partially documented functions (e.g. `NtQueryInformationProcess`, `RtlNtStatusToDosError`, `NtOpenProcess`, `NtReadVirtualMemory`).
* NT constants and `NTSTATUS` helpers so your code compiles cleanly and is easier to maintain across Windows versions.

Why use PHNT instead of copying random headers:

* Version correctness: PHNT maintainers track subtle layout changes that break naive PoCs.
* Clear names and typedefs reduce bugs (no guessing pointer offsets).
* Fewer defines/compat hacks in your source — your PoC focuses on logic, not header fights.

---

# Why PHNT is useful for security PoCs

Security PoCs often need to interact with Windows internals that are not part of the Win32 API surface:

* Inspecting a target process’ PEB/ProcessParameters (command line, image path).
* Reading native handles, loader lists, or subtle flags like `BeingDebugged`.
* Calling native APIs for speed or to bypass higher-level restrictions.

Using PHNT you can:

* Reliably declare `PEB`, `PEB_LDR_DATA`, `PRTL_USER_PROCESS_PARAMETERS`, `PROCESS_BASIC_INFORMATION`.
* Call `NtQueryInformationProcess` to get the PEB address and then `ReadProcessMemory` to copy exact typed structures.
* Avoid custom bit/byte errors by reusing tested struct definitions.


---

# Remote-PEB inspector (PoC)

[This repo](https://github.com/adanto/remote-PEB) contains a compact PoC called [**remote-PEB**](https://github.com/adanto/remote-PEB) that demonstrates using PHNT to enumerate running processes and print:

* CommandLine (from `RTL_USER_PROCESS_PARAMETERS`)
* ImagePathName
* `BeingDebugged`
* `ImageBaseAddress`
* `OSMajorVersion`, `OSMinorVersion`, `OSBuildNumber`, `OSCSDVersion`
