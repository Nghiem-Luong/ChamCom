from Database.database import get_connection


class ChiTietAnModel:

    # ==========================================
    # THÊM BẢN GHI CHẤM CƠM
    # ==========================================
    @staticmethod
    def them_chi_tiet(
        nguoi_an_id,
        ngay_an_id,
        da_an,
        so_tien_phai_tra,
        ghi_chu=None
    ):

        if so_tien_phai_tra < 0:
            raise ValueError(
                "Số tiền phải trả không được âm."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # ----------------------------------
            # Kiểm tra người ăn có tồn tại
            # ----------------------------------
            cursor.execute("""
                SELECT Id
                FROM NguoiAn
                WHERE Id = ?
            """, (nguoi_an_id,))

            if cursor.fetchone() is None:
                raise ValueError(
                    "Người ăn không tồn tại."
                )

            # ----------------------------------
            # Kiểm tra ngày ăn có tồn tại
            # ----------------------------------
            cursor.execute("""
                SELECT Id
                FROM NgayAn
                WHERE Id = ?
            """, (ngay_an_id,))

            if cursor.fetchone() is None:
                raise ValueError(
                    "Ngày ăn không tồn tại."
                )

            # ----------------------------------
            # Kiểm tra đã có bản ghi chưa
            # ----------------------------------
            cursor.execute("""
                SELECT Id
                FROM ChiTietAn
                WHERE NguoiAnId = ?
                  AND NgayAnId = ?
            """, (
                nguoi_an_id,
                ngay_an_id
            ))

            if cursor.fetchone():
                raise ValueError(
                    "Người này đã được chấm cơm trong ngày."
                )

            # ----------------------------------
            # Thêm bản ghi
            # ----------------------------------
            cursor.execute("""
                INSERT INTO ChiTietAn (
                    NguoiAnId,
                    NgayAnId,
                    DaAn,
                    SoTienPhaiTra,
                    GhiChu
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                nguoi_an_id,
                ngay_an_id,
                1 if da_an else 0,
                so_tien_phai_tra,
                ghi_chu
            ))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    # ==========================================
    # CẬP NHẬT TRẠNG THÁI ĂN
    # ==========================================
    @staticmethod
    def cap_nhat(
        chi_tiet_id,
        da_an,
        so_tien_phai_tra,
        ghi_chu=None
    ):

        if so_tien_phai_tra < 0:
            raise ValueError(
                "Số tiền phải trả không được âm."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE ChiTietAn
                SET
                    DaAn = ?,
                    SoTienPhaiTra = ?,
                    GhiChu = ?
                WHERE Id = ?
            """, (
                1 if da_an else 0,
                so_tien_phai_tra,
                ghi_chu,
                chi_tiet_id
            ))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    # ==========================================
    # XÓA BẢN GHI CHẤM CƠM
    # ==========================================
    @staticmethod
    def xoa(chi_tiet_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM ChiTietAn
                WHERE Id = ?
            """, (chi_tiet_id,))

            connection.commit()

            return cursor.rowcount

        finally:
            connection.close()

    # ==========================================
    # KIỂM TRA ĐÃ CHẤM CHƯA
    # ==========================================
    @staticmethod
    def da_co_ban_ghi(
        nguoi_an_id,
        ngay_an_id
    ):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT Id
                FROM ChiTietAn
                WHERE NguoiAnId = ?
                  AND NgayAnId = ?
            """, (
                nguoi_an_id,
                ngay_an_id
            ))

            result = cursor.fetchone()

            return result is not None

        finally:
            connection.close()

    # ==========================================
    # LẤY CHI TIẾT THEO NGÀY
    # ==========================================
    @staticmethod
    def lay_theo_ngay(ngay_an_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    c.Id,
                    c.NguoiAnId,
                    n.HoTen,
                    n.SDT,
                    c.NgayAnId,
                    c.DaAn,
                    c.SoTienPhaiTra,
                    c.GhiChu
                FROM ChiTietAn c
                INNER JOIN NguoiAn n
                    ON c.NguoiAnId = n.Id
                WHERE c.NgayAnId = ?
                ORDER BY n.HoTen
            """, (ngay_an_id,))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================
    # LẤY CHI TIẾT CỦA MỘT NGƯỜI
    # ==========================================
    @staticmethod
    def lay_theo_nguoi(nguoi_an_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    c.Id,
                    c.NguoiAnId,
                    n.HoTen,
                    c.NgayAnId,
                    a.Ngay,
                    c.DaAn,
                    c.SoTienPhaiTra,
                    c.GhiChu
                FROM ChiTietAn c

                INNER JOIN NguoiAn n
                    ON c.NguoiAnId = n.Id

                INNER JOIN NgayAn a
                    ON c.NgayAnId = a.Id

                WHERE c.NguoiAnId = ?

                ORDER BY a.Ngay DESC
            """, (nguoi_an_id,))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================
    # TÍNH TỔNG TIỀN CƠM CỦA MỘT NGÀY
    # ==========================================
    @staticmethod
    def tinh_tong_tien_ngay(ngay_an_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(SoTienPhaiTra),
                        0
                    )
                FROM ChiTietAn
                WHERE NgayAnId = ?
                  AND DaAn = 1
            """, (ngay_an_id,))

            result = cursor.fetchone()

            return result[0] or 0

        finally:
            connection.close()

    # ==========================================
    # ĐẾM SỐ NGƯỜI ĂN TRONG NGÀY
    # ==========================================
    @staticmethod
    def dem_so_nguoi_an(ngay_an_id):

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM ChiTietAn
                WHERE NgayAnId = ?
                  AND DaAn = 1
            """, (ngay_an_id,))

            result = cursor.fetchone()

            return result[0] or 0

        finally:
            connection.close()

    # ==========================================
    # LƯU DANH SÁCH ĐĂNG KÝ ĂN TRONG NGÀY
    # ==========================================
    @staticmethod
    def luu_danh_sach_dang_ky(
        ngay_an_id,
        danh_sach_nguoi_an,
        don_gia
    ):
        """
        danh_sach_nguoi_an:
            danh sách ID những người đăng ký ăn.

        Ví dụ:
            [1, 2, 4, 5]

        Những người có ID nằm trong danh sách
        sẽ được đánh dấu DaAn = 1.

        Những người không nằm trong danh sách
        sẽ được đánh dấu DaAn = 0.
        """

        if don_gia < 0:
            raise ValueError(
                "Đơn giá không được âm."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # ----------------------------------
            # Kiểm tra ngày ăn
            # ----------------------------------
            cursor.execute("""
                SELECT Id
                FROM NgayAn
                WHERE Id = ?
            """, (ngay_an_id,))

            if cursor.fetchone() is None:
                raise ValueError(
                    "Ngày ăn không tồn tại."
                )

            # ----------------------------------
            # Lấy tất cả người ăn
            # ----------------------------------
            cursor.execute("""
                SELECT Id
                FROM NguoiAn
                WHERE DangHoatDong = 1
            """)

            tat_ca_nguoi = cursor.fetchall()

            so_nguoi_dang_ky = 0

            # ----------------------------------
            # Cập nhật từng người
            # ----------------------------------
            for row in tat_ca_nguoi:

                nguoi_an_id = row[0]

                dang_ky = (
                    nguoi_an_id
                    in danh_sach_nguoi_an
                )

                # Nếu đăng ký:
                # DaAn = 1
                # Số tiền = đơn giá
                #
                # Nếu không đăng ký:
                # DaAn = 0
                # Số tiền = 0
                da_an = 1 if dang_ky else 0
                so_tien = don_gia if dang_ky else 0

                # ----------------------------------
                # Kiểm tra đã có bản ghi chưa
                # ----------------------------------
                cursor.execute("""
                    SELECT Id
                    FROM ChiTietAn
                    WHERE NguoiAnId = ?
                      AND NgayAnId = ?
                """, (
                    nguoi_an_id,
                    ngay_an_id
                ))

                ban_ghi = cursor.fetchone()

                if ban_ghi:

                    cursor.execute("""
                        UPDATE ChiTietAn
                        SET
                            DaAn = ?,
                            SoTienPhaiTra = ?
                        WHERE Id = ?
                    """, (
                        da_an,
                        so_tien,
                        ban_ghi[0]
                    ))

                else:

                    cursor.execute("""
                        INSERT INTO ChiTietAn (
                            NguoiAnId,
                            NgayAnId,
                            DaAn,
                            SoTienPhaiTra
                        )
                        VALUES (?, ?, ?, ?)
                    """, (
                        nguoi_an_id,
                        ngay_an_id,
                        da_an,
                        so_tien
                    ))

                if dang_ky:
                    so_nguoi_dang_ky += 1

            connection.commit()

            return so_nguoi_dang_ky

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()