# Speakeasy — Quick notes (Mandiant Emulator)

**Speakeasy** is a lightweight Windows userspace emulator by Mandiant. It’s **especially useful for emulating shellcode and small programs** without running them on a live system—great for rapid triage, API tracing, and extracting IOCs.

---

## Why use it

* **Shellcode-first workflow:** feed raw bytes and see APIs resolved, memory mapped, and output artifacts (files/registry/network) *without* a VM.
* **Deterministic & fast:** step, re-run, and diff behavior quickly.
* **Rich telemetry:** logs Windows API calls, arguments, and buffers; optional artifact dumps.

---

## Quick start

```bash
# Install
git clone https://github.com/mandiant/speakeasy
cd speakeasy
python3 -m pip install -r requirements.txt
python3 setup.py install

# Emulate raw shellcode
speakeasy -r ./sc.bin --arch x64 

# Emulate a PE 
speakeasy -t ./sample.sys --arch x86
```

---

## References

* GitHub: **[mandiant/speakeasy](https://github.com/mandiant/speakeasy)**
