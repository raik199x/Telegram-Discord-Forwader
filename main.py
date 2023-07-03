import sys
import yaml
from Bot.telegram.botRunner import start_telegram_client
from Bot.shared.variables import DirectoryTempFiles
from os import path
from shutil import rmtree


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
        sys.exit(1)

    with open(sys.argv[1], 'rb') as f:
        config = yaml.safe_load(f)

    if path.exists(DirectoryTempFiles):
        rmtree(DirectoryTempFiles)

    start_telegram_client(config)
