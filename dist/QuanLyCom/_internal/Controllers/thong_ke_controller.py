from Database.database import get_connection


class ThongKeController:

    @staticmethod
    def thong_ke_theo_khoang_ngay(
        tu_ngay,
        den_ngay
    ):
        if not tu_ngay or not den_ngay:
            return {
                "success": False,
                "message": "Vui lòng chọn đầy đủ ngày.",
                "data": None
            }

        if tu_ngay > den_ngay:
            return {
                "success": False,
                "message": "Ngày bắt đầu không được lớn hơn ngày kết thúc.",
                "data": None
            }

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # Số người đã ăn
            cursor.execute("""
                SELECT COUNT(*)
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON c.NgayAnId = n.Id
                WHERE c.DaAn = 1
                  AND n.Ngay BETWEEN ? AND ?
            """, (tu_ngay, den_ngay))

            tong_luot_an = cursor.fetchone()[0] or 0

            # Tổng tiền phải thu
            cursor.execute("""
                SELECT COALESCE(SUM(c.SoTienPhaiTra), 0)
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON c.NgayAnId = n.Id
                WHERE c.DaAn = 1
                  AND n.Ngay BETWEEN ? AND ?
            """, (tu_ngay, den_ngay))

            tong_tien = cursor.fetchone()[0] or 0

            # Số ngày có dữ liệu
            cursor.execute("""
                SELECT COUNT(*)
                FROM NgayAn
                WHERE Ngay BETWEEN ? AND ?
            """, (tu_ngay, den_ngay))

            so_ngay = cursor.fetchone()[0] or 0

            # Trung bình tiền / lượt ăn
            if tong_luot_an > 0:
                trung_binh = tong_tien / tong_luot_an
            else:
                trung_binh = 0

            return {
                "success": True,
                "data": {
                    "tu_ngay": tu_ngay,
                    "den_ngay": den_ngay,
                    "so_ngay": so_ngay,
                    "tong_luot_an": tong_luot_an,
                    "tong_tien": tong_tien,
                    "trung_binh": trung_binh
                }
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi thống kê: {error}",
                "data": None
            }

        finally:
            connection.close()

    @staticmethod
    def thong_ke_theo_ngay(ngay):
        return ThongKeController.thong_ke_theo_khoang_ngay(
            ngay,
            ngay
        )

    @staticmethod
    def thong_ke_tung_ngay(
        tu_ngay,
        den_ngay
    ):
        if not tu_ngay or not den_ngay:
            return {
                "success": False,
                "message": "Vui lòng chọn đầy đủ ngày.",
                "data": []
            }

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Ngay,
                    COUNT(
                        CASE
                            WHEN c.DaAn = 1 THEN 1
                        END
                    ) AS SoNguoiAn,
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
                FROM NgayAn n
                LEFT JOIN ChiTietAn c
                    ON c.NgayAnId = n.Id
                WHERE n.Ngay BETWEEN ? AND ?
                GROUP BY n.Id, n.Ngay
                ORDER BY n.Ngay
            """, (tu_ngay, den_ngay))

            return {
                "success": True,
                "data": cursor.fetchall()
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi thống kê: {error}",
                "data": []
            }

        finally:
            connection.close()

    @staticmethod
    def thong_ke_theo_nguoi(
            tu_ngay,
            den_ngay
    ):
        if not tu_ngay or not den_ngay:
            return {
                "success": False,
                "message": "Vui lòng chọn đầy đủ ngày.",
                "data": []
            }

        if tu_ngay > den_ngay:
            return {
                "success": False,
                "message": "Ngày bắt đầu không được lớn hơn ngày kết thúc.",
                "data": []
            }

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                           SELECT n.Id,
                                  n.HoTen,
                                  COUNT(
                                          CASE
                                              WHEN c.DaAn = 1 THEN 1
                                              END
                                  ) AS SoLanAn,
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
                           FROM NguoiAn n
                                    LEFT JOIN ChiTietAn c
                                              ON c.NguoiAnId = n.Id
                                    LEFT JOIN NgayAn a
                                              ON c.NgayAnId = a.Id
                           WHERE a.Ngay BETWEEN ? AND ?
                              OR a.Ngay IS NULL
                           GROUP BY n.Id, n.HoTen
                           ORDER BY n.HoTen
                           """, (tu_ngay, den_ngay))

            return {
                "success": True,
                "data": cursor.fetchall()
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi thống kê: {error}",
                "data": []
            }

        finally:
            connection.close()
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    n.Id,
                    n.HoTen,
                    COUNT(
                        CASE
                            WHEN c.DaAn = 1 THEN 1
                        END
                    ) AS SoLanAn,
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
                FROM NguoiAn n
                LEFT JOIN ChiTietAn c
                    ON c.NguoiAnId = n.Id
                LEFT JOIN NgayAn a
                    ON c.NgayAnId = a.Id
                    AND a.Ngay BETWEEN ? AND ?
                GROUP BY n.Id, n.HoTen
                ORDER BY n.HoTen
            """, (tu_ngay, den_ngay))

            return {
                "success": True,
                "data": cursor.fetchall()
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi thống kê: {error}",
                "data": []
            }

        finally:
            connection.close()