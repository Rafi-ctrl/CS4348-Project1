# driver.py — launches logger & encrypt backends, connects pipes, interactive menu
import sys, subprocess, os

MENU = """
Commands:
  password  - set passkey (letters only)
  encrypt   - encrypt a string (letters only)
  decrypt   - decrypt a string (letters only)
  history   - show history (this run only)
  quit      - exit
"""

def letters_only(s: str) -> bool:
    return all(ch.isalpha() for ch in s)

# Resolve paths so the driver works no matter where it's launched from
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", ".."))
LOGGER_PATH = os.path.join(ROOT_DIR, "src", "logger", "logger.py")
CRYPTO_PATH = os.path.join(ROOT_DIR, "src", "crypto", "encrypt.py")

def start_logger(logfile):
    return subprocess.Popen(
        [sys.executable, LOGGER_PATH, logfile],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True
    )

def start_crypto():
    return subprocess.Popen(
        [sys.executable, CRYPTO_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

def ensure_crypto(p_crypto):
    # restart the backend if it exited
    if p_crypto is None or p_crypto.poll() is not None:
        return start_crypto()
    return p_crypto

def log(p_logger, action, message=""):
    """Best-effort logging: never crash if logger pipe is closed."""
    if not p_logger or not p_logger.stdin:
        return
    try:
        line = action if not message else f"{action} {message}"
        p_logger.stdin.write(line + "\n")
        p_logger.stdin.flush()
    except (BrokenPipeError, OSError, ValueError):
        pass

def send_crypto(p_crypto, line):
    # safe write/read; if child died return an error marker
    try:
        p_crypto.stdin.write(line + "\n")
        p_crypto.stdin.flush()
        out = p_crypto.stdout.readline()
        if not out:
            raise BrokenPipeError("no output from backend")
        return out.rstrip("\n")
    except (BrokenPipeError, OSError, ValueError):
        return "ERROR backend unavailable"

def pick_from_history(history, prompt):
    if not history:
        print("History is empty.")
        return None
    while True:
        print("\nHistory:")
        for i, s in enumerate(history, 1):
            print(f"  {i}) {s}")
        print("  0) Enter a new string")
        choice = input(f"{prompt} [0..{len(history)}]: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                return None
            if 1 <= idx <= len(history):
                return history[idx-1]
        print("Invalid choice.")

def main():
    if len(sys.argv) != 2:
        print("usage: python src\\driver\\driver.py <logfile>")
        sys.exit(1)
    logfile = sys.argv[1]

    p_logger = start_logger(logfile)
    p_crypto = start_crypto()
    history = []

    try:
        log(p_logger, "START", "Driver started")

        while True:
            print(MENU)
            cmd = input("Enter command: ").strip().lower()

            if cmd == "password":
                existing = pick_from_history(history, "Select a history string for password or 0 for new")
                pw = existing if existing is not None else input("Enter passkey (letters only): ").strip()
                if not pw or not letters_only(pw):
                    print("Error: letters only.")
                    log(p_logger, "ERROR", "Invalid password input")
                    continue
                log(p_logger, "CMD", "password ****")  # never log plaintext
                p_crypto = ensure_crypto(p_crypto)
                resp = send_crypto(p_crypto, f"PASS {pw}")
                if resp == "ERROR backend unavailable":
                    # try once more by restarting
                    p_crypto = ensure_crypto(p_crypto)
                    resp = send_crypto(p_crypto, f"PASS {pw}")
                print(resp)
                if resp.startswith("RESULT"):
                    log(p_logger, "RESULT", "password set")
                else:
                    # log only the message part if it begins with ERROR
                    msg = resp.split(" ", 1)[1] if resp.startswith("ERROR ") else resp
                    log(p_logger, "ERROR", msg)

            elif cmd == "encrypt":
                existing = pick_from_history(history, "Select a history string to encrypt or 0 for new")
                if existing is None:
                    # re-prompt until letters-only
                    while True:
                        s = input("Enter letters to encrypt: ").strip()
                        if s and letters_only(s):
                            history.append(s)
                            break
                        print("Error: letters only. Try again.")
                        log(p_logger, "ERROR", "encrypt invalid input")
                else:
                    s = existing

                log(p_logger, "CMD", "encrypt")
                p_crypto = ensure_crypto(p_crypto)
                resp = send_crypto(p_crypto, f"ENCRYPT {s}")
                if resp == "ERROR backend unavailable":
                    p_crypto = ensure_crypto(p_crypto)
                    resp = send_crypto(p_crypto, f"ENCRYPT {s}")
                print(resp)
                if resp.startswith("RESULT "):
                    result = resp.split(" ", 1)[1]
                    history.append(result)
                    log(p_logger, "RESULT", f"encrypt -> {result}")
                else:
                    msg = resp.split(" ", 1)[1] if resp.startswith("ERROR ") else resp
                    log(p_logger, "ERROR", msg)

            elif cmd == "decrypt":
                existing = pick_from_history(history, "Select a history string to decrypt or 0 for new")
                if existing is None:
                    # re-prompt until letters-only
                    while True:
                        s = input("Enter letters to decrypt: ").strip()
                        if s and letters_only(s):
                            history.append(s)
                            break
                        print("Error: letters only. Try again.")
                        log(p_logger, "ERROR", "decrypt invalid input")
                else:
                    s = existing

                log(p_logger, "CMD", "decrypt")
                p_crypto = ensure_crypto(p_crypto)
                resp = send_crypto(p_crypto, f"DECRYPT {s}")
                if resp == "ERROR backend unavailable":
                    p_crypto = ensure_crypto(p_crypto)
                    resp = send_crypto(p_crypto, f"DECRYPT {s}")
                print(resp)
                if resp.startswith("RESULT "):
                    result = resp.split(" ", 1)[1]
                    history.append(result)
                    log(p_logger, "RESULT", f"decrypt -> {result}")
                else:
                    msg = resp.split(" ", 1)[1] if resp.startswith("ERROR ") else resp
                    log(p_logger, "ERROR", msg)

            elif cmd == "history":
                if not history:
                    print("(empty)")
                else:
                    print("History:")
                    for i, s in enumerate(history, 1):
                        print(f"  {i}) {s}")
                log(p_logger, "CMD", "history")
                log(p_logger, "RESULT", f"history count {len(history)}")

            elif cmd == "quit":
                log(p_logger, "CMD", "quit")
                try:
                    p_crypto.stdin.write("QUIT\n"); p_crypto.stdin.flush()
                except Exception:
                    pass
                try:
                    p_logger.stdin.write("QUIT\n"); p_logger.stdin.flush()
                except Exception:
                    pass
                print("Goodbye!")
                log(p_logger, "EXIT", "Driver exiting")
                break

            else:
                print("Unknown command.")
                log(p_logger, "ERROR", f"Unknown command '{cmd}'")
    finally:
        for p in (p_crypto, p_logger):
            if p:
                try:
                    p.wait(timeout=1)
                except Exception:
                    try:
                        p.kill()
                    except Exception:
                        pass

if __name__ == "__main__":
    main()
