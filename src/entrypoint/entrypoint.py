import argparse
import subprocess
import sys

SCRIPT_BASE_PATH = "/root/src/src/src/entrypoint"


def parse_args():
    parser = argparse.ArgumentParser(description="Choose between API or Telegram UI")
    parser.add_argument("--api", action="store_true", help="Run API UI")
    return parser.parse_args()


def run_script(script_name: str):
    try:
        script_path = f"{SCRIPT_BASE_PATH}/{script_name}"
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")


if __name__ == "__main__":
    args = parse_args()

    if args.api:
        run_script("api_ui.py")
    else:
        run_script("telegram_ui.py")
