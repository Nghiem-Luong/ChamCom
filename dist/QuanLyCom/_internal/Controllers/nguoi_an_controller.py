from Models.nguoi_an_model import NguoiAnModel
from Models.audit_log_model import AuditLogModel


class NguoiAnController:

    @staticmethod
    def them_nguoi_an(ho_ten, sdt=None):
        try:
            nguoi_an_id = NguoiAnModel.them_nguoi_an(
                ho_ten=ho_ten,
                sdt=sdt
            )

            AuditLogModel.ghi_log(
                hanh_dong="THÊM NGƯỜI ĂN",
                mo_ta=f"Thêm người ăn: {ho_ten}"
            )

            return {
                "success": True,
                "message": "Thêm người ăn thành công.",
                "id": nguoi_an_id
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
    def lay_danh_sach():
        try:
            return {
                "success": True,
                "data": NguoiAnModel.lay_tat_ca()
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy danh sách: {error}",
                "data": []
            }

    @staticmethod
    def lay_danh_sach_dang_hoat_dong():
        try:
            return {
                "success": True,
                "data": NguoiAnModel.lay_dang_hoat_dong()
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy danh sách: {error}",
                "data": []
            }

    @staticmethod
    def tim_kiem(ho_ten):
        try:
            return {
                "success": True,
                "data": NguoiAnModel.tim_theo_ten(ho_ten)
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể tìm kiếm: {error}",
                "data": []
            }

    @staticmethod
    def cap_nhat(nguoi_an_id, ho_ten, sdt=None):
        try:
            so_dong = NguoiAnModel.cap_nhat(
                nguoi_an_id=nguoi_an_id,
                ho_ten=ho_ten,
                sdt=sdt
            )

            if so_dong == 0:
                return {
                    "success": False,
                    "message": "Không tìm thấy người ăn."
                }

            AuditLogModel.ghi_log(
                hanh_dong="CẬP NHẬT NGƯỜI ĂN",
                mo_ta=f"Cập nhật người ăn ID: {nguoi_an_id}"
            )

            return {
                "success": True,
                "message": "Cập nhật thành công."
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
    def ngung_hoat_dong(nguoi_an_id):
        try:
            so_dong = NguoiAnModel.ngung_hoat_dong(
                nguoi_an_id
            )

            if so_dong == 0:
                return {
                    "success": False,
                    "message": "Không tìm thấy người ăn."
                }

            AuditLogModel.ghi_log(
                hanh_dong="NGỪNG HOẠT ĐỘNG",
                mo_ta=f"Ngừng hoạt động người ăn ID: {nguoi_an_id}"
            )

            return {
                "success": True,
                "message": "Đã ngừng hoạt động."
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi xảy ra: {error}"
            }

    @staticmethod
    def kich_hoat_lai(nguoi_an_id):
        try:
            so_dong = NguoiAnModel.kich_hoat_lai(
                nguoi_an_id
            )

            if so_dong == 0:
                return {
                    "success": False,
                    "message": "Không tìm thấy người ăn."
                }

            AuditLogModel.ghi_log(
                hanh_dong="KÍCH HOẠT LẠI",
                mo_ta=f"Kích hoạt lại người ăn ID: {nguoi_an_id}"
            )

            return {
                "success": True,
                "message": "Đã kích hoạt lại."
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Có lỗi xảy ra: {error}"
            }