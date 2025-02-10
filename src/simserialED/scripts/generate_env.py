from pathlib import Path
ROOT = Path(__file__).parent.parent

def generate_secret():
    import secrets
    env_file = ROOT / ".env"
    if env_file.exists():
        return
    with open(env_file, "w") as f:
        f.write(f"FLASK_SECRET_KEY={secrets.token_hex()}\n")


def main():
    generate_secret()

if __name__ == "__main__":
    main()
    