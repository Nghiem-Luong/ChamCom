from pathlib import Path


# Thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent


# Cơ sở dữ liệu
DATABASE_DIR = BASE_DIR / "Data"
DATABASE_FILE = DATABASE_DIR / "QuanLyCom.db"


# Thư mục backup
BACKUP_DIR = BASE_DIR / "Backup"


# Tạo thư mục nếu chưa tồn tại
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True
)