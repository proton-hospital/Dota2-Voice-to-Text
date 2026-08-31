# Dota 2 Voice-to-Text

Молниеносный инструмент автоматизации голосового чата без отрыва от геймплея, созданный для хай-ММР пабликов. Программа использует локальную нейросеть для распознавания речи и моментально отправляет текст в чат Доты, позволяя тебе не терять фокус на линии, ластхитах и микроконтроле.

[📺 Смотреть демонстрацию работы на YouTube](https://www.youtube.com/@ProtonDota2)

**Ключевые фишки:**
* **Никаких задержек и сбитого фокуса:** Сверхбыстрая эмуляция клавиатуры (~30 мс) сама открывает чат, вставляет текст и нажимает Enter, не ломая твой АПМ.
* **Локальный ИИ:** Работает на базе `faster-whisper` (напрямую через видеокарту). Распознает речь оффлайн и идеально понимает дотерский сленг.
* **Легкий интерфейс:** Простая настройка биндов, выбор нужного микрофона и переключение между общим/командным чатом в пару кликов.
* **Безопасно и легально:** Никакого внедрения в память игры, работает исключительно через стандартный Windows API (буфер обмена и нажатия клавиш). Не требует `sv_cheats` и абсолютно безопасно для VAC.
* **Звуковой отклик:** Опциональные микро-писки подскажут, когда запись началась и закончилась — отрывать взгляд от монитора больше не нужно.

**Как использовать (Для игроков):**
1. Перейди в раздел [Releases](../../releases) справа и скачай последний `.exe` файл.
2. Запусти программу (рекомендуется от имени Администратора, чтобы перехват кнопок работал поверх полноэкранной игры).
3. Нажми **Настройки ⚙️**, выбери свой микрофон, удобную кнопку активации и укажи папку с моделями Whisper.
4. В игре просто зажми кнопку, скажи инфу в микрофон и отпусти. Текст моментально улетит в чат.

**Сборка из исходников (Для энтузиастов и разработчиков):**
1. Склонируй репозиторий.
2. Установи зависимости: `pip install -r requirements.txt`
3. Запусти скрипт: `python vtt_proton.py`

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
