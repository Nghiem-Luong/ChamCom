from Models.chi_tiet_an_model import ChiTietAnModel
from Models.audit_log_model import AuditLogModel


class ChiTietAnController:

    @staticmethod
    def them_chi_tiet(
        nguoi_an_id,
        ngay_an_id,
        da_an,
        so_tien_phai_tra,
        ghi_chu=None
    ):
        try:
            so_tien_phai_tra = float(so_tien_phai_tra)

            chi_tiet_id = ChiTietAnModel.them_chi_tiet(
                nguoi_an_id=nguoi_an_id,
                ngay_an_id=ngay_an_id,
                da_an=da_an,
                so_tien_phai_tra=so_tien_phai_tra,
                ghi_chu=ghi_chu
            )

            AuditLogModel.ghi_log(
                hanh_dong="CHẤM CƠM",
                mo_ta=(
                    f"Thêm chi tiết ăn - "
                    f"Người ăn ID: {nguoi_an_id}, "
                    f"Ngày ăn ID: {ngay_an_id}, "
                    f"Đã ăn: {da_an}, "
                    f"Số tiền: {so_tien_phai_tra}"
                )
            )

            return {
                "success": True,
                "message": "Chấm cơm thành công.",
                "id": chi_tiet_id
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

    @staticmethod
    def cap_nhat(
        chi_tiet_id,
        da_an,
        so_tien_phai_tra,
        ghi_chu=None
    ):
        try:
            so_tien_phai_tra = float(so_tien_phai_tra)

            so_dong = ChiTietAnModel.cap_nhat(
                chi_tiet_id=chi_tiet_id,
                da_an=da_an,
                so_tien_phai_tra=so_tien_phai_tra,
                ghi_chu=ghi_chu
            )

            if so_dong == 0:
                return {
                    "success": False,
                    "message": "Không tìm thấy bản ghi chấm cơm."
                }

            AuditLogModel.ghi_log(
                hanh_dong="CẬP NHẬT CHẤM CƠM",
                mo_ta=f"Cập nhật chi tiết ăn ID: {chi_tiet_id}"
            )

            return {
                "success": True,
                "message": "Cập nhật chấm cơm thành công."
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

    @staticmethod
    def xoa(chi_tiet_id):
        try:
            so_dong = ChiTietAnModel.xoa(chi_tiet_id)

            if so_dong == 0:
                return {
                    "success": False,
                    "message": "Không tìm thấy bản ghi."
                }

            AuditLogModel.ghi_log(
                hanh_dong="XÓA CHẤM CƠM",
                mo_ta=f"Xóa chi tiết ăn ID: {chi_tiet_id}"
            )

            return {
                "success": True,
                "message": "Xóa bản ghi thành công."
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi xảy ra: {error}"
            }

    @staticmethod
    def kiem_tra_da_co(nguoi_an_id, ngay_an_id):
        try:
            da_co = ChiTietAnModel.da_co_ban_ghi(
                nguoi_an_id=nguoi_an_id,
                ngay_an_id=ngay_an_id
            )

            return {
                "success": True,
                "data": da_co
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể kiểm tra: {error}",
                "data": False
            }

    @staticmethod
    def lay_theo_ngay(ngay_an_id):
        try:
            return {
                "success": True,
                "data": ChiTietAnModel.lay_theo_ngay(
                    ngay_an_id
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy dữ liệu: {error}",
                "data": []
            }

    @staticmethod
    def lay_theo_nguoi(nguoi_an_id):
        try:
            return {
                "success": True,
                "data": ChiTietAnModel.lay_theo_nguoi(
                    nguoi_an_id
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy dữ liệu: {error}",
                "data": []
            }

    @staticmethod
    def tinh_tong_tien_ngay(ngay_an_id):
        try:
            tong_tien = ChiTietAnModel.tinh_tong_tien_ngay(
                ngay_an_id
            )

            return {
                "success": True,
                "data": tong_tien
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể tính tổng tiền: {error}",
                "data": 0
            }

    @staticmethod
    def dem_so_nguoi_an(ngay_an_id):
        try:
            so_nguoi = ChiTietAnModel.dem_so_nguoi_an(
                ngay_an_id
            )

            return {
                "success": True,
                "data": so_nguoi
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể đếm số người ăn: {error}",
                "data": 0
            }

    @staticmethod
    def luu_danh_sach_dang_ky(
        ngay_an_id,
        danh_sach_nguoi_an,
        don_gia
    ):
        try:
            don_gia = float(don_gia)

            if don_gia < 0:
                return {
                    "success": False,
                    "message": "Đơn giá không được âm."
                }

            so_nguoi = ChiTietAnModel.luu_danh_sach_dang_ky(
                ngay_an_id=ngay_an_id,
                danh_sach_nguoi_an=danh_sach_nguoi_an,
                don_gia=don_gia
            )

            # Ghi lịch sử thao tác
            AuditLogModel.ghi_log(
                hanh_dong="ĐĂNG KÝ CHẤM CƠM",
                mo_ta=(
                    f"Lưu đăng ký ăn - "
                    f"Ngày ăn ID: {ngay_an_id}, "
                    f"Số người đăng ký: {so_nguoi}, "
                    f"Đơn giá: {don_gia}"
                )
            )

            return {
                "success": True,
                "message": (
                    f"Đã lưu đăng ký cho "
                    f"{so_nguoi} người."
                ),
                "so_nguoi": so_nguoi
            }

        except ValueError as error:
            return {
                "success": False,
                "message": str(error)
            }

        except Exception as error:
            return {
                "success": False,
                "message": (
                    f"Có lỗi xảy ra: {error}"
                )
            }