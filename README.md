# Minecraft Server Updater & Installer
**Version 2.0** | **Author: UnDadFeated**

A generic Python utility designed to **Install**, **Update**, and **Manage** your Minecraft server. It supports **Windows & Linux**, and works with **Vanilla**, **Forge**, and **NeoForge** servers.

## Key Features

*   **Dual Mode: Installer & Updater**
    *   **Installation**: Automatically detects if the server is missing and walks you through a clean install.
    *   **Updates**: Checks Mojang's version manifest to keep your Vanilla server up-to-date.
*   **Operating System Support**:
    *   **Windows**: Auto-installs to your chosen directory.
    *   **Linux**: Auto-installs to `/home/{username}/MCServer/`.
*   **Multi-Loader Support**:
    *   **Vanilla**: Auto-download and version matching.
    *   **Forge & NeoForge**: Installer support (prompts for direct URL) and **Safe Update Protection** (avoids breaking modded servers).
*   **Smart Dependencies**:
    *   Checks for the correct Java version (Java 8, 16, 17, 21) based on the Minecraft version.
    *   Auto-Generates `eula.txt` and startup scripts (`Manual_Run.bat` / `Manual_Run.sh`).
*   **Automated Backups**:
    *   Safe backups of `minecraft_server.jar` and the `world` folder before any major operations.

## Configuration

Open `MS_Update.py` to adjust optional settings:

```python
UPDATE_TO_SNAPSHOT = False    # Set to True to update to snapshots (Vanilla only)
BACKUP_DIR = 'world_backups'
SERVER_JAR = 'minecraft_server.jar'
START_BATCH_FILE = 'Manual_Run.bat'
```

## Usage

1.  **Install Dependencies**:
    ```bash
    pip install requests
    ```
2.  **Run the Tool**:
    ```bash
    python MS_Update.py
    ```
    *   *If no server is found*: It will launch the **Installer** wizard.
    *   *If a server is found*: It will check for **Updates** (Vanilla) or ensure the server starts (Modded).

## Warning
The script uses OS-specific commands (`TASKKILL` on Windows, `pkill` on Linux) to stop the server before updates. Ensure this is safe for your environment.
