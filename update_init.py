with open("components/esp8266_chime/__init__.py", "r") as f:
    content = f.read()

old_options = 'options = ["1. Ding Dong", "2. Trill Alarm", "3. Sweep Sound", "4. Solid Beep", "5. G5 Chime", "6. Siren", "7. Doorbell", "8. Notification", "9. Error", "10. Success"]'
new_options = '''options = [
        "1. Ding Dong", "2. Trill Alarm", "3. Sweep Sound", "4. Solid Beep", "5. G5 Chime",
        "6. Siren", "7. Doorbell", "8. Notification", "9. Error", "10. Success",
        "11. Washing Machine", "12. Mail Delivered", "13. Window Open", "14. Pre Alarm", "15. Access Granted",
        "16. Cyberpunk", "17. UI Click 1", "18. UI Click 2", "19. UI Click 3", "20. Level Up",
        "21. Game Over", "22. Coin", "23. Wood Knock", "24. Glass Ping", "25. Elevator Ding",
        "26. Arcade Start", "27. Sci Fi Alert", "28. Soft Bell", "29. Magic Sparkle", "30. Bass Drop"
    ]'''

content = content.replace(old_options, new_options)

with open("components/esp8266_chime/__init__.py", "w") as f:
    f.write(content)
