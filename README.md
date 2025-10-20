# CS4348 Project 1 — Spring 2025

Three programs communicating via pipes:
- **logger** — reads stdin and appends `YYYY-MM-DD HH:MM [ACTION] MESSAGE` to a log file.
- **encrypt** — Vigenère backend. Commands: `PASS <key>`, `ENCRYPT <text>`, `DECRYPT <text>`, `QUIT`. Replies `RESULT ...` / `ERROR ...`.
- **driver** — interactive menu; launches the other two, wires pipes, logs start/commands/results/exit, and keeps per-run history (passwords **not** logged).

## Run (Windows)
```powershell
python src\driver\driver.py project.log
