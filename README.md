# CS4348 Project 1 — Spring 2025

Three programs communicating via pipes:
- **logger** — reads stdin and appends `YYYY-MM-DD HH:MM [ACTION] MESSAGE` to a log file.
- **encrypt** — Vigenère backend. Commands: `PASS <key>`, `ENCRYPT <text>`, `DECRYPT <text>`, `QUIT`. Replies `RESULT ...` / `ERROR ...`.
- **driver** — interactive menu; launches the other two, wires pipes, logs start/commands/results/exit, and keeps per-run history (passwords **not** logged).

## Run (Windows)
```powershell
python src\driver\driver.py project.log
```
## Commands & Rules
```
password  - set passkey (letters only)
encrypt   - encrypt a string (letters only)
decrypt   - decrypt a string (letters only)
history   - show history (this run only)
quit      - exit
```
## Quick Example
```
password
0  ---> Letters only 
HELLO   ---> RESULT 
encrypt
0
HELLO
decrypt
2
history
quit
```
## Check Log
```
notepad project.log
```
You should see lines like
```
YYYY-MM-DD HH:MM [START] Driver started
YYYY-MM-DD HH:MM [CMD] password ****
YYYY-MM-DD HH:MM [RESULT] password set
YYYY-MM-DD HH:MM [CMD] encrypt
YYYY-MM-DD HH:MM [RESULT] encrypt -> OIWWC
YYYY-MM-DD HH:MM [EXIT] Driver exiting
```
## Layout
```
src/logger/logger.py
src/crypto/encrypt.py
src/driver/driver.py
```
### .gitignore
```
__pycache__/
*.pyc
.venv/
project.log
demo_output.txt
```
