# PRIMEXARMY.py
import secrets, string, hashlib, sys, socket, getpass, urllib.request, urllib.parse
from datetime import datetime, timedelta
from colorama import Fore, init
import pyfiglet

# Init colorama
init(autoreset=True)

# ================== CONFIG ==================
VERSION = "v1.0"
ADMIN_USERNAME = "@your_admin"
CHANNEL_USERNAME = "@your_channel"
MADE_BY = "🔥 PRIMEXARMY 🔥"
OWNER = "# PRIMEXARMY111"
KEYS_FILE = "keys.txt"

# Tamper lock — FIRST RUN prints hash; paste it here and re-run
EXPECTED_HASH = "TO_BE_FILLED"

# Optional Telegram notify (silent usage log)
BOT_TOKEN = ""      # e.g. 123456:ABC-DEF...
CHAT_ID = ""        # your user/channel/group chat_id
# ============================================

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def check_integrity():
    current_hash = sha256_file(__file__)
    if EXPECTED_HASH == "TO_BE_FILLED":
        print(Fore.YELLOW + "🔒 First-time setup detected.")
        print(Fore.CYAN + f"Paste this into EXPECTED_HASH: {current_hash}")
        sys.exit(0)
    if current_hash != EXPECTED_HASH:
        print(Fore.RED + "❌ File integrity check failed! Unauthorized changes detected.")
        sys.exit(1)

def silent_notify(msg: str):
    if not BOT_TOKEN or not CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": msg}).encode()
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=5).read()
    except Exception:
        # stay silent
        pass

# -------------------- Banner --------------------
def banner():
    ascii_banner = pyfiglet.figlet_format("PRIMEXARMY")
    print(Fore.RED + ascii_banner)
    print(Fore.YELLOW + f"🚀 Stylish Key Generator {VERSION} 🚀")
    print(Fore.CYAN + "════════════════════════════════════\n")

# -------------------- Key Generator --------------------
def generate_key(expiry_hours: int):
    alphabet = string.ascii_letters + string.digits
    raw = ''.join(secrets.choice(alphabet) for _ in range(24))
    key = f"PRIMEXARMY_DAY_{raw}"
    expiry_time = datetime.now() + timedelta(hours=expiry_hours)
    # Save key with Admin + Channel info
    with open(KEYS_FILE, "a") as f:
        f.write(f"{key} | Expiry: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')} | Admin: {ADMIN_USERNAME} | Channel: {CHANNEL_USERNAME}\n")
    return key, expiry_time

# -------------------- Menu --------------------
def menu():
    options = {
        "1": ("1 Hour", 1),
        "2": ("5 Hours", 5),
        "3": ("1 Day", 24),
        "4": ("3 Days", 72),
        "5": ("5 Days", 120),
        "6": ("30 Days", 720)
    }
    print(Fore.MAGENTA + "Select Key Validity:")
    for k, (label, _) in options.items():
        print(Fore.YELLOW + f"  {k}. {label}")
    print()
    choice = input(Fore.CYAN + ">> Choose option: ").strip()
    if choice in options:
        label, hours = options[choice]
        key, expiry = generate_key(hours)
        print(Fore.GREEN + f"\n✅ Generated Key ({label}): {key}")
        print(Fore.CYAN + f"⏳ Expiry: {expiry.strftime('%Y-%m-%d %H:%M:%S')}")
        print(Fore.YELLOW + f"💾 Saved to {KEYS_FILE}\n")
    else:
        print(Fore.RED + "❌ Invalid choice")

# -------------------- Main --------------------
def main():
    check_integrity()
    # hidden usage notice
    user = getpass.getuser()
    host = socket.gethostname()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    silent_notify(f"🔔 PRIMEXARMY used by {user}@{host} at {now}")
    banner()
    print(Fore.YELLOW + f"Admin: {ADMIN_USERNAME} | Channel: {CHANNEL_USERNAME}")
    print(Fore.CYAN + "════════════════════════════════════\n")
    while True:
        menu()
        again = input(Fore.MAGENTA + "Generate another key? (y/n): ").lower()
        if again != "y":
            print(Fore.RED + "\n🛑 Exiting PRIMEXARMY Key Generator...")
            break

if __name__ == "__main__":
    main()
