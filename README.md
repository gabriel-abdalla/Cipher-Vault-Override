# Cipher Vault Override

A Pygame entry inspired by Waterloo's "Worst Interface Challenge" — the goal isn't good UX, it's the opposite. The player has 60 seconds to enter a randomly generated 4-digit code, but the interface actively works against them.

## How it (deliberately badly) works

- A random 4-digit verification code is displayed on screen
- To enter each digit, the player must type the **English word** for that number (e.g. `one`, `two`) — but spelled using a randomly generated symbol cipher shown in a partially-redacted key table (some mappings are hidden behind `?`)
- A shuffled list of the correctly-ciphered number words is shown elsewhere on screen as a hint
- A 60-second countdown timer runs at all times; on timeout, the cipher, the code, and all progress reset and a new round begins
- A delete button removes the last accepted digit

## Requirements

- Python 3
- `pygame`
- `pygame_widgets`

## Running it

```bash
pip install pygame pygame_widgets
python worstinterface.py
```

## Design intent

The interface intentionally combines an unfamiliar cipher, incomplete information (redacted symbols), a strict time limit, and an indirect input method (spelling numbers instead of typing digits) to maximize player frustration while still being technically solvable — the whole point of the challenge.
