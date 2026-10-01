from datetime import date, timedelta

from Database.database import get_connection


class ThongKeController:

    @staticmethod
    def _to_date(value):
        if isinstance(value, date):
            return value

        if not value:
            return None

        try:
            return date.fromisoformat(str(value)[:10])
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _normalize_week_range(tu_ngay, den_ngay):
        start = ThongKeController._to_date(tu_ngay)
        end = ThongKeController._to_date(den_ngay)

        if not start or not end:
            return None, None

        monday = start - timedelta(days=start.weekday())
        saturday = monday + timedelta(days=5)

        if end > saturday:
            monday = end - timedelta(days=end.weekday())
            saturday = monday + timedelta(days=5)

        return monday, saturday

    @staticmethod
    def thong_ke_tong_hop(tu_ngay, den_ngay, bo_phan_id=None):
        if not tu_ngay or not den_ngay:
            return {
                "success": False,
                "message": "Vui lòng chọn đầy đủ ngày.",
                "data": [],
            }

        start = ThongKeController._to_date(tu_ngay)
        end = ThongKeController._to_date(den_ngay)

        if not start or not end:
            return {
                "success": False,
                "message": "Khoảng ngày không hợp lệ.",
                "data": [],
            }

        if start > end:
            return {
                "success": False,
                "message": "Ngày bắt đầu không được lớn hơn ngày kết thúc.",
                "data": [],
            }

        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                SELECT
                    n.Id,
                    n.HoTen,
                    COALESCE(b.TenBoPhan, 'Chưa phân bộ phận') AS TenBoPhan,
                    COUNT(DISTINCT a.Ngay) AS SoNgayAn,
                    COUNT(CASE WHEN c.DaAn = 1 THEN 1 END) AS SoSuat,
                    COALESCE(
                        SUM(
                            CASE
                                WHEN c.DaAn = 1 THEN c.SoTienPhaiTra
                                ELSE 0
                            END
                        ),
                        0
                    ) AS TienCom
                FROM NguoiAn n
                LEFT JOIN BoPhan b
                    ON n.BoPhanId = b.Id
                INNER JOIN ChiTietAn c
                    ON c.NguoiAnId = n.Id
                INNER JOIN NgayAn a
                    ON c.NgayAnId = a.Id
                WHERE a.Ngay BETWEEN ? AND ?
                  AND c.DaAn = 1
            """

            params = [
                start.isoformat(),
                end.isoformat(),
            ]

            if bo_phan_id is not None:
                sql += """
                    AND n.BoPhanId = ?
                """
                params.append(bo_phan_id)

            sql += """
                GROUP BY
                    n.Id,
                    n.HoTen,
                    b.TenBoPhan
                ORDER BY
                    n.HoTen COLLATE NOCASE
            """

            cursor.execute(sql, params)
            rows = cursor.fetchall()

            tong_nguoi = len(rows)
            tong_ngay_an = sum(
                int(row[3] or 0)
                for row in rows
            )
            tong_suat = sum(
                int(row[4] or 0)
                for row in rows
            )
            tong_tien = sum(
                float(row[5] or 0)
                for row in rows
            )

            return {
                "success": True,
                "data": rows,
                "summary": {
                    "tong_nguoi": tong_nguoi,
                    "tong_ngay_an": tong_ngay_an,
                    "tong_suat": tong_suat,
                    "tong_tien": tong_tien,
                },
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi thống kê: {error}",
                "data": [],
            }

        finally:
            connection.close()

    @staticmethod
    def lay_bo_phan():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Id,
                    TenBoPhan
                FROM BoPhan
                WHERE DangHoatDong = 1
                ORDER BY TenBoPhan COLLATE NOCASE
            """)

            return cursor.fetchall()

        except Exception:
            return []

        finally:
            connection.close()

    @staticmethod
    def thong_ke_theo_khoang_ngay(tu_ngay, den_ngay):
        if not tu_ngay or not den_ngay:
            return {
                "success": False,
                "message": "Khoảng ngày không hợp lệ.",
                "data": None,
            }

        start = ThongKeController._to_date(tu_ngay)
        end = ThongKeController._to_date(den_ngay)

        if not start or not end or start > end:
            return {
                "success": False,
                "message": "Khoảng ngày không hợp lệ.",
                "data": None,
            }

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COUNT(DISTINCT n.Ngay),
                    COUNT(
                        CASE
                            WHEN c.DaAn = 1 THEN 1
                        END
                    ),
                    COALESCE(
                        SUM(
                            CASE
                                WHEN c.DaAn = 1 THEN c.SoTienPhaiTra
                                ELSE 0
                            END
                        ),
                        0
                    )
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON c.NgayAnId = n.Id
                WHERE c.DaAn = 1
                  AND n.Ngay BETWEEN ? AND ?
            """, (
                start.isoformat(),
                end.isoformat(),
            ))

            row = cursor.fetchone()

            tong_luot_an = int(row[1] or 0)
            tong_tien = float(row[2] or 0)

            return {
                "success": True,
                "data": {
                    "so_ngay": int(row[0] or 0),
                    "tong_luot_an": tong_luot_an,
                    "tong_tien": tong_tien,
                    "trung_binh": (
                        tong_tien / tong_luot_an
                        if tong_luot_an
                        else 0
                    ),
                },
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi thống kê: {error}",
                "data": None,
            }

        finally:
            connection.close()

    @staticmethod
    def thong_ke_theo_tuan(tu_ngay, den_ngay, bo_phan_id=None):
        start, end = ThongKeController._normalize_week_range(
            tu_ngay,
            den_ngay,
        )

        if not start or not end:
            return {
                "success": False,
                "message": "Khoảng tuần không hợp lệ.",
                "data": [],
            }

        return ThongKeController.thong_ke_tong_hop(
            start.isoformat(),
            end.isoformat(),
            bo_phan_id,
        )

    @staticmethod
    def thong_ke_theo_thang(nam, thang, bo_phan_id=None):
        try:
            nam = int(nam)
            thang = int(thang)

            if thang < 1 or thang > 12:
                return {
                    "success": False,
                    "message": "Tháng không hợp lệ.",
                    "data": [],
                }

            ngay_dau = date(nam, thang, 1)

            if thang == 12:
                ngay_cuoi = date(nam + 1, 1, 1) - timedelta(days=1)
            else:
                ngay_cuoi = date(nam, thang + 1, 1) - timedelta(days=1)

            return ThongKeController.thong_ke_tong_hop(
                ngay_dau.isoformat(),
                ngay_cuoi.isoformat(),
                bo_phan_id,
            )

        except (ValueError, TypeError):
            return {
                "success": False,
                "message": "Năm hoặc tháng không hợp lệ.",
                "data": [],
            }