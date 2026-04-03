with open("README.md", "r") as f:
    content = f.read()

content = content.replace("Cyberpunk, UI Click 1, UI Click 2, UI Click 3", "Notification Chime, Notification Bloop, Notification Pop, Notification Sparkle")
content = content.replace("Wood Knock,", "Notification Alert,")

with open("README.md", "w") as f:
    f.write(content)
