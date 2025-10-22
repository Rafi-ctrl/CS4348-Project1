## 2025-10-19 16:18 – Initial planning
- Read project spec. Plan to implement three Python programs: logger, encrypt (Vigenère), driver.
- Driver will spawn two subprocesses and pipe stdin/stdout accordingly.
- Goals: letters-only validation, case-insensitive cipher, per-run history, masked password logging.

**Plan for this session**
- Set up repo structure `src/logger`, `src/crypto`, `src/driver`.
- Implement `logger.py` and a minimal `encrypt.py` skeleton.
- Prove the logging format matches spec.

## 2025-10-19 17:30 – Work session
- Implemented logger.py; tested manual writes; format matches YYYY-MM-DD HH:MM [ACTION] MESSAGE.
- Built encrypt.py with PASS/ENCRYPT/DECRYPT/QUIT; verified with manual session.
- Driver wired pipes; handled Windows pipe edge cases; added history + logging.
- Plan next: README + final test + submission artifacts.

**Work performed**
- **logger.py**: wrote timestamp helper; parse `[ACTION] MESSAGE` from a line; created parent dirs for logfile if needed; flush after each write.
- **encrypt.py**: implemented `letters_only`, `norm`, `vigenere(text, key, enc)`; command loop with `PASS/ENCRYPT/DECRYPT/QUIT` and required responses; `stdout.flush()` after every reply; verified:
  - `ENCRYPT HELLO` → `ERROR Password not set`
  - `PASS HELLO` → `RESULT`
  - `ENCRYPT HELLO` → `RESULT OIWWC`
  - `DECRYPT OIWWC` → `RESULT HELLO`

**Issues & fixes**
- Hit `OSError: [Errno 22] Invalid argument` on Windows when a child pipe closed → fixed by guarding writes and restarting the backend if needed.
- User input flow confusion (“0” at the “enter letters” prompt) → added clearer prompts + re-prompt loop.

**Results**
- End-to-end run works: set password → encrypt → decrypt → history → quit. Log file shows START/CMD/RESULT/EXIT lines.

**Next session**
- Polish README; add demo transcript and final devlog entry; push to GitHub; prepare submission zip.

## 2025-10-19 21:15 – Final reflection
- Verified end-to-end: password/encrypt/decrypt/history/quit.
- Errors for non-letters; passwords never logged.
- README added; repo cleaned; ready to zip and submit.
