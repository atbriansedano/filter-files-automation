from pathlib import Path
from datetime import date
import shutil

def get_file_paths(monitored_paths: list):

    file_paths = []

    for current_path in monitored_paths:
        root_path = Path(current_path)
        file_paths.extend([current_file for current_file in root_path.iterdir() if current_file.is_file()])
        
    return file_paths

def move_files(file_paths: list, move_to_path: Path, is_date_subfolder: bool, is_extension_subfolder: bool):

    for current_path in file_paths:
        destination_path = move_to_path
        if is_extension_subfolder:
            extension = current_path.suffix.lstrip('.').upper() or 'NA'
            destination_path = destination_path / extension
        if is_date_subfolder:
            destination_path = destination_path / date.today().isoformat()

        destination_path.mkdir(parents=True, exist_ok=True)
        destination_path = destination_path / current_path.name
        shutil.move(str(current_path), str(destination_path))

def main():
    #Get the file path to monitor from the user
    #Get all files from the paths specified by the user
    monitor_paths = []

    monitor_path = Path.home() / "Downloads"
    monitor_paths.append(monitor_path)

    move_to_path = downloads_dir = Path.home() / "Documents/File Automation" 
    file_paths = get_file_paths(monitor_paths)
    move_files(file_paths, move_to_path, 1, 1)


if __name__ == '__main__':
    main()