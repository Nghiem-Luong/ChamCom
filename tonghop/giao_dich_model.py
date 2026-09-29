# -*- coding: utf-8 -*-

from Database.database import get_connection


class GiaoDichNopTienModel:

    # ==========================================================
    # THÊM GIAO DỊCH
    # ==========================================================

    @staticmethod
    def them_giao_dich(
        nguoi_an_id,
        ngay_nop,
        so_tien,
        hinh_thuc="Tiền mặt",
        ghi_chu=None
    ):
        if not ngay_nop:
            raise ValueError(
                "Ngày nộp không được để trống."
            )

        try:
            so_tien = float(so_tien)
        except (TypeError, ValueError):
            raise ValueError(
                "Số tiền nộp không hợp lệ."
            )

        if so_tien <= 0:
            raise ValueError(
                "Số tiền nộp phải lớn hơn 0."
            )

        if not hinh_thuc:
            hinh_thuc = "Tiền mặt"

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # --------------------------------------------------
            # Kiểm tra người ăn
            # --------------------------------------------------

            cursor.execute("""
                SELECT Id
                FROM NguoiAn
                WHERE Id = ?
            """, (nguoi_an_id,))

            if cursor.fetchone() is None:
                raise ValueError(
                    "Người ăn không tồn tại."
                )

            # --------------------------------------------------
            # Thêm giao dịch
            # --------------------------------------------------

            cursor.execute("""
                INSERT INTO GiaoDichNopTien (
                    NguoiAnId,
                    NgayNop,
                    SoTien,
                    HinhThuc,
                    GhiChu
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                nguoi_an_id,
                ngay_nop,
                so_tien,
                hinh_thuc,
                ghi_chu
            ))

            connection.commit()

            return cursor.lastrowid

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    # ==========================================================
    # LẤY TẤT CẢ GIAO DỊCH
    # ==========================================================

    @staticmethod
    def lay_tat_ca():

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    g.Id,
                    g.NguoiAnId,
                    n.HoTen,
                    n.BoPhanId,
                    b.TenBoPhan,
                    g.NgayNop,
                    g.SoTien,
                    g.HinhThuc,
                    g.GhiChu
                FROM GiaoDichNopTien g

                INNER JOIN NguoiAn n
                    ON g.NguoiAnId = n.Id

                LEFT JOIN BoPhan b
                    ON n.BoPhanId = b.Id

                ORDER BY
                    g.NgayNop DESC,
                    g.Id DESC
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # LẤY GIAO DỊCH THEO NGƯỜI
    # ==========================================================

    @staticmethod
    def lay_theo_nguoi(
        nguoi_an_id
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    g.Id,
                    g.NguoiAnId,
                    n.HoTen,
                    g.NgayNop,
                    g.SoTien,
                    g.HinhThuc,
                    g.GhiChu
                FROM GiaoDichNopTien g

                INNER JOIN NguoiAn n
                    ON g.NguoiAnId = n.Id

                WHERE g.NguoiAnId = ?

                ORDER BY
                    g.NgayNop DESC,
                    g.Id DESC
            """, (
                nguoi_an_id,
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # LẤY MỘT GIAO DỊCH THEO ID
    # ==========================================================

    @staticmethod
    def tim_theo_id(
        giao_dich_id
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    g.Id,
                    g.NguoiAnId,
                    n.HoTen,
                    n.BoPhanId,
                    b.TenBoPhan,
                    g.NgayNop,
                    g.SoTien,
                    g.HinhThuc,
                    g.GhiChu
                FROM GiaoDichNopTien g

                INNER JOIN NguoiAn n
                    ON g.NguoiAnId = n.Id

                LEFT JOIN BoPhan b
                    ON n.BoPhanId = b.Id

                WHERE g.Id = ?
            """, (
                giao_dich_id,
            ))

            return cursor.fetchone()

        finally:
            connection.close()

    # ==========================================================
    # CẬP NHẬT GIAO DỊCH
    # ==========================================================

    @staticmethod
    def cap_nhat(
        giao_dich_id,
        nguoi_an_id,
        ngay_nop,
        so_tien,
        hinh_thuc="Tiền mặt",
        ghi_chu=None
    ):

        if not giao_dich_id:
            raise ValueError(
                "ID giao dịch không hợp lệ."
            )

        if not nguoi_an_id:
            raise ValueError(
                "Người nộp không được để trống."
            )

        if not ngay_nop:
            raise ValueError(
                "Ngày nộp không được để trống."
            )

        try:
            so_tien = float(so_tien)
        except (TypeError, ValueError):
            raise ValueError(
                "Số tiền nộp không hợp lệ."
            )

        if so_tien <= 0:
            raise ValueError(
                "Số tiền nộp phải lớn hơn 0."
            )

        if not hinh_thuc:
            hinh_thuc = "Tiền mặt"

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # --------------------------------------------------
            # Kiểm tra giao dịch
            # --------------------------------------------------

            cursor.execute("""
                SELECT Id
                FROM GiaoDichNopTien
                WHERE Id = ?
            """, (
                giao_dich_id,
            ))

            if cursor.fetchone() is None:
                raise ValueError(
                    "Giao dịch không tồn tại."
                )

            # --------------------------------------------------
            # Kiểm tra người ăn
            # --------------------------------------------------

            cursor.execute("""
                SELECT Id
                FROM NguoiAn
                WHERE Id = ?
            """, (
                nguoi_an_id,
            ))

            if cursor.fetchone() is None:
                raise ValueError(
                    "Người ăn không tồn tại."
                )

            # --------------------------------------------------
            # Cập nhật
            # --------------------------------------------------

            cursor.execute("""
                UPDATE GiaoDichNopTien
                SET
                    NguoiAnId = ?,
                    NgayNop = ?,
                    SoTien = ?,
                    HinhThuc = ?,
                    GhiChu = ?
                WHERE Id = ?
            """, (
                nguoi_an_id,
                ngay_nop,
                so_tien,
                hinh_thuc,
                ghi_chu,
                giao_dich_id
            ))

            connection.commit()

            return cursor.rowcount

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    # ==========================================================
    # TỔNG TIỀN ĐÃ NỘP THEO NGƯỜI
    # ==========================================================

    @staticmethod
    def tong_tien_da_nop(
        nguoi_an_id
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(SoTien),
                        0
                    )
                FROM GiaoDichNopTien

                WHERE NguoiAnId = ?
            """, (
                nguoi_an_id,
            ))

            result = cursor.fetchone()

            return result[0] or 0

        finally:
            connection.close()

    # ==========================================================
    # TỔNG TIỀN ĐÃ NỘP TRONG KHOẢNG THỜI GIAN
    # ==========================================================

    @staticmethod
    def tong_tien_theo_khoang_thoi_gian(
        tu_ngay=None,
        den_ngay=None,
        nguoi_an_id=None
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            dieu_kien = []
            params = []

            if tu_ngay:
                dieu_kien.append(
                    "g.NgayNop >= ?"
                )
                params.append(tu_ngay)

            if den_ngay:
                dieu_kien.append(
                    "g.NgayNop <= ?"
                )
                params.append(den_ngay)

            if nguoi_an_id:
                dieu_kien.append(
                    "g.NguoiAnId = ?"
                )
                params.append(nguoi_an_id)

            where_sql = ""

            if dieu_kien:
                where_sql = (
                    "WHERE "
                    + " AND ".join(
                        dieu_kien
                    )
                )

            cursor.execute(
                f"""
                SELECT
                    COALESCE(
                        SUM(g.SoTien),
                        0
                    )
                FROM GiaoDichNopTien g

                {where_sql}
                """,
                tuple(params)
            )

            result = cursor.fetchone()

            return result[0] or 0

        finally:
            connection.close()

    # ==========================================================
    # LẤY GIAO DỊCH THEO KHOẢNG THỜI GIAN
    # ==========================================================

    @staticmethod
    def lay_theo_khoang_thoi_gian(
        tu_ngay=None,
        den_ngay=None,
        nguoi_an_id=None,
        bo_phan_id=None,
        hinh_thuc=None
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            dieu_kien = []
            params = []

            # --------------------------------------------------
            # Khoảng ngày
            # --------------------------------------------------

            if tu_ngay:
                dieu_kien.append(
                    "g.NgayNop >= ?"
                )
                params.append(tu_ngay)

            if den_ngay:
                dieu_kien.append(
                    "g.NgayNop <= ?"
                )
                params.append(den_ngay)

            # --------------------------------------------------
            # Người
            # --------------------------------------------------

            if nguoi_an_id:
                dieu_kien.append(
                    "g.NguoiAnId = ?"
                )
                params.append(nguoi_an_id)

            # --------------------------------------------------
            # Bộ phận
            # --------------------------------------------------

            if bo_phan_id:
                dieu_kien.append(
                    "n.BoPhanId = ?"
                )
                params.append(bo_phan_id)

            # --------------------------------------------------
            # Hình thức
            # --------------------------------------------------

            if hinh_thuc:
                dieu_kien.append(
                    "g.HinhThuc = ?"
                )
                params.append(hinh_thuc)

            where_sql = ""

            if dieu_kien:
                where_sql = (
                    "WHERE "
                    + " AND ".join(
                        dieu_kien
                    )
                )

            cursor.execute(
                f"""
                SELECT
                    g.Id,
                    g.NguoiAnId,
                    n.HoTen,
                    n.BoPhanId,
                    b.TenBoPhan,
                    g.NgayNop,
                    g.SoTien,
                    g.HinhThuc,
                    g.GhiChu
                FROM GiaoDichNopTien g

                INNER JOIN NguoiAn n
                    ON g.NguoiAnId = n.Id

                LEFT JOIN BoPhan b
                    ON n.BoPhanId = b.Id

                {where_sql}

                ORDER BY
                    g.NgayNop DESC,
                    g.Id DESC
                """,
                tuple(params)
            )

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # TỔNG TIỀN THEO HÌNH THỨC
    # ==========================================================

    @staticmethod
    def tong_tien_theo_hinh_thuc(
        tu_ngay=None,
        den_ngay=None
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            dieu_kien = []
            params = []

            if tu_ngay:
                dieu_kien.append(
                    "NgayNop >= ?"
                )
                params.append(tu_ngay)

            if den_ngay:
                dieu_kien.append(
                    "NgayNop <= ?"
                )
                params.append(den_ngay)

            where_sql = ""

            if dieu_kien:
                where_sql = (
                    "WHERE "
                    + " AND ".join(
                        dieu_kien
                    )
                )

            cursor.execute(
                f"""
                SELECT
                    HinhThuc,
                    COALESCE(
                        SUM(SoTien),
                        0
                    )
                FROM GiaoDichNopTien

                {where_sql}

                GROUP BY HinhThuc
                ORDER BY HinhThuc
                """,
                tuple(params)
            )

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # ĐẾM SỐ LẦN NỘP THEO NGƯỜI
    # ==========================================================

    @staticmethod
    def dem_so_lan_nop(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            dieu_kien = [
                "NguoiAnId = ?"
            ]

            params = [
                nguoi_an_id
            ]

            if tu_ngay:

                dieu_kien.append(
                    "NgayNop >= ?"
                )

                params.append(
                    tu_ngay
                )

            if den_ngay:

                dieu_kien.append(
                    "NgayNop <= ?"
                )

                params.append(
                    den_ngay
                )

            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM GiaoDichNopTien
                WHERE {" AND ".join(dieu_kien)}
                """,
                tuple(params)
            )

            result = cursor.fetchone()

            return result[0] or 0

        finally:
            connection.close()

    # ==========================================================
    # XÓA GIAO DỊCH
    # ==========================================================

    @staticmethod
    def xoa(
        giao_dich_id
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM GiaoDichNopTien
                WHERE Id = ?
            """, (
                giao_dich_id,
            ))

            connection.commit()

            return cursor.rowcount

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()