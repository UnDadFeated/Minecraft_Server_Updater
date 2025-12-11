import os
import time
import shutil
import hashlib
import subprocess
import logging
import requests
from datetime import datetime

# CONFIGURATION
UPDATE_TO_SNAPSHOT = False
MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
BACKUP_DIR = 'world_backups'
JARBACKUP_DIR = 'previous_jars'
LOG_FILENAME = 'Update_Log.log'
SERVER_JAR = 'minecraft_server.jar'
START_BATCH_FILE = 'Manual_Run.bat'
VERSION_FILE = 'version_info.txt'

# Setup Logging
logging.basicConfig(
    filename=LOG_FILENAME, 
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_remote_version_info(update_to_snapshot):
    """Retrieves the latest version info from Mojang."""
    try:
        response = requests.get(MANIFEST_URL)
        response.raise_for_status()
        data = response.json()
        
        if update_to_snapshot:
            minecraft_ver = data['latest']['snapshot']
        else:
            minecraft_ver = data['latest']['release']
            
        for version in data['versions']:
            if version['id'] == minecraft_ver:
                return minecraft_ver, version['url']
        return None, None
    except Exception as e:
        logging.error(f"Failed to retrieve version manifest: {e}")
        return None, None

def get_local_sha1(filename):
    """Calculates SHA1 of a local file efficiently."""
    if not os.path.exists(filename):
        return ""
    
    sha = hashlib.sha1()
    try:
        with open(filename, 'rb') as f:
            while chunk := f.read(65536):
                sha.update(chunk)
        return sha.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating SHA1 for {filename}: {e}")
        return ""

def get_current_version_name(local_sha):
    """Retrieves the cached version name, falling back to truncated SHA."""
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, 'r') as f:
                return f.read().strip()
        except:
            pass
    
    return f"Unknown (SHA: {local_sha[:7]})" if local_sha else "None"

def save_current_version_name(version_name):
    """Saves the current version name to file."""
    try:
        with open(VERSION_FILE, 'w') as f:
            f.write(str(version_name))
    except Exception as e:
        logging.error(f"Failed to save version info: {e}")

def stop_server():
    """Stops the Minecraft server."""
    logging.info('Stopping server...')
    print('Stopping server...')
    # WARNING: This kills ALL java processes. Ensure no other Java apps are running.
    # In a production environment, you should use RCON or send a stop command to the screen session.
    os.system("TASKKILL /F /IM java.exe")
    time.sleep(3)

def backup_server_jar(current_sha):
    """Backs up the current server jar."""
    if not os.path.exists(JARBACKUP_DIR):
        os.makedirs(JARBACKUP_DIR)

    backup_path = os.path.join(JARBACKUP_DIR, f"minecraft_server_sha={current_sha}.jar")
    try:
        shutil.copy(SERVER_JAR, backup_path)
        logging.info(f"Backed up {SERVER_JAR} to {backup_path}")
    except Exception as e:
        logging.error(f"Failed to backup server jar: {e}")

def download_server_jar(url):
    """Downloads the server jar from the given URL."""
    logging.info(f'Downloading {SERVER_JAR} from {url}...')
    print(f'Downloading {SERVER_JAR} from {url}...')
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(SERVER_JAR, 'wb') as jar_file:
            jar_file.write(response.content)
        logging.info('Downloaded successfully.')
        print('Downloaded successfully.')
        return True
    except Exception as e:
        logging.error(f"Failed to download server jar: {e}")
        print(f"Failed to download server jar: {e}")
        return False

def backup_world(current_sha):
    """Backs up the world directory."""
    if not os.path.exists('world'):
        logging.warning("No 'world' folder found to backup.")
        return

    logging.info('Backing up world...')
    print('Backing up world...')
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().isoformat().replace(':', '-')
    backup_name = f"world_backup_{timestamp}_sha={current_sha}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    try:
        shutil.copytree("world", backup_path)
        logging.info('Backed up world.')
        print('Backed up world.')
    except Exception as e:
        logging.error(f"Failed to backup world: {e}")
        print(f"Failed to backup world: {e}")

def start_server():
    """Starts the Minecraft server."""
    logging.info('Starting server...')
    print('Starting server...')
    logging.info('=' * 78)
    
    if os.path.exists(START_BATCH_FILE):
        # Uses 'start' to run in a separate window/process
        os.system(f'start call {START_BATCH_FILE}')
    else:
        logging.error(f"Startup script {START_BATCH_FILE} not found!")
        print(f"Startup script {START_BATCH_FILE} not found!")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    target_ver, json_url = get_remote_version_info(UPDATE_TO_SNAPSHOT)
    if not target_ver or not json_url:
        print("Could not retrieve version info.")
        return

    try:
        jar_data = requests.get(json_url).json()
        remote_sha = jar_data['downloads']['server']['sha1']
        download_url = jar_data['downloads']['server']['url']
    except Exception as e:
        logging.error(f"Failed to get jar info: {e}")
        return

    local_sha = get_local_sha1(SERVER_JAR)

    if local_sha != remote_sha:
        current_version_name = get_current_version_name(local_sha)
        
        logging.info('Update Found.')
        print('=' * 78)
        print('Update Found.')
        print()
        
        msg = f"Update available: Upgrading from version '{current_version_name}' to '{target_ver}'."
        sha_msg = f"(SHA: {local_sha[:7]}... -> {remote_sha[:7]}...)"
        
        logging.info(msg)
        logging.info(sha_msg)
        print(msg)
        print(sha_msg)
        print('=' * 78)
        time.sleep(1)

        print('Updating server...')
        time.sleep(3)

        stop_server()
        
        if local_sha: # Only backup if we actually have a file
            backup_server_jar(local_sha)
        
        if download_server_jar(download_url):
            backup_world(local_sha)
            save_current_version_name(target_ver)
            start_server()
        else:
            print("Update failed during download. Server not restarted.")
            logging.error("Update failed during download.")

    else:
        print("Server Isn't running or Server is already up to date.")
        print(f'Latest version is {target_ver}')
        time.sleep(5)

if __name__ == "__main__":
    main()
