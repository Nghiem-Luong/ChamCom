# -*- coding: utf-8 -*-

from Models.suat_an_phat_sinh_model import (
    SuatAnPhatSinhModel
)

from Models.audit_log_model import AuditLogModel


class SuatAnPhatSinhController:

    @staticmethod
    def them(
        ngay_an_id,
        ho_ten,
        don_vi=None,
        so_luong=1,
        don_gia=0,
        ghi_chu=None
    ):
        """
        Thêm suất ăn phát sinh.
        """

        suat_an_id = SuatAnPhatSinhModel.them(
            ngay_an_id=ngay_an_id,
            ho_ten=ho_ten,
            don_vi=don_vi,
            so_luong=so_luong,
            don_gia=don_gia,
            ghi_chu=ghi_chu
        )

        AuditLogModel.them(
            "THÊM SUẤT ĂN PHÁT SINH",
            (
                f"Thêm '{ho_ten}' - "
                f"{so_luong} suất - "
                f"Đơn giá {don_gia:,.0f} VNĐ"
            )
        )

        return suat_an_id

    @staticmethod
    def lay_theo_ngay(ngay_an_id):
        """
        Lấy toàn bộ suất ăn phát sinh của ngày.
        """

        return SuatAnPhatSinhModel.lay_theo_ngay(
            ngay_an_id
        )

    @staticmethod
    def tim_theo_id(suat_an_id):
        """
        Tìm suất ăn phát sinh theo ID.
        """

        return SuatAnPhatSinhModel.tim_theo_id(
            suat_an_id
        )

    @staticmethod
    def cap_nhat(
        suat_an_id,
        ho_ten,
        don_vi=None,
        so_luong=1,
        don_gia=0,
        ghi_chu=None
    ):
        """
        Cập nhật suất ăn phát sinh.
        """

        du_lieu_cu = (
            SuatAnPhatSinhModel.tim_theo_id(
                suat_an_id
            )
        )

        so_dong = SuatAnPhatSinhModel.cap_nhat(
            suat_an_id=suat_an_id,
            ho_ten=ho_ten,
            don_vi=don_vi,
            so_luong=so_luong,
            don_gia=don_gia,
            ghi_chu=ghi_chu
        )

        if so_dong > 0:

            if du_lieu_cu:

                ho_ten_cu = du_lieu_cu[2]

            else:

                ho_ten_cu = "Không xác định"

            AuditLogModel.them(
                "SỬA SUẤT ĂN PHÁT SINH",
                (
                    f"Sửa '{ho_ten_cu}' "
                    f"thành '{ho_ten}' - "
                    f"{so_luong} suất - "
                    f"Đơn giá {don_gia:,.0f} VNĐ"
                )
            )

        return so_dong

    @staticmethod
    def xoa(suat_an_id):
        """
        Xóa một suất ăn phát sinh.
        """

        du_lieu = (
            SuatAnPhatSinhModel.tim_theo_id(
                suat_an_id
            )
        )

        so_dong = SuatAnPhatSinhModel.xoa(
            suat_an_id
        )

        if so_dong > 0:

            if du_lieu:

                ho_ten = du_lieu[2]
                so_luong = du_lieu[4]

            else:

                ho_ten = "Không xác định"
                so_luong = 0

            AuditLogModel.them(
                "XÓA SUẤT ĂN PHÁT SINH",
                (
                    f"Xóa '{ho_ten}' - "
                    f"{so_luong} suất"
                )
            )

        return so_dong

    @staticmethod
    def xoa_theo_ngay(ngay_an_id):
        """
        Xóa toàn bộ suất phát sinh của một ngày.
        """

        so_dong = (
            SuatAnPhatSinhModel.xoa_theo_ngay(
                ngay_an_id
            )
        )

        if so_dong > 0:

            AuditLogModel.them(
                "XÓA SUẤT ĂN PHÁT SINH THEO NGÀY",
                (
                    f"Xóa {so_dong} dòng "
                    f"suất ăn phát sinh"
                )
            )

        return so_dong

    @staticmethod
    def tinh_tong_so_luong(ngay_an_id):
        """
        Tổng số suất phát sinh.
        """

        return (
            SuatAnPhatSinhModel.tinh_tong_so_luong(
                ngay_an_id
            )
        )

    @staticmethod
    def tinh_tong_tien(ngay_an_id):
        """
        Tổng tiền suất phát sinh.
        """

        return (
            SuatAnPhatSinhModel.tinh_tong_tien(
                ngay_an_id
            )
        )

    @staticmethod
    def them_thanh_toan(suat_an_phat_sinh_id, ngay_thu, so_tien, hinh_thuc="Tiền mặt", ghi_chu=None):
        return SuatAnPhatSinhModel.them_thanh_toan(
            suat_an_phat_sinh_id, ngay_thu, so_tien, hinh_thuc, ghi_chu
        )

    @staticmethod
    def lay_thanh_toan(suat_an_phat_sinh_id):
        return SuatAnPhatSinhModel.lay_thanh_toan(suat_an_phat_sinh_id)

    @staticmethod
    def tim_thanh_toan_theo_id(payment_id):
        return SuatAnPhatSinhModel.tim_thanh_toan_theo_id(payment_id)

    @staticmethod
    def cap_nhat_thanh_toan(payment_id, suat_an_phat_sinh_id, ngay_thu, so_tien, hinh_thuc="Tiền mặt", ghi_chu=None):
        return SuatAnPhatSinhModel.cap_nhat_thanh_toan(
            payment_id, suat_an_phat_sinh_id, ngay_thu, so_tien, hinh_thuc, ghi_chu
        )

    @staticmethod
    def xoa_thanh_toan(payment_id):
        return SuatAnPhatSinhModel.xoa_thanh_toan(payment_id)

    @staticmethod
    def tong_da_thu(suat_an_phat_sinh_id):
        return SuatAnPhatSinhModel.tong_da_thu(suat_an_phat_sinh_id)

    @staticmethod
    def lay_bao_cao_thanh_toan(tu_ngay=None, den_ngay=None):
        return SuatAnPhatSinhModel.lay_bao_cao_thanh_toan(tu_ngay, den_ngay)

    @staticmethod
    def lay_thanh_toan_theo_khoang_thu(tu_ngay=None, den_ngay=None):
        return SuatAnPhatSinhModel.lay_thanh_toan_theo_khoang_thu(tu_ngay, den_ngay)

    @staticmethod
    def tong_tien_thu_theo_hinh_thuc(tu_ngay=None, den_ngay=None):
        return SuatAnPhatSinhModel.tong_tien_thu_theo_hinh_thuc(tu_ngay, den_ngay)
