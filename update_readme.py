with open("README.md", "r") as f:
    content = f.read()

content = content.replace("**10 in PROGMEM gespeicherte WAV-Dateien**", "**30 in PROGMEM gespeicherte WAV-Dateien**")
content = content.replace("* **10 Integrierte PROGMEM Sounds:** Ding Dong, Trill Alarm, Sweep Sound, Solid Beep, G5 Chime, Siren, Doorbell, Notification, Error, Success.", "* **30 Integrierte PROGMEM Sounds:**\n  - **Standard:** Ding Dong, Trill Alarm, Sweep Sound, Solid Beep, G5 Chime, Siren, Doorbell, Notification, Error, Success.\n  - **Smart Home Eskalation:** Washing Machine, Mail Delivered, Window Open, Pre Alarm.\n  - **Sci-Fi / UI:** Access Granted, Cyberpunk, UI Click 1, UI Click 2, UI Click 3, Sci Fi Alert.\n  - **Retro Gaming:** Level Up, Game Over, Coin, Arcade Start.\n  - **Organisch & Specials:** Wood Knock, Glass Ping, Elevator Ding, Soft Bell, Magic Sparkle, Bass Drop.\n  (Alle 8000Hz, Mono, als Hex-Arrays integriert).")
content = content.replace('3. `select`: "Chime Ton" (Auswahl aus 10 Sounds).', '3. `select`: "Chime Ton" (Auswahl aus 30 Sounds).')
content = content.replace('6. `select`: "Alarm Ton" (Auswahl aus 10 Sounds).', '6. `select`: "Alarm Ton" (Auswahl aus 30 Sounds).')

with open("README.md", "w") as f:
    f.write(content)
