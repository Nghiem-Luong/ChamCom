from Models.ngay_an_model import NgayAnModel
from Models.audit_log_model import AuditLogModel


class NgayAnController:

    @staticmethod
    def tao_ngay_an(ngay, don_gia_mac_dinh, ghi_chu=None):
        try:
            don_gia_mac_dinh = float(don_gia_mac_dinh)

            ngay_an_id = NgayAnModel.tao_ngay_an(
                ngay=ngay,
                don_gia_mac_dinh=don_gia_mac_dinh,
                ghi_chu=ghi_chu
            )

            AuditLogModel.ghi_log(
                hanh_dong="TẠO NGÀY ĂN",
                mo_ta=(
                    f"Tạo ngày ăn {ngay}, "
                    f"đơn giá {don_gia_mac_dinh}"
                )
            )

            return {
                "success": True,
                "message": "Tạo ngày ăn thành công.",
                "id": ngay_an_id
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
                "data": NgayAnModel.lay_tat_ca()
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy danh sách: {error}",
                "data": []
            }

    @staticmethod
    def tim_theo_ngay(ngay):
        try:
            return {
                "success": True,
                "data": NgayAnModel.tim_theo_ngay(ngay)
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể tìm ngày ăn: {error}",
                "data": None
            }

    @staticmethod
    def lay_ngay_truoc_do(ngay):
        try:
            return {
                "success": True,
                "data": NgayAnModel.lay_ngay_truoc_do(ngay)
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy ngày trước đó: {error}",
                "data": None
            }

    @staticmethod
    def cap_nhat(
        ngay_an_id,
        ngay,
        don_gia_mac_dinh,
        ghi_chu=None
    ):
        try:
            don_gia_mac_dinh = float(don_gia_mac_dinh)

            so_dong = NgayAnModel.cap_nhat(
                ngay_an_id=ngay_an_id,
                ngay=ngay,
                don_gia_mac_dinh=don_gia_mac_dinh,
                ghi_chu=ghi_chu
            )

            if so_dong == 0:
                return {
                    "success": False,
                    "message": "Không tìm thấy ngày ăn."
                }

            AuditLogModel.ghi_log(
                hanh_dong="CẬP NHẬT NGÀY ĂN",
                mo_ta=f"Cập nhật ngày ăn ID: {ngay_an_id}"
            )

            return {
                "success": True,
                "message": "Cập nhật ngày ăn thành công."
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