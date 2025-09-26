# Frida — Quick README

A super-short reference for using **Frida** to instrument Windows binaries and trace API calls (JS hooks). Frida is a dynamic instrumentation toolkit that lets you inject JavaScript into running processes to intercept function calls, inspect/modify arguments and return values, and build interactive analysis workflows.

---

## Links

- Documentation with link to the typescript repo: [https://frida.re/docs/javascript-api/](https://frida.re/docs/javascript-api/)


## Install

```bash
pip install frida-tools
```

> Use matching `frida-server` on devices when attaching to Android/iOS targets. Ensure Frida host bindings and frida-server versions match.

---

## Example: trace `*ServiceA` APIs with `frida-trace`

**Command used in this example**:

```bash
frida-trace --decorate -i "*ServiceA" ./BadRentdrv2.exe 6666
```

**Script (handler) — example `CreateServiceA` handler**:

```js
defineHandler({
  onEnter(log, args, state) {
    log('CreateServiceA(' + args[0] +', '+ args[1].readCString() +', '+ args[2].readCString() +', '+ args[3] +', '+ args[4] +', '+ args[5] +', '+ args[6] +', '+ args[7].readCString() +', '+ args[8].readCString(), ') [ADVAPI32.dll]');
  },

  onLeave(log, retval, state) {
  }
});
```

---

## Sample output (what you should see)

```
frida-trace --decorate -i "*ServiceA" ./BadRentdrv2.exe 6666
Instrumenting...
StartServiceA: Loaded handler at "---\BadRentdrv2\BadRentdrv2\Release\__handlers__\ADVAPI32.dll\StartServiceA.js"
OpenServiceA: Loaded handler at "---\BadRentdrv2\BadRentdrv2\Release\__handlers__\ADVAPI32.dll\OpenServiceA.js"
CreateServiceA: Loaded handler at "---\BadRentdrv2\BadRentdrv2\Release\__handlers__\ADVAPI32.dll\CreateServiceA.js"
WSASetServiceA: Loaded handler at "---\BadRentdrv2\BadRentdrv2\Release\__handlers__\WS2_32.dll\WSASetServiceA.js"
OpenServiceA: Loaded handler at "---\BadRentdrv2\BadRentdrv2\Release\__handlers__\sechost.dll\OpenServiceA.js"
CreateServiceA: Loaded handler at "---\BadRentdrv2\BadRentdrv2\Release\__handlers__\sechost.dll\CreateServiceA.js"
StartServiceA: Loaded handler at "---\BadRentdrv2\BadRentdrv2\Release\__handlers__\sechost.dll\StartServiceA.js"
Hello World!
Started tracing 7 functions. Web UI available at http://localhost:50331/
[!] Driver is initialized !
[!] Kill process started !
[!] Kill process ended !
[!] Press any key to stop driver and clean up all POC files to avoid detection !
           /* TID 0x1e60 */
     0 ms  CreateServiceA(0xb6ec48, rentdrv2, rentdrv2, 0xf003f, 0x1, 0x1, 0x1, ---\BadRentdrv2\BadRentdrv2\Release\rentdrv2.sys, null ) [ADVAPI32.dll]
     0 ms     | CreateServiceA() [sechost.dll]
     0 ms  OpenServiceA() [ADVAPI32.dll]
     0 ms     | OpenServiceA()
     0 ms  StartServiceA() [ADVAPI32.dll]
     0 ms     | StartServiceA() [sechost.dll]
[!] All PoC files are cleaned !!
```

---

## Notes

* `frida-trace` auto-generates handler stubs under `__handlers__` when you instrument APIs. Customize them (JS) to log arguments in the shape you prefer.
* If you want a web UI, some community projects wrap Frida (e.g. House, FridaGUI). `frida-trace` itself may print a `Web UI available at` line when using certain versions or wrappers.

---

If you want, I can add more snippet examples (e.g., `DeviceIoControl` / `CreateFile` traces) or produce a ready-to-copy `myhooks.js` that logs CreateService / DeviceIoControl with argument parsing.