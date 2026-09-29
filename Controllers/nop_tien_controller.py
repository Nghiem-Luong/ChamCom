from Models.giao_dich_model import GiaoDichNopTienModel
from Models.audit_log_model import AuditLogModel
from Models.chi_tiet_an_model import ChiTietAnModel
from Database.database import get_connection


class NopTienController:

    @staticmethod
    def them_giao_dich(
        nguoi_an_id,
        ngay_nop,
        so_tien,
        hinh_thuc="Tiền mặt",
        ghi_chu=None
    ):
        try:
            so_tien = float(so_tien)

            giao_dich_id = GiaoDichNopTienModel.them_giao_dich(
                nguoi_an_id=nguoi_an_id,
                ngay_nop=ngay_nop,
                so_tien=so_tien,
                hinh_thuc=hinh_thuc,
                ghi_chu=ghi_chu
            )

            AuditLogModel.ghi_log(
                hanh_dong="NỘP TIỀN",
                mo_ta=(
                    f"Người ăn ID: {nguoi_an_id}, "
                    f"Số tiền: {so_tien}, "
                    f"Ngày nộp: {ngay_nop}"
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

    @staticmethod
    def lay_tat_ca():
        try:
            return {
                "success": True,
                "data": GiaoDichNopTienModel.lay_tat_ca()
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy giao dịch: {error}",
                "data": []
            }

    @staticmethod
    def lay_theo_nguoi(nguoi_an_id):
        try:
            return {
                "success": True,
                "data": GiaoDichNopTienModel.lay_theo_nguoi(
                    nguoi_an_id
                )
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể lấy giao dịch: {error}",
                "data": []
            }

    @staticmethod
    def tong_tien_da_nop(nguoi_an_id):
        try:
            tong_tien = GiaoDichNopTienModel.tong_tien_da_nop(
                nguoi_an_id
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
    def tinh_tien_phai_tra(nguoi_an_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COALESCE(SUM(SoTienPhaiTra), 0)
                FROM ChiTietAn
                WHERE NguoiAnId = ?
                  AND DaAn = 1
            """, (nguoi_an_id,))

            result = cursor.fetchone()

            return result[0] or 0

        finally:
            connection.close()

    @staticmethod
    def tinh_so_du(nguoi_an_id):
        try:
            tong_da_nop = (
                GiaoDichNopTienModel.tong_tien_da_nop(
                    nguoi_an_id
                )
            )

            tong_phai_tra = (
                NopTienController.tinh_tien_phai_tra(
                    nguoi_an_id
                )
            )

            so_du = tong_da_nop - tong_phai_tra

            return {
                "success": True,
                "data": so_du,
                "tong_da_nop": tong_da_nop,
                "tong_phai_tra": tong_phai_tra
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Không thể tính số dư: {error}",
                "data": 0,
                "tong_da_nop": 0,
                "tong_phai_tra": 0
            }

    @staticmethod
    def lay_chi_tiet_tien_com(nguoi_an_id):
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
                "message": f"Không thể lấy chi tiết tiền cơm: {error}",
                "data": []
            }

    @staticmethod
    def xoa(giao_dich_id):
        try:
            so_dong = GiaoDichNopTienModel.xoa(
                giao_dich_id
            )

            if so_dong == 0:
                return {
                    "success": False,
                    "message": "Không tìm thấy giao dịch."
                }

            AuditLogModel.ghi_log(
                hanh_dong="XÓA GIAO DỊCH NỘP TIỀN",
                mo_ta=f"Xóa giao dịch ID: {giao_dich_id}"
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