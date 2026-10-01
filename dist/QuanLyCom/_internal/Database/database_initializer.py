# -*- coding: utf-8 -*-

from Database.database import get_connection


def _lay_cac_cot(cursor, ten_bang):
    """
    Lấy danh sách tên cột hiện tại của một bảng SQLite.
    """

    cursor.execute(
        f"PRAGMA table_info({ten_bang})"
    )

    rows = cursor.fetchall()

    return {
        row[1]
        for row in rows
    }


def _them_cot_neu_chua_co(
    cursor,
    ten_bang,
    ten_cot,
    dinh_nghia,
):
    """
    Thêm cột mới nếu DB cũ chưa có.

    Không xóa dữ liệu hiện tại.
    """

    cac_cot = _lay_cac_cot(
        cursor,
        ten_bang,
    )

    if ten_cot not in cac_cot:

        cursor.execute(
            f"""
            ALTER TABLE {ten_bang}
            ADD COLUMN {ten_cot} {dinh_nghia}
            """
        )


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    try:

        # ======================================================
        # 1. BẢNG BỘ PHẬN
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BoPhan (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                TenBoPhan TEXT NOT NULL UNIQUE,

                DangHoatDong INTEGER NOT NULL DEFAULT 1,

                NgayTao TEXT NOT NULL
            )
        """)

        # ======================================================
        # 2. BẢNG NGƯỜI ĂN
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NguoiAn (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                HoTen TEXT NOT NULL,

                SDT TEXT,

                DangHoatDong INTEGER NOT NULL DEFAULT 1,

                NgayTao TEXT NOT NULL
            )
        """)

        # ------------------------------------------------------
        # THÊM BỘ PHẬN CHO DB CŨ
        # ------------------------------------------------------

        _them_cot_neu_chua_co(
            cursor,
            "NguoiAn",
            "BoPhanId",
            "INTEGER",
        )

        # ======================================================
        # 3. BẢNG NGÀY ĂN
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NgayAn (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                Ngay TEXT NOT NULL UNIQUE,

                DonGiaMacDinh REAL NOT NULL DEFAULT 0,

                GhiChu TEXT
            )
        """)

        # ======================================================
        # 4. BẢNG CHI TIẾT ĂN
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ChiTietAn (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                NguoiAnId INTEGER NOT NULL,

                NgayAnId INTEGER NOT NULL,

                DaAn INTEGER NOT NULL DEFAULT 0,

                SoTienPhaiTra REAL NOT NULL DEFAULT 0,

                GhiChu TEXT,

                FOREIGN KEY (NguoiAnId)
                    REFERENCES NguoiAn(Id),

                FOREIGN KEY (NgayAnId)
                    REFERENCES NgayAn(Id),

                UNIQUE (NguoiAnId, NgayAnId)
            )
        """)

        # ------------------------------------------------------
        # THÊM TRẠNG THÁI CHO DB CŨ
        # ------------------------------------------------------

        _them_cot_neu_chua_co(
            cursor,
            "ChiTietAn",
            "TrangThai",
            "TEXT NOT NULL DEFAULT 'Đăng ký'",
        )

        # ======================================================
        # 5. BẢNG SUẤT ĂN PHÁT SINH
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SuatAnPhatSinh (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                NgayAnId INTEGER NOT NULL,

                HoTen TEXT NOT NULL,

                DonVi TEXT,

                SoLuong INTEGER NOT NULL DEFAULT 1,

                DonGia REAL NOT NULL DEFAULT 0,

                GhiChu TEXT,

                NgayTao TEXT NOT NULL,

                FOREIGN KEY (NgayAnId)
                    REFERENCES NgayAn(Id)
            )
        """)

        # ======================================================
        # 6. BẢNG GIAO DỊCH NỘP TIỀN
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS GiaoDichNopTien (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                NguoiAnId INTEGER NOT NULL,

                NgayNop TEXT NOT NULL,

                SoTien REAL NOT NULL CHECK (SoTien > 0),

                HinhThuc TEXT NOT NULL DEFAULT 'Tiền mặt',

                GhiChu TEXT,

                FOREIGN KEY (NguoiAnId)
                    REFERENCES NguoiAn(Id)
            )
        """)

        # ======================================================
        # 7. BẢNG AUDIT LOG
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AuditLog (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                ThoiGian TEXT NOT NULL,

                HanhDong TEXT NOT NULL,

                MoTa TEXT,

                NguoiThaoTac TEXT NOT NULL DEFAULT 'Chính tôi'
            )
        """)

        # ======================================================
        # 8. BẢNG CHỐT SUẤT ĂN
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ChotSuatAn (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                NgayAnId INTEGER NOT NULL,

                NguoiAnId INTEGER,

                HoTen TEXT NOT NULL,

                BoPhan TEXT,

                TrangThai TEXT NOT NULL DEFAULT 'Đăng ký',

                SoTien REAL NOT NULL DEFAULT 0,

                GhiChu TEXT,

                NgayChot TEXT NOT NULL,

                FOREIGN KEY (NgayAnId)
                    REFERENCES NgayAn(Id),

                FOREIGN KEY (NguoiAnId)
                    REFERENCES NguoiAn(Id)
            )
        """)

        # ======================================================
        # 8.1. NÂNG CẤP BẢNG CHỐT CHO SUẤT ĂN PHÁT SINH
        # ======================================================
        #
        # LoaiNguoi:
        #   - Nhân viên
        #   - Phát sinh
        #
        # SuatAnPhatSinhId:
        #   ID của bản ghi trong SuatAnPhatSinh.
        #
        # SoLuong:
        #   Số suất của dòng chốt.
        #
        # DonGia:
        #   Đơn giá của một suất.
        #
        # Các cột này được thêm bằng migration,
        # không ảnh hưởng dữ liệu ChotSuatAn cũ.
        # ======================================================

        _them_cot_neu_chua_co(
            cursor,
            "ChotSuatAn",
            "LoaiNguoi",
            "TEXT NOT NULL DEFAULT 'Nhân viên'",
        )

        _them_cot_neu_chua_co(
            cursor,
            "ChotSuatAn",
            "SuatAnPhatSinhId",
            "INTEGER",
        )

        _them_cot_neu_chua_co(
            cursor,
            "ChotSuatAn",
            "SoLuong",
            "INTEGER NOT NULL DEFAULT 1",
        )

        _them_cot_neu_chua_co(
            cursor,
            "ChotSuatAn",
            "DonGia",
            "REAL NOT NULL DEFAULT 0",
        )

        # ======================================================
        # 9. BẢNG TRẠNG THÁI CHỐT
        # ======================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TrangThaiChot (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,

                NgayAnId INTEGER NOT NULL UNIQUE,

                DaChot INTEGER NOT NULL DEFAULT 0,

                NgayChot TEXT,

                NguoiChot TEXT,

                GhiChu TEXT,

                FOREIGN KEY (NgayAnId)
                    REFERENCES NgayAn(Id)
            )
        """)

        # ======================================================
        # 10. INDEX
        # ======================================================

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_nguoi_an_bophan
            ON NguoiAn(BoPhanId)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chi_tiet_an_ngay
            ON ChiTietAn(NgayAnId)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chi_tiet_an_nguoi
            ON ChiTietAn(NguoiAnId)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_suat_an_phat_sinh_ngay
            ON SuatAnPhatSinh(NgayAnId)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chot_suat_an_ngay
            ON ChotSuatAn(NgayAnId)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chot_suat_an_nguoi
            ON ChotSuatAn(NguoiAnId)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chot_suat_an_phat_sinh
            ON ChotSuatAn(SuatAnPhatSinhId)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_trang_thai_chot_ngay
            ON TrangThaiChot(NgayAnId)
        """)

        # ======================================================
        # 11. COMMIT
        # ======================================================

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()