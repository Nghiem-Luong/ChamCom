# -*- coding: utf-8 -*-

from datetime import date, timedelta

from Database.database import get_connection


class TraCuuModel:
    """
    Model phục vụ:
        - Hỗ trợ & tra cứu
        - Thống kê chấm cơm
        - Theo người
        - So sánh nhiều người
        - Theo bộ phận
        - Công nợ
        - Đối chiếu ăn / tiền
        - Phát hiện bất thường
        - Kiểm tra dữ liệu
        - Tổng hợp

    Database:
        NguoiAn
        BoPhan
        NgayAn
        ChiTietAn
        GiaoDichNopTien

    Quy ước:
        - ChiTietAn.DaAn = 1: đã ăn
        - ChiTietAn.DaAn = 0: chưa ăn
        - Số suất = số dòng ChiTietAn có DaAn = 1
        - Số người ăn = COUNT(DISTINCT NguoiAnId)
        - Tiền phải trả = SUM(ChiTietAn.SoTienPhaiTra)
        - Tiền đã nộp = SUM(GiaoDichNopTien.SoTien)
        - Còn nợ = MAX(Tiền phải trả - Tiền đã nộp, 0)
        - Nộp vượt = MAX(Tiền đã nộp - Tiền phải trả, 0)

    Lưu ý:
        Các truy vấn tiền ăn và tiền nộp được tách riêng,
        tránh lỗi nhân bản dữ liệu khi JOIN nhiều bảng.
    """

    # ==========================================================
    # HÀM TIỆN ÍCH
    # ==========================================================

    @staticmethod
    def _lay_ngay_hom_nay():
        return date.today().isoformat()

    @staticmethod
    def _lay_ngay_hom_qua():
        return (
            date.today() - timedelta(days=1)
        ).isoformat()

    @staticmethod
    def _lay_ngay_7_ngay_truoc():
        return (
            date.today() - timedelta(days=6)
        ).isoformat()

    @staticmethod
    def _lay_ngay_dau_thang():
        hom_nay = date.today()
        return date(
            hom_nay.year,
            hom_nay.month,
            1
        ).isoformat()

    @staticmethod
    def _chuan_hoa_khoang_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        if not tu_ngay:
            tu_ngay = TraCuuModel._lay_ngay_hom_nay()

        if not den_ngay:
            den_ngay = tu_ngay

        try:
            ngay_1 = date.fromisoformat(
                str(tu_ngay)[:10]
            )
            ngay_2 = date.fromisoformat(
                str(den_ngay)[:10]
            )
        except (
            ValueError,
            TypeError
        ):
            return (
                TraCuuModel._lay_ngay_hom_nay(),
                TraCuuModel._lay_ngay_hom_nay()
            )

        if ngay_1 > ngay_2:
            ngay_1, ngay_2 = ngay_2, ngay_1

        return (
            ngay_1.isoformat(),
            ngay_2.isoformat()
        )

    @staticmethod
    def _placeholders(values):
        return ",".join(
            ["?"] * len(values)
        )

    @staticmethod
    def _chuan_hoa_ids(
        danh_sach_ids
    ):
        if danh_sach_ids is None:
            return []

        if not isinstance(
            danh_sach_ids,
            (list, tuple, set)
        ):
            danh_sach_ids = [
                danh_sach_ids
            ]

        ket_qua = []

        for value in danh_sach_ids:
            try:
                value = int(value)
            except (
                TypeError,
                ValueError
            ):
                continue

            if value not in ket_qua:
                ket_qua.append(value)

        return ket_qua

    @staticmethod
    def _ngay_nop_condition(alias="g"):
        """
        NgayNop có thể lưu:
            2026-09-28
        hoặc:
            2026-09-28 10:20:00

        Lấy 10 ký tự đầu để lọc ngày ổn định.
        """
        return (
            f"substr(COALESCE({alias}.NgayNop, ''), 1, 10)"
        )

    # ==========================================================
    # DANH SÁCH NGƯỜI
    # ==========================================================

    @staticmethod
    def lay_danh_sach_nguoi():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    n.BoPhanId,
                    COALESCE(b.TenBoPhan, 'Chưa có bộ phận')
                FROM NguoiAn n
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                WHERE n.DangHoatDong = 1
                ORDER BY n.HoTen COLLATE NOCASE
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_tat_ca_nguoi():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    n.DangHoatDong,
                    n.SDT,
                    n.BoPhanId,
                    COALESCE(b.TenBoPhan, 'Chưa có bộ phận')
                FROM NguoiAn n
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                ORDER BY n.HoTen COLLATE NOCASE
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_nguoi_theo_id(
        nguoi_an_id
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    n.BoPhanId,
                    COALESCE(b.TenBoPhan, 'Chưa có bộ phận'),
                    n.DangHoatDong,
                    n.SDT
                FROM NguoiAn n
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                WHERE n.Id = ?
                LIMIT 1
            """, (nguoi_an_id,))

            return cursor.fetchone()

        finally:
            connection.close()

    # ==========================================================
    # BỘ PHẬN
    # ==========================================================

    @staticmethod
    def lay_danh_sach_bo_phan():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    TenBoPhan
                FROM BoPhan
                ORDER BY TenBoPhan COLLATE NOCASE
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # NGÀY ĂN
    # ==========================================================

    @staticmethod
    def lay_ngay_an_id(
        ngay
    ):
        ngay = str(ngay)[:10]

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT Id
                FROM NgayAn
                WHERE substr(Ngay, 1, 10) = ?
                LIMIT 1
            """, (ngay,))

            row = cursor.fetchone()

            return row[0] if row else None

        finally:
            connection.close()

    # ==========================================================
    # 1. CHẤM CƠM - TỔNG QUAN
    # ==========================================================

    @staticmethod
    def dem_nguoi_an_theo_khoang(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(DISTINCT c.NguoiAnId)
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON n.Id = c.NgayAnId
                WHERE c.DaAn = 1
                  AND substr(n.Ngay, 1, 10)
                      BETWEEN ? AND ?
            """, (
                tu_ngay,
                den_ngay
            ))

            row = cursor.fetchone()

            return int(
                row[0] or 0
            )

        finally:
            connection.close()

    @staticmethod
    def dem_nguoi_an_hom_nay():
        ngay = TraCuuModel._lay_ngay_hom_nay()

        return TraCuuModel.dem_nguoi_an_theo_khoang(
            ngay,
            ngay
        )

    @staticmethod
    def lay_nguoi_da_an_theo_khoang(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    COALESCE(b.TenBoPhan, 'Chưa có bộ phận') AS BoPhan,
                    COUNT(c.Id) AS SoLanAn,
                    COALESCE(
                        SUM(c.SoTienPhaiTra),
                        0
                    ) AS TongTien
                FROM ChiTietAn c
                INNER JOIN NgayAn na
                    ON na.Id = c.NgayAnId
                INNER JOIN NguoiAn n
                    ON n.Id = c.NguoiAnId
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                WHERE c.DaAn = 1
                  AND substr(na.Ngay, 1, 10)
                      BETWEEN ? AND ?
                GROUP BY
                    n.Id,
                    n.HoTen,
                    b.TenBoPhan
                ORDER BY
                    SoLanAn DESC,
                    n.HoTen COLLATE NOCASE
            """, (
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_nguoi_chua_an_theo_ngay(
        ngay
    ):
        ngay = str(ngay)[:10]

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    COALESCE(b.TenBoPhan, 'Chưa có bộ phận')
                FROM NguoiAn n
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                WHERE n.DangHoatDong = 1
                  AND NOT EXISTS (
                      SELECT 1
                      FROM ChiTietAn c
                      INNER JOIN NgayAn na
                          ON na.Id = c.NgayAnId
                      WHERE c.NguoiAnId = n.Id
                        AND c.DaAn = 1
                        AND substr(na.Ngay, 1, 10) = ?
                  )
                ORDER BY n.HoTen COLLATE NOCASE
            """, (ngay,))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_nguoi_chua_an_hom_nay():
        return TraCuuModel.lay_nguoi_chua_an_theo_ngay(
            TraCuuModel._lay_ngay_hom_nay()
        )

    @staticmethod
    def lay_nguoi_chua_an_theo_khoang(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    COALESCE(b.TenBoPhan, 'Chưa có bộ phận')
                FROM NguoiAn n
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                WHERE n.DangHoatDong = 1
                  AND NOT EXISTS (
                      SELECT 1
                      FROM ChiTietAn c
                      INNER JOIN NgayAn na
                          ON na.Id = c.NgayAnId
                      WHERE c.NguoiAnId = n.Id
                        AND c.DaAn = 1
                        AND substr(na.Ngay, 1, 10)
                            BETWEEN ? AND ?
                  )
                ORDER BY n.HoTen COLLATE NOCASE
            """, (
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_nguoi_chua_tung_an(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.lay_nguoi_chua_an_theo_khoang(
            tu_ngay,
            den_ngay
        )

    # ==========================================================
    # SUẤT ĂN
    # ==========================================================

    @staticmethod
    def tong_so_suat_an(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON n.Id = c.NgayAnId
                WHERE c.DaAn = 1
                  AND substr(n.Ngay, 1, 10)
                      BETWEEN ? AND ?
            """, (
                tu_ngay,
                den_ngay
            ))

            row = cursor.fetchone()

            return int(row[0] or 0)

        finally:
            connection.close()

    @staticmethod
    def tong_tien_an_theo_khoang(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(c.SoTienPhaiTra),
                        0
                    )
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON n.Id = c.NgayAnId
                WHERE c.DaAn = 1
                  AND substr(n.Ngay, 1, 10)
                      BETWEEN ? AND ?
            """, (
                tu_ngay,
                den_ngay
            ))

            row = cursor.fetchone()

            return float(row[0] or 0)

        finally:
            connection.close()

    @staticmethod
    def tong_tien_an_hom_nay():
        ngay = TraCuuModel._lay_ngay_hom_nay()

        return TraCuuModel.tong_tien_an_theo_khoang(
            ngay,
            ngay
        )

    # ==========================================================
    # NGƯỜI ĂN NHIỀU / ÍT
    # ==========================================================

    @staticmethod
    def lay_nguoi_an_nhieu_lan(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_nguoi_da_an_theo_khoang(
            tu_ngay,
            den_ngay
        )

        return [
            (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            )
            for row in rows
            if row[3] > 1
        ]

    @staticmethod
    def lay_nguoi_an_mot_suat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_nguoi_da_an_theo_khoang(
            tu_ngay,
            den_ngay
        )

        return [
            (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            )
            for row in rows
            if row[3] == 1
        ]

    @staticmethod
    def lay_nguoi_an_nhieu_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_nguoi_da_an_theo_khoang(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        max_value = max(
            row[3]
            for row in rows
        )

        return [
            row
            for row in rows
            if row[3] == max_value
        ]

    @staticmethod
    def lay_nguoi_an_it_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_nguoi_da_an_theo_khoang(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        min_value = min(
            row[3]
            for row in rows
        )

        return [
            row
            for row in rows
            if row[3] == min_value
        ]

    # ==========================================================
    # THỐNG KÊ THEO NGÀY
    # ==========================================================

    @staticmethod
    def thong_ke_an_theo_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    substr(na.Ngay, 1, 10) AS Ngay,
                    COUNT(c.Id) AS SoSuat,
                    COUNT(
                        DISTINCT c.NguoiAnId
                    ) AS SoNguoi,
                    COALESCE(
                        SUM(c.SoTienPhaiTra),
                        0
                    ) AS TongTien
                FROM ChiTietAn c
                INNER JOIN NgayAn na
                    ON na.Id = c.NgayAnId
                WHERE c.DaAn = 1
                  AND substr(na.Ngay, 1, 10)
                      BETWEEN ? AND ?
                GROUP BY substr(na.Ngay, 1, 10)
                ORDER BY Ngay
            """, (
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def thong_ke_theo_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

    @staticmethod
    def trung_binh_suat_moi_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        tong = sum(
            row[1]
            for row in rows
        )

        trung_binh = tong / len(rows)

        return [
            (
                "Khoảng thời gian",
                len(rows),
                tong,
                round(trung_binh, 2)
            )
        ]

    @staticmethod
    def trung_binh_suat_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.trung_binh_suat_moi_ngay(
            tu_ngay,
            den_ngay
        )

    @staticmethod
    def thong_ke_tien_theo_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        return [
            (
                row[0],
                row[3],
                row[1],
                row[2]
            )
            for row in rows
        ]

    @staticmethod
    def thong_ke_nguoi_theo_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        return [
            (
                row[0],
                row[2],
                row[1],
                row[3]
            )
            for row in rows
        ]

    @staticmethod
    def trung_binh_tien_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        tong_tien = sum(
            float(row[3] or 0)
            for row in rows
        )

        trung_binh = (
            tong_tien / len(rows)
        )

        return [
            (
                "Khoảng thời gian",
                len(rows),
                tong_tien,
                round(trung_binh, 2)
            )
        ]

    @staticmethod
    def ngay_nhieu_nguoi_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        max_value = max(
            row[2]
            for row in rows
        )

        return [
            row
            for row in rows
            if row[2] == max_value
        ]

    @staticmethod
    def ngay_it_nguoi_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        min_value = min(
            row[2]
            for row in rows
        )

        return [
            row
            for row in rows
            if row[2] == min_value
        ]

    @staticmethod
    def ngay_tien_cao_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        max_value = max(
            float(row[3] or 0)
            for row in rows
        )

        return [
            row
            for row in rows
            if float(row[3] or 0) == max_value
        ]

    @staticmethod
    def ngay_tien_thap_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        min_value = min(
            float(row[3] or 0)
            for row in rows
        )

        return [
            row
            for row in rows
            if float(row[3] or 0) == min_value
        ]

    @staticmethod
    def lay_ngay_an_nhieu_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._lay_ngay_cuc_tri(
            tu_ngay,
            den_ngay,
            cot_index=1,
            lon_hon=True
        )

    @staticmethod
    def lay_ngay_an_it_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._lay_ngay_cuc_tri(
            tu_ngay,
            den_ngay,
            cot_index=1,
            lon_hon=False
        )

    @staticmethod
    def _lay_ngay_cuc_tri(
        tu_ngay,
        den_ngay,
        cot_index,
        lon_hon=True
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        gia_tri = [
            row[cot_index]
            for row in rows
        ]

        muc = (
            max(gia_tri)
            if lon_hon
            else min(gia_tri)
        )

        return [
            row
            for row in rows
            if row[cot_index] == muc
        ]

    # ==========================================================
    # THEO NGƯỜI
    # ==========================================================

    @staticmethod
    def dem_so_lan_an(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON n.Id = c.NgayAnId
                WHERE c.NguoiAnId = ?
                  AND c.DaAn = 1
                  AND substr(n.Ngay, 1, 10)
                      BETWEEN ? AND ?
            """, (
                nguoi_an_id,
                tu_ngay,
                den_ngay
            ))

            row = cursor.fetchone()

            return int(row[0] or 0)

        finally:
            connection.close()

    @staticmethod
    def tong_da_nop_nguoi(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            condition = (
                TraCuuModel._ngay_nop_condition("g")
            )

            cursor.execute(f"""
                SELECT
                    COALESCE(
                        SUM(g.SoTien),
                        0
                    )
                FROM GiaoDichNopTien g
                WHERE g.NguoiAnId = ?
                  AND {condition}
                      BETWEEN ? AND ?
            """, (
                nguoi_an_id,
                tu_ngay,
                den_ngay
            ))

            row = cursor.fetchone()

            return float(row[0] or 0)

        finally:
            connection.close()

    @staticmethod
    def kiem_tra_da_an(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):
        return (
            TraCuuModel.dem_so_lan_an(
                nguoi_an_id,
                tu_ngay,
                den_ngay
            ) > 0
        )

    @staticmethod
    def kiem_tra_da_an_hom_nay(
        nguoi_an_id
    ):
        ngay = TraCuuModel._lay_ngay_hom_nay()

        return TraCuuModel.kiem_tra_da_an(
            nguoi_an_id,
            ngay,
            ngay
        )

    # ==========================================================
    # TỔNG QUAN MỘT NGƯỜI
    # ==========================================================

    @staticmethod
    def lay_tong_quan_nguoi(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):
        nguoi = TraCuuModel.lay_nguoi_theo_id(
            nguoi_an_id
        )

        if not nguoi:
            return None

        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        tong_phai_tra = (
            TraCuuModel.tong_phai_tra_nguoi_value(
                nguoi_an_id,
                tu_ngay,
                den_ngay
            )
        )

        tong_da_nop = (
            TraCuuModel.tong_da_nop_nguoi(
                nguoi_an_id,
                tu_ngay,
                den_ngay
            )
        )

        so_lan_an = (
            TraCuuModel.dem_so_lan_an(
                nguoi_an_id,
                tu_ngay,
                den_ngay
            )
        )

        con_no = max(
            tong_phai_tra - tong_da_nop,
            0
        )

        du = max(
            tong_da_nop - tong_phai_tra,
            0
        )

        return {
            "id": nguoi[0],
            "ho_ten": nguoi[1],
            "bo_phan_id": nguoi[2],
            "bo_phan": nguoi[3],
            "dang_hoat_dong": nguoi[4],
            "sdt": nguoi[5],
            "tong_phai_tra": tong_phai_tra,
            "tong_da_nop": tong_da_nop,
            "con_no": con_no,
            "du": du,
            "so_lan_an": so_lan_an,
            "da_an": so_lan_an > 0,
            "thanh_toan_du": (
                tong_phai_tra > 0
                and tong_da_nop >= tong_phai_tra
            )
        }

    @staticmethod
    def tong_phai_tra_nguoi_value(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(c.SoTienPhaiTra),
                        0
                    )
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON n.Id = c.NgayAnId
                WHERE c.NguoiAnId = ?
                  AND c.DaAn = 1
                  AND substr(n.Ngay, 1, 10)
                      BETWEEN ? AND ?
            """, (
                nguoi_an_id,
                tu_ngay,
                den_ngay
            ))

            row = cursor.fetchone()

            return float(row[0] or 0)

        finally:
            connection.close()

    # ==========================================================
    # TỔNG PHẢI TRẢ NHIỀU NGƯỜI
    # ==========================================================

    @staticmethod
    def tong_phai_tra_nguoi(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        ids = TraCuuModel._chuan_hoa_ids(
            danh_sach_nguoi_ids
        )

        data = []

        for nguoi_id in ids:

            nguoi = TraCuuModel.lay_nguoi_theo_id(
                nguoi_id
            )

            if not nguoi:
                continue

            value = (
                TraCuuModel
                .tong_phai_tra_nguoi_value(
                    nguoi_id,
                    tu_ngay,
                    den_ngay
                )
            )

            data.append({
                "ID": nguoi[0],
                "Họ tên": nguoi[1],
                "Bộ phận": nguoi[3],
                "Tổng phải trả": value
            })

        return data

    # ==========================================================
    # CÔNG NỢ MỘT / NHIỀU NGƯỜI
    # ==========================================================

    @staticmethod
    def lay_cong_no_nguoi(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        ids = TraCuuModel._chuan_hoa_ids(
            danh_sach_nguoi_ids
        )

        if not ids:
            return []

        data = []

        for nguoi_id in ids:

            item = TraCuuModel.lay_tong_quan_nguoi(
                nguoi_id,
                tu_ngay,
                den_ngay
            )

            if not item:
                continue

            data.append({
                "ID": item["id"],
                "Họ tên": item["ho_ten"],
                "Bộ phận": item["bo_phan"],
                "Tổng phải trả": item["tong_phai_tra"],
                "Tổng đã nộp": item["tong_da_nop"],
                "Còn nợ": item["con_no"],
                "Dư": item["du"]
            })

        return data

    @staticmethod
    def lay_nguoi_thanh_toan_du(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_cong_no_nguoi(
            danh_sach_nguoi_ids,
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Tổng phải trả"] > 0
            and row["Tổng đã nộp"]
            >= row["Tổng phải trả"]
        ]

    @staticmethod
    def lay_nguoi_nop_vuot(
        *args
    ):
        """
        Hỗ trợ 2 kiểu gọi:

        1.
            lay_nguoi_nop_vuot(
                danh_sach_ids,
                tu_ngay,
                den_ngay
            )

        2.
            lay_nguoi_nop_vuot(
                tu_ngay,
                den_ngay
            )
        """

        if len(args) == 3:
            danh_sach_ids, tu_ngay, den_ngay = args

        elif len(args) == 2:
            danh_sach_ids = None
            tu_ngay, den_ngay = args

        else:
            danh_sach_ids = None
            tu_ngay = None
            den_ngay = None

        if danh_sach_ids is None:
            ids = [
                row[0]
                for row in TraCuuModel.lay_tat_ca_nguoi()
                if row[2] == 1
            ]
        else:
            ids = TraCuuModel._chuan_hoa_ids(
                danh_sach_ids
            )

        rows = TraCuuModel.lay_cong_no_nguoi(
            ids,
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Dư"] > 0
        ]

    # ==========================================================
    # CÔNG NỢ TOÀN BỘ
    # ==========================================================

    @staticmethod
    def lay_danh_sach_dang_no(
        tu_ngay=None,
        den_ngay=None
    ):
        all_people = (
            TraCuuModel.lay_danh_sach_nguoi()
        )

        data = []

        for person in all_people:

            item = TraCuuModel.lay_tong_quan_nguoi(
                person[0],
                tu_ngay,
                den_ngay
            )

            if not item:
                continue

            if item["con_no"] > 0:

                data.append((
                    item["id"],
                    item["ho_ten"],
                    item["bo_phan"],
                    item["tong_phai_tra"],
                    item["tong_da_nop"]
                ))

        return data

    @staticmethod
    def tong_cong_no(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_danh_sach_dang_no(
            tu_ngay,
            den_ngay
        )

        return sum(
            max(
                float(row[3] or 0)
                - float(row[4] or 0),
                0
            )
            for row in rows
        )

    @staticmethod
    def dem_nguoi_dang_no(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_danh_sach_dang_no(
            tu_ngay,
            den_ngay
        )

        return len(rows)

    @staticmethod
    def lay_nguoi_no_nhieu_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_danh_sach_dang_no(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        rows = [
            (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                max(
                    row[3] - row[4],
                    0
                )
            )
            for row in rows
        ]

        muc = max(
            row[5]
            for row in rows
        )

        return [
            row
            for row in rows
            if row[5] == muc
        ]

    @staticmethod
    def lay_nguoi_no_it_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_danh_sach_dang_no(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        rows = [
            (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                max(
                    row[3] - row[4],
                    0
                )
            )
            for row in rows
        ]

        muc = min(
            row[5]
            for row in rows
        )

        return [
            row
            for row in rows
            if row[5] == muc
        ]

    # ==========================================================
    # CÔNG NỢ - CHƯA NỘP / NỘP THIẾU / ĐỦ / VƯỢT
    # ==========================================================

    @staticmethod
    def _lay_toan_bo_cong_no(
        tu_ngay=None,
        den_ngay=None
    ):
        all_people = (
            TraCuuModel.lay_danh_sach_nguoi()
        )

        data = []

        for person in all_people:

            item = TraCuuModel.lay_tong_quan_nguoi(
                person[0],
                tu_ngay,
                den_ngay
            )

            if not item:
                continue

            data.append({
                "ID": item["id"],
                "Họ tên": item["ho_ten"],
                "Bộ phận": item["bo_phan"],
                "Tổng phải trả": item["tong_phai_tra"],
                "Tổng đã nộp": item["tong_da_nop"],
                "Còn nợ": item["con_no"],
                "Dư": item["du"],
                "Số suất": item["so_lan_an"]
            })

        return data

    @staticmethod
    def lay_nguoi_an_nhung_chua_nop(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Số suất"] > 0
            and row["Tổng phải trả"] > row["Tổng đã nộp"]
        ]

    @staticmethod
    def lay_nguoi_an_nop_thieu(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Số suất"] > 0
            and row["Tổng đã nộp"] > 0
            and row["Còn nợ"] > 0
        ]

    @staticmethod
    def lay_nguoi_an_nhung_con_no(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Số suất"] > 0
            and row["Còn nợ"] > 0
        ]

    @staticmethod
    def lay_nguoi_nop_du(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Tổng phải trả"] > 0
            and row["Tổng đã nộp"]
            >= row["Tổng phải trả"]
        ]

    @staticmethod
    def lay_nguoi_chua_tung_nop(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Tổng phải trả"] > 0
            and row["Tổng đã nộp"] <= 0
        ]

    @staticmethod
    def lay_nguoi_da_nop_nhung_chua_an(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            {
                "ID": row["ID"],
                "Họ tên": row["Họ tên"],
                "Bộ phận": row["Bộ phận"],
                "Đã nộp": row["Tổng đã nộp"]
            }
            for row in rows
            if row["Tổng đã nộp"] > 0
            and row["Số suất"] == 0
        ]

    # ==========================================================
    # LỊCH SỬ ĂN
    # ==========================================================

    @staticmethod
    def lay_lich_su_an(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    substr(na.Ngay, 1, 10) AS Ngay,
                    c.DaAn,
                    COALESCE(
                        c.SoTienPhaiTra,
                        0
                    ),
                    c.GhiChu
                FROM ChiTietAn c
                INNER JOIN NgayAn na
                    ON na.Id = c.NgayAnId
                WHERE c.NguoiAnId = ?
                  AND substr(na.Ngay, 1, 10)
                      BETWEEN ? AND ?
                ORDER BY Ngay DESC, c.Id DESC
            """, (
                nguoi_an_id,
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # LỊCH SỬ NỘP TIỀN
    # ==========================================================

    @staticmethod
    def lay_lich_su_nop_tien(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            condition = (
                TraCuuModel._ngay_nop_condition("g")
            )

            cursor.execute(f"""
                SELECT
                    substr(
                        COALESCE(g.NgayNop, ''),
                        1,
                        19
                    ),
                    COALESCE(g.SoTien, 0),
                    g.HinhThuc,
                    g.GhiChu
                FROM GiaoDichNopTien g
                WHERE g.NguoiAnId = ?
                  AND {condition}
                      BETWEEN ? AND ?
                ORDER BY
                    g.Id DESC
            """, (
                nguoi_an_id,
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # LẦN ĂN GẦN NHẤT
    # ==========================================================

    @staticmethod
    def lay_lan_an_gan_nhat(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        ids = TraCuuModel._chuan_hoa_ids(
            danh_sach_nguoi_ids
        )

        data = []

        for nguoi_id in ids:

            nguoi = TraCuuModel.lay_nguoi_theo_id(
                nguoi_id
            )

            if not nguoi:
                continue

            rows = TraCuuModel.lay_lich_su_an(
                nguoi_id,
                tu_ngay,
                den_ngay
            )

            da_an = [
                row
                for row in rows
                if row[1]
            ]

            data.append({
                "ID": nguoi[0],
                "Họ tên": nguoi[1],
                "Bộ phận": nguoi[3],
                "Lần ăn gần nhất": (
                    da_an[0][0]
                    if da_an
                    else None
                )
            })

        return data

    # ==========================================================
    # LẦN NỘP GẦN NHẤT
    # ==========================================================

    @staticmethod
    def lay_lan_nop_gan_nhat(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        ids = TraCuuModel._chuan_hoa_ids(
            danh_sach_nguoi_ids
        )

        data = []

        for nguoi_id in ids:

            nguoi = TraCuuModel.lay_nguoi_theo_id(
                nguoi_id
            )

            if not nguoi:
                continue

            rows = TraCuuModel.lay_lich_su_nop_tien(
                nguoi_id,
                tu_ngay,
                den_ngay
            )

            data.append({
                "ID": nguoi[0],
                "Họ tên": nguoi[1],
                "Bộ phận": nguoi[3],
                "Lần nộp gần nhất": (
                    rows[0][0]
                    if rows
                    else None
                )
            })

        return data

    # ==========================================================
    # NGÀY CHƯA ĂN
    # ==========================================================

    @staticmethod
    def lay_ngay_chua_an(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        ids = TraCuuModel._chuan_hoa_ids(
            danh_sach_nguoi_ids
        )

        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        if not ids:
            return []

        connection = get_connection()

        try:
            cursor = connection.cursor()

            placeholders = (
                TraCuuModel._placeholders(ids)
            )

            cursor.execute(f"""
                SELECT
                    n.Id,
                    n.HoTen,
                    d.Ngay
                FROM NguoiAn n
                CROSS JOIN (
                    SELECT DISTINCT
                        substr(Ngay, 1, 10) AS Ngay
                    FROM NgayAn
                    WHERE substr(Ngay, 1, 10)
                        BETWEEN ? AND ?
                ) d
                LEFT JOIN (
                    SELECT
                        c.NguoiAnId,
                        substr(na.Ngay, 1, 10) AS Ngay
                    FROM ChiTietAn c
                    INNER JOIN NgayAn na
                        ON na.Id = c.NgayAnId
                    WHERE c.DaAn = 1
                      AND substr(na.Ngay, 1, 10)
                          BETWEEN ? AND ?
                ) an
                    ON an.NguoiAnId = n.Id
                   AND an.Ngay = d.Ngay
                WHERE n.Id IN ({placeholders})
                  AND an.NguoiAnId IS NULL
                ORDER BY
                    n.HoTen COLLATE NOCASE,
                    d.Ngay
            """, (
                tu_ngay,
                den_ngay,
                tu_ngay,
                den_ngay,
                *ids
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # ĂN NHIỀU LẦN TRONG NGÀY
    # ==========================================================

    @staticmethod
    def lay_an_nhieu_lan_trong_ngay(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        ids = TraCuuModel._chuan_hoa_ids(
            danh_sach_nguoi_ids
        )

        if not ids:
            return []

        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            placeholders = (
                TraCuuModel._placeholders(ids)
            )

            cursor.execute(f"""
                SELECT
                    n.Id,
                    n.HoTen,
                    COALESCE(
                        b.TenBoPhan,
                        'Chưa có bộ phận'
                    ),
                    substr(na.Ngay, 1, 10),
                    COUNT(c.Id) AS SoLan
                FROM ChiTietAn c
                INNER JOIN NgayAn na
                    ON na.Id = c.NgayAnId
                INNER JOIN NguoiAn n
                    ON n.Id = c.NguoiAnId
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                WHERE c.DaAn = 1
                  AND c.NguoiAnId IN ({placeholders})
                  AND substr(na.Ngay, 1, 10)
                      BETWEEN ? AND ?
                GROUP BY
                    n.Id,
                    n.HoTen,
                    b.TenBoPhan,
                    substr(na.Ngay, 1, 10)
                HAVING COUNT(c.Id) > 1
                ORDER BY
                    substr(na.Ngay, 1, 10) DESC,
                    SoLan DESC
            """, (
                *ids,
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # SO SÁNH NHIỀU NGƯỜI
    # ==========================================================

    @staticmethod
    def _lay_du_lieu_so_sanh_nguoi(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        ids = TraCuuModel._chuan_hoa_ids(
            danh_sach_nguoi_ids
        )

        data = []

        for nguoi_id in ids:

            item = TraCuuModel.lay_tong_quan_nguoi(
                nguoi_id,
                tu_ngay,
                den_ngay
            )

            if not item:
                continue

            connection = get_connection()

            try:
                cursor = connection.cursor()

                tu, den = (
                    TraCuuModel._chuan_hoa_khoang_ngay(
                        tu_ngay,
                        den_ngay
                    )
                )

                cursor.execute("""
                    SELECT COUNT(DISTINCT substr(na.Ngay, 1, 10))
                    FROM ChiTietAn c
                    INNER JOIN NgayAn na
                        ON na.Id = c.NgayAnId
                    WHERE c.NguoiAnId = ?
                      AND c.DaAn = 1
                      AND substr(na.Ngay, 1, 10)
                          BETWEEN ? AND ?
                """, (
                    nguoi_id,
                    tu,
                    den
                ))

                row = cursor.fetchone()

                so_ngay_an = int(
                    row[0] or 0
                )

            finally:
                connection.close()

            data.append({
                "ID": item["id"],
                "Họ tên": item["ho_ten"],
                "Bộ phận": item["bo_phan"],
                "Số suất": item["so_lan_an"],
                "Số ngày ăn": so_ngay_an,
                "Tổng phải trả": item["tong_phai_tra"],
                "Đã nộp": item["tong_da_nop"],
                "Còn nợ": item["con_no"],
                "Dư": item["du"]
            })

        return data

    @staticmethod
    def so_sanh_so_suat(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return [
            {
                "ID": row["ID"],
                "Họ tên": row["Họ tên"],
                "Bộ phận": row["Bộ phận"],
                "Số suất": row["Số suất"]
            }
            for row in TraCuuModel._lay_du_lieu_so_sanh_nguoi(
                danh_sach_nguoi_ids,
                tu_ngay,
                den_ngay
            )
        ]

    @staticmethod
    def so_sanh_phai_tra(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return [
            {
                "ID": row["ID"],
                "Họ tên": row["Họ tên"],
                "Bộ phận": row["Bộ phận"],
                "Tổng phải trả": row["Tổng phải trả"]
            }
            for row in TraCuuModel._lay_du_lieu_so_sanh_nguoi(
                danh_sach_nguoi_ids,
                tu_ngay,
                den_ngay
            )
        ]

    @staticmethod
    def so_sanh_da_nop(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return [
            {
                "ID": row["ID"],
                "Họ tên": row["Họ tên"],
                "Bộ phận": row["Bộ phận"],
                "Đã nộp": row["Đã nộp"]
            }
            for row in TraCuuModel._lay_du_lieu_so_sanh_nguoi(
                danh_sach_nguoi_ids,
                tu_ngay,
                den_ngay
            )
        ]

    @staticmethod
    def so_sanh_cong_no(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return [
            {
                "ID": row["ID"],
                "Họ tên": row["Họ tên"],
                "Bộ phận": row["Bộ phận"],
                "Tổng phải trả": row["Tổng phải trả"],
                "Đã nộp": row["Đã nộp"],
                "Còn nợ": row["Còn nợ"]
            }
            for row in TraCuuModel._lay_du_lieu_so_sanh_nguoi(
                danh_sach_nguoi_ids,
                tu_ngay,
                den_ngay
            )
        ]

    @staticmethod
    def so_sanh_so_ngay_an(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return [
            {
                "ID": row["ID"],
                "Họ tên": row["Họ tên"],
                "Bộ phận": row["Bộ phận"],
                "Số ngày ăn": row["Số ngày ăn"]
            }
            for row in TraCuuModel._lay_du_lieu_so_sanh_nguoi(
                danh_sach_nguoi_ids,
                tu_ngay,
                den_ngay
            )
        ]

    @staticmethod
    def so_sanh_suat_va_tien(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._lay_du_lieu_so_sanh_nguoi(
            danh_sach_nguoi_ids,
            tu_ngay,
            den_ngay
        )

    # ==========================================================
    # CÁC HÀM "AI HƠN / ÍT HƠN"
    # ==========================================================

    @staticmethod
    def _so_sanh_theo_chi_so(
        danh_sach_nguoi_ids,
        tu_ngay,
        den_ngay,
        key,
        lon_hon=True
    ):
        rows = (
            TraCuuModel
            ._lay_du_lieu_so_sanh_nguoi(
                danh_sach_nguoi_ids,
                tu_ngay,
                den_ngay
            )
        )

        if len(rows) < 2:
            return rows

        muc = max(
            row[key]
            for row in rows
        )

        if not lon_hon:
            muc = min(
                row[key]
                for row in rows
            )

        return [
            row
            for row in rows
            if row[key] == muc
        ]

    @staticmethod
    def ai_an_nhieu_hon(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._so_sanh_theo_chi_so(
            danh_sach_nguoi_ids,
            tu_ngay,
            den_ngay,
            "Số suất",
            True
        )

    @staticmethod
    def ai_an_it_hon(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._so_sanh_theo_chi_so(
            danh_sach_nguoi_ids,
            tu_ngay,
            den_ngay,
            "Số suất",
            False
        )

    @staticmethod
    def ai_nop_nhieu_hon(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._so_sanh_theo_chi_so(
            danh_sach_nguoi_ids,
            tu_ngay,
            den_ngay,
            "Đã nộp",
            True
        )

    @staticmethod
    def ai_no_nhieu_hon(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._so_sanh_theo_chi_so(
            danh_sach_nguoi_ids,
            tu_ngay,
            den_ngay,
            "Còn nợ",
            True
        )

    # ==========================================================
    # BỘ PHẬN
    # ==========================================================

    @staticmethod
    def lay_thong_ke_bo_phan(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    b.Id,
                    b.TenBoPhan,

                    COUNT(
                        DISTINCT CASE
                            WHEN n.DangHoatDong = 1
                            THEN n.Id
                        END
                    ) AS SoNguoi,

                    COUNT(
                        CASE
                            WHEN c.DaAn = 1
                            THEN c.Id
                        END
                    ) AS SoSuat,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN c.DaAn = 1
                                THEN c.SoTienPhaiTra
                                ELSE 0
                            END
                        ),
                        0
                    ) AS TongTien

                FROM BoPhan b

                LEFT JOIN NguoiAn n
                    ON n.BoPhanId = b.Id

                LEFT JOIN ChiTietAn c
                    ON c.NguoiAnId = n.Id
                   AND c.DaAn = 1
                   AND c.NgayAnId IN (
                       SELECT na.Id
                       FROM NgayAn na
                       WHERE substr(na.Ngay, 1, 10)
                           BETWEEN ? AND ?
                   )

                GROUP BY
                    b.Id,
                    b.TenBoPhan

                ORDER BY
                    b.TenBoPhan COLLATE NOCASE
            """, (
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_thong_ke_bo_phan_day_du(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan(
            tu_ngay,
            den_ngay
        )

        result = []

        for row in rows:

            bo_phan_id = row[0]

            connection = get_connection()

            try:
                cursor = connection.cursor()

                tu, den = (
                    TraCuuModel._chuan_hoa_khoang_ngay(
                        tu_ngay,
                        den_ngay
                    )
                )

                condition = (
                    TraCuuModel._ngay_nop_condition("g")
                )

                cursor.execute(f"""
                    SELECT
                        COALESCE(
                            SUM(g.SoTien),
                            0
                        )
                    FROM GiaoDichNopTien g
                    INNER JOIN NguoiAn n
                        ON n.Id = g.NguoiAnId
                    WHERE n.BoPhanId = ?
                      AND {condition}
                          BETWEEN ? AND ?
                """, (
                    bo_phan_id,
                    tu,
                    den
                ))

                paid_row = cursor.fetchone()

                da_thu = float(
                    paid_row[0] or 0
                )

            finally:
                connection.close()

            tong_tien = float(
                row[4] or 0
            )

            con_no = max(
                tong_tien - da_thu,
                0
            )

            du = max(
                da_thu - tong_tien,
                0
            )

            result.append({
                "ID bộ phận": row[0],
                "Bộ phận": row[1],
                "Số người": row[2],
                "Số suất": row[3],
                "Tổng tiền ăn": tong_tien,
                "Đã thu": da_thu,
                "Còn nợ": con_no,
                "Dư": du
            })

        return result

    @staticmethod
    def _lay_nguoi_bo_phan(
        bo_phan_id
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    COALESCE(
                        b.TenBoPhan,
                        'Chưa có bộ phận'
                    )
                FROM NguoiAn n
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                WHERE n.DangHoatDong = 1
                  AND n.BoPhanId = ?
                ORDER BY n.HoTen COLLATE NOCASE
            """, (bo_phan_id,))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def bo_phan_so_nguoi(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        return [
            (
                bo_phan_id,
                len(
                    TraCuuModel._lay_nguoi_bo_phan(
                        bo_phan_id
                    )
                )
            )
        ]

    @staticmethod
    def bo_phan_so_nguoi_an(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["ID bộ phận"] == bo_phan_id
        ]

    @staticmethod
    def bo_phan_so_suat(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        return [
            (
                row["ID bộ phận"],
                row["Bộ phận"],
                row["Số suất"]
            )
            for row in rows
            if row["ID bộ phận"] == bo_phan_id
        ]

    @staticmethod
    def bo_phan_tong_tien(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        return [
            (
                row["ID bộ phận"],
                row["Bộ phận"],
                row["Tổng tiền ăn"]
            )
            for row in rows
            if row["ID bộ phận"] == bo_phan_id
        ]

    @staticmethod
    def bo_phan_da_thu(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        return [
            (
                row["ID bộ phận"],
                row["Bộ phận"],
                row["Đã thu"]
            )
            for row in rows
            if row["ID bộ phận"] == bo_phan_id
        ]

    @staticmethod
    def bo_phan_cong_no(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        return [
            (
                row["ID bộ phận"],
                row["Bộ phận"],
                row["Còn nợ"]
            )
            for row in rows
            if row["ID bộ phận"] == bo_phan_id
        ]

    @staticmethod
    def lay_nguoi_no_theo_bo_phan(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        result = []

        for row in rows:

            nguoi = TraCuuModel.lay_nguoi_theo_id(
                row["ID"]
            )

            if not nguoi:
                continue

            if (
                nguoi[2] == bo_phan_id
                and row["Còn nợ"] > 0
            ):
                result.append((
                    row["ID"],
                    row["Họ tên"],
                    row["Tổng phải trả"],
                    row["Đã nộp"]
                ))

        return result

    @staticmethod
    def bo_phan_nguoi_chua_an(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_nguoi_chua_an_theo_khoang(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row[2] is not None
            and (
                TraCuuModel.lay_nguoi_theo_id(
                    row[0]
                )[2] == bo_phan_id
            )
        ]

    @staticmethod
    def bo_phan_nguoi_no(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.lay_nguoi_no_theo_bo_phan(
            bo_phan_id,
            tu_ngay,
            den_ngay
        )

    @staticmethod
    def bo_phan_nop_chua_an(
        bo_phan_id,
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_nguoi_da_nop_nhung_chua_an(
            tu_ngay,
            den_ngay
        )

        result = []

        for row in rows:

            nguoi = TraCuuModel.lay_nguoi_theo_id(
                row["ID"]
            )

            if nguoi and nguoi[2] == bo_phan_id:

                result.append(row)

        return result

    @staticmethod
    def so_sanh_bo_phan_suat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        return [
            {
                "Bộ phận": row["Bộ phận"],
                "Số người": row["Số người"],
                "Số suất": row["Số suất"],
                "Tổng tiền": row["Tổng tiền ăn"]
            }
            for row in rows
        ]

    @staticmethod
    def so_sanh_bo_phan_no(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        return [
            {
                "Bộ phận": row["Bộ phận"],
                "Tổng tiền": row["Tổng tiền ăn"],
                "Đã thu": row["Đã thu"],
                "Còn nợ": row["Còn nợ"],
                "Dư": row["Dư"]
            }
            for row in rows
        ]

    @staticmethod
    def bo_phan_an_nhieu_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        max_value = max(
            row["Số người"]
            for row in rows
        )

        return [
            row
            for row in rows
            if row["Số người"] == max_value
        ]

    @staticmethod
    def bo_phan_no_nhieu_nhat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

        if not rows:
            return []

        max_value = max(
            row["Còn nợ"]
            for row in rows
        )

        return [
            row
            for row in rows
            if row["Còn nợ"] == max_value
        ]

    # ==========================================================
    # ĐỐI CHIẾU ĂN ↔ TIỀN
    # ==========================================================

    @staticmethod
    def doi_chieu_nguoi(
        danh_sach_nguoi_ids,
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._lay_du_lieu_so_sanh_nguoi(
            danh_sach_nguoi_ids,
            tu_ngay,
            den_ngay
        )

    @staticmethod
    def doi_chieu_an_tien(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

    @staticmethod
    def lay_nguoi_an_da_du(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Số suất"] > 0
            and row["Tổng phải trả"] > 0
            and row["Tổng đã nộp"]
                >= row["Tổng phải trả"]
        ]

    @staticmethod
    def lay_nguoi_tien_khong_khop(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if (
                row["Tổng phải trả"]
                != row["Tổng đã nộp"]
            )
        ]

    @staticmethod
    def lay_nguoi_suat_khong_khop_tien(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if (
                row["Số suất"] > 0
                and row["Tổng phải trả"] <= 0
            )
            or (
                row["Số suất"] == 0
                and row["Tổng phải trả"] > 0
            )
        ]

    @staticmethod
    def lay_nguoi_an_tien_bang_0(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Số suất"] > 0
            and row["Tổng phải trả"] <= 0
        ]

    @staticmethod
    def lay_nguoi_co_tien_nhung_khong_suat(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel._lay_toan_bo_cong_no(
            tu_ngay,
            den_ngay
        )

        return [
            row
            for row in rows
            if row["Tổng phải trả"] > 0
            and row["Số suất"] == 0
        ]

    @staticmethod
    def lay_nguoi_co_tien_nhung_khong_an(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.lay_nguoi_co_tien_nhung_khong_suat(
            tu_ngay,
            den_ngay
        )

    # ==========================================================
    # BẤT THƯỜNG - CHẤM NHIỀU LẦN
    # ==========================================================

    @staticmethod
    def lay_du_lieu_an_trung(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.HoTen,
                    substr(na.Ngay, 1, 10) AS Ngay,
                    COUNT(c.Id) AS SoLan
                FROM ChiTietAn c
                INNER JOIN NguoiAn n
                    ON n.Id = c.NguoiAnId
                INNER JOIN NgayAn na
                    ON na.Id = c.NgayAnId
                WHERE c.DaAn = 1
                  AND substr(na.Ngay, 1, 10)
                      BETWEEN ? AND ?
                GROUP BY
                    c.NguoiAnId,
                    substr(na.Ngay, 1, 10)
                HAVING COUNT(c.Id) > 1
                ORDER BY
                    Ngay DESC,
                    SoLan DESC
            """, (
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_nguoi_an_nhieu_lan_theo_ngay(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.lay_du_lieu_an_trung(
            tu_ngay,
            den_ngay
        )

    # ==========================================================
    # NGƯỜI NGỪNG HOẠT ĐỘNG NHƯNG VẪN ĂN
    # ==========================================================

    @staticmethod
    def lay_nguoi_ngung_hoat_dong_nhung_co_du_lieu(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    COALESCE(
                        b.TenBoPhan,
                        'Chưa có bộ phận'
                    ),
                    COUNT(c.Id)
                FROM NguoiAn n
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                INNER JOIN ChiTietAn c
                    ON c.NguoiAnId = n.Id
                   AND c.DaAn = 1
                INNER JOIN NgayAn na
                    ON na.Id = c.NgayAnId
                WHERE n.DangHoatDong = 0
                  AND substr(na.Ngay, 1, 10)
                      BETWEEN ? AND ?
                GROUP BY
                    n.Id,
                    n.HoTen,
                    b.TenBoPhan
                ORDER BY
                    n.HoTen COLLATE NOCASE
            """, (
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # NGƯỜI NGỪNG HOẠT ĐỘNG NHƯNG VẪN NỘP
    # ==========================================================

    @staticmethod
    def lay_nguoi_ngung_hoat_dong_nhung_nop_tien(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            condition = (
                TraCuuModel._ngay_nop_condition("g")
            )

            cursor.execute(f"""
                SELECT
                    n.Id,
                    n.HoTen,
                    COALESCE(
                        b.TenBoPhan,
                        'Chưa có bộ phận'
                    ),
                    COUNT(g.Id),
                    COALESCE(
                        SUM(g.SoTien),
                        0
                    )
                FROM GiaoDichNopTien g
                INNER JOIN NguoiAn n
                    ON n.Id = g.NguoiAnId
                LEFT JOIN BoPhan b
                    ON b.Id = n.BoPhanId
                WHERE n.DangHoatDong = 0
                  AND {condition}
                      BETWEEN ? AND ?
                GROUP BY
                    n.Id,
                    n.HoTen,
                    b.TenBoPhan
                ORDER BY
                    n.HoTen COLLATE NOCASE
            """, (
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # NGƯỜI KHÔNG CÓ BỘ PHẬN
    # ==========================================================

    @staticmethod
    def lay_nguoi_khong_co_bo_phan(
        tu_ngay=None,
        den_ngay=None
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    n.DangHoatDong,
                    n.SDT
                FROM NguoiAn n
                WHERE n.DangHoatDong = 1
                  AND (
                      n.BoPhanId IS NULL
                      OR NOT EXISTS (
                          SELECT 1
                          FROM BoPhan b
                          WHERE b.Id = n.BoPhanId
                      )
                  )
                ORDER BY n.HoTen COLLATE NOCASE
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def lay_nguoi_thieu_bo_phan():
        return TraCuuModel.lay_nguoi_khong_co_bo_phan()

    # ==========================================================
    # TRÙNG TÊN
    # ==========================================================

    @staticmethod
    def lay_nguoi_trung_ten():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    HoTen,
                    COUNT(*) AS SoLuong,
                    GROUP_CONCAT(Id, ', ') AS DanhSachId
                FROM NguoiAn
                WHERE TRIM(COALESCE(HoTen, '')) <> ''
                GROUP BY
                    LOWER(TRIM(HoTen))
                HAVING COUNT(*) > 1
                ORDER BY SoLuong DESC
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # TRÙNG SỐ ĐIỆN THOẠI
    # ==========================================================

    @staticmethod
    def lay_so_dien_thoai_trung():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    SDT,
                    COUNT(*) AS SoLuong,
                    GROUP_CONCAT(Id, ', ') AS DanhSachId
                FROM NguoiAn
                WHERE TRIM(COALESCE(SDT, '')) <> ''
                GROUP BY
                    TRIM(SDT)
                HAVING COUNT(*) > 1
                ORDER BY SoLuong DESC
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # KIỂM TRA DỮ LIỆU - CHI TIẾT KHÔNG CÓ NGÀY
    # ==========================================================

    @staticmethod
    def lay_chi_tiet_khong_co_ngay():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    c.Id,
                    c.NguoiAnId,
                    c.NgayAnId,
                    c.SoTienPhaiTra,
                    c.DaAn,
                    c.GhiChu
                FROM ChiTietAn c
                LEFT JOIN NgayAn n
                    ON n.Id = c.NgayAnId
                WHERE c.NgayAnId IS NULL
                   OR n.Id IS NULL
                ORDER BY c.Id DESC
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # GIAO DỊCH KHÔNG CÓ NGƯỜI
    # ==========================================================

    @staticmethod
    def lay_giao_dich_khong_co_nguoi():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    g.Id,
                    g.NguoiAnId,
                    g.SoTien,
                    g.NgayNop,
                    g.HinhThuc,
                    g.GhiChu
                FROM GiaoDichNopTien g
                LEFT JOIN NguoiAn n
                    ON n.Id = g.NguoiAnId
                WHERE g.NguoiAnId IS NULL
                   OR n.Id IS NULL
                ORDER BY g.Id DESC
            """)

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # GIAO DỊCH NGHI TRÙNG
    # ==========================================================

    @staticmethod
    def lay_giao_dich_nghi_trung(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            condition = (
                TraCuuModel._ngay_nop_condition("g")
            )

            cursor.execute(f"""
                SELECT
                    g.NguoiAnId,
                    n.HoTen,
                    {condition} AS NgayNop,
                    g.SoTien,
                    COUNT(*) AS SoLan
                FROM GiaoDichNopTien g
                LEFT JOIN NguoiAn n
                    ON n.Id = g.NguoiAnId
                WHERE {condition}
                      BETWEEN ? AND ?
                GROUP BY
                    g.NguoiAnId,
                    {condition},
                    g.SoTien
                HAVING COUNT(*) > 1
                ORDER BY
                    NgayNop DESC,
                    SoLan DESC
            """, (
                tu_ngay,
                den_ngay
            ))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # NGÀY DỮ LIỆU BẤT THƯỜNG
    # ==========================================================

    @staticmethod
    def lay_ngay_du_lieu_bat_thuong(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = TraCuuModel.thong_ke_an_theo_ngay(
            tu_ngay,
            den_ngay
        )

        result = []

        for row in rows:

            if row[1] <= 0:
                result.append(row)

        return result

    # ==========================================================
    # DỮ LIỆU THIẾU LIÊN KẾT
    # ==========================================================

    @staticmethod
    def lay_du_lieu_thieu_lien_ket():
        result = []

        result.extend([
            (
                "ChiTietAn",
                *row
            )
            for row in TraCuuModel.lay_chi_tiet_khong_co_ngay()
        ])

        result.extend([
            (
                "GiaoDichNopTien",
                *row
            )
            for row in TraCuuModel.lay_giao_dich_khong_co_nguoi()
        ])

        return result

    # ==========================================================
    # TỔNG HỢP
    # ==========================================================

    @staticmethod
    def lay_tong_hop_khoang(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        tong_nguoi = len(
            TraCuuModel.lay_danh_sach_nguoi()
        )

        so_nguoi_an = (
            TraCuuModel.dem_nguoi_an_theo_khoang(
                tu_ngay,
                den_ngay
            )
        )

        tong_suat = (
            TraCuuModel.tong_so_suat_an(
                tu_ngay,
                den_ngay
            )
        )

        tong_tien = (
            TraCuuModel.tong_tien_an_theo_khoang(
                tu_ngay,
                den_ngay
            )
        )

        tong_thu = (
            TraCuuModel.tong_da_thu(
                tu_ngay,
                den_ngay
            )
        )

        cong_no = max(
            tong_tien - tong_thu,
            0
        )

        so_nguoi_no = (
            TraCuuModel.dem_nguoi_dang_no(
                tu_ngay,
                den_ngay
            )
        )

        so_giao_dich = (
            TraCuuModel.dem_giao_dich(
                tu_ngay,
                den_ngay
            )
        )

        return {
            "tu_ngay": tu_ngay,
            "den_ngay": den_ngay,
            "tong_nguoi_hoat_dong": tong_nguoi,
            "so_nguoi_da_an": so_nguoi_an,
            "tong_so_suat": tong_suat,
            "tong_tien_an": tong_tien,
            "tong_da_thu": tong_thu,
            "tong_cong_no": cong_no,
            "so_nguoi_dang_no": so_nguoi_no,
            "so_giao_dich": so_giao_dich
        }

    @staticmethod
    def tong_da_thu(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            condition = (
                TraCuuModel._ngay_nop_condition("g")
            )

            cursor.execute(f"""
                SELECT
                    COALESCE(
                        SUM(g.SoTien),
                        0
                    )
                FROM GiaoDichNopTien g
                WHERE {condition}
                      BETWEEN ? AND ?
            """, (
                tu_ngay,
                den_ngay
            ))

            row = cursor.fetchone()

            return float(row[0] or 0)

        finally:
            connection.close()

    @staticmethod
    def dem_giao_dich(
        tu_ngay=None,
        den_ngay=None
    ):
        tu_ngay, den_ngay = (
            TraCuuModel._chuan_hoa_khoang_ngay(
                tu_ngay,
                den_ngay
            )
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            condition = (
                TraCuuModel._ngay_nop_condition("g")
            )

            cursor.execute(f"""
                SELECT COUNT(*)
                FROM GiaoDichNopTien g
                WHERE {condition}
                      BETWEEN ? AND ?
            """, (
                tu_ngay,
                den_ngay
            ))

            row = cursor.fetchone()

            return int(row[0] or 0)

        finally:
            connection.close()

    # ==========================================================
    # ĐỐI CHIẾU TỔNG SỐ SUẤT
    # ==========================================================

    @staticmethod
    def doi_chieu_tong_suat(
        tu_ngay=None,
        den_ngay=None
    ):
        tong_suat = TraCuuModel.tong_so_suat_an(
            tu_ngay,
            den_ngay
        )

        return [{
            "Chỉ tiêu": "Tổng số suất ăn",
            "Giá trị": tong_suat
        }]

    # ==========================================================
    # ĐỐI CHIẾU TỔNG TIỀN
    # ==========================================================

    @staticmethod
    def doi_chieu_tong_tien(
        tu_ngay=None,
        den_ngay=None
    ):
        tong_tien = (
            TraCuuModel.tong_tien_an_theo_khoang(
                tu_ngay,
                den_ngay
            )
        )

        return [{
            "Chỉ tiêu": "Tổng tiền ăn",
            "Giá trị": tong_tien
        }]

    # ==========================================================
    # ĐỐI CHIẾU TỔNG THU
    # ==========================================================

    @staticmethod
    def doi_chieu_tong_thu(
        tu_ngay=None,
        den_ngay=None
    ):
        tong_thu = TraCuuModel.tong_da_thu(
            tu_ngay,
            den_ngay
        )

        return [{
            "Chỉ tiêu": "Tổng tiền đã thu",
            "Giá trị": tong_thu
        }]

    # ==========================================================
    # ĐỐI CHIẾU TỔNG CÔNG NỢ
    # ==========================================================

    @staticmethod
    def doi_chieu_tong_cong_no(
        tu_ngay=None,
        den_ngay=None
    ):
        tong_tien = (
            TraCuuModel.tong_tien_an_theo_khoang(
                tu_ngay,
                den_ngay
            )
        )

        tong_thu = (
            TraCuuModel.tong_da_thu(
                tu_ngay,
                den_ngay
            )
        )

        cong_no = max(
            tong_tien - tong_thu,
            0
        )

        return [{
            "Chỉ tiêu": "Tổng công nợ",
            "Tiền ăn": tong_tien,
            "Đã thu": tong_thu,
            "Còn nợ": cong_no
        }]

    # ==========================================================
    # ĐỐI CHIẾU TỔNG NGƯỜI
    # ==========================================================

    @staticmethod
    def doi_chieu_tong_nguoi(
        tu_ngay=None,
        den_ngay=None
    ):
        tong_nguoi = (
            TraCuuModel.dem_nguoi_an_theo_khoang(
                tu_ngay,
                den_ngay
            )
        )

        return [{
            "Chỉ tiêu": "Số người đã ăn",
            "Giá trị": tong_nguoi
        }]

    # ==========================================================
    # ĐỐI CHIẾU BỘ PHẬN
    # ==========================================================

    @staticmethod
    def doi_chieu_bo_phan(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.lay_thong_ke_bo_phan_day_du(
            tu_ngay,
            den_ngay
        )

    # ==========================================================
    # KIỂM TRA CHÊNH LỆCH TOÀN BỘ
    # ==========================================================

    @staticmethod
    def kiem_tra_chenh_lech(
        tu_ngay=None,
        den_ngay=None
    ):
        rows = (
            TraCuuModel
            ._lay_toan_bo_cong_no(
                tu_ngay,
                den_ngay
            )
        )

        result = []

        for row in rows:

            if (
                row["Số suất"] > 0
                and row["Tổng phải trả"] <= 0
            ):
                result.append({
                    "Loại": "Ăn nhưng tiền bằng 0",
                    **row
                })

            elif (
                row["Số suất"] == 0
                and row["Tổng phải trả"] > 0
            ):
                result.append({
                    "Loại": "Có tiền phải trả nhưng không có suất",
                    **row
                })

            elif (
                row["Tổng đã nộp"]
                > row["Tổng phải trả"]
                and row["Tổng phải trả"] > 0
            ):
                result.append({
                    "Loại": "Nộp vượt",
                    **row
                })

        return result

    # ==========================================================
    # TỔNG HỢP TOÀN BỘ
    # ==========================================================

    @staticmethod
    def tong_hop_toan_bo(
        tu_ngay=None,
        den_ngay=None
    ):
        data = (
            TraCuuModel
            .lay_tong_hop_khoang(
                tu_ngay,
                den_ngay
            )
        )

        return [{
            "Chỉ tiêu": "Tổng người hoạt động",
            "Giá trị": data["tong_nguoi_hoat_dong"]
        }, {
            "Chỉ tiêu": "Số người đã ăn",
            "Giá trị": data["so_nguoi_da_an"]
        }, {
            "Chỉ tiêu": "Tổng số suất",
            "Giá trị": data["tong_so_suat"]
        }, {
            "Chỉ tiêu": "Tổng tiền ăn",
            "Giá trị": data["tong_tien_an"]
        }, {
            "Chỉ tiêu": "Tổng đã thu",
            "Giá trị": data["tong_da_thu"]
        }, {
            "Chỉ tiêu": "Tổng công nợ",
            "Giá trị": data["tong_cong_no"]
        }, {
            "Chỉ tiêu": "Số người đang nợ",
            "Giá trị": data["so_nguoi_dang_no"]
        }, {
            "Chỉ tiêu": "Số giao dịch",
            "Giá trị": data["so_giao_dich"]
        }]

    # ==========================================================
    # CÁC ALIAS TƯƠNG THÍCH VỚI CODE CŨ
    # ==========================================================

    @staticmethod
    def lay_nguoi_an_nhung_chua_nop_tien(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.lay_nguoi_an_nhung_chua_nop(
            tu_ngay,
            den_ngay
        )

    @staticmethod
    def lay_nguoi_nop_du_tien(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.lay_nguoi_nop_du(
            tu_ngay,
            den_ngay
        )

    @staticmethod
    def lay_nguoi_nop_vuot_tien(
        tu_ngay=None,
        den_ngay=None
    ):
        return TraCuuModel.lay_nguoi_nop_vuot(
            tu_ngay,
            den_ngay
        )