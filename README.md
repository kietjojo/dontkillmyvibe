# DontKillMyVibe

Control your media player (MusicBee, Spotify, etc.) with voice commands and smart hotkeys.

---

- Reconfig the paths in `config.json` (Remember to write in correct format. Ask AI lol)

```json
{
  "app_path": "F:\\MusicBee\\MusicBee.exe",
  "icon_path": "D:\\Code\\Python\\dontkillmyvibe\\chikawa.ico"
}
```

- Then run `build.bat` to build the `exe`. It will be built in the folder `dist`

- If you want it to start when boot up:
  - Create a shortcut for the exe
  - Press `Ctrl + R`
  - Type `shell:startup` then press `Enter`
  - Put the shortcut there

## Feature
### Voice commands
- Save me: Open the app in `config.json` and play  
- Play music: Play/pause music
- Stop music: Stop music         
- Next song: Next song
- Previous song: Previous song
- Volume up: Volume up
- Volume down: Volume down

(pretty straight forward ik)

### Hotkeys
- CapsLock x2: Play/Pause
- Alt + Up Arrow: Volume up
- Alt + Down Arrow: Volume down
- Alt + Right Arrow: Next song
- Alt + Left Arrow: Previous song


