import idaapi

def main():
	idaapi.msg_clear()
	idaapi.load_debugger("win32", 0)

	state = idaapi.get_process_state()

	match state:
		case idaapi.DSTATE_NOTASK:
			ea = idaapi.inf_get_main()
			if ea == idaapi.BADADDR:
				ea = idaapi.inf_get_start_ea()

			idaapi.run_to(ea)
			code = idaapi.wait_for_next_event(idaapi.WFNE_SUSP, -1)
			if code <= 0:
				return (False, "Failed to run main")

		case idaapi.DSTATE_SUSP:
			print(">>> Process is already suspended...")
		case idaapi.DSTATE_RUN:
			print(">>> Process is running, suspending it")
			idaapi.suspend_process()
			code = idaapi.wait_for_next_event(idaapi.WFNE_SUSP, -1)

	for _ in range(10):
		idaapi.step_into()
		code = idaapi.wait_for_next_event(idaapi.WFNE_SUSP | idaapi.WFNE_SUSP, -1)
		if code <- 0:
			return (False, "Failed to wait for next event")

		ev = idaapi.get_debug_event()
		if ev.eid() == idaapi.STEP:
			print(f">>> Step into: {ev.ea:x}")
		else:
			print(f">>> Event: {ev.eid()}")
			return (False, f"Failed to step into: {ev.eid}")
	
	idaapi.exit_process()
	code = idaapi.wait_for_next_event(idaapi.WFNE_CONT | idaapi.WFNE_SUSP, -1)
	if code == idaapi.PROCESS_EXITED:
		print(">>> Process exited")

	return (True, "Success")


if __name__ == "__main__":
	
	old_options = idaapi.set_debugger_options(
		idaapi.DOPT_TEMP_HWBPT | idaapi.DOPT_FAST_STEP)

	ok, msg = main()
	if not ok: 
		print(msg)

	idaapi.set_debugger_options(old_options)