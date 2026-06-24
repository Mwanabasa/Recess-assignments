from pathlib import Path
import shutil
from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    source_dir: Path
    destination_dir: Path
    dry_run: bool = True

EXTENSION_MAP = {
    'Images': [".jpeg", ".jpg", ".png", ".svg"],
    'Documents': [".pdf", ".docx", ".txt"],
    'Videos': [".mp4", ".mkv", ".mov"],
    'Code': [".html", ".js", ".py", ".css"],
    'Archives': [".zip", ".rar", ".7z"],
    'Executables': [".exe", ".msi"]
}

def get_target_category(filepath: Path) -> str:
    ext = filepath.suffix.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return "Others"

def organize_files(config: Config):
    if not config.source_dir.exists():
        print(f"Source directory does not exist: {config.source_dir}")
        return

    for item in config.source_dir.iterdir():
        if item.is_file():
            category = get_target_category(item)
            target_folder = config.destination_dir / category
            target_folder.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            destination = target_folder / item.name

            if config.dry_run:
                print(f"[DRY RUN] {timestamp} → Would move: {item} → {destination}")
            else:
                shutil.move(str(item), str(destination))
                print(f"[MOVED] {timestamp} → {item.name} → {category}")

if __name__ == "__main__":
    downloads = Path.home() / "Downloads"
    organized_root = downloads / "Organized"

    config = Config(
        source_dir=downloads,
        destination_dir=organized_root,
        dry_run=False  # Change to True to test without moving files
    )

    organize_files(config)
