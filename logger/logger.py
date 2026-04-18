from datetime import datetime

def log(step):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs.txt", "a") as f:
        f.write(f"[{timestamp}] {step}\n")
