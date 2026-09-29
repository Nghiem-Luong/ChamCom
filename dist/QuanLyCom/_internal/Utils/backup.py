from datetime import datetime
import shutil

from config import DATABASE_FILE, BACKUP_DIR


def tao_backup():
    """
    Sao lưu cơ sở dữ liệu QuanLyCom.db
    vào thư mục Backup.
    """

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            "Không tìm thấy cơ sở dữ liệu QuanLyCom.db."
        )

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    thoi_gian = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    ten_file_backup = (
        f"QuanLyCom_backup_{thoi_gian}.db"
    )

    duong_dan_backup = (
        BACKUP_DIR / ten_file_backup
    )

    shutil.copy2(
        DATABASE_FILE,
        duong_dan_backup
    )

    return duong_dan_backup


def khoi_phuc_backup(duong_dan_backup):
    """
    Khôi phục cơ sở dữ liệu từ file backup.

    Trước khi khôi phục sẽ tự động tạo
    một backup của cơ sở dữ liệu hiện tại.
    """

    duong_dan_backup = (
        BACKUP_DIR / duong_dan_backup
    )

    if not duong_dan_backup.exists():
        raise FileNotFoundError(
            "Không tìm thấy file backup."
        )

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            "Không tìm thấy cơ sở dữ liệu hiện tại."
        )

    # Backup CSDL hiện tại trước khi restore
    tao_backup()

    # Khôi phục dữ liệu
    shutil.copy2(
        duong_dan_backup,
        DATABASE_FILE
    )

    return DATABASE_FILE