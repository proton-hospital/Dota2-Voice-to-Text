import os
import sys
import ctypes
import time
import re
import wave
import json
import threading
import tkinter as tk
from tkinter import ttk, filedialog
import pyaudio
import keyboard
import pydirectinput
from faster_whisper import WhisperModel
import pyperclip
import webbrowser
import winsound

# --- 1. АВТО-АДМИН ---
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# --- 2. РАБОТА С НАСТРОЙКАМИ ---
CONFIG_FILE = "settings.json"
DEFAULT_CONFIG = {
    "hotkey": "alt",
    "chat_mode": "Общий чат (Shift + Enter)", 
    "microphone": "По умолчанию",
    "model_dir": r"D:\WhisperModels",
    "model_size": "medium",
    "sound_enabled": True  # Новая настройка для звука
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

config = load_config()

for key in DEFAULT_CONFIG:
    if key not in config:
        config[key] = DEFAULT_CONFIG[key]

WAVE_OUTPUT_FILENAME = "temp_voice.wav"
model = None
app = None
log_text = None

def log(message):
    if log_text:
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)

def get_microphones():
    p = pyaudio.PyAudio()
    mics = ["По умолчанию"]
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            mics.append(info["name"])
    p.terminate()
    return mics

# --- 4. ЛОГИКА ЗАПИСИ И РАСПОЗНАВАНИЯ ---
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000  
    
    p = pyaudio.PyAudio()
    input_index = None
    
    if config["microphone"] != "По умолчанию":
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0 and info["name"] == config["microphone"]:
                input_index = i
                break
                
    if input_index is not None:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=input_index, frames_per_buffer=CHUNK)
    else:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    frames = []
    log("\n[🎙️] Запись пошла. Говори...")
    
    # Пищим только если стоит галочка
    if config.get("sound_enabled", True):
        winsound.Beep(1000, 100) 
    
    while keyboard.is_pressed(config["hotkey"]):
        data = stream.read(CHUNK)
        frames.append(data)
        
    if config.get("sound_enabled", True):
        winsound.Beep(800, 150)
        
    log("[✓] Запись завершена. Распознаю...")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def transcribe_audio():
    dota_slang = (
        "дота, мид, топ, бот, изи, хард, лейн, ганг, пуш, рошан, аегис, руна, сс, "
        "катка, репорт, крипы, деф, варды, сентри, смока, дасты, тп, тпшка, ботл, бкб, "
        "блинк, аганим, хекс, манта, тараска, рампага, фб, гг, вп, ггвп, энд, трон, "
        "хайграунд, хг, байбек, кура, глиф, фортифай, пауза, пинг, "
        "тинкер, сф, инвокер, пак, шторм, зевс, пудж, квопа, войд, ам, снайпер, врка, эмбер, "
        "стан, сало, сайленс, баш, рут, мисс, мана, хил, кд, кулдаун, ульта, "
        "афк, фид, смурф, бустер, руинер, анпауз, тавер, шрайн, лотус, здарова, лина, чё, лине, крипов, терзатель."
    )
    
    segments, info = model.transcribe(
        WAVE_OUTPUT_FILENAME, 
        beam_size=1, 
        language="ru", 
        vad_filter=True,
        initial_prompt=dota_slang
    )
    text = "".join([segment.text for segment in segments]).strip()
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def background_worker():
    global model
    log("Загрузка модели в память видеокарты... Подождите.")
    
    if os.path.exists(WAVE_OUTPUT_FILENAME):
        try: os.remove(WAVE_OUTPUT_FILENAME)
        except: pass
    
    try:
        model = WhisperModel(config["model_size"], device="cuda", compute_type="float16", download_root=config["model_dir"])
        log(f"Готово! Зажми [{config['hotkey'].upper()}] для записи.")
    except Exception as e:
        log(f"Ошибка загрузки модели: {e}")
        return

    while True:
        try:
            if keyboard.is_pressed(config["hotkey"]):
                record_audio()
                result = transcribe_audio()
                log(f"> Распознано: {result}")
                
                if result:
                    try:
                        pyperclip.copy(result)
                        pydirectinput.PAUSE = 0.01 
                        
                        if "Общий" in config.get("chat_mode", ""):
                            pydirectinput.keyDown('shift')
                            pydirectinput.press('enter')
                            pydirectinput.keyUp('shift')
                        else:
                            pydirectinput.press('enter')
                        
                        time.sleep(0.05)
                        
                        pydirectinput.keyDown('ctrl')
                        pydirectinput.press('v')
                        pydirectinput.keyUp('ctrl')
                        pydirectinput.press('enter')
                        
                        log("[✓] Текст влетел в чат!")
                    except Exception as e:
                        log(f"[!] Ошибка отправки: {e}")
                    
                if os.path.exists(WAVE_OUTPUT_FILENAME):
                    os.remove(WAVE_OUTPUT_FILENAME)
                    
            time.sleep(0.01) 
        except Exception as e:
            time.sleep(0.1)

# --- 5. ГРАФИЧЕСКИЙ ИНТЕРФЕЙС (GUI) ---
def open_settings():
    settings_win = tk.Toplevel(app)
    settings_win.title("Настройки")
    settings_win.geometry("550x330") # Увеличили высоту для галочки
    settings_win.resizable(False, False)
    settings_win.grab_set() 
    
    tk.Label(settings_win, text="Кнопка записи:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    hotkey_entry = tk.Entry(settings_win, width=25)
    hotkey_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    hotkey_entry.insert(0, config["hotkey"])
    
    hotkey_btn = tk.Button(settings_win, text="Задать кнопку", width=15)
    hotkey_btn.grid(row=0, column=2, padx=10, pady=10)
    
    def assign_hotkey():
        hotkey_btn.config(text="Жду нажатия...", state=tk.DISABLED)
        def listener():
            key = keyboard.read_key() 
            hotkey_entry.delete(0, tk.END)
            hotkey_entry.insert(0, key)
            hotkey_btn.config(text="Задать кнопку", state=tk.NORMAL)
        threading.Thread(target=listener, daemon=True).start()
        
    hotkey_btn.config(command=assign_hotkey)
    
    tk.Label(settings_win, text="Микрофон:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    mic_list = get_microphones()
    mic_cb = ttk.Combobox(settings_win, values=mic_list, width=38, state="readonly")
    mic_cb.grid(row=1, column=1, padx=10, pady=5, sticky="w", columnspan=2)
    mic_cb.set(config["microphone"] if config["microphone"] in mic_list else "По умолчанию")
    
    tk.Label(settings_win, text="Куда отправлять текст:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    chat_mode_cb = ttk.Combobox(settings_win, values=["Общий чат (Shift + Enter)", "Командный чат (Enter)"], width=38, state="readonly")
    chat_mode_cb.grid(row=2, column=1, padx=10, pady=5, sticky="w", columnspan=2)
    chat_mode_cb.set(config["chat_mode"])
    
    tk.Label(settings_win, text="Папка с моделями ИИ:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    model_entry = tk.Entry(settings_win, width=41)
    model_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w", columnspan=2)
    model_entry.insert(0, config["model_dir"])
    
    def browse_model():
        folderpath = filedialog.askdirectory(title="Выберите папку")
        if folderpath:
            model_entry.delete(0, tk.END)
            model_entry.insert(0, folderpath)
            
    tk.Button(settings_win, text="Обзор...", command=browse_model, width=15).grid(row=3, column=2, padx=10, pady=5, sticky="e")
    
    # --- Галочка для звука ---
    sound_var = tk.BooleanVar(value=config.get("sound_enabled", True))
    sound_cb = tk.Checkbutton(settings_win, text="Звуковое оповещение о записи", variable=sound_var)
    sound_cb.grid(row=4, column=0, columnspan=3, pady=5)
    
    # --- БЛОК АВТОРСТВА ---
    social_frame = tk.Frame(settings_win)
    social_frame.grid(row=5, column=0, columnspan=3, pady=5)
    
    yt_link = tk.Label(social_frame, text="▶️ YouTube", fg="#c4302b", font=("Arial", 10, "underline", "bold"), cursor="hand2")
    yt_link.pack(side=tk.LEFT, padx=15)
    yt_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.youtube.com/@ProtonDota2"))
    
    tg_link = tk.Label(social_frame, text="✈️ Telegram", fg="#0088cc", font=("Arial", 10, "underline", "bold"), cursor="hand2")
    tg_link.pack(side=tk.LEFT, padx=15)
    tg_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://t.me/proton_photon"))
    
    def save_and_close():
        config["hotkey"] = hotkey_entry.get().strip()
        config["microphone"] = mic_cb.get()
        config["chat_mode"] = chat_mode_cb.get() 
        config["model_dir"] = model_entry.get().strip()
        config["sound_enabled"] = sound_var.get()
        save_config(config)
        log(f"[⚙️] Сохранено! Кнопка: {config['hotkey'].upper()} | Звук: {'Вкл' if config['sound_enabled'] else 'Выкл'}")
        settings_win.destroy()
        
    tk.Button(settings_win, text="Сохранить", command=save_and_close, width=20, bg="#d9f0d3").grid(row=6, column=0, columnspan=3, pady=10)

def create_gui():
    global app, log_text
    app = tk.Tk()
    app.title("Dota 2 Voice-to-Text Chat by Proton")
    app.geometry("550x380")
    app.configure(bg="white")
    
    top_frame = tk.Frame(app, bg="white")
    top_frame.pack(fill=tk.X, padx=10, pady=10)
    
    settings_btn = tk.Button(top_frame, text="Настройки ⚙️", command=open_settings, font=("Arial", 10))
    settings_btn.pack(side=tk.RIGHT)
    
    tk.Label(top_frame, text="Лог работы:", bg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
    
    log_text = tk.Text(app, height=15, width=60, state=tk.DISABLED, bg="#f4f4f4", font=("Consolas", 10))
    log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    bottom_frame = tk.Frame(app, bg="white")
    bottom_frame.pack(fill=tk.X, padx=10, side=tk.BOTTOM, pady=5)
    tk.Label(bottom_frame, text="VTT by Proton", bg="white", fg="gray", font=("Arial", 8, "italic")).pack(side=tk.LEFT)
    
    worker_thread = threading.Thread(target=background_worker, daemon=True)
    worker_thread.start()
    
    app.mainloop()

if __name__ == "__main__":
    create_gui()
