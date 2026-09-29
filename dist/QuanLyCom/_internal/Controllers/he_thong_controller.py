from pathlib import Path
from datetime import datetime
import shutil

from Database.database import get_connection
from Models.audit_log_model import AuditLogModel


class HeThongController:

    @staticmethod
    def sao_luu_database():
        try:
            base_dir = Path(__file__).resolve().parent.parent

            database_path = (
                base_dir
                / "Data"
                / "QuanLyCom.db"
            )

            backup_folder = base_dir / "Backup"

            backup_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            if not database_path.exists():
                return {
                    "success": False,
                    "message": "Không tìm thấy database."
                }

            thoi_gian = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            backup_path = (
                backup_folder
                / f"QuanLyCom_{thoi_gian}.db"
            )

            shutil.copy2(
                database_path,
                backup_path
            )

            AuditLogModel.ghi_log(
                hanh_dong="SAO LƯU DATABASE",
                mo_ta=f"Sao lưu database: {backup_path.name}"
            )

            return {
                "success": True,
                "message": "Sao lưu database thành công.",
                "file_path": str(backup_path)
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể sao lưu: {error}"
            }

    @staticmethod
    def khoi_phuc_database(ten_file_backup):
        try:
            base_dir = Path(__file__).resolve().parent.parent

            database_path = (
                base_dir
                / "Data"
                / "QuanLyCom.db"
            )

            backup_folder = base_dir / "Backup"

            backup_path = (
                backup_folder
                / ten_file_backup
            )

            if not backup_path.exists():
                return {
                    "success": False,
                    "message": "Không tìm thấy file backup."
                }

            if not database_path.exists():
                return {
                    "success": False,
                    "message": "Không tìm thấy database hiện tại."
                }

            # Tạo backup database hiện tại trước khi khôi phục
            ket_qua_backup = (
                HeThongController.sao_luu_database()
            )

            if not ket_qua_backup["success"]:
                return {
                    "success": False,
                    "message": (
                        "Không thể tạo backup an toàn trước khi "
                        "khôi phục: "
                        + ket_qua_backup["message"]
                    )
                }

            # Khôi phục database
            shutil.copy2(
                backup_path,
                database_path
            )

            AuditLogModel.ghi_log(
                hanh_dong="KHÔI PHỤC DATABASE",
                mo_ta=(
                    f"Khôi phục database từ: "
                    f"{ten_file_backup}"
                )
            )

            return {
                "success": True,
                "message": (
                    "Khôi phục database thành công. "
                    "Vui lòng khởi động lại ứng dụng."
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": (
                    f"Không thể khôi phục database: {error}"
                )
            }

    @staticmethod
    def lay_audit_log():
        try:
            return {
                "success": True,
                "data": AuditLogModel.lay_tat_ca()
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy nhật ký: {error}",
                "data": []
            }

    @staticmethod
    def lay_audit_log_theo_hanh_dong(
        hanh_dong
    ):
        try:
            return {
                "success": True,
                "data": AuditLogModel.lay_theo_hanh_dong(
                    hanh_dong
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy nhật ký: {error}",
                "data": []
            }

    @staticmethod
    def thong_tin_he_thong():
        try:
            base_dir = Path(__file__).resolve().parent.parent

            database_path = (
                base_dir
                / "Data"
                / "QuanLyCom.db"
            )

            backup_folder = base_dir / "Backup"
            log_folder = base_dir / "Logs"

            return {
                "success": True,
                "data": {
                    "database_path": str(database_path),
                    "database_exists": database_path.exists(),
                    "backup_folder": str(backup_folder),
                    "log_folder": str(log_folder)
                }
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy thông tin hệ thống: {error}",
                "data": None
            }