from datetime import datetime

from Database.database import get_connection


class NguoiAnModel:

    # ==========================================
    # THÊM NGƯỜI ĂN
    # ==========================================
    @staticmethod
    def them_nguoi_an(ho_ten, sdt=None):

        ho_ten = ho_ten.strip()

        if not ho_ten:
            raise ValueError("Họ tên không được để trống.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO NguoiAn (
                    HoTen,
                    SDT,
                    DangHoatDong,
                    NgayTao
                )
                VALUES (?, ?, ?, ?)
            """, (
                ho_ten,
                sdt,
                1,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    # ==========================================
    # LẤY TẤT CẢ NGƯỜI ĂN
    # ==========================================
    @staticmethod
    def lay_tat_ca():

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    HoTen,
                    SDT,
                    DangHoatDong,
                    NgayTao
                FROM NguoiAn
                ORDER BY HoTen
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================
    # LẤY NGƯỜI ĂN ĐANG HOẠT ĐỘNG
    # ==========================================
    @staticmethod
    def lay_dang_hoat_dong():

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    HoTen,
                    SDT,
                    DangHoatDong,
                    NgayTao
                FROM NguoiAn
                WHERE DangHoatDong = 1
                ORDER BY HoTen
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================
    # TÌM THEO ID
    # ==========================================
    @staticmethod
    def tim_theo_id(nguoi_an_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    HoTen,
                    SDT,
                    DangHoatDong,
                    NgayTao
                FROM NguoiAn
                WHERE Id = ?
            """, (nguoi_an_id,))

            return cursor.fetchone()

        finally:
            connection.close()

    # ==========================================
    # TÌM THEO TÊN
    # ==========================================
    @staticmethod
    def tim_theo_ten(ho_ten):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    HoTen,
                    SDT,
                    DangHoatDong,
                    NgayTao
                FROM NguoiAn
                WHERE HoTen LIKE ?
                ORDER BY HoTen
            """, (f"%{ho_ten}%",))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================
    # CẬP NHẬT THÔNG TIN
    # ==========================================
    @staticmethod
    def cap_nhat(nguoi_an_id, ho_ten, sdt=None):

        ho_ten = ho_ten.strip()

        if not ho_ten:
            raise ValueError("Họ tên không được để trống.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE NguoiAn
                SET
                    HoTen = ?,
                    SDT = ?
                WHERE Id = ?
            """, (
                ho_ten,
                sdt,
                nguoi_an_id
            ))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    # ==========================================
    # NGỪNG HOẠT ĐỘNG
    # ==========================================
    @staticmethod
    def ngung_hoat_dong(nguoi_an_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE NguoiAn
                SET DangHoatDong = 0
                WHERE Id = ?
            """, (nguoi_an_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    # ==========================================
    # KÍCH HOẠT LẠI
    # ==========================================
    @staticmethod
    def kich_hoat_lai(nguoi_an_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE NguoiAn
                SET DangHoatDong = 1
                WHERE Id = ?
            """, (nguoi_an_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()