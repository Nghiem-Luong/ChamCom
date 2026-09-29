from Database.database import get_connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    # =========================
    # BẢNG NGƯỜI ĂN
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NguoiAn (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            HoTen TEXT NOT NULL,
            SDT TEXT,
            DangHoatDong INTEGER NOT NULL DEFAULT 1,
            NgayTao TEXT NOT NULL
        )
    """)

    # =========================
    # BẢNG NGÀY ĂN
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NgayAn (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Ngay TEXT NOT NULL UNIQUE,
            DonGiaMacDinh REAL NOT NULL DEFAULT 0,
            GhiChu TEXT
        )
    """)

    # =========================
    # BẢNG CHI TIẾT ĂN
    # =========================
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

    # =========================
    # BẢNG GIAO DỊCH NỘP TIỀN
    # =========================
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

    # =========================
    # BẢNG AUDIT LOG
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AuditLog (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,

            ThoiGian TEXT NOT NULL,

            HanhDong TEXT NOT NULL,

            MoTa TEXT,

            NguoiThaoTac TEXT NOT NULL DEFAULT 'Chính tôi'
        )
    """)

    connection.commit()

    connection.close()