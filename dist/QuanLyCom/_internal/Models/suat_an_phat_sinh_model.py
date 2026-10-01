# -*- coding: utf-8 -*-

from datetime import datetime

from Database.database import get_connection


class SuatAnPhatSinhModel:

    @staticmethod
    def them(
        ngay_an_id,
        ho_ten,
        don_vi=None,
        so_luong=1,
        don_gia=0,
        ghi_chu=None
    ):
        """
        Thêm suất ăn phát sinh.

        Dùng cho:
        - Khách
        - Người ngoài công ty
        - Nhà thầu
        - Người chưa có trong danh sách
        - Đoàn khách
        - Người chưa xác định đầy đủ thông tin
        """

        ho_ten = (ho_ten or "").strip()
        don_vi = (don_vi or "").strip()
        ghi_chu = (ghi_chu or "").strip()

        if not ho_ten:
            raise ValueError(
                "Tên người ăn hoặc tên nhóm không được để trống."
            )

        try:
            so_luong = int(so_luong)
        except (TypeError, ValueError):
            raise ValueError(
                "Số lượng phải là số nguyên."
            )

        if so_luong <= 0:
            raise ValueError(
                "Số lượng phải lớn hơn 0."
            )

        try:
            don_gia = float(don_gia)
        except (TypeError, ValueError):
            raise ValueError(
                "Đơn giá không hợp lệ."
            )

        if don_gia < 0:
            raise ValueError(
                "Đơn giá không được âm."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO SuatAnPhatSinh (
                    NgayAnId,
                    HoTen,
                    DonVi,
                    SoLuong,
                    DonGia,
                    GhiChu,
                    NgayTao
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ngay_an_id,
                    ho_ten,
                    don_vi,
                    so_luong,
                    don_gia,
                    ghi_chu,
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    @staticmethod
    def lay_theo_ngay(ngay_an_id):
        """
        Lấy toàn bộ suất ăn phát sinh của một ngày.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    Id,
                    NgayAnId,
                    HoTen,
                    DonVi,
                    SoLuong,
                    DonGia,
                    GhiChu,
                    NgayTao
                FROM SuatAnPhatSinh
                WHERE NgayAnId = ?
                ORDER BY Id DESC
                """,
                (ngay_an_id,)
            )

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def tim_theo_id(suat_an_id):
        """
        Tìm một suất ăn phát sinh theo ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    Id,
                    NgayAnId,
                    HoTen,
                    DonVi,
                    SoLuong,
                    DonGia,
                    GhiChu,
                    NgayTao
                FROM SuatAnPhatSinh
                WHERE Id = ?
                """,
                (suat_an_id,)
            )

            return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def cap_nhat(
        suat_an_id,
        ho_ten,
        don_vi=None,
        so_luong=1,
        don_gia=0,
        ghi_chu=None
    ):
        """
        Cập nhật suất ăn phát sinh.
        """

        ho_ten = (ho_ten or "").strip()
        don_vi = (don_vi or "").strip()
        ghi_chu = (ghi_chu or "").strip()

        if not ho_ten:
            raise ValueError(
                "Tên người ăn hoặc tên nhóm không được để trống."
            )

        try:
            so_luong = int(so_luong)
        except (TypeError, ValueError):
            raise ValueError(
                "Số lượng phải là số nguyên."
            )

        if so_luong <= 0:
            raise ValueError(
                "Số lượng phải lớn hơn 0."
            )

        try:
            don_gia = float(don_gia)
        except (TypeError, ValueError):
            raise ValueError(
                "Đơn giá không hợp lệ."
            )

        if don_gia < 0:
            raise ValueError(
                "Đơn giá không được âm."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE SuatAnPhatSinh
                SET
                    HoTen = ?,
                    DonVi = ?,
                    SoLuong = ?,
                    DonGia = ?,
                    GhiChu = ?
                WHERE Id = ?
                """,
                (
                    ho_ten,
                    don_vi,
                    so_luong,
                    don_gia,
                    ghi_chu,
                    suat_an_id
                )
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def xoa(suat_an_id):
        """
        Xóa suất ăn phát sinh.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            SuatAnPhatSinhModel._ensure_payment_table()
            cursor.execute(
                """
                DELETE FROM GiaoDichSuatAnPhatSinh
                WHERE SuatAnPhatSinhId = ?
                """,
                (suat_an_id,)
            )
            cursor.execute(
                """
                DELETE FROM SuatAnPhatSinh
                WHERE Id = ?
                """,
                (suat_an_id,)
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def xoa_theo_ngay(ngay_an_id):
        """
        Xóa toàn bộ suất ăn phát sinh của một ngày.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            SuatAnPhatSinhModel._ensure_payment_table()
            cursor.execute(
                """
                DELETE FROM GiaoDichSuatAnPhatSinh
                WHERE SuatAnPhatSinhId IN (
                    SELECT Id FROM SuatAnPhatSinh WHERE NgayAnId = ?
                )
                """,
                (ngay_an_id,)
            )
            cursor.execute(
                """
                DELETE FROM SuatAnPhatSinh
                WHERE NgayAnId = ?
                """,
                (ngay_an_id,)
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def _ensure_payment_table():
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS GiaoDichSuatAnPhatSinh (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    SuatAnPhatSinhId INTEGER NOT NULL,
                    NgayThu TEXT NOT NULL,
                    SoTien REAL NOT NULL,
                    HinhThuc TEXT NOT NULL DEFAULT 'Tiền mặt',
                    GhiChu TEXT,
                    NgayTao TEXT NOT NULL,
                    FOREIGN KEY (SuatAnPhatSinhId) REFERENCES SuatAnPhatSinh(Id)
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_GiaoDichSuatAnPhatSinh_SuatAnPhatSinhId
                ON GiaoDichSuatAnPhatSinh(SuatAnPhatSinhId)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_GiaoDichSuatAnPhatSinh_NgayThu
                ON GiaoDichSuatAnPhatSinh(NgayThu)
            """)
            connection.commit()
        finally:
            connection.close()

    @staticmethod
    def them_thanh_toan(
        suat_an_phat_sinh_id,
        ngay_thu,
        so_tien,
        hinh_thuc="Tiền mặt",
        ghi_chu=None
    ):
        if not suat_an_phat_sinh_id:
            raise ValueError("Suất ăn phát sinh không hợp lệ.")
        if not ngay_thu:
            raise ValueError("Ngày thu không được để trống.")
        try:
            so_tien = float(so_tien)
        except (TypeError, ValueError):
            raise ValueError("Số tiền thu không hợp lệ.")
        if so_tien <= 0:
            raise ValueError("Số tiền thu phải lớn hơn 0.")
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Id FROM SuatAnPhatSinh WHERE Id = ?", (suat_an_phat_sinh_id,))
            if cursor.fetchone() is None:
                raise ValueError("Suất ăn phát sinh không tồn tại.")
            cursor.execute("""
                INSERT INTO GiaoDichSuatAnPhatSinh
                (SuatAnPhatSinhId, NgayThu, SoTien, HinhThuc, GhiChu, NgayTao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                suat_an_phat_sinh_id,
                str(ngay_thu)[:10],
                so_tien,
                hinh_thuc or "Tiền mặt",
                (ghi_chu or "").strip(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            connection.commit()
            return cursor.lastrowid
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def lay_thanh_toan(suat_an_phat_sinh_id):
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT Id, SuatAnPhatSinhId, NgayThu, SoTien, HinhThuc, GhiChu, NgayTao
                FROM GiaoDichSuatAnPhatSinh
                WHERE SuatAnPhatSinhId = ?
                ORDER BY NgayThu DESC, Id DESC
            """, (suat_an_phat_sinh_id,))
            return cursor.fetchall()
        finally:
            connection.close()

    @staticmethod
    def tim_thanh_toan_theo_id(payment_id):
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT Id, SuatAnPhatSinhId, NgayThu, SoTien, HinhThuc, GhiChu, NgayTao
                FROM GiaoDichSuatAnPhatSinh
                WHERE Id = ?
            """, (payment_id,))
            return cursor.fetchone()
        finally:
            connection.close()

    @staticmethod
    def cap_nhat_thanh_toan(
        payment_id,
        suat_an_phat_sinh_id,
        ngay_thu,
        so_tien,
        hinh_thuc="Tiền mặt",
        ghi_chu=None
    ):
        try:
            so_tien = float(so_tien)
        except (TypeError, ValueError):
            raise ValueError("Số tiền thu không hợp lệ.")
        if so_tien <= 0:
            raise ValueError("Số tiền thu phải lớn hơn 0.")
        if not ngay_thu:
            raise ValueError("Ngày thu không được để trống.")
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Id FROM SuatAnPhatSinh WHERE Id = ?", (suat_an_phat_sinh_id,))
            if cursor.fetchone() is None:
                raise ValueError("Suất ăn phát sinh không tồn tại.")
            cursor.execute("""
                UPDATE GiaoDichSuatAnPhatSinh
                SET SuatAnPhatSinhId = ?, NgayThu = ?, SoTien = ?, HinhThuc = ?, GhiChu = ?
                WHERE Id = ?
            """, (
                suat_an_phat_sinh_id, str(ngay_thu)[:10], so_tien,
                hinh_thuc or "Tiền mặt", (ghi_chu or "").strip(), payment_id
            ))
            connection.commit()
            return cursor.rowcount
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def xoa_thanh_toan(payment_id):
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM GiaoDichSuatAnPhatSinh WHERE Id = ?", (payment_id,))
            connection.commit()
            return cursor.rowcount
        finally:
            connection.close()

    @staticmethod
    def tong_da_thu(suat_an_phat_sinh_id):
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(SoTien), 0)
                FROM GiaoDichSuatAnPhatSinh
                WHERE SuatAnPhatSinhId = ?
            """, (suat_an_phat_sinh_id,))
            return float(cursor.fetchone()[0] or 0)
        finally:
            connection.close()

    @staticmethod
    def lay_bao_cao_thanh_toan(tu_ngay=None, den_ngay=None):
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            conditions = []
            params = []
            if tu_ngay:
                conditions.append("n.Ngay >= ?")
                params.append(str(tu_ngay)[:10])
            if den_ngay:
                conditions.append("n.Ngay <= ?")
                params.append(str(den_ngay)[:10])
            where_sql = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            cursor.execute(f"""
                SELECT
                    s.Id, s.NgayAnId, n.Ngay, s.HoTen, s.DonVi, s.SoLuong, s.DonGia,
                    (s.SoLuong * s.DonGia) AS ThanhTien,
                    COALESCE((
                        SELECT SUM(p.SoTien)
                        FROM GiaoDichSuatAnPhatSinh p
                        WHERE p.SuatAnPhatSinhId = s.Id
                    ), 0) AS DaThu,
                    s.GhiChu, s.NgayTao
                FROM SuatAnPhatSinh s
                INNER JOIN NgayAn n ON n.Id = s.NgayAnId
                {where_sql}
                ORDER BY n.Ngay DESC, s.Id DESC
            """, tuple(params))
            return cursor.fetchall()
        finally:
            connection.close()

    @staticmethod
    def lay_thanh_toan_theo_khoang_thu(tu_ngay=None, den_ngay=None):
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            conditions = []
            params = []
            if tu_ngay:
                conditions.append("p.NgayThu >= ?")
                params.append(str(tu_ngay)[:10])
            if den_ngay:
                conditions.append("p.NgayThu <= ?")
                params.append(str(den_ngay)[:10])
            where_sql = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            cursor.execute(f"""
                SELECT p.Id, p.SuatAnPhatSinhId, n.Ngay, s.HoTen, s.DonVi,
                       p.NgayThu, p.SoTien, p.HinhThuc, p.GhiChu
                FROM GiaoDichSuatAnPhatSinh p
                INNER JOIN SuatAnPhatSinh s ON s.Id = p.SuatAnPhatSinhId
                INNER JOIN NgayAn n ON n.Id = s.NgayAnId
                {where_sql}
                ORDER BY p.NgayThu DESC, p.Id DESC
            """, tuple(params))
            return cursor.fetchall()
        finally:
            connection.close()

    @staticmethod
    def tong_tien_thu_theo_hinh_thuc(tu_ngay=None, den_ngay=None):
        SuatAnPhatSinhModel._ensure_payment_table()
        connection = get_connection()
        try:
            cursor = connection.cursor()
            conditions = []
            params = []
            if tu_ngay:
                conditions.append("NgayThu >= ?")
                params.append(str(tu_ngay)[:10])
            if den_ngay:
                conditions.append("NgayThu <= ?")
                params.append(str(den_ngay)[:10])
            where_sql = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            cursor.execute(f"""
                SELECT HinhThuc, COALESCE(SUM(SoTien), 0)
                FROM GiaoDichSuatAnPhatSinh
                {where_sql}
                GROUP BY HinhThuc
                ORDER BY SUM(SoTien) DESC
            """, tuple(params))
            return cursor.fetchall()
        finally:
            connection.close()

    @staticmethod
    def tinh_tong_so_luong(ngay_an_id):
        """
        Tổng số suất ăn phát sinh.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(SoLuong), 0)
                FROM SuatAnPhatSinh
                WHERE NgayAnId = ?
                """,
                (ngay_an_id,)
            )

            row = cursor.fetchone()

            return int(row[0] or 0)

        finally:
            connection.close()

    @staticmethod
    def tinh_tong_tien(ngay_an_id):
        """
        Tổng tiền suất ăn phát sinh.

        Công thức:
        Số lượng × Đơn giá
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    COALESCE(
                        SUM(SoLuong * DonGia),
                        0
                    )
                FROM SuatAnPhatSinh
                WHERE NgayAnId = ?
                """,
                (ngay_an_id,)
            )

            row = cursor.fetchone()

            return float(row[0] or 0)

        finally:
            connection.close()