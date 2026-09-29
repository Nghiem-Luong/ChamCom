from datetime import datetime
from Database.database import get_connection


class AuditLogModel:

    @staticmethod
    def ghi_log(
        hanh_dong,
        mo_ta=None,
        nguoi_thao_tac="Chính tôi"
    ):
        if not hanh_dong:
            raise ValueError("Hành động không được để trống.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO AuditLog (
                    ThoiGian,
                    HanhDong,
                    MoTa,
                    NguoiThaoTac
                )
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                hanh_dong,
                mo_ta,
                nguoi_thao_tac
            ))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    @staticmethod
    def lay_tat_ca():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    ThoiGian,
                    HanhDong,
                    MoTa,
                    NguoiThaoTac
                FROM AuditLog
                ORDER BY Id DESC
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_theo_hanh_dong(hanh_dong):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    ThoiGian,
                    HanhDong,
                    MoTa,
                    NguoiThaoTac
                FROM AuditLog
                WHERE HanhDong = ?
                ORDER BY Id DESC
            """, (hanh_dong,))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def xoa_log(log_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM AuditLog
                WHERE Id = ?
            """, (log_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()