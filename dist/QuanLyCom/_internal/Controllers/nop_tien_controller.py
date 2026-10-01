# -*- coding: utf-8 -*-

from datetime import date, timedelta

import pandas as pd

from Models.giao_dich_model import GiaoDichNopTienModel
from Models.audit_log_model import AuditLogModel
from Models.chi_tiet_an_model import ChiTietAnModel
from Database.database import get_connection


class NopTienController:

    # ==========================================================
    # HÀM PHỤ
    # ==========================================================

    @staticmethod
    def _to_date(value):
        if value is None:
            return None

        if isinstance(value, date):
            return value

        try:
            return date.fromisoformat(
                str(value)[:10]
            )
        except Exception:
            return None

    @staticmethod
    def _status(balance):
        balance = float(balance or 0)

        # Tránh sai số float rất nhỏ
        if abs(balance) < 0.01:
            return "Đã đủ"

        if balance < 0:
            return "Còn nợ"

        return "Nộp thừa"

    @staticmethod
    def _month_range(year, month):

        start = date(
            int(year),
            int(month),
            1
        )

        if int(month) == 12:

            end = date(
                int(year) + 1,
                1,
                1
            ) - timedelta(days=1)

        else:

            end = date(
                int(year),
                int(month) + 1,
                1
            ) - timedelta(days=1)

        return start, end

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

        try:

            if nguoi_an_id is None:
                raise ValueError(
                    "Chưa chọn người nộp."
                )

            so_tien = float(so_tien)

            if so_tien <= 0:
                raise ValueError(
                    "Số tiền phải lớn hơn 0."
                )

            if not ngay_nop:
                raise ValueError(
                    "Ngày nộp không hợp lệ."
                )

            giao_dich_id = (
                GiaoDichNopTienModel
                .them_giao_dich(
                    nguoi_an_id=nguoi_an_id,
                    ngay_nop=ngay_nop,
                    so_tien=so_tien,
                    hinh_thuc=hinh_thuc,
                    ghi_chu=ghi_chu
                )
            )

            AuditLogModel.ghi_log(
                hanh_dong="NỘP TIỀN",
                mo_ta=(
                    f"Người ăn ID: {nguoi_an_id}, "
                    f"Số tiền: {so_tien:,.0f}, "
                    f"Ngày nộp: {ngay_nop}, "
                    f"Hình thức: {hinh_thuc}"
                )
            )

            return {
                "success": True,
                "message": "Nộp tiền thành công.",
                "id": giao_dich_id
            }

        except ValueError as error:

            return {
                "success": False,
                "message": str(error)
            }

        except Exception as error:

            return {
                "success": False,
                "message": f"Có lỗi xảy ra: {error}"
            }

    # ==========================================================
    # LẤY TẤT CẢ
    # ==========================================================

    @staticmethod
    def lay_tat_ca():

        try:

            return {
                "success": True,
                "data": (
                    GiaoDichNopTienModel
                    .lay_tat_ca()
                )
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể lấy giao dịch: {error}"
                ),
                "data": []
            }

    # ==========================================================
    # THEO NGƯỜI
    # ==========================================================

    @staticmethod
    def lay_theo_nguoi(nguoi_an_id):

        try:

            return {
                "success": True,
                "data": (
                    GiaoDichNopTienModel
                    .lay_theo_nguoi(
                        nguoi_an_id
                    )
                )
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể lấy giao dịch: {error}"
                ),
                "data": []
            }

    # ==========================================================
    # TÌM THEO ID
    # ==========================================================

    @staticmethod
    def tim_theo_id(giao_dich_id):

        try:

            data = (
                GiaoDichNopTienModel
                .tim_theo_id(
                    giao_dich_id
                )
            )

            if data is None:

                return {
                    "success": False,
                    "message": "Không tìm thấy giao dịch.",
                    "data": None
                }

            return {
                "success": True,
                "data": data
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể lấy giao dịch: {error}"
                ),
                "data": None
            }

    # ==========================================================
    # SỬA GIAO DỊCH
    # ==========================================================

    @staticmethod
    def cap_nhat_giao_dich(
        giao_dich_id,
        nguoi_an_id,
        ngay_nop,
        so_tien,
        hinh_thuc="Tiền mặt",
        ghi_chu=None
    ):

        try:

            so_tien = float(so_tien)

            if so_tien <= 0:
                raise ValueError(
                    "Số tiền phải lớn hơn 0."
                )

            giao_dich_cu = (
                GiaoDichNopTienModel
                .tim_theo_id(
                    giao_dich_id
                )
            )

            if giao_dich_cu is None:

                return {
                    "success": False,
                    "message": "Không tìm thấy giao dịch."
                }

            so_dong = (
                GiaoDichNopTienModel
                .cap_nhat(
                    giao_dich_id=giao_dich_id,
                    nguoi_an_id=nguoi_an_id,
                    ngay_nop=ngay_nop,
                    so_tien=so_tien,
                    hinh_thuc=hinh_thuc,
                    ghi_chu=ghi_chu
                )
            )

            if so_dong == 0:

                return {
                    "success": False,
                    "message": (
                        "Không có dữ liệu nào được thay đổi."
                    )
                }

            AuditLogModel.ghi_log(
                hanh_dong="SỬA GIAO DỊCH NỘP TIỀN",
                mo_ta=(
                    f"Giao dịch ID: {giao_dich_id}. "
                    f"Trước: người={giao_dich_cu[2]}, "
                    f"ngày={giao_dich_cu[5]}, "
                    f"tiền={giao_dich_cu[6]:,.0f}, "
                    f"hình thức={giao_dich_cu[7]}. "
                    f"Sau: người ID={nguoi_an_id}, "
                    f"ngày={ngay_nop}, "
                    f"tiền={so_tien:,.0f}, "
                    f"hình thức={hinh_thuc}."
                )
            )

            return {
                "success": True,
                "message": (
                    "Cập nhật giao dịch thành công."
                )
            }

        except ValueError as error:

            return {
                "success": False,
                "message": str(error)
            }

        except Exception as error:

            return {
                "success": False,
                "message": f"Có lỗi xảy ra: {error}"
            }

    # ==========================================================
    # TỔNG ĐÃ NỘP
    # ==========================================================

    @staticmethod
    def tong_tien_da_nop(nguoi_an_id):

        try:

            value = (
                GiaoDichNopTienModel
                .tong_tien_da_nop(
                    nguoi_an_id
                )
            )

            return {
                "success": True,
                "data": float(value or 0)
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể tính tổng tiền: {error}"
                ),
                "data": 0
            }

    # ==========================================================
    # TỔNG ĐÃ NỘP THEO KHOẢNG
    # ==========================================================

    @staticmethod
    def tong_tien_theo_khoang_thoi_gian(
        tu_ngay=None,
        den_ngay=None,
        nguoi_an_id=None
    ):

        try:

            value = (
                GiaoDichNopTienModel
                .tong_tien_theo_khoang_thoi_gian(
                    tu_ngay=tu_ngay,
                    den_ngay=den_ngay,
                    nguoi_an_id=nguoi_an_id
                )
            )

            return {
                "success": True,
                "data": float(value or 0)
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể tính tổng tiền: {error}"
                ),
                "data": 0
            }

    # ==========================================================
    # LẤY GIAO DỊCH THEO KHOẢNG
    # ==========================================================

    @staticmethod
    def lay_theo_khoang_thoi_gian(
        tu_ngay=None,
        den_ngay=None,
        nguoi_an_id=None,
        bo_phan_id=None,
        hinh_thuc=None
    ):

        try:

            data = (
                GiaoDichNopTienModel
                .lay_theo_khoang_thoi_gian(
                    tu_ngay=tu_ngay,
                    den_ngay=den_ngay,
                    nguoi_an_id=nguoi_an_id,
                    bo_phan_id=bo_phan_id,
                    hinh_thuc=hinh_thuc
                )
            )

            return {
                "success": True,
                "data": data
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể lấy giao dịch: {error}"
                ),
                "data": []
            }

    # ==========================================================
    # THỐNG KÊ HÌNH THỨC NỘP
    # ==========================================================

    @staticmethod
    def tong_tien_theo_hinh_thuc(
        tu_ngay=None,
        den_ngay=None
    ):

        try:

            raw = (
                GiaoDichNopTienModel
                .tong_tien_theo_hinh_thuc(
                    tu_ngay=tu_ngay,
                    den_ngay=den_ngay
                )
            )

            result = []

            for row in raw or []:

                method = (
                    row[0]
                    if len(row) > 0
                    else ""
                )

                amount = (
                    row[1]
                    if len(row) > 1
                    else 0
                )

                result.append(
                    {
                        "hinh_thuc": method,
                        "so_giao_dich": 0,
                        "tong_tien": float(
                            amount or 0
                        )
                    }
                )

            # Đếm số giao dịch riêng
            connection = get_connection()

            try:

                cursor = connection.cursor()

                dieu_kien = []
                params = []

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

                where = ""

                if dieu_kien:
                    where = (
                        "WHERE "
                        + " AND ".join(
                            dieu_kien
                        )
                    )

                cursor.execute(
                    f"""
                    SELECT
                        HinhThuc,
                        COUNT(*)
                    FROM GiaoDichNopTien
                    {where}
                    GROUP BY HinhThuc
                    """,
                    tuple(params)
                )

                count_map = {
                    row[0]: row[1]
                    for row in cursor.fetchall()
                }

            finally:

                connection.close()

            for item in result:

                item["so_giao_dich"] = (
                    count_map.get(
                        item["hinh_thuc"],
                        0
                    )
                )

            return {
                "success": True,
                "data": result
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể thống kê hình thức nộp: {error}"
                ),
                "data": []
            }

    # ==========================================================
    # ĐẾM SỐ LẦN NỘP
    # ==========================================================

    @staticmethod
    def dem_so_lan_nop(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):

        try:

            value = (
                GiaoDichNopTienModel
                .dem_so_lan_nop(
                    nguoi_an_id=nguoi_an_id,
                    tu_ngay=tu_ngay,
                    den_ngay=den_ngay
                )
            )

            return {
                "success": True,
                "data": int(value or 0)
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể đếm số lần nộp: {error}"
                ),
                "data": 0
            }

    # ==========================================================
    # TIỀN PHẢI TRẢ TOÀN BỘ
    # ==========================================================

    @staticmethod
    def tinh_tien_phai_tra(
        nguoi_an_id
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    COALESCE(
                        SUM(SoTienPhaiTra),
                        0
                    )
                FROM ChiTietAn
                WHERE NguoiAnId = ?
                  AND DaAn = 1
                """,
                (
                    nguoi_an_id,
                )
            )

            result = cursor.fetchone()

            return float(
                result[0] or 0
            )

        finally:

            connection.close()

    # ==========================================================
    # TIỀN PHẢI TRẢ THEO KHOẢNG
    #
    # Chỉ tính DaAn = 1.
    #
    # Vì vậy:
    # - Đi công tác
    # - Không ăn
    # - Nghỉ
    #
    # nếu không có DaAn = 1 thì không bị tính tiền.
    # ==========================================================

    @staticmethod
    def tinh_tien_phai_tra_theo_khoang(
        nguoi_an_id=None,
        tu_ngay=None,
        den_ngay=None
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            dieu_kien = [
                "c.DaAn = 1"
            ]

            params = []

            if nguoi_an_id is not None:

                dieu_kien.append(
                    "c.NguoiAnId = ?"
                )

                params.append(
                    nguoi_an_id
                )

            if tu_ngay:

                dieu_kien.append(
                    "n.Ngay >= ?"
                )

                params.append(
                    tu_ngay
                )

            if den_ngay:

                dieu_kien.append(
                    "n.Ngay <= ?"
                )

                params.append(
                    den_ngay
                )

            cursor.execute(
                f"""
                SELECT
                    COALESCE(
                        SUM(c.SoTienPhaiTra),
                        0
                    )
                FROM ChiTietAn c
                INNER JOIN NgayAn n
                    ON c.NgayAnId = n.Id
                WHERE
                    {" AND ".join(dieu_kien)}
                """,
                tuple(params)
            )

            result = cursor.fetchone()

            return float(
                result[0] or 0
            )

        finally:

            connection.close()

    # ==========================================================
    # SUẤT ĂN PHÁT SINH
    #
    # Không gán vào công nợ cá nhân vì bảng
    # SuatAnPhatSinh không có NguoiAnId.
    # ==========================================================

    @staticmethod
    def lay_suat_an_phat_sinh(
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
                    "n.Ngay >= ?"
                )

                params.append(
                    tu_ngay
                )

            if den_ngay:

                dieu_kien.append(
                    "n.Ngay <= ?"
                )

                params.append(
                    den_ngay
                )

            where = ""

            if dieu_kien:

                where = (
                    "WHERE "
                    + " AND ".join(
                        dieu_kien
                    )
                )

            cursor.execute(
                f"""
                SELECT
                    s.Id,
                    s.NgayAnId,
                    n.Ngay,
                    s.HoTen,
                    s.DonVi,
                    s.SoLuong,
                    s.DonGia,
                    COALESCE(
                        s.SoLuong * s.DonGia,
                        0
                    ) AS ThanhTien,
                    s.GhiChu,
                    s.NgayTao
                FROM SuatAnPhatSinh s
                LEFT JOIN NgayAn n
                    ON s.NgayAnId = n.Id
                {where}
                ORDER BY
                    n.Ngay DESC,
                    s.Id DESC
                """,
                tuple(params)
            )

            return cursor.fetchall()

        finally:

            connection.close()

    @staticmethod
    def tong_tien_suat_an_phat_sinh(
        tu_ngay=None,
        den_ngay=None
    ):

        rows = (
            NopTienController
            .lay_suat_an_phat_sinh(
                tu_ngay=tu_ngay,
                den_ngay=den_ngay
            )
        )

        total = 0

        for row in rows:

            try:
                total += float(
                    row[7] or 0
                )
            except Exception:
                pass

        return total

    # ==========================================================
    # SỐ DƯ TOÀN BỘ
    # ==========================================================

    @staticmethod
    def tinh_so_du(nguoi_an_id):

        try:

            tong_da_nop = (
                GiaoDichNopTienModel
                .tong_tien_da_nop(
                    nguoi_an_id
                )
            )

            tong_phai_tra = (
                NopTienController
                .tinh_tien_phai_tra(
                    nguoi_an_id
                )
            )

            so_du = (
                float(tong_da_nop or 0)
                - float(tong_phai_tra or 0)
            )

            return {
                "success": True,
                "data": so_du,
                "tong_da_nop": float(
                    tong_da_nop or 0
                ),
                "tong_phai_tra": float(
                    tong_phai_tra or 0
                ),
                "status": (
                    NopTienController
                    ._status(so_du)
                )
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể tính số dư: {error}"
                ),
                "data": 0,
                "tong_da_nop": 0,
                "tong_phai_tra": 0,
                "status": "Không xác định"
            }

    # ==========================================================
    # CÔNG NỢ TRONG KỲ
    # ==========================================================

    @staticmethod
    def tinh_cong_no_theo_khoang(
        nguoi_an_id=None,
        tu_ngay=None,
        den_ngay=None
    ):

        try:

            tong_da_nop = (
                GiaoDichNopTienModel
                .tong_tien_theo_khoang_thoi_gian(
                    tu_ngay=tu_ngay,
                    den_ngay=den_ngay,
                    nguoi_an_id=nguoi_an_id
                )
            )

            tong_phai_tra = (
                NopTienController
                .tinh_tien_phai_tra_theo_khoang(
                    nguoi_an_id=nguoi_an_id,
                    tu_ngay=tu_ngay,
                    den_ngay=den_ngay
                )
            )

            so_du = (
                float(tong_da_nop or 0)
                - float(tong_phai_tra or 0)
            )

            return {
                "success": True,
                "tong_da_nop": float(
                    tong_da_nop or 0
                ),
                "tong_phai_tra": float(
                    tong_phai_tra or 0
                ),
                "so_du": so_du,
                "trang_thai": (
                    NopTienController
                    ._status(so_du)
                )
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể tính công nợ: {error}"
                ),
                "tong_da_nop": 0,
                "tong_phai_tra": 0,
                "so_du": 0,
                "trang_thai": "Không xác định"
            }

    # ==========================================================
    # CÔNG NỢ LŨY KẾ
    #
    # opening = payment trước kỳ - due trước kỳ
    # closing = opening + payment kỳ - due kỳ
    # ==========================================================

    @staticmethod
    def tinh_cong_no_luy_ke(
        nguoi_an_id,
        tu_ngay,
        den_ngay
    ):

        try:

            start = (
                NopTienController
                ._to_date(tu_ngay)
            )

            end = (
                NopTienController
                ._to_date(den_ngay)
            )

            if not start or not end:

                raise ValueError(
                    "Khoảng ngày không hợp lệ."
                )

            if start > end:

                raise ValueError(
                    "Từ ngày không được lớn hơn đến ngày."
                )

            ngay_truoc = (
                start
                - timedelta(days=1)
            ).isoformat()

            # ------------------------------
            # Đầu kỳ
            # ------------------------------

            opening_paid = (
                GiaoDichNopTienModel
                .tong_tien_theo_khoang_thoi_gian(
                    tu_ngay=None,
                    den_ngay=ngay_truoc,
                    nguoi_an_id=nguoi_an_id
                )
            )

            opening_due = (
                NopTienController
                .tinh_tien_phai_tra_theo_khoang(
                    nguoi_an_id=nguoi_an_id,
                    tu_ngay=None,
                    den_ngay=ngay_truoc
                )
            )

            opening_balance = (
                float(opening_paid or 0)
                - float(opening_due or 0)
            )

            # ------------------------------
            # Trong kỳ
            # ------------------------------

            period_paid = (
                GiaoDichNopTienModel
                .tong_tien_theo_khoang_thoi_gian(
                    tu_ngay=start.isoformat(),
                    den_ngay=end.isoformat(),
                    nguoi_an_id=nguoi_an_id
                )
            )

            period_due = (
                NopTienController
                .tinh_tien_phai_tra_theo_khoang(
                    nguoi_an_id=nguoi_an_id,
                    tu_ngay=start.isoformat(),
                    den_ngay=end.isoformat()
                )
            )

            closing_balance = (
                opening_balance
                + float(period_paid or 0)
                - float(period_due or 0)
            )

            return {
                "success": True,
                "opening_balance": opening_balance,
                "period_due": float(
                    period_due or 0
                ),
                "period_paid": float(
                    period_paid or 0
                ),
                "closing_balance": closing_balance,
                "status": (
                    NopTienController
                    ._status(
                        closing_balance
                    )
                )
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể tính công nợ lũy kế: {error}"
                ),
                "opening_balance": 0,
                "period_due": 0,
                "period_paid": 0,
                "closing_balance": 0,
                "status": "Không xác định"
            }

    # ==========================================================
    # TỔNG HỢP TUẦN
    # ==========================================================

    @staticmethod
    def tong_hop_theo_tuan(
        nguoi_an_id,
        tu_ngay,
        den_ngay
    ):

        try:

            start = (
                NopTienController
                ._to_date(tu_ngay)
            )

            end = (
                NopTienController
                ._to_date(den_ngay)
            )

            if not start or not end:
                raise ValueError(
                    "Khoảng ngày không hợp lệ."
                )

            if start > end:
                raise ValueError(
                    "Khoảng ngày không hợp lệ."
                )

            result = []

            first_monday = (
                start
                - timedelta(days=start.weekday())
            )

            last_saturday = (
                end
                + timedelta(days=5 - end.weekday())
            )

            current = first_monday

            while current <= last_saturday:

                week_end = current + timedelta(days=5)

                summary = (
                    NopTienController
                    .tinh_cong_no_luy_ke(
                        nguoi_an_id=nguoi_an_id,
                        tu_ngay=current.isoformat(),
                        den_ngay=week_end.isoformat()
                    )
                )

                if summary.get("success"):

                    result.append(
                        {
                            "tu_ngay": current,
                            "den_ngay": week_end,
                            "opening_balance": summary[
                                "opening_balance"
                            ],
                            "period_due": summary[
                                "period_due"
                            ],
                            "period_paid": summary[
                                "period_paid"
                            ],
                            "closing_balance": summary[
                                "closing_balance"
                            ],
                            "status": summary[
                                "status"
                            ]
                        }
                    )

                current = (
                    week_end
                    + timedelta(days=2)
                )

            return {
                "success": True,
                "data": result
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể tổng hợp theo tuần: {error}"
                ),
                "data": []
            }

    # ==========================================================
    # TỔNG HỢP THÁNG
    # ==========================================================

    @staticmethod
    def tong_hop_theo_thang(
        nguoi_an_id,
        nam,
        thang
    ):

        try:

            start, end = (
                NopTienController
                ._month_range(
                    nam,
                    thang
                )
            )

            summary = (
                NopTienController
                .tinh_cong_no_luy_ke(
                    nguoi_an_id=nguoi_an_id,
                    tu_ngay=start.isoformat(),
                    den_ngay=end.isoformat()
                )
            )

            if not summary.get("success"):
                return summary

            weekly = (
                NopTienController
                .tong_hop_theo_tuan(
                    nguoi_an_id=nguoi_an_id,
                    tu_ngay=start.isoformat(),
                    den_ngay=end.isoformat()
                )
            )

            return {
                "success": True,
                "nam": int(nam),
                "thang": int(thang),
                "tu_ngay": start,
                "den_ngay": end,
                "opening_balance": summary[
                    "opening_balance"
                ],
                "period_due": summary[
                    "period_due"
                ],
                "period_paid": summary[
                    "period_paid"
                ],
                "closing_balance": summary[
                    "closing_balance"
                ],
                "status": summary[
                    "status"
                ],
                "weeks": weekly.get(
                    "data",
                    []
                )
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể tổng hợp tháng: {error}"
                )
            }

    # ==========================================================
    # CHI TIẾT TIỀN CƠM
    # ==========================================================

    @staticmethod
    def lay_chi_tiet_tien_com(
        nguoi_an_id,
        tu_ngay=None,
        den_ngay=None
    ):

        try:

            data = (
                ChiTietAnModel
                .lay_theo_nguoi(
                    nguoi_an_id
                )
            )

            if not tu_ngay and not den_ngay:
                return {
                    "success": True,
                    "data": data
                }

            start = (
                NopTienController
                ._to_date(tu_ngay)
            )

            end = (
                NopTienController
                ._to_date(den_ngay)
            )

            filtered = []

            for row in data:

                ngay = (
                    NopTienController
                    ._to_date(
                        row[4]
                        if len(row) > 4
                        else None
                    )
                )

                if start and (
                    not ngay
                    or ngay < start
                ):
                    continue

                if end and (
                    not ngay
                    or ngay > end
                ):
                    continue

                filtered.append(row)

            return {
                "success": True,
                "data": filtered
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"Không thể lấy chi tiết tiền cơm: {error}"
                ),
                "data": []
            }

    # ==========================================================
    # XÓA
    # ==========================================================

    @staticmethod
    def xoa(giao_dich_id):

        try:

            giao_dich = (
                GiaoDichNopTienModel
                .tim_theo_id(
                    giao_dich_id
                )
            )

            if giao_dich is None:

                return {
                    "success": False,
                    "message": "Không tìm thấy giao dịch."
                }

            so_dong = (
                GiaoDichNopTienModel
                .xoa(
                    giao_dich_id
                )
            )

            if so_dong == 0:

                return {
                    "success": False,
                    "message": "Không tìm thấy giao dịch."
                }

            AuditLogModel.ghi_log(
                hanh_dong="XÓA GIAO DỊCH NỘP TIỀN",
                mo_ta=(
                    f"Giao dịch ID: {giao_dich_id}, "
                    f"Người: {giao_dich[2]}, "
                    f"Ngày: {giao_dich[5]}, "
                    f"Số tiền: {giao_dich[6]:,.0f}, "
                    f"Hình thức: {giao_dich[7]}"
                )
            )

            return {
                "success": True,
                "message": "Xóa giao dịch thành công."
            }

        except Exception as error:

            return {
                "success": False,
                "message": f"Có lỗi xảy ra: {error}"
            }

    # ==========================================================
    # DATAFRAME - TỔNG HỢP NGƯỜI
    # ==========================================================

    @staticmethod
    def tao_dataframe_tong_hop(
        people,
        tu_ngay=None,
        den_ngay=None
    ):
        """
        Tạo DataFrame dùng cho:
        - màn hình
        - Excel
        """

        rows = []

        for person in people:

            try:

                nguoi_id = person[0]
                ho_ten = person[1]

                bo_phan_id = (
                    person[5]
                    if len(person) > 5
                    else None
                )

                bo_phan = (
                    person[6]
                    if len(person) > 6
                    else ""
                )

            except Exception:

                continue

            if tu_ngay and den_ngay:

                result = (
                    NopTienController
                    .tinh_cong_no_luy_ke(
                        nguoi_an_id=nguoi_id,
                        tu_ngay=tu_ngay,
                        den_ngay=den_ngay
                    )
                )

            else:

                result = (
                    NopTienController
                    .tinh_so_du(
                        nguoi_id
                        if False
                        else nguoi_id
                    )
                )

                if result.get("success"):

                    result = {
                        "success": True,
                        "opening_balance": 0,
                        "period_due": result.get(
                            "tong_phai_tra",
                            0
                        ),
                        "period_paid": result.get(
                            "tong_da_nop",
                            0
                        ),
                        "closing_balance": result.get(
                            "data",
                            0
                        ),
                        "status": result.get(
                            "status",
                            NopTienController._status(
                                result.get(
                                    "data",
                                    0
                                )
                            )
                        )
                    }

            if not result.get("success"):
                continue

            opening = float(
                result.get(
                    "opening_balance",
                    0
                ) or 0
            )

            due = float(
                result.get(
                    "period_due",
                    0
                ) or 0
            )

            paid = float(
                result.get(
                    "period_paid",
                    0
                ) or 0
            )

            closing = float(
                result.get(
                    "closing_balance",
                    0
                ) or 0
            )

            rows.append(
                {
                    "Người ID": nguoi_id,
                    "Người": ho_ten,
                    "Bộ phận ID": bo_phan_id,
                    "Bộ phận": bo_phan or "",
                    "Nợ đầu kỳ": opening,
                    "Phải trả": due,
                    "Đã nộp": paid,
                    "Còn nợ": (
                        abs(closing)
                        if closing < 0
                        else 0
                    ),
                    "Nộp thừa": (
                        closing
                        if closing > 0
                        else 0
                    ),
                    "Số dư": closing,
                    "Trạng thái": result.get(
                        "status",
                        NopTienController._status(
                            closing
                        )
                    )
                }
            )

        return pd.DataFrame(rows)

    # ==========================================================
    # DATAFRAME - THEO TUẦN
    # ==========================================================

    @staticmethod
    def tao_dataframe_tong_hop_tuan(
        people,
        tu_ngay,
        den_ngay
    ):

        start = (
            NopTienController
            ._to_date(tu_ngay)
        )

        end = (
            NopTienController
            ._to_date(den_ngay)
        )

        rows = []

        if not start or not end:
            return pd.DataFrame()

        # Tuần chuẩn của công ty: Thứ 2 đến Thứ 7.
        # Khi khoảng lọc là tháng, tuần đầu/cuối có thể nằm ngoài tháng
        # để giữ đúng tuần lịch thực tế, giống logic báo cáo.
        first_monday = (
            start
            - timedelta(days=start.weekday())
        )

        last_saturday = (
            end
            + timedelta(days=5 - end.weekday())
        )

        current = first_monday
        week_number = 1

        while current <= last_saturday:

            week_end = current + timedelta(days=5)

            opening = 0
            due = 0
            paid = 0
            closing = 0

            for person in people:

                result = (
                    NopTienController
                    .tinh_cong_no_luy_ke(
                        nguoi_an_id=person[0],
                        tu_ngay=current.isoformat(),
                        den_ngay=week_end.isoformat()
                    )
                )

                if not result.get("success"):
                    continue

                opening += float(
                    result.get(
                        "opening_balance",
                        0
                    ) or 0
                )

                due += float(
                    result.get(
                        "period_due",
                        0
                    ) or 0
                )

                paid += float(
                    result.get(
                        "period_paid",
                        0
                    ) or 0
                )

                closing += float(
                    result.get(
                        "closing_balance",
                        0
                    ) or 0
                )

            rows.append(
                {
                    "Tuần": f"Tuần {week_number}",
                    "Từ ngày": current,
                    "Đến ngày": week_end,
                    "Nợ đầu kỳ": opening,
                    "Phải trả": due,
                    "Đã nộp": paid,
                    "Còn nợ": (
                        abs(closing)
                        if closing < 0
                        else 0
                    ),
                    "Nộp thừa": (
                        closing
                        if closing > 0
                        else 0
                    ),
                    "Trạng thái": (
                        NopTienController
                        ._status(closing)
                    )
                }
            )

            current = (
                week_end
                + timedelta(days=2)
            )

            week_number += 1

        return pd.DataFrame(rows)

    # ==========================================================
    # DATAFRAME - CHI TIẾT CÁ NHÂN
    # ==========================================================

    @staticmethod
    def tao_dataframe_chi_tiet_ca_nhan(
        people,
        tu_ngay=None,
        den_ngay=None
    ):

        summary = (
            NopTienController
            .tao_dataframe_tong_hop(
                people,
                tu_ngay,
                den_ngay
            )
        )

        if summary.empty:
            return summary

        return summary[
            [
                "Người ID",
                "Người",
                "Bộ phận",
                "Nợ đầu kỳ",
                "Phải trả",
                "Đã nộp",
                "Còn nợ",
                "Nộp thừa",
                "Số dư",
                "Trạng thái"
            ]
        ].copy()

    # ==========================================================
    # DATAFRAME - TIỀN CƠM
    # ==========================================================

    @staticmethod
    def tao_dataframe_chi_tiet_tien_com(
        people,
        tu_ngay=None,
        den_ngay=None
    ):

        rows = []

        person_map = {}

        for person in people:

            try:

                person_map[
                    person[0]
                ] = {
                    "name": person[1],
                    "department": (
                        person[6]
                        if len(person) > 6
                        else ""
                    )
                }

            except Exception:
                pass

        for nguoi_id, info in person_map.items():

            result = (
                NopTienController
                .lay_chi_tiet_tien_com(
                    nguoi_id,
                    tu_ngay,
                    den_ngay
                )
            )

            if not result.get("success"):
                continue

            for row in result.get(
                "data",
                []
            ):

                rows.append(
                    {
                        "Người ID": nguoi_id,
                        "Người": info["name"],
                        "Bộ phận": info["department"],
                        "Ngày": (
                            row[4]
                            if len(row) > 4
                            else None
                        ),
                        "Đã ăn": (
                            "Có"
                            if len(row) > 5
                            and row[5]
                            else "Không"
                        ),
                        "Số tiền": (
                            float(row[6] or 0)
                            if len(row) > 6
                            else 0
                        ),
                        "Trạng thái": (
                            "Đã ăn"
                            if len(row) > 5
                            and row[5]
                            else "Đăng ký"
                        ),
                        "Ghi chú": (
                            row[7]
                            if len(row) > 7
                            else ""
                        )
                    }
                )

        return pd.DataFrame(rows)

    # ==========================================================
    # DATAFRAME - LỊCH SỬ NỘP TIỀN
    # ==========================================================

    @staticmethod
    def tao_dataframe_lich_su_nop_tien(
        people,
        tu_ngay=None,
        den_ngay=None
    ):

        person_ids = set()

        person_map = {}

        for person in people:

            try:

                person_ids.add(
                    person[0]
                )

                person_map[
                    person[0]
                ] = {
                    "name": person[1],
                    "department": (
                        person[6]
                        if len(person) > 6
                        else ""
                    )
                }

            except Exception:
                pass

        rows = []

        for person_id in person_ids:

            result = (
                NopTienController
                .lay_theo_khoang_thoi_gian(
                    tu_ngay=tu_ngay,
                    den_ngay=den_ngay,
                    nguoi_an_id=person_id
                )
            )

            if not result.get("success"):
                continue

            for row in result.get(
                "data",
                []
            ):

                rows.append(
                    {
                        "Giao dịch ID": row[0],
                        "Người ID": row[1],
                        "Người": row[2],
                        "Bộ phận": (
                            row[4]
                            if len(row) > 4
                            else ""
                        ),
                        "Ngày nộp": row[5],
                        "Số tiền": float(
                            row[6] or 0
                        ),
                        "Hình thức": row[7],
                        "Ghi chú": (
                            row[8]
                            if len(row) > 8
                            else ""
                        )
                    }
                )

        return pd.DataFrame(rows)

    # ==========================================================
    # DATAFRAME - SUẤT ĂN PHÁT SINH
    # ==========================================================

    @staticmethod
    def tao_dataframe_suat_an_phat_sinh(
        tu_ngay=None,
        den_ngay=None
    ):

        data = (
            NopTienController
            .lay_suat_an_phat_sinh(
                tu_ngay=tu_ngay,
                den_ngay=den_ngay
            )
        )

        rows = []

        for row in data:

            rows.append(
                {
                    "Phát sinh ID": row[0],
                    "Ngày ăn": row[2],
                    "Họ tên": row[3],
                    "Đơn vị": row[4],
                    "Số lượng": row[5],
                    "Đơn giá": row[6],
                    "Số tiền": row[7],
                    "Ghi chú": row[8],
                    "Ngày tạo": row[9]
                }
            )

        return pd.DataFrame(rows)

    # ==========================================================
    # DATAFRAME - VẤN ĐỀ PHÁT SINH
    # ==========================================================

    @staticmethod
    @staticmethod
    @staticmethod
    def tao_dataframe_van_de(
            people,
            tu_ngay=None,
            den_ngay=None
    ):

        rows = []

        summary = (
            NopTienController
            .tao_dataframe_tong_hop(
                people,
                tu_ngay,
                den_ngay
            )
        )

        if not summary.empty:

            for _, item in summary.iterrows():

                if item["Trạng thái"] == "Còn nợ":

                    rows.append(
                        {
                            "Loại": "Công nợ",
                            "Người ID": item["Người ID"],
                            "Người": item["Người"],
                            "Bộ phận": item["Bộ phận"],
                            "Số tiền": abs(
                                item["Còn nợ"]
                            ),
                            "Vấn đề": (
                                "Còn công nợ "
                                "chưa thanh toán"
                            ),
                            "Trạng thái": "Cần xử lý"
                        }
                    )

                elif item["Trạng thái"] == "Nộp thừa":

                    rows.append(
                        {
                            "Loại": "Số dư",
                            "Người ID": item["Người ID"],
                            "Người": item["Người"],
                            "Bộ phận": item["Bộ phận"],
                            "Số tiền": item["Nộp thừa"],
                            "Vấn đề": (
                                "Người ăn đang có "
                                "số tiền dư"
                            ),
                            "Trạng thái": (
                                "Theo dõi kỳ sau"
                            )
                        }
                    )

        extra_df = (
            NopTienController
            .tao_dataframe_suat_an_phat_sinh(
                tu_ngay,
                den_ngay
            )
        )

        if not extra_df.empty:
            total_extra = float(
                pd.to_numeric(
                    extra_df["Số tiền"],
                    errors="coerce"
                ).fillna(0).sum()
            )

            rows.append(
                {
                    "Loại": "Suất ăn phát sinh",
                    "Người ID": pd.NA,
                    "Người": "",
                    "Bộ phận": "",
                    "Số tiền": total_extra,
                    "Vấn đề": (
                        "Có suất ăn phát sinh "
                        "chưa gắn với người ăn"
                    ),
                    "Trạng thái": "Cần đối chiếu"
                }
            )

        df = pd.DataFrame(rows)

        if "Người ID" in df.columns:
            df["Người ID"] = pd.to_numeric(
                df["Người ID"],
                errors="coerce"
            ).astype("Int64")

        if "Số tiền" in df.columns:
            df["Số tiền"] = pd.to_numeric(
                df["Số tiền"],
                errors="coerce"
            ).fillna(0.0)

        return df