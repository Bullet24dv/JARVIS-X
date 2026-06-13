import requests

def check():
    try:
        r = requests.get("http://localhost:8000/health", timeout=5)
        if r.status_code == 200:
            print("✅ JARVIS-X is healthy")
        else:
            print("❌ JARVIS-X is unhealthy")
    except:
        print("❌ Cannot connect to JARVIS-X")

if __name__ == "__main__":
    check()