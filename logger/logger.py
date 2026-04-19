from datetime import datetime

def log(step):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs.txt", "a") as f:
        if step == "Starting Retrieval Planner Agent":
            f.write(f"\n[{timestamp}] {step}\n")
        else:
            f.write(f"[{timestamp}] {step}\n")
