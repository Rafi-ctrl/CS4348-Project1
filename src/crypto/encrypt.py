# encrypt.py — Vigenère backend over STDIN/STDOUT
# Commands: PASS <key> | ENCRYPT <text> | DECRYPT <text> | QUIT
# Responses: RESULT ... | ERROR ...
import sys

key = None

def letters_only(s: str) -> bool:
    return all(ch.isalpha() for ch in s)

def norm(s: str) -> str:
    # keep letters only, uppercase (case-insensitive)
    return "".join(ch.upper() for ch in s if ch.isalpha())

def vigenere(text: str, k: str, enc: bool) -> str:
    A = ord('A')
    T = norm(text)
    K = norm(k)
    out = []
    for i, ch in enumerate(T):
        p = ord(ch) - A
        shift = ord(K[i % len(K)]) - A
        c = (p + shift) % 26 if enc else (p - shift) % 26
        out.append(chr(A + c))
    return "".join(out)

def handle(cmd: str, arg: str):
    global key
    if cmd in ("PASS", "PASSKEY"):
        if not arg or not letters_only(arg):
            print("ERROR Passkey must contain letters only")
        else:
            key = arg
            print("RESULT")
    elif cmd == "ENCRYPT":
        if key is None:
            print("ERROR Password not set")
        elif not arg or not letters_only(arg):
            print("ERROR Input must be letters only")
        else:
            print("RESULT " + vigenere(arg, key, True))
    elif cmd == "DECRYPT":
        if key is None:
            print("ERROR Password not set")
        elif not arg or not letters_only(arg):
            print("ERROR Input must be letters only")
        else:
            print("RESULT " + vigenere(arg, key, False))
    else:
        print("ERROR Unknown command")
    sys.stdout.flush()

def main():
    for raw in sys.stdin:
        line = raw.rstrip("\n")
        if not line:
            continue
        if line == "QUIT":
            break
        parts = line.split(" ", 1)
        cmd = parts[0]
        arg = parts[1] if len(parts) == 2 else ""
        handle(cmd, arg)

if __name__ == "__main__":
    main()
