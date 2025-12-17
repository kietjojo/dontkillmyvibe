import speech_recognition as sr
from pynput.keyboard import Key, Controller, Listener
import time
from threading import Thread
import subprocess
import json
import os

# Load config từ file
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        return {'app_path': ''}
    except json.JSONDecodeError:
        print("❌ Invalid JSON in config file")
        return {'app_path': ''}

CONFIG = load_config()

class VoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.keyboard = Controller()
        self.running = False
        self.pressed_keys = set()
        self.last_alt_time = 0.0
        self.alt_tap_count = 0
        
        self.commands = {
            'save me': self.open_and_play,
            'play': self.play_pause,
            'stop': self.stop_media,
            'next song': self.next_media,
            'previous song': self.previous_media,
            'volume up': self.volume_up,
            'volume down': self.volume_down
        }
        
        self.keyboard_commands = {
            'p': self.play_pause,
            'n': self.next_media,
            'b': self.previous_media,
            'u': self.volume_up,
            'd': self.volume_down
        }
    
    def open_and_play(self):
        try:
            print(f"🚀 Opening: {CONFIG['app_path']}")
            subprocess.Popen(CONFIG['app_path'])
            time.sleep(2)  # Chờ app mở
            print("▶️ Playing...")
            self.keyboard.press(Key.media_play_pause)
            self.keyboard.release(Key.media_play_pause)
        except Exception as e:
            print(f"❌ Failed to open app: {e}")
    
    def play_pause(self):
        self.keyboard.press(Key.media_play_pause)
        self.keyboard.release(Key.media_play_pause)
    
    def stop_media(self):
        # Không có media stop key riêng, dùng play/pause
        self.keyboard.press(Key.media_play_pause)
        self.keyboard.release(Key.media_play_pause)
    
    def next_media(self):
        self.keyboard.press(Key.media_next)
        self.keyboard.release(Key.media_next)
    
    def previous_media(self):
        self.keyboard.press(Key.media_previous)
        self.keyboard.release(Key.media_previous)
    
    def volume_up(self):
        self.keyboard.press(Key.media_volume_up)
        self.keyboard.release(Key.media_volume_up)
    
    def volume_down(self):
        self.keyboard.press(Key.media_volume_down)
        self.keyboard.release(Key.media_volume_down)
    
    def listen(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                print("🎤 Listening...")
                # Nghe liên tục, bỏ time limit
                audio = self.recognizer.listen(source, timeout=None)
            
            print("🔄 Processing audio...")
            text = self.recognizer.recognize_google(audio, language='en-US').lower()
            print(f"📝 Detected: {text}")
            
            for command, action in self.commands.items():
                if command in text:
                    print(f"✅ Executing: {command}")
                    # Chạy action trong thread riêng, không block
                    Thread(target=action, daemon=True).start()
                    return
                
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
        except sr.RequestError as e:
            print(f"❌ API error: {e}")
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run(self):
        self.running = True
        print("🚀 Voice control started!")
        while self.running:
            try:
                self.listen()
            except Exception as e:
                print(f"❌ Run error: {e}")
    
    def stop(self):
        self.running = False
    
    def on_key_press(self, key):
        # Track pressed keys for modifier detection
        self.pressed_keys.add(key)

        # Alt double-tap -> Play/Pause
        if key in (Key.alt, Key.alt_l, Key.alt_r):
            now = time.time()
            if now - self.last_alt_time <= 0.4:
                self.alt_tap_count += 1
            else:
                self.alt_tap_count = 1
            self.last_alt_time = now

            if self.alt_tap_count >= 2:
                Thread(target=self.play_pause, daemon=True).start()
                print("Keyboard: Alt x2 -> Play/Pause")
                self.alt_tap_count = 0
            return

        # Alt-modified arrow hotkeys
        alt_pressed = bool(self.ppressed_alt_keys())
        if alt_pressed:
            if key == Key.up:
                Thread(target=self.volume_up, daemon=True).start()
                print("Keyboard: Alt+Up -> Volume up")
                return
            if key == Key.down:
                Thread(target=self.volume_down, daemon=True).start()
                print("Keyboard: Alt+Down -> Volume down")
                return
            if key == Key.right:
                Thread(target=self.next_media, daemon=True).start()
                print("Keyboard: Alt+Right -> Next song")
                return
            if key == Key.left:
                Thread(target=self.previous_media, daemon=True).start()
                print("Keyboard: Alt+Left -> Previous song")
                return

        # Single-letter fallbacks (no modifiers)
        try:
            if hasattr(key, 'char') and key.char in self.keyboard_commands:
                Thread(target=self.keyboard_commands[key.char], daemon=True).start()
                print(f"Keyboard: {key.char}")
        except Exception:
            pass

    def on_key_release(self, key):
        # Remove from pressed set when released
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def ppressed_alt_keys(self):
        # Helper to normalize alt detection (some keyboards report alt/alt_l/alt_r)
        return {Key.alt, Key.alt_l, Key.alt_r}.intersection(self.pressed_keys)

if __name__ == "__main__":
    controller = VoiceController()
    
    # Thread cho voice control
    thread = Thread(target=controller.run, daemon=True)
    thread.start()
    
    # Keyboard listener (track press + release)
    listener = Listener(on_press=controller.on_key_press, on_release=controller.on_key_release)
    listener.start()
    
    print("Voice control active. Keyboard control:")
    print("  Alt x2    - Play/Pause")
    print("  Alt+Up    - Volume up")
    print("  Alt+Down  - Volume down")
    print("  Alt+Right - Next song")
    print("  Alt+Left  - Previous song")
    print("  p/n/b/u/d - Legacy single-key shortcuts")
    print("Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()
        listener.stop()
        print("Stopped")