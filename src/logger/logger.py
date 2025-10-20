# logger.py — reads lines from STDIN, writes timestamped lines to logfile
# Format: YYYY-MM-DD HH:MM [ACTION] MESSAGE
import sys, os
from datetime import datetime

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def parse_action_and_message(line: str) -> tuple[str, str]:
    stripped = line.strip()
    parts = stripped.split(maxsplit=1)
    if len(parts) == 1:
        return (parts[0], "")
    return (parts[0], parts[1])

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python logger.py <logfile>", file=sys.stderr)
        return 1

    log_file_path = sys.argv[1]
    parent = os.path.dirname(log_file_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            for raw_line in sys.stdin:
                line = raw_line.rstrip("\n")
                if not line.strip():
                    continue
                if line.strip().upper() == "QUIT":
                    break
                action, message = parse_action_and_message(line)
                action = (action or "INFO").upper()
                f.write(f"{ts()} [{action}] {message}\n")
                f.flush()
        return 0
    except Exception as e:
        print(f"ERROR: cannot write log file: {e}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
