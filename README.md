# Minecraft Server Auto-Updater
**Version 1.0**

A Python utility designed to keep your Minecraft server up-to-date with the latest official releases or snapshots from Mojang. It automates the entire update process: checking for new versions, safely stopping the server, backing up world data and the old server jar, downloading the new server executable, and restarting the server.

## Features

*   **Automatic Version Detection**: Checks Mojang's version manifest for the latest Release or Snapshot.
*   **Safe Updates**: Verifies file integrity using SHA1 hashes to ensure you only update when a new version is actually available.
*   **Automated Backups**:
    *   Backs up the current `minecraft_server.jar` before replacing it.
    *   Creates a timestamped backup of the `world` folder into `world_backups/` before applying updates.
*   **Process Management**: Automatically stops the running Java server process and restarts it using your startup script.

## Configuration

Open `MS_Update.py` and adjust the configuration variables at the top of the file to match your environment:

```python
UPDATE_TO_SNAPSHOT = False    # Set to True to update to snapshots
BACKUP_DIR = 'world_backups'  # Directory for world backups
SERVER_JAR = 'server.jar'     # Name of your server jar file
START_BATCH_FILE = 'run.bat'  # Your server startup script
```

## Usage

1.  **Install Dependencies**:
    ```bash
    pip install requests
    ```
2.  **Run the Script**:
    ```bash
    python MS_Update.py
    ```

## Warning
This script uses `TASKKILL /F /IM java.exe` to stop the server, which kills **all** running Java processes on the machine. Ensure this is safe for your server environment before running.
