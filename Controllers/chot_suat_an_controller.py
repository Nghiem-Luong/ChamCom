# -*- coding: utf-8 -*-

from Models.chot_suat_an_model import ChotSuatAnModel


class ChotSuatAnController:

    # ==========================================================
    # KIỂM TRA NGÀY ĐÃ CHỐT
    # ==========================================================

    @staticmethod
    def da_chot(ngay_an_id):
        return ChotSuatAnModel.da_chot(
            ngay_an_id
        )

    # ==========================================================
    # LẤY TRẠNG THÁI CHỐT
    # ==========================================================

    @staticmethod
    def lay_trang_thai(ngay_an_id):
        row = ChotSuatAnModel.lay_trang_thai(
            ngay_an_id
        )

        if row is None:
            return {
                "id": None,
                "ngay_an_id": ngay_an_id,
                "da_chot": False,
                "ngay_chot": None,
                "nguoi_chot": None,
                "ghi_chu": None,
            }

        return {
            "id": row[0],
            "ngay_an_id": row[1],
            "da_chot": bool(row[2]),
            "ngay_chot": row[3],
            "nguoi_chot": row[4],
            "ghi_chu": row[5],
        }

    # ==========================================================
    # TẠO TRẠNG THÁI NẾU CHƯA CÓ
    # ==========================================================

    @staticmethod
    def tao_trang_thai_neu_chua_co(
        ngay_an_id
    ):
        return ChotSuatAnModel.tao_trang_thai_neu_chua_co(
            ngay_an_id
        )

    # ==========================================================
    # LẤY DANH SÁCH ĐÃ CHỐT
    # ==========================================================

    @staticmethod
    def lay_danh_sach_chot(ngay_an_id):
        rows = ChotSuatAnModel.lay_danh_sach_chot(
            ngay_an_id
        )

        ket_qua = []

        for row in rows:

            # --------------------------------------------------
            # 9 CỘT CŨ
            # --------------------------------------------------

            item = {
                "id": row[0],
                "ngay_an_id": row[1],
                "nguoi_an_id": row[2],
                "ho_ten": row[3],
                "bo_phan": row[4],
                "trang_thai": row[5],
                "so_tien": row[6],
                "ghi_chu": row[7],
                "ngay_chot": row[8],
            }

            # --------------------------------------------------
            # 4 CỘT MỚI
            # --------------------------------------------------

            item["loai_nguoi"] = (
                row[9]
                if len(row) > 9
                else "Nhân viên"
            )

            item["suat_an_phat_sinh_id"] = (
                row[10]
                if len(row) > 10
                else None
            )

            item["so_luong"] = (
                row[11]
                if len(row) > 11
                else 1
            )

            item["don_gia"] = (
                row[12]
                if len(row) > 12
                else 0
            )

            ket_qua.append(item)

        return ket_qua

    # ==========================================================
    # LƯU DANH SÁCH CHỐT
    # ==========================================================

    @staticmethod
    def chot_suat_an(
        ngay_an_id,
        danh_sach,
        nguoi_chot="Chính tôi",
        ghi_chu=None,
    ):
        if not ngay_an_id:
            raise ValueError(
                "Ngày ăn không hợp lệ."
            )

        if not danh_sach:
            raise ValueError(
                "Danh sách chốt đang trống."
            )

        # ------------------------------------------------------
        # Kiểm tra trạng thái
        # ------------------------------------------------------

        if ChotSuatAnModel.da_chot(
            ngay_an_id
        ):
            raise ValueError(
                "Ngày ăn này đã được chốt."
            )

        # ------------------------------------------------------
        # Chuẩn hóa dữ liệu
        # ------------------------------------------------------

        danh_sach_chuan_hoa = []

        for item in danh_sach:

            if not isinstance(
                item,
                dict
            ):
                continue

            ho_ten = str(
                item.get(
                    "ho_ten",
                    ""
                ) or ""
            ).strip()

            if not ho_ten:
                continue

            # --------------------------------------------------
            # Trạng thái
            # --------------------------------------------------

            trang_thai = str(
                item.get(
                    "trang_thai",
                    "Đăng ký",
                ) or "Đăng ký"
            ).strip()

            if not trang_thai:
                trang_thai = "Đăng ký"

            # --------------------------------------------------
            # Bộ phận
            # --------------------------------------------------

            bo_phan = str(
                item.get(
                    "bo_phan",
                    "",
                ) or ""
            ).strip()

            # --------------------------------------------------
            # Ghi chú
            # --------------------------------------------------

            ghi_chu_dong = item.get(
                "ghi_chu"
            )

            # --------------------------------------------------
            # Loại người
            # --------------------------------------------------

            loai_nguoi = str(
                item.get(
                    "loai_nguoi",
                    "Nhân viên",
                ) or "Nhân viên"
            ).strip()

            if loai_nguoi not in (
                "Nhân viên",
                "Phát sinh",
            ):
                loai_nguoi = "Nhân viên"

            # --------------------------------------------------
            # ID nhân viên
            # --------------------------------------------------

            nguoi_an_id = item.get(
                "nguoi_an_id"
            )

            # --------------------------------------------------
            # ID suất phát sinh
            # --------------------------------------------------

            suat_an_phat_sinh_id = item.get(
                "suat_an_phat_sinh_id"
            )

            # --------------------------------------------------
            # Số lượng
            # --------------------------------------------------

            try:
                so_luong = int(
                    item.get(
                        "so_luong",
                        1
                    ) or 1
                )
            except (
                TypeError,
                ValueError,
            ):
                so_luong = 1

            if so_luong <= 0:
                so_luong = 1

            # --------------------------------------------------
            # Đơn giá
            # --------------------------------------------------

            try:
                don_gia = float(
                    item.get(
                        "don_gia",
                        0
                    ) or 0
                )
            except (
                TypeError,
                ValueError,
            ):
                don_gia = 0

            # --------------------------------------------------
            # Thành tiền
            # --------------------------------------------------

            try:
                so_tien = float(
                    item.get(
                        "so_tien",
                        0
                    ) or 0
                )
            except (
                TypeError,
                ValueError,
            ):
                so_tien = 0

            # --------------------------------------------------
            # Nhân viên
            # --------------------------------------------------

            if loai_nguoi == "Nhân viên":

                suat_an_phat_sinh_id = None

                so_luong = 1

                if (
                    don_gia <= 0
                    and so_tien > 0
                ):
                    don_gia = so_tien

            # --------------------------------------------------
            # Phát sinh
            # --------------------------------------------------

            else:

                nguoi_an_id = None

                if (
                    so_tien <= 0
                    and don_gia > 0
                ):
                    so_tien = (
                        so_luong * don_gia
                    )

            # --------------------------------------------------
            # Thêm vào danh sách chuẩn hóa
            # --------------------------------------------------

            danh_sach_chuan_hoa.append({
                "nguoi_an_id": nguoi_an_id,

                "ho_ten": ho_ten,

                "bo_phan": bo_phan,

                "trang_thai": trang_thai,

                "so_tien": so_tien,

                "ghi_chu": ghi_chu_dong,

                "loai_nguoi": loai_nguoi,

                "suat_an_phat_sinh_id":
                    suat_an_phat_sinh_id,

                "so_luong": so_luong,

                "don_gia": don_gia,
            })

        # ------------------------------------------------------
        # Kiểm tra dữ liệu sau chuẩn hóa
        # ------------------------------------------------------

        if not danh_sach_chuan_hoa:
            raise ValueError(
                "Không có dữ liệu hợp lệ để chốt."
            )

        # ------------------------------------------------------
        # Gọi Model lưu snapshot
        # ------------------------------------------------------

        return ChotSuatAnModel.luu_danh_sach_chot(
            ngay_an_id=ngay_an_id,
            danh_sach=danh_sach_chuan_hoa,
            nguoi_chot=nguoi_chot,
            ghi_chu=ghi_chu,
        )

    # ==========================================================
    # MỞ CHỐT
    # ==========================================================

    @staticmethod
    def mo_chot(
        ngay_an_id,
        nguoi_thao_tac="Chính tôi",
    ):
        if not ngay_an_id:
            raise ValueError(
                "Ngày ăn không hợp lệ."
            )

        if not ChotSuatAnModel.da_chot(
            ngay_an_id
        ):
            raise ValueError(
                "Ngày ăn này chưa được chốt."
            )

        return ChotSuatAnModel.mo_chot(
            ngay_an_id,
            nguoi_thao_tac,
        )

    # ==========================================================
    # THỐNG KÊ DANH SÁCH CHỐT
    # ==========================================================

    @staticmethod
    def thong_ke_chot(ngay_an_id):
        return ChotSuatAnModel.thong_ke_chot(
            ngay_an_id
        )

    # ==========================================================
    # THỐNG KÊ TỔNG SỐ SUẤT
    # ==========================================================

    @staticmethod
    def thong_ke_so_suat(ngay_an_id):
        return ChotSuatAnModel.thong_ke_so_suat(
            ngay_an_id
        )

    # ==========================================================
    # THỐNG KÊ SUẤT PHÁT SINH
    # ==========================================================

    @staticmethod
    def thong_ke_phat_sinh(ngay_an_id):
        return ChotSuatAnModel.thong_ke_phat_sinh(
            ngay_an_id
        )