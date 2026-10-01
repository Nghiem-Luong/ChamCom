# -*- coding: utf-8 -*-

from datetime import datetime

from Database.database import get_connection


class ChotSuatAnModel:

    # ==========================================================
    # KIỂM TRA NGÀY ĐÃ CHỐT CHƯA
    # ==========================================================

    @staticmethod
    def da_chot(ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT DaChot
                FROM TrangThaiChot
                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            row = cursor.fetchone()

            if row is None:
                return False

            return bool(row[0])

        finally:
            connection.close()

    # ==========================================================
    # LẤY TRẠNG THÁI CHỐT
    # ==========================================================

    @staticmethod
    def lay_trang_thai(ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    NgayAnId,
                    DaChot,
                    NgayChot,
                    NguoiChot,
                    GhiChu
                FROM TrangThaiChot
                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            return cursor.fetchone()

        finally:
            connection.close()

    # ==========================================================
    # TẠO TRẠNG THÁI CHƯA CHỐT
    # ==========================================================

    @staticmethod
    def tao_trang_thai_neu_chua_co(ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT OR IGNORE INTO TrangThaiChot (
                    NgayAnId,
                    DaChot
                )
                VALUES (?, 0)
            """, (ngay_an_id,))

            connection.commit()

        finally:
            connection.close()

    # ==========================================================
    # LẤY DANH SÁCH ĐÃ CHỐT
    # ==========================================================
    #
    # GIỮ NGUYÊN 9 CỘT CŨ Ở ĐẦU.
    #
    # Các cột mới được thêm phía sau để không làm hỏng
    # Controller/View hiện tại.
    #
    # 0  Id
    # 1  NgayAnId
    # 2  NguoiAnId
    # 3  HoTen
    # 4  BoPhan
    # 5  TrangThai
    # 6  SoTien
    # 7  GhiChu
    # 8  NgayChot
    # 9  LoaiNguoi
    # 10 SuatAnPhatSinhId
    # 11 SoLuong
    # 12 DonGia
    #
    # ==========================================================

    @staticmethod
    def lay_danh_sach_chot(ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    NgayAnId,
                    NguoiAnId,
                    HoTen,
                    BoPhan,
                    TrangThai,
                    SoTien,
                    GhiChu,
                    NgayChot,
                    LoaiNguoi,
                    SuatAnPhatSinhId,
                    SoLuong,
                    DonGia
                FROM ChotSuatAn
                WHERE NgayAnId = ?
                ORDER BY
                    CASE
                        WHEN LoaiNguoi = 'Nhân viên'
                        THEN 0
                        ELSE 1
                    END,
                    BoPhan,
                    HoTen
            """, (ngay_an_id,))

            return cursor.fetchall()

        finally:
            connection.close()

    # ==========================================================
    # XÓA DANH SÁCH CHỐT CŨ
    # ==========================================================

    @staticmethod
    def xoa_danh_sach_chot(ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM ChotSuatAn
                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            connection.commit()

        finally:
            connection.close()

    # ==========================================================
    # THÊM MỘT DÒNG VÀO DANH SÁCH CHỐT
    # ==========================================================

    @staticmethod
    def them_dong_chot(
        ngay_an_id,
        nguoi_an_id,
        ho_ten,
        bo_phan,
        trang_thai,
        so_tien,
        ghi_chu=None,
        loai_nguoi="Nhân viên",
        suat_an_phat_sinh_id=None,
        so_luong=1,
        don_gia=0,
    ):
        """
        Thêm một dòng vào snapshot chốt.

        Nhân viên:
            loai_nguoi = "Nhân viên"
            nguoi_an_id có giá trị
            suat_an_phat_sinh_id = None
            so_luong = 1

        Phát sinh:
            loai_nguoi = "Phát sinh"
            nguoi_an_id = None
            suat_an_phat_sinh_id có giá trị
            so_luong >= 1
            don_gia = giá một suất
        """

        ho_ten = str(
            ho_ten or ""
        ).strip()

        bo_phan = str(
            bo_phan or ""
        ).strip()

        trang_thai = str(
            trang_thai or "Đăng ký"
        ).strip()

        loai_nguoi = str(
            loai_nguoi or "Nhân viên"
        ).strip()

        if not ho_ten:
            raise ValueError(
                "Tên người ăn không được để trống."
            )

        try:
            so_tien = float(
                so_tien or 0
            )
        except (
            TypeError,
            ValueError,
        ):
            so_tien = 0

        try:
            so_luong = int(
                so_luong or 1
            )
        except (
            TypeError,
            ValueError,
        ):
            so_luong = 1

        if so_luong <= 0:
            so_luong = 1

        try:
            don_gia = float(
                don_gia or 0
            )
        except (
            TypeError,
            ValueError,
        ):
            don_gia = 0

        # ------------------------------------------------------
        # Nếu là nhân viên
        # ------------------------------------------------------

        if loai_nguoi == "Nhân viên":

            suat_an_phat_sinh_id = None

            so_luong = 1

            if don_gia <= 0 and so_tien > 0:
                don_gia = so_tien

        # ------------------------------------------------------
        # Nếu là phát sinh
        # ------------------------------------------------------

        elif loai_nguoi == "Phát sinh":

            nguoi_an_id = None

            # Nếu có số lượng nhưng chưa có tổng tiền,
            # tự tính theo đơn giá.
            if so_tien <= 0 and don_gia > 0:
                so_tien = so_luong * don_gia

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO ChotSuatAn (
                    NgayAnId,
                    NguoiAnId,
                    HoTen,
                    BoPhan,
                    TrangThai,
                    SoTien,
                    GhiChu,
                    NgayChot,
                    LoaiNguoi,
                    SuatAnPhatSinhId,
                    SoLuong,
                    DonGia
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?
                )
            """, (
                ngay_an_id,
                nguoi_an_id,
                ho_ten,
                bo_phan,
                trang_thai,
                so_tien,
                ghi_chu,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                loai_nguoi,
                suat_an_phat_sinh_id,
                so_luong,
                don_gia,
            ))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    # ==========================================================
    # LƯU TOÀN BỘ DANH SÁCH CHỐT
    # ==========================================================

    @staticmethod
    def luu_danh_sach_chot(
        ngay_an_id,
        danh_sach,
        nguoi_chot="Chính tôi",
        ghi_chu=None,
    ):
        """
        Lưu snapshot danh sách chốt.

        Hỗ trợ cả:

        1. Nhân viên

        {
            "nguoi_an_id": 1,
            "ho_ten": "Nguyễn Văn A",
            "bo_phan": "Kế toán",
            "trang_thai": "Đăng ký",
            "so_tien": 30000,
            "ghi_chu": "",
            "loai_nguoi": "Nhân viên",
            "suat_an_phat_sinh_id": None,
            "so_luong": 1,
            "don_gia": 30000
        }

        2. Suất ăn phát sinh

        {
            "nguoi_an_id": None,
            "ho_ten": "Khách Samsung",
            "bo_phan": "Khách",
            "trang_thai": "Đăng ký",
            "so_tien": 60000,
            "ghi_chu": "",
            "loai_nguoi": "Phát sinh",
            "suat_an_phat_sinh_id": 5,
            "so_luong": 2,
            "don_gia": 30000
        }
        """

        if not ngay_an_id:
            raise ValueError(
                "Ngày ăn không hợp lệ."
            )

        if not danh_sach:
            raise ValueError(
                "Danh sách chốt đang trống."
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # --------------------------------------------------
            # Kiểm tra ngày đã chốt
            # --------------------------------------------------

            cursor.execute("""
                SELECT DaChot
                FROM TrangThaiChot
                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            row = cursor.fetchone()

            if row is not None and row[0] == 1:
                raise ValueError(
                    "Ngày ăn này đã được chốt."
                )

            # --------------------------------------------------
            # Xóa snapshot cũ
            # --------------------------------------------------

            cursor.execute("""
                DELETE FROM ChotSuatAn
                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            thoi_gian_chot = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            so_dong_hop_le = 0

            # --------------------------------------------------
            # Lưu từng dòng
            # --------------------------------------------------

            for item in danh_sach:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                ho_ten = str(
                    item.get(
                        "ho_ten",
                        ""
                    ) or ""
                ).strip()

                if not ho_ten:
                    continue

                loai_nguoi = str(
                    item.get(
                        "loai_nguoi",
                        "Nhân viên"
                    ) or "Nhân viên"
                ).strip()

                if loai_nguoi not in (
                    "Nhân viên",
                    "Phát sinh",
                ):
                    loai_nguoi = "Nhân viên"

                nguoi_an_id = item.get(
                    "nguoi_an_id"
                )

                suat_an_phat_sinh_id = item.get(
                    "suat_an_phat_sinh_id"
                )

                # --------------------------------------------------
                # Chuẩn hóa trạng thái
                # --------------------------------------------------

                trang_thai = str(
                    item.get(
                        "trang_thai",
                        "Đăng ký"
                    ) or "Đăng ký"
                ).strip()

                if not trang_thai:
                    trang_thai = "Đăng ký"

                # --------------------------------------------------
                # Bộ phận / đơn vị
                # --------------------------------------------------

                bo_phan = str(
                    item.get(
                        "bo_phan",
                        ""
                    ) or ""
                ).strip()

                # --------------------------------------------------
                # Ghi chú
                # --------------------------------------------------

                ghi_chu_dong = item.get(
                    "ghi_chu"
                )

                # --------------------------------------------------
                # Số tiền
                # --------------------------------------------------

                try:
                    so_tien = float(
                        item.get(
                            "so_tien",
                            0
                        ) or 0
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    so_tien = 0

                # --------------------------------------------------
                # Số lượng
                # --------------------------------------------------

                try:
                    so_luong = int(
                        item.get(
                            "so_luong",
                            1
                        ) or 1
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    so_luong = 1

                if so_luong <= 0:
                    so_luong = 1

                # --------------------------------------------------
                # Đơn giá
                # --------------------------------------------------

                try:
                    don_gia = float(
                        item.get(
                            "don_gia",
                            0
                        ) or 0
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    don_gia = 0

                # --------------------------------------------------
                # Chuẩn hóa theo loại
                # --------------------------------------------------

                if loai_nguoi == "Nhân viên":

                    # Nhân viên luôn liên kết NguoiAn
                    suat_an_phat_sinh_id = None

                    so_luong = 1

                    if (
                        don_gia <= 0
                        and so_tien > 0
                    ):
                        don_gia = so_tien

                else:

                    # Phát sinh không liên kết NguoiAn
                    nguoi_an_id = None

                    # Nếu chỉ có đơn giá thì tự tính tổng
                    if (
                        so_tien <= 0
                        and don_gia > 0
                    ):
                        so_tien = (
                            so_luong * don_gia
                        )

                # --------------------------------------------------
                # INSERT SNAPSHOT
                # --------------------------------------------------

                cursor.execute("""
                    INSERT INTO ChotSuatAn (
                        NgayAnId,
                        NguoiAnId,
                        HoTen,
                        BoPhan,
                        TrangThai,
                        SoTien,
                        GhiChu,
                        NgayChot,
                        LoaiNguoi,
                        SuatAnPhatSinhId,
                        SoLuong,
                        DonGia
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?
                    )
                """, (
                    ngay_an_id,
                    nguoi_an_id,
                    ho_ten,
                    bo_phan,
                    trang_thai,
                    so_tien,
                    ghi_chu_dong,
                    thoi_gian_chot,
                    loai_nguoi,
                    suat_an_phat_sinh_id,
                    so_luong,
                    don_gia,
                ))

                so_dong_hop_le += 1

            # --------------------------------------------------
            # Kiểm tra sau khi chuẩn hóa
            # --------------------------------------------------

            if so_dong_hop_le == 0:
                raise ValueError(
                    "Không có dữ liệu hợp lệ để chốt."
                )

            # --------------------------------------------------
            # Cập nhật trạng thái ngày ăn
            # --------------------------------------------------

            cursor.execute("""
                INSERT INTO TrangThaiChot (
                    NgayAnId,
                    DaChot,
                    NgayChot,
                    NguoiChot,
                    GhiChu
                )
                VALUES (
                    ?, 1, ?, ?, ?
                )

                ON CONFLICT(NgayAnId)
                DO UPDATE SET
                    DaChot = 1,
                    NgayChot = excluded.NgayChot,
                    NguoiChot = excluded.NguoiChot,
                    GhiChu = excluded.GhiChu
            """, (
                ngay_an_id,
                thoi_gian_chot,
                nguoi_chot,
                ghi_chu,
            ))

            connection.commit()

            return True

        except Exception:

            connection.rollback()

            raise

        finally:

            connection.close()

    # ==========================================================
    # MỞ CHỐT
    # ==========================================================

    @staticmethod
    def mo_chot(
        ngay_an_id,
        nguoi_thao_tac="Chính tôi",
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            # --------------------------------------------------
            # Mở trạng thái chốt
            # --------------------------------------------------

            cursor.execute("""
                UPDATE TrangThaiChot
                SET
                    DaChot = 0,
                    NgayChot = NULL,
                    NguoiChot = NULL
                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            # --------------------------------------------------
            # Xóa snapshot
            #
            # Không xóa:
            # - ChiTietAn
            # - SuatAnPhatSinh
            # - NguoiAn
            #
            # Chỉ xóa bản snapshot đã chốt.
            # --------------------------------------------------

            cursor.execute("""
                DELETE FROM ChotSuatAn
                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            connection.commit()

            return True

        except Exception:

            connection.rollback()

            raise

        finally:

            connection.close()

    # ==========================================================
    # THỐNG KÊ DANH SÁCH CHỐT
    # ==========================================================

    @staticmethod
    def thong_ke_chot(ngay_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*) AS TongSo,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN TrangThai = 'Đăng ký'
                                THEN 1
                                ELSE 0
                            END
                        ),
                        0
                    ) AS SoNguoiAn,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN TrangThai = 'Không ăn'
                                THEN 1
                                ELSE 0
                            END
                        ),
                        0
                    ) AS SoNguoiKhongAn,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN TrangThai IN (
                                    'Công tác',
                                    'Đi công tác'
                                )
                                THEN 1
                                ELSE 0
                            END
                        ),
                        0
                    ) AS SoNguoiCongTac,

                    COALESCE(
                        SUM(SoTien),
                        0
                    ) AS TongTien

                FROM ChotSuatAn

                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            row = cursor.fetchone()

            if row is None:
                return {
                    "tong_so": 0,
                    "so_nguoi_an": 0,
                    "so_nguoi_khong_an": 0,
                    "so_nguoi_cong_tac": 0,
                    "tong_tien": 0,
                }

            return {
                "tong_so": row[0] or 0,
                "so_nguoi_an": row[1] or 0,
                "so_nguoi_khong_an": row[2] or 0,
                "so_nguoi_cong_tac": row[3] or 0,
                "tong_tien": row[4] or 0,
            }

        finally:
            connection.close()

    # ==========================================================
    # THỐNG KÊ TỔNG SỐ SUẤT
    # ==========================================================

    @staticmethod
    def thong_ke_so_suat(ngay_an_id):
        """
        Tổng số suất thực tế trong snapshot.

        Ví dụ:
            Nguyễn Văn A = 1 suất
            Khách Samsung = 2 suất
            Đoàn kỹ thuật = 5 suất

        Tổng = 8 suất.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(
                            CASE
                                WHEN TrangThai = 'Đăng ký'
                                THEN SoLuong
                                ELSE 0
                            END
                        ),
                        0
                    )
                FROM ChotSuatAn
                WHERE NgayAnId = ?
            """, (ngay_an_id,))

            row = cursor.fetchone()

            if row is None:
                return 0

            return int(
                row[0] or 0
            )

        finally:
            connection.close()

    # ==========================================================
    # THỐNG KÊ SUẤT PHÁT SINH
    # ==========================================================

    @staticmethod
    def thong_ke_phat_sinh(ngay_an_id):
        """
        Thống kê riêng các dòng phát sinh.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(
                        SUM(SoLuong),
                        0
                    ),
                    COALESCE(
                        SUM(SoTien),
                        0
                    )
                FROM ChotSuatAn
                WHERE
                    NgayAnId = ?
                    AND LoaiNguoi = 'Phát sinh'
                    AND TrangThai = 'Đăng ký'
            """, (ngay_an_id,))

            row = cursor.fetchone()

            if row is None:
                return {
                    "so_dong": 0,
                    "so_suat": 0,
                    "tong_tien": 0,
                }

            return {
                "so_dong": row[0] or 0,
                "so_suat": row[1] or 0,
                "tong_tien": row[2] or 0,
            }

        finally:
            connection.close()