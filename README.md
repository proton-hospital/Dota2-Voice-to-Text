# Dota 2 Voice-to-Text

A lightning-fast, zero-distraction voice chat automation tool designed for high-MMR Dota 2 gameplay. Built to ensure your focus stays entirely on the lane and your APM remains uninterrupted, this application uses local AI to transcribe your speech and injects it directly into the game chat in milliseconds. 

## Key Features
* **Zero-Interruption Execution:** Uses ultra-fast keyboard emulation to open chat, paste the transcribed text, and hit enter before you miss a single last hit.
* **Local AI Processing:** Powered by `faster-whisper` (running on your GPU) for highly accurate, offline transcription perfectly tuned to understand Dota 2 slang.
* **Lightweight GUI:** A simple interface to bind custom hotkeys, select your preferred microphone, and switch between All Chat and Allied Chat.
* **Safe & Legal:** Operates entirely via standard Windows API keyboard/clipboard emulation. No memory injection, no VAC risks.

## How to Use (For Players)
1. Go to the [Releases](../../releases) tab on the right and download the latest `.exe` file.
2. Run the application (Run as Administrator is recommended for keyboard hooks to work over the game).
3. Click **Settings ⚙️** to select your microphone, chat hotkey, and set the Whisper models folder.
4. Hold your hotkey in-game, speak, and release. The text will instantly appear in Dota 2 chat.

## Running from Source (For Developers)
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the script: `python voice_chat.py`
