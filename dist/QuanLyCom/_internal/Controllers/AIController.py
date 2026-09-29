# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta

from Database.database import get_connection


# ==========================================================
# THỜI GIAN HIỆN TẠI
# ==========================================================

def lay_thoi_gian_hien_tai():
    """
    Lấy thời gian hiện tại của máy tính.
    """

    now = datetime.now()

    return (
        f"Bây giờ là {now.strftime('%H:%M:%S')}, "
        f"ngày {now.strftime('%d/%m/%Y')}."
    )


# ==========================================================
# CHUYỂN NGÀY TỪ CÂU HỎI
# ==========================================================

def lay_ngay_tu_cau_hoi(cau_hoi):
    """
    Nhận diện:
    - hôm nay
    - hôm qua
    - ngày DD/MM/YYYY
    - ngày DD-MM-YYYY
    - DD/MM
    """

    cau_hoi = cau_hoi.lower().strip()

    now = datetime.now()

    # ------------------------------------------------------
    # HÔM NAY
    # ------------------------------------------------------

    if "hôm nay" in cau_hoi:
        return now.strftime("%Y-%m-%d")

    # ------------------------------------------------------
    # HÔM QUA
    # ------------------------------------------------------

    if "hôm qua" in cau_hoi:
        ngay = now - timedelta(days=1)
        return ngay.strftime("%Y-%m-%d")

    # ------------------------------------------------------
    # NGÀY DD/MM/YYYY
    # ------------------------------------------------------

    match = re.search(
        r"(?:ngày\s*)?(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})",
        cau_hoi
    )

    if match:

        ngay = int(match.group(1))
        thang = int(match.group(2))
        nam = int(match.group(3))

        try:
            date_obj = datetime(nam, thang, ngay)

            return date_obj.strftime("%Y-%m-%d")

        except ValueError:
            return None

    # ------------------------------------------------------
    # DD/MM - lấy năm hiện tại
    # ------------------------------------------------------

    match = re.search(
        r"(?:ngày\s*)?(\d{1,2})[\/\-](\d{1,2})",
        cau_hoi
    )

    if match:

        ngay = int(match.group(1))
        thang = int(match.group(2))

        try:
            date_obj = datetime(
                now.year,
                thang,
                ngay
            )

            return date_obj.strftime("%Y-%m-%d")

        except ValueError:
            return None

    return None


# ==========================================================
# SỐ NGƯỜI ĂN TRONG NGÀY
# ==========================================================

def lay_so_nguoi_an(ngay=None):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        if ngay:

            cursor.execute("""
                SELECT COUNT(*)
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON c.NgayAnId = n.Id
                WHERE n.Ngay = ?
                  AND c.DaAn = 1
            """, (ngay,))

        else:

            cursor.execute("""
                SELECT COUNT(*)
                FROM ChiTietAn c
                WHERE c.DaAn = 1
                  AND c.NgayAnId IN (
                      SELECT Id
                      FROM NgayAn
                      WHERE Ngay = DATE('now', 'localtime')
                  )
            """)

        result = cursor.fetchone()

        return result[0] or 0

    finally:

        connection.close()


# ==========================================================
# TỔNG TIỀN TRONG NGÀY
# ==========================================================

def lay_tong_tien_ngay(ngay=None):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        if ngay:

            cursor.execute("""
                SELECT COALESCE(
                    SUM(c.SoTienPhaiTra),
                    0
                )
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON c.NgayAnId = n.Id
                WHERE n.Ngay = ?
                  AND c.DaAn = 1
            """, (ngay,))

        else:

            cursor.execute("""
                SELECT COALESCE(
                    SUM(c.SoTienPhaiTra),
                    0
                )
                FROM ChiTietAn c
                WHERE c.DaAn = 1
            """)

        result = cursor.fetchone()

        return result[0] or 0

    finally:

        connection.close()


# ==========================================================
# DANH SÁCH NGƯỜI ĂN TRONG NGÀY
# ==========================================================

def lay_danh_sach_nguoi_an(ngay=None):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        if ngay:

            cursor.execute("""
                SELECT n.HoTen
                FROM ChiTietAn c
                INNER JOIN NguoiAn n
                    ON c.NguoiAnId = n.Id
                INNER JOIN NgayAn a
                    ON c.NgayAnId = a.Id
                WHERE a.Ngay = ?
                  AND c.DaAn = 1
                ORDER BY n.HoTen
            """, (ngay,))

        else:

            cursor.execute("""
                SELECT n.HoTen
                FROM ChiTietAn c
                INNER JOIN NguoiAn n
                    ON c.NguoiAnId = n.Id
                INNER JOIN NgayAn a
                    ON c.NgayAnId = a.Id
                WHERE a.Ngay = DATE('now', 'localtime')
                  AND c.DaAn = 1
                ORDER BY n.HoTen
            """)

        rows = cursor.fetchall()

        return [
            row[0]
            for row in rows
        ]

    finally:

        connection.close()


# ==========================================================
# LỊCH SỬ ĂN CỦA MỘT NGƯỜI
# ==========================================================

def lay_lich_su_nguoi_an(ten_nguoi):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                n.HoTen,
                a.Ngay,
                c.DaAn,
                c.SoTienPhaiTra
            FROM ChiTietAn c

            INNER JOIN NguoiAn n
                ON c.NguoiAnId = n.Id

            INNER JOIN NgayAn a
                ON c.NgayAnId = a.Id

            WHERE n.HoTen LIKE ?

            ORDER BY a.Ngay DESC
        """, (f"%{ten_nguoi}%",))

        rows = cursor.fetchall()

        return rows

    finally:

        connection.close()


# ==========================================================
# TÌM NGƯỜI TRONG CSDL
# ==========================================================

def tim_nguoi(cau_hoi):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                Id,
                HoTen,
                SDT
            FROM NguoiAn
            WHERE DangHoatDong = 1
            ORDER BY HoTen
        """)

        rows = cursor.fetchall()

        cau_hoi_lower = cau_hoi.lower()

        ket_qua = []

        for row in rows:

            ho_ten = str(row[1])

            if ho_ten.lower() in cau_hoi_lower:

                ket_qua.append(row)

        return ket_qua

    finally:

        connection.close()


# ==========================================================
# TỔNG QUAN CSDL
# ==========================================================

def lay_tong_quan_he_thong():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # --------------------------------------------------
        # Tổng số người
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM NguoiAn
            WHERE DangHoatDong = 1
        """)

        tong_nguoi = cursor.fetchone()[0] or 0

        # --------------------------------------------------
        # Tổng số ngày đã có dữ liệu
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM NgayAn
        """)

        tong_ngay = cursor.fetchone()[0] or 0

        # --------------------------------------------------
        # Tổng lượt ăn
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM ChiTietAn
            WHERE DaAn = 1
        """)

        tong_luot_an = cursor.fetchone()[0] or 0

        # --------------------------------------------------
        # Tổng tiền cơm
        # --------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(
                SUM(SoTienPhaiTra),
                0
            )
            FROM ChiTietAn
            WHERE DaAn = 1
        """)

        tong_tien = cursor.fetchone()[0] or 0

        return {
            "tong_nguoi": tong_nguoi,
            "tong_ngay": tong_ngay,
            "tong_luot_an": tong_luot_an,
            "tong_tien": tong_tien
        }

    finally:

        connection.close()


# ==========================================================
# TỔNG TIỀN TRONG KHOẢNG THỜI GIAN
# ==========================================================

def lay_thong_ke_khoang_thoi_gian(
    tu_ngay,
    den_ngay
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(c.Id),
                COUNT(
                    DISTINCT c.NguoiAnId
                ),
                COALESCE(
                    SUM(c.SoTienPhaiTra),
                    0
                )
            FROM ChiTietAn c

            INNER JOIN NgayAn a
                ON c.NgayAnId = a.Id

            WHERE a.Ngay BETWEEN ?
              AND ?
              AND c.DaAn = 1
        """, (
            tu_ngay,
            den_ngay
        ))

        row = cursor.fetchone()

        return {
            "so_luot_an": row[0] or 0,
            "so_nguoi": row[1] or 0,
            "tong_tien": row[2] or 0
        }

    finally:

        connection.close()

# ==========================================================
# CÔNG NỢ CỦA MỘT NGƯỜI
# ==========================================================

def lay_cong_no_nguoi(nguoi_an_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # --------------------------------------------------
        # Tổng tiền cơm phải trả
        # --------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(
                SUM(SoTienPhaiTra),
                0
            )
            FROM ChiTietAn
            WHERE NguoiAnId = ?
              AND DaAn = 1
        """, (nguoi_an_id,))

        tong_phai_tra = cursor.fetchone()[0] or 0

        # --------------------------------------------------
        # Tổng tiền đã nộp
        # --------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(
                SUM(SoTien),
                0
            )
            FROM GiaoDichNopTien
            WHERE NguoiAnId = ?
        """, (nguoi_an_id,))

        tong_da_nop = cursor.fetchone()[0] or 0

        # --------------------------------------------------
        # Tính công nợ
        # --------------------------------------------------

        cong_no = tong_phai_tra - tong_da_nop

        return {
            "tong_phai_tra": tong_phai_tra,
            "tong_da_nop": tong_da_nop,
            "cong_no": cong_no
        }

    finally:

        connection.close()
# ==========================================================
# PHÂN TÍCH CÂU HỎI
# ==========================================================

def lay_du_lieu_cho_ai(cau_hoi):

    cau_hoi_goc = cau_hoi.strip()

    cau_hoi_lower = cau_hoi_goc.lower()

    du_lieu = []

    # ======================================================
    # 1. GIỜ / NGÀY HIỆN TẠI
    # ======================================================

    if any(
        tu in cau_hoi_lower
        for tu in [
            "mấy giờ",
            "bây giờ",
            "giờ hiện tại",
            "thời gian hiện tại",
            "hôm nay là ngày mấy",
            "ngày hôm nay"
        ]
    ):

        du_lieu.append(
            lay_thoi_gian_hien_tai()
        )

    # ======================================================
    # 2. XÁC ĐỊNH NGÀY
    # ======================================================

    ngay = lay_ngay_tu_cau_hoi(
        cau_hoi_lower
    )

    # Nếu có chữ "hôm nay"
    if "hôm nay" in cau_hoi_lower:
        ngay_hien_tai = datetime.now()

        ngay = ngay_hien_tai.strftime(
            "%Y-%m-%d"
        )

    # ======================================================
    # 3. SỐ NGƯỜI / SUẤT ĂN
    # ======================================================

    if any(
        tu in cau_hoi_lower
        for tu in [
            "bao nhiêu người ăn",
            "số người ăn",
            "người ăn",
            "bao nhiêu suất",
            "số suất",
            "suất ăn"
        ]
    ):

        so_nguoi = lay_so_nguoi_an(ngay)

        if ngay:

            ngay_hien_thi = datetime.strptime(
                ngay,
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

            du_lieu.append(
                f"Ngày {ngay_hien_thi} "
                f"có {so_nguoi} người đã ăn."
            )

        else:

            du_lieu.append(
                f"Hôm nay có {so_nguoi} người đã ăn."
            )

    # ======================================================
    # 4. TIỀN CƠM
    # ======================================================

    if any(
        tu in cau_hoi_lower
        for tu in [
            "tổng tiền",
            "tiền cơm",
            "tiền phải thu",
            "phải trả",
            "doanh thu"
        ]
    ):

        tong_tien = lay_tong_tien_ngay(ngay)

        if ngay:

            ngay_hien_thi = datetime.strptime(
                ngay,
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

            du_lieu.append(
                f"Ngày {ngay_hien_thi} "
                f"có tổng tiền cơm "
                f"{tong_tien:,.0f} đồng."
            )

        else:

            du_lieu.append(
                f"Tổng tiền cơm hiện có trong dữ liệu "
                f"là {tong_tien:,.0f} đồng."
            )

    # ======================================================
    # 5. AI HỎI AI CÓ NHỮNG AI ĂN
    # ======================================================

    if any(
        tu in cau_hoi_lower
        for tu in [
            "ai ăn",
            "những ai ăn",
            "danh sách người ăn",
            "người nào ăn"
        ]
    ):

        danh_sach = lay_danh_sach_nguoi_an(
            ngay
        )

        if danh_sach:

            noi_dung = ", ".join(
                danh_sach
            )

            if ngay:

                ngay_hien_thi = datetime.strptime(
                    ngay,
                    "%Y-%m-%d"
                ).strftime("%d/%m/%Y")

                du_lieu.append(
                    f"Ngày {ngay_hien_thi}, "
                    f"những người đã ăn gồm: "
                    f"{noi_dung}."
                )

            else:

                du_lieu.append(
                    "Hôm nay những người đã ăn gồm: "
                    f"{noi_dung}."
                )

        else:

            du_lieu.append(
                "Không tìm thấy người nào đã ăn "
                "trong ngày được hỏi."
            )

    # ======================================================
    # 6. LỊCH SỬ MỘT NGƯỜI
    # ======================================================

    nguoi_tim_duoc = tim_nguoi(
        cau_hoi_goc
    )

    if (
        nguoi_tim_duoc
        and any(
            tu in cau_hoi_lower
            for tu in [
                "lịch sử",
                "đã ăn",
                "ăn những ngày",
                "những ngày nào",
                "bao nhiêu ngày"
            ]
        )
    ):

        for nguoi in nguoi_tim_duoc[:3]:

            ten = nguoi[1]

            lich_su = lay_lich_su_nguoi_an(
                ten
            )

            if not lich_su:

                du_lieu.append(
                    f"Chưa có dữ liệu ăn của {ten}."
                )

                continue

            so_ngay_an = sum(
                1
                for row in lich_su
                if row[2] == 1
            )

            tong_tien = sum(
                int(row[3] or 0)
                for row in lich_su
                if row[2] == 1
            )

            cac_ngay = [
                row[1]
                for row in lich_su
                if row[2] == 1
            ]

            du_lieu.append(
                f"{ten}: đã ăn {so_ngay_an} ngày, "
                f"tổng tiền {tong_tien:,.0f} đồng. "
                f"Các ngày đã ăn: "
                f"{', '.join(map(str, cac_ngay))}."
            )
    # ==========================================================
    # 7. CÔNG NỢ CỦA MỘT NGƯỜI
    # ==========================================================

    if (
            nguoi_tim_duoc
            and any(
        tu in cau_hoi_lower
        for tu in [
            "còn nợ",
            "công nợ",
            "nợ bao nhiêu",
            "nợ tiền",
            "tiền nợ",
            "chưa trả",
            "chưa nộp",
            "đã nộp bao nhiêu"
        ]
    )
    ):

        for nguoi in nguoi_tim_duoc[:3]:

            nguoi_an_id = nguoi[0]
            ten = nguoi[1]

            cong_no = lay_cong_no_nguoi(
                nguoi_an_id
            )

            tong_phai_tra = cong_no["tong_phai_tra"]
            tong_da_nop = cong_no["tong_da_nop"]
            so_con_no = cong_no["cong_no"]

            if so_con_no > 0:

                du_lieu.append(
                    f"{ten} đã phát sinh "
                    f"{tong_phai_tra:,.0f} đồng tiền cơm, "
                    f"đã nộp {tong_da_nop:,.0f} đồng, "
                    f"còn nợ {so_con_no:,.0f} đồng."
                )

            elif so_con_no == 0:

                du_lieu.append(
                    f"{ten} đã phát sinh "
                    f"{tong_phai_tra:,.0f} đồng tiền cơm "
                    f"và đã nộp đủ {tong_da_nop:,.0f} đồng. "
                    f"Hiện không còn nợ."
                )

            else:

                du_lieu.append(
                    f"{ten} đã phát sinh "
                    f"{tong_phai_tra:,.0f} đồng tiền cơm, "
                    f"đã nộp {tong_da_nop:,.0f} đồng. "
                    f"Số tiền nộp dư là "
                    f"{abs(so_con_no):,.0f} đồng."
                )
    # ======================================================
    # 8. TỔNG QUAN HỆ THỐNG
    # ======================================================

    if any(
        tu in cau_hoi_lower
        for tu in [
            "hệ thống có bao nhiêu người",
            "có bao nhiêu người",
            "tổng số người",
            "tổng quan hệ thống"
        ]
    ):

        thong_ke = lay_tong_quan_he_thong()

        du_lieu.append(
            f"Hệ thống hiện có "
            f"{thong_ke['tong_nguoi']} người đang hoạt động, "
            f"{thong_ke['tong_ngay']} ngày có dữ liệu, "
            f"{thong_ke['tong_luot_an']} lượt ăn và "
            f"{thong_ke['tong_tien']:,.0f} đồng tiền cơm."
        )

    # ======================================================
    # 9. KHÔNG CÓ DỮ LIỆU DB
    # ======================================================

    return "\n".join(du_lieu)