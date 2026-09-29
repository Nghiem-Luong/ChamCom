from datetime import datetime

from Database.database import get_connection


class NgayAnModel:

    # ==========================================
    # TẠO NGÀY ĂN
    # ==========================================
    @staticmethod
    def tao_ngay_an(ngay, don_gia_mac_dinh, ghi_chu=None):

        if not ngay:
            raise ValueError("Ngày ăn không được để trống.")

        if don_gia_mac_dinh < 0:
            raise ValueError("Đơn giá không được âm.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # Kiểm tra ngày đã tồn tại chưa
            cursor.execute("""
                SELECT Id
                FROM NgayAn
                WHERE Ngay = ?
            """, (ngay,))

            ngay_ton_tai = cursor.fetchone()

            if ngay_ton_tai:
                raise ValueError(
                    f"Ngày {ngay} đã tồn tại."
                )

            cursor.execute("""
                INSERT INTO NgayAn (
                    Ngay,
                    DonGiaMacDinh,
                    GhiChu
                )
                VALUES (?, ?, ?)
            """, (
                ngay,
                don_gia_mac_dinh,
                ghi_chu
            ))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    # ==========================================
    # LẤY NGÀY THEO ID
    # ==========================================
    @staticmethod
    def tim_theo_id(ngay_an_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    Ngay,
                    DonGiaMacDinh,
                    GhiChu
                FROM NgayAn
                WHERE Id = ?
            """, (ngay_an_id,))

            return cursor.fetchone()

        finally:
            connection.close()

    # ==========================================
    # LẤY NGÀY THEO NGÀY
    # ==========================================
    @staticmethod
    def tim_theo_ngay(ngay):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    Ngay,
                    DonGiaMacDinh,
                    GhiChu
                FROM NgayAn
                WHERE Ngay = ?
            """, (ngay,))

            return cursor.fetchone()

        finally:
            connection.close()

    # ==========================================
    # LẤY TẤT CẢ NGÀY ĂN
    # ==========================================
    @staticmethod
    def lay_tat_ca():

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    Ngay,
                    DonGiaMacDinh,
                    GhiChu
                FROM NgayAn
                ORDER BY Ngay DESC
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================
    # LẤY NGÀY ĂN GẦN NHẤT TRƯỚC ĐÓ
    # ==========================================
    @staticmethod
    def lay_ngay_truoc_do(ngay):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    Ngay,
                    DonGiaMacDinh,
                    GhiChu
                FROM NgayAn
                WHERE Ngay < ?
                ORDER BY Ngay DESC
                LIMIT 1
            """, (ngay,))

            return cursor.fetchone()

        finally:
            connection.close()

    # ==========================================
    # CẬP NHẬT NGÀY ĂN
    # ==========================================
    @staticmethod
    def cap_nhat(
        ngay_an_id,
        ngay,
        don_gia_mac_dinh,
        ghi_chu=None
    ):

        if not ngay:
            raise ValueError("Ngày ăn không được để trống.")

        if don_gia_mac_dinh < 0:
            raise ValueError("Đơn giá không được âm.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # Kiểm tra ngày trùng với bản ghi khác
            cursor.execute("""
                SELECT Id
                FROM NgayAn
                WHERE Ngay = ?
                  AND Id != ?
            """, (
                ngay,
                ngay_an_id
            ))

            ngay_trung = cursor.fetchone()

            if ngay_trung:
                raise ValueError(
                    f"Ngày {ngay} đã tồn tại."
                )

            cursor.execute("""
                UPDATE NgayAn
                SET
                    Ngay = ?,
                    DonGiaMacDinh = ?,
                    GhiChu = ?
                WHERE Id = ?
            """, (
                ngay,
                don_gia_mac_dinh,
                ghi_chu,
                ngay_an_id
            ))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()