# -*- coding: utf-8 -*-

from Database.database import get_connection


class ChiTietAnModel:

    @staticmethod
    def them_chi_tiet(
        nguoi_an_id,
        ngay_an_id,
        da_an,
        so_tien_phai_tra,
        ghi_chu=None,
        trang_thai="Đăng ký"
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            # Kiểm tra người ăn
            cursor.execute(
                """
                SELECT Id
                FROM NguoiAn
                WHERE Id = ?
                """,
                (nguoi_an_id,)
            )

            if cursor.fetchone() is None:
                raise ValueError("Người ăn không tồn tại.")

            # Kiểm tra ngày ăn
            cursor.execute(
                """
                SELECT Id
                FROM NgayAn
                WHERE Id = ?
                """,
                (ngay_an_id,)
            )

            if cursor.fetchone() is None:
                raise ValueError("Ngày ăn không tồn tại.")

            # Không cho phép trùng người ăn trong cùng một ngày
            cursor.execute(
                """
                SELECT Id
                FROM ChiTietAn
                WHERE NguoiAnId = ?
                  AND NgayAnId = ?
                """,
                (nguoi_an_id, ngay_an_id)
            )

            if cursor.fetchone() is not None:
                raise ValueError(
                    "Người này đã có dữ liệu chấm cơm trong ngày."
                )

            cursor.execute(
                """
                INSERT INTO ChiTietAn (
                    NguoiAnId,
                    NgayAnId,
                    DaAn,
                    SoTienPhaiTra,
                    GhiChu,
                    TrangThai
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    nguoi_an_id,
                    ngay_an_id,
                    int(da_an),
                    float(so_tien_phai_tra),
                    ghi_chu,
                    trang_thai
                )
            )

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    @staticmethod
    def cap_nhat(
        chi_tiet_id,
        da_an,
        so_tien_phai_tra,
        ghi_chu=None,
        trang_thai="Đăng ký"
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE ChiTietAn
                SET
                    DaAn = ?,
                    SoTienPhaiTra = ?,
                    GhiChu = ?,
                    TrangThai = ?
                WHERE Id = ?
                """,
                (
                    int(da_an),
                    float(so_tien_phai_tra),
                    ghi_chu,
                    trang_thai,
                    chi_tiet_id
                )
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def xoa(chi_tiet_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM ChiTietAn
                WHERE Id = ?
                """,
                (chi_tiet_id,)
            )

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    @staticmethod
    def da_co_ban_ghi(nguoi_an_id, ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Id
                FROM ChiTietAn
                WHERE NguoiAnId = ?
                  AND NgayAnId = ?
                """,
                (nguoi_an_id, ngay_an_id)
            )

            return cursor.fetchone() is not None

        finally:
            connection.close()

    @staticmethod
    def tim_theo_id(chi_tiet_id):
        """
        Lấy một bản ghi chấm cơm theo ID.

        Cấu trúc kết quả:
        0 - Id
        1 - NguoiAnId
        2 - HoTen
        3 - NgayAnId
        4 - Ngay
        5 - DaAn
        6 - SoTienPhaiTra
        7 - GhiChu
        8 - TrangThai
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    c.Id,
                    c.NguoiAnId,
                    n.HoTen,
                    c.NgayAnId,
                    a.Ngay,
                    c.DaAn,
                    c.SoTienPhaiTra,
                    c.GhiChu,
                    COALESCE(
                        c.TrangThai,
                        CASE
                            WHEN c.DaAn = 1
                            THEN 'Đăng ký'
                            ELSE 'Không ăn'
                        END
                    ) AS TrangThai
                FROM ChiTietAn c
                INNER JOIN NguoiAn n
                    ON c.NguoiAnId = n.Id
                INNER JOIN NgayAn a
                    ON c.NgayAnId = a.Id
                WHERE c.Id = ?
                """,
                (chi_tiet_id,)
            )

            return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def lay_theo_ngay(ngay_an_id):
        """
        Lấy toàn bộ danh sách chấm cơm của một ngày.

        Cấu trúc kết quả:
        0 - ChiTietAn.Id
        1 - NguoiAnId
        2 - HoTen
        3 - SDT
        4 - NgayAnId
        5 - DaAn
        6 - SoTienPhaiTra
        7 - GhiChu
        8 - TrangThai
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    c.Id,
                    c.NguoiAnId,
                    n.HoTen,
                    n.SDT,
                    c.NgayAnId,
                    c.DaAn,
                    c.SoTienPhaiTra,
                    c.GhiChu,
                    COALESCE(
                        c.TrangThai,
                        CASE
                            WHEN c.DaAn = 1
                            THEN 'Đăng ký'
                            ELSE 'Không ăn'
                        END
                    ) AS TrangThai
                FROM ChiTietAn c
                INNER JOIN NguoiAn n
                    ON c.NguoiAnId = n.Id
                WHERE c.NgayAnId = ?
                ORDER BY n.HoTen
                """,
                (ngay_an_id,)
            )

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_theo_nguoi(nguoi_an_id):
        """
        Lấy lịch sử chấm cơm của một người.

        Cấu trúc kết quả:
        0 - ChiTietAn.Id
        1 - NguoiAnId
        2 - HoTen
        3 - NgayAnId
        4 - Ngay
        5 - DaAn
        6 - SoTienPhaiTra
        7 - GhiChu
        8 - TrangThai
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    c.Id,
                    c.NguoiAnId,
                    n.HoTen,
                    c.NgayAnId,
                    a.Ngay,
                    c.DaAn,
                    c.SoTienPhaiTra,
                    c.GhiChu,
                    COALESCE(
                        c.TrangThai,
                        CASE
                            WHEN c.DaAn = 1
                            THEN 'Đăng ký'
                            ELSE 'Không ăn'
                        END
                    ) AS TrangThai
                FROM ChiTietAn c
                INNER JOIN NguoiAn n
                    ON c.NguoiAnId = n.Id
                INNER JOIN NgayAn a
                    ON c.NgayAnId = a.Id
                WHERE c.NguoiAnId = ?
                ORDER BY a.Ngay DESC
                """,
                (nguoi_an_id,)
            )

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def tinh_tong_tien_ngay(ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(SoTienPhaiTra), 0)
                FROM ChiTietAn
                WHERE NgayAnId = ?
                  AND DaAn = 1
                """,
                (ngay_an_id,)
            )

            result = cursor.fetchone()

            if result:
                return float(result[0] or 0)

            return 0.0

        finally:
            connection.close()

    @staticmethod
    def dem_so_nguoi_an(ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ChiTietAn
                WHERE NgayAnId = ?
                  AND DaAn = 1
                """,
                (ngay_an_id,)
            )

            result = cursor.fetchone()

            if result:
                return int(result[0] or 0)

            return 0

        finally:
            connection.close()

    @staticmethod
    def luu_danh_sach_dang_ky(
        ngay_an_id,
        danh_sach_nguoi_an,
        don_gia
    ):
        """
        Lưu danh sách đăng ký ăn của toàn bộ người ăn.

        danh_sach_nguoi_an:
            [
                {
                    "nguoi_an_id": 1,
                    "da_an": True
                },
                ...
            ]

        Nếu da_an=True:
            DaAn = 1
            SoTienPhaiTra = don_gia
            TrangThai = Đăng ký

        Nếu da_an=False:
            DaAn = 0
            SoTienPhaiTra = 0
            TrangThai = Không ăn
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            for item in danh_sach_nguoi_an:

                nguoi_an_id = item["nguoi_an_id"]
                da_an = bool(item["da_an"])

                if da_an:
                    so_tien = float(don_gia)
                    trang_thai = "Đăng ký"
                else:
                    so_tien = 0.0
                    trang_thai = "Không ăn"

                # Kiểm tra bản ghi đã tồn tại chưa
                cursor.execute(
                    """
                    SELECT Id
                    FROM ChiTietAn
                    WHERE NguoiAnId = ?
                      AND NgayAnId = ?
                    """,
                    (
                        nguoi_an_id,
                        ngay_an_id
                    )
                )

                ban_ghi = cursor.fetchone()

                if ban_ghi:
                    cursor.execute(
                        """
                        UPDATE ChiTietAn
                        SET
                            DaAn = ?,
                            SoTienPhaiTra = ?,
                            TrangThai = ?
                        WHERE Id = ?
                        """,
                        (
                            int(da_an),
                            so_tien,
                            trang_thai,
                            ban_ghi[0]
                        )
                    )

                else:
                    cursor.execute(
                        """
                        INSERT INTO ChiTietAn (
                            NguoiAnId,
                            NgayAnId,
                            DaAn,
                            SoTienPhaiTra,
                            GhiChu,
                            TrangThai
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            nguoi_an_id,
                            ngay_an_id,
                            int(da_an),
                            so_tien,
                            None,
                            trang_thai
                        )
                    )

            connection.commit()

            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()