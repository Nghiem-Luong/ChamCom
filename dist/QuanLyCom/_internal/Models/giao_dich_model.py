from Database.database import get_connection


class GiaoDichNopTienModel:

    @staticmethod
    def them_giao_dich(
        nguoi_an_id,
        ngay_nop,
        so_tien,
        hinh_thuc="Tiền mặt",
        ghi_chu=None
    ):
        if not ngay_nop:
            raise ValueError("Ngày nộp không được để trống.")

        if so_tien <= 0:
            raise ValueError("Số tiền nộp phải lớn hơn 0.")

        if not hinh_thuc:
            hinh_thuc = "Tiền mặt"

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # Kiểm tra người ăn có tồn tại không
            cursor.execute("""
                SELECT Id
                FROM NguoiAn
                WHERE Id = ?
            """, (nguoi_an_id,))

            if cursor.fetchone() is None:
                raise ValueError("Người ăn không tồn tại.")

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

        finally:
            connection.close()

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
                    g.NgayNop,
                    g.SoTien,
                    g.HinhThuc,
                    g.GhiChu
                FROM GiaoDichNopTien g
                INNER JOIN NguoiAn n
                    ON g.NguoiAnId = n.Id
                ORDER BY g.NgayNop DESC, g.Id DESC
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_theo_nguoi(nguoi_an_id):
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
                ORDER BY g.NgayNop DESC, g.Id DESC
            """, (nguoi_an_id,))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def tong_tien_da_nop(nguoi_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COALESCE(SUM(SoTien), 0)
                FROM GiaoDichNopTien
                WHERE NguoiAnId = ?
            """, (nguoi_an_id,))

            result = cursor.fetchone()

            return result[0] or 0

        finally:
            connection.close()

    @staticmethod
    def xoa(giao_dich_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM GiaoDichNopTien
                WHERE Id = ?
            """, (giao_dich_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()