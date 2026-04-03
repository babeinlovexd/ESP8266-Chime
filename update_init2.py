with open("components/esp8266_chime/__init__.py", "r") as f:
    content = f.read()

content = content.replace('"16. Cyberpunk"', '"16. Notification Chime"')
content = content.replace('"17. UI Click 1"', '"17. Notification Bloop"')
content = content.replace('"18. UI Click 2"', '"18. Notification Pop"')
content = content.replace('"19. UI Click 3"', '"19. Notification Sparkle"')
content = content.replace('"23. Wood Knock"', '"23. Notification Alert"')

with open("components/esp8266_chime/__init__.py", "w") as f:
    f.write(content)
