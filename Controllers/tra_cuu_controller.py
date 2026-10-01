# -*- coding: utf-8 -*-

from datetime import date

import pandas as pd

from Models.tra_cuu_model import TraCuuModel


class TraCuuController:
    """
    Controller cho chức năng:
        - Hỗ trợ & Tra cứu
        - Thống kê
        - Đối chiếu
        - Phát hiện bất thường
        - Kiểm tra dữ liệu

    Lưu ý:
        Controller không trực tiếp xử lý SQL.
        Toàn bộ dữ liệu được lấy thông qua TraCuuModel.
    """

    # ==========================================================
    # DANH SÁCH CÂU HỎI
    # ==========================================================

    CAU_HOI = {

        # ======================================================
        # 1. CHẤM CƠM
        # ======================================================

        "🍚 Chấm cơm": [

            {
                "id": "dem_nguoi_an_hom_nay",
                "text": "Hôm nay có bao nhiêu người ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_da_an_hom_nay",
                "text": "Hôm nay những ai đã ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_chua_an_hom_nay",
                "text": "Hôm nay những ai chưa ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_so_suat",
                "text": "Trong khoảng thời gian có bao nhiêu suất ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_tien_an_hom_nay",
                "text": "Tổng tiền ăn trong khoảng thời gian là bao nhiêu?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_an_nhieu_lan",
                "text": "Ai ăn nhiều hơn 1 suất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_an_mot_suat",
                "text": "Ai chỉ ăn 1 suất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_an_nhieu_nhat",
                "text": "Ai có số suất ăn nhiều nhất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_an_it_nhat",
                "text": "Ai có số suất ăn ít nhất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "thong_ke_an_theo_ngay",
                "text": "Thống kê số suất ăn theo từng ngày",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "trung_binh_suat_moi_ngay",
                "text": "Trung bình mỗi ngày có bao nhiêu suất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_chua_tung_an",
                "text": "Ai chưa từng ăn trong khoảng thời gian?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_ngay_an_nhieu_nhat",
                "text": "Ngày nào có nhiều suất ăn nhất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_ngay_an_it_nhat",
                "text": "Ngày nào có ít suất ăn nhất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },
        ],

        # ======================================================
        # 2. THEO NGƯỜI
        # ======================================================

        "👤 Theo người": [

            {
                "id": "tong_quan_nguoi",
                "text": "Thông tin tổng quan của người này",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "da_an_hom_nay",
                "text": "Người này đã ăn chưa?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_lan_an",
                "text": "Người này đã ăn bao nhiêu lần?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "lich_su_an",
                "text": "Lịch sử ăn của người này",
                "need_person": True,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ngay_chua_an",
                "text": "Người này chưa ăn những ngày nào?",
                "need_person": True,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_phai_tra_nguoi",
                "text": "Người này phải trả bao nhiêu tiền?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_da_nop",
                "text": "Người này đã nộp bao nhiêu tiền?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "cong_no_nguoi",
                "text": "Người này còn nợ bao nhiêu?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "thanh_toan_du",
                "text": "Người này đã thanh toán đủ chưa?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nop_vuot",
                "text": "Người này đã nộp vượt bao nhiêu?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "lan_an_gan_nhat",
                "text": "Lần gần nhất người này ăn là khi nào?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "lan_nop_gan_nhat",
                "text": "Lần gần nhất người này nộp tiền là khi nào?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_nhieu_lan_trong_ngay",
                "text": "Người này có ngày nào ăn nhiều lần không?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "lich_su_nop_tien",
                "text": "Lịch sử nộp tiền của người này",
                "need_person": True,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "doi_chieu_nguoi",
                "text": "Đối chiếu tiền ăn và tiền đã nộp của người này",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },
        ],

        # ======================================================
        # 3. SO SÁNH NHIỀU NGƯỜI
        # ======================================================

        "👥 So sánh nhiều người": [

            {
                "id": "so_sanh_so_suat",
                "text": "So sánh số suất ăn của nhiều người",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_sanh_phai_tra",
                "text": "So sánh số tiền phải trả của nhiều người",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_sanh_da_nop",
                "text": "So sánh số tiền đã nộp của nhiều người",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_sanh_cong_no",
                "text": "So sánh công nợ của nhiều người",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_sanh_so_ngay_an",
                "text": "So sánh số ngày ăn của nhiều người",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ai_an_nhieu_hon",
                "text": "Ai ăn nhiều hơn người được chọn?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ai_an_it_hon",
                "text": "Ai ăn ít hơn người được chọn?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ai_nop_nhieu_hon",
                "text": "Ai đã nộp nhiều tiền hơn người được chọn?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ai_no_nhieu_hon",
                "text": "Ai đang nợ nhiều hơn người được chọn?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_sanh_suat_va_tien",
                "text": "Ai có số suất ăn và số tiền không tương ứng?",
                "need_person": True,
                "multi_person": True,
                "need_department": False,
                "need_date": True
            },
        ],

        # ======================================================
        # 4. THEO BỘ PHẬN
        # ======================================================

        "🏢 Theo bộ phận": [

            {
                "id": "bo_phan_so_nguoi",
                "text": "Bộ phận có bao nhiêu người?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "bo_phan_so_nguoi_an",
                "text": "Bộ phận có bao nhiêu người ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "bo_phan_so_suat",
                "text": "Bộ phận có bao nhiêu suất ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "bo_phan_tong_tien",
                "text": "Tổng tiền ăn của bộ phận?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "bo_phan_da_thu",
                "text": "Bộ phận đã thu bao nhiêu tiền?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "bo_phan_cong_no",
                "text": "Bộ phận còn nợ bao nhiêu?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "bo_phan_nguoi_chua_an",
                "text": "Ai trong bộ phận chưa ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "bo_phan_nguoi_no",
                "text": "Ai trong bộ phận đang nợ?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "bo_phan_nop_chua_an",
                "text": "Ai trong bộ phận đã nộp nhưng chưa ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": True,
                "need_date": True
            },

            {
                "id": "so_sanh_bo_phan_suat",
                "text": "So sánh số suất giữa các bộ phận",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_sanh_bo_phan_no",
                "text": "So sánh công nợ giữa các bộ phận",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "bo_phan_an_nhieu_nhat",
                "text": "Bộ phận nào có nhiều người ăn nhất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "bo_phan_no_nhieu_nhat",
                "text": "Bộ phận nào có nhiều công nợ nhất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },
        ],

        # ======================================================
        # 5. THEO THỜI GIAN
        # ======================================================

        "📅 Theo thời gian": [

            {
                "id": "thong_ke_theo_ngay",
                "text": "Thống kê số suất theo từng ngày",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tien_theo_ngay",
                "text": "Thống kê tiền ăn theo từng ngày",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_theo_ngay",
                "text": "Thống kê số người ăn theo từng ngày",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "trung_binh_suat_ngay",
                "text": "Trung bình số suất mỗi ngày",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "trung_binh_tien_ngay",
                "text": "Trung bình tiền ăn mỗi ngày",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ngay_nhieu_nguoi_nhat",
                "text": "Ngày có nhiều người ăn nhất",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ngay_it_nguoi_nhat",
                "text": "Ngày có ít người ăn nhất",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ngay_tien_cao_nhat",
                "text": "Ngày có tổng tiền ăn cao nhất",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "ngay_tien_thap_nhat",
                "text": "Ngày có tổng tiền ăn thấp nhất",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "so_sanh_khoang_thoi_gian",
                "text": "So sánh hai khoảng thời gian",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "lich_su_nguoi_theo_khoang",
                "text": "Lịch sử ăn của một người trong khoảng thời gian",
                "need_person": True,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },
        ],

        # ======================================================
        # 6. CÔNG NỢ
        # ======================================================

        "💰 Công nợ": [

            {
                "id": "dem_nguoi_dang_no",
                "text": "Có bao nhiêu người đang nợ?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "danh_sach_dang_no",
                "text": "Ai đang nợ tiền?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_cong_no",
                "text": "Tổng công nợ hiện tại là bao nhiêu?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "no_nhieu_nhat",
                "text": "Ai đang nợ nhiều nhất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "no_it_nhat",
                "text": "Ai đang nợ ít nhất?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_chua_nop",
                "text": "Ai đã ăn nhưng chưa nộp tiền?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_nop_thieu",
                "text": "Ai đã ăn nhưng nộp thiếu tiền?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "da_thanh_toan_du",
                "text": "Ai đã thanh toán đủ tiền?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "da_nop_vuot",
                "text": "Ai đã nộp vượt tiền ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "chua_tung_nop",
                "text": "Ai chưa từng nộp tiền?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nop_chua_an",
                "text": "Ai đã nộp tiền nhưng chưa ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_con_no",
                "text": "Ai đã ăn nhưng hiện còn nợ?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },
        ],

        # ======================================================
        # 7. ĐỐI CHIẾU ĂN ↔ TIỀN
        # ======================================================

        "🔄 Đối chiếu ăn ↔ tiền": [

            {
                "id": "doi_chieu_an_tien",
                "text": "Đối chiếu số suất ăn với tiền phải trả",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_chua_nop",
                "text": "Ăn nhưng chưa nộp tiền",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_nop_thieu",
                "text": "Ăn nhưng nộp thiếu",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_da_du",
                "text": "Ăn và đã thanh toán đủ",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nop_chua_an",
                "text": "Nộp tiền nhưng chưa ăn",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nop_vuot",
                "text": "Nộp tiền nhiều hơn tiền ăn",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tien_khong_khop",
                "text": "Ai có tiền ăn và tiền nộp không khớp?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "suat_khong_khop_tien",
                "text": "Ai có số suất ăn không tương ứng với số tiền?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_tien_bang_0",
                "text": "Ai có suất ăn nhưng tiền phải trả bằng 0?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tien_phai_tra_khong_suat",
                "text": "Ai có tiền phải trả nhưng không có suất ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },
        ],

        # ======================================================
        # 8. BẤT THƯỜNG
        # ======================================================

        "⚠️ Bất thường": [

            {
                "id": "an_nhieu_lan",
                "text": "Ai chấm cơm nhiều lần trong cùng một ngày?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "du_lieu_an_trung",
                "text": "Có dữ liệu chấm cơm trùng không?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_ngung_van_an",
                "text": "Người ngừng hoạt động nhưng vẫn chấm cơm?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_ngung_van_nop",
                "text": "Người ngừng hoạt động nhưng vẫn nộp tiền?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "an_nhung_tien_0",
                "text": "Có người ăn nhưng tiền phải trả bằng 0 không?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "co_tien_nhung_khong_an",
                "text": "Có người có tiền phải trả nhưng không có suất ăn không?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "du_lieu_thieu_lien_ket",
                "text": "Có dữ liệu chấm cơm thiếu liên kết không?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_khong_bo_phan",
                "text": "Ai đang hoạt động nhưng chưa có bộ phận?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_co_ten_trung",
                "text": "Có người bị trùng tên không?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": False
            },

            {
                "id": "so_dien_thoai_trung",
                "text": "Có số điện thoại bị trùng không?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": False
            },
        ],

        # ======================================================
        # 9. KIỂM TRA DỮ LIỆU
        # ======================================================

        "🗃️ Kiểm tra dữ liệu": [

            {
                "id": "chi_tiet_khong_co_ngay",
                "text": "Chi tiết ăn nào không có ngày ăn?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": False
            },

            {
                "id": "giao_dich_khong_co_nguoi",
                "text": "Giao dịch nào không có người ăn tương ứng?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": False
            },

            {
                "id": "nguoi_thieu_bo_phan",
                "text": "Người nào đang thiếu bộ phận?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": False
            },

            {
                "id": "ten_trung",
                "text": "Kiểm tra người bị trùng tên",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": False
            },

            {
                "id": "sdt_trung",
                "text": "Kiểm tra số điện thoại trùng",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": False
            },

            {
                "id": "ngay_du_lieu_bat_thuong",
                "text": "Kiểm tra ngày dữ liệu bất thường",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "giao_dich_nghi_trung",
                "text": "Kiểm tra giao dịch nộp tiền nghi trùng",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_ngung_co_du_lieu",
                "text": "Người ngừng hoạt động nhưng còn dữ liệu?",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "nguoi_chua_tung_an",
                "text": "Người đang hoạt động nhưng chưa từng ăn",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },
        ],

        # ======================================================
        # 10. ĐỐI CHIẾU TỔNG HỢP
        # ======================================================

        "📊 Đối chiếu tổng hợp": [

            {
                "id": "tong_suat_doi_chieu",
                "text": "Đối chiếu tổng số suất ăn",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_tien_doi_chieu",
                "text": "Đối chiếu tổng tiền ăn",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_thu_doi_chieu",
                "text": "Đối chiếu tổng tiền đã thu",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_cong_no_doi_chieu",
                "text": "Đối chiếu tổng công nợ",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "doi_chieu_tong_nguoi",
                "text": "Đối chiếu tổng số người ăn",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "doi_chieu_bo_phan",
                "text": "Đối chiếu số liệu giữa các bộ phận",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "kiem_tra_chenh_lech",
                "text": "Kiểm tra toàn bộ dữ liệu có chênh lệch",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },

            {
                "id": "tong_hop_toan_bo",
                "text": "Tổng hợp toàn bộ tình hình ăn và thu tiền",
                "need_person": False,
                "multi_person": False,
                "need_department": False,
                "need_date": True
            },
        ],
    }

    # ==========================================================
    # CÁC HÀM CƠ BẢN
    # ==========================================================

    @staticmethod
    def lay_nhom_cau_hoi():
        return list(TraCuuController.CAU_HOI.keys())

    @staticmethod
    def lay_cau_hoi_theo_nhom(nhom):
        return TraCuuController.CAU_HOI.get(nhom, [])

    @staticmethod
    def tim_cau_hoi(cau_hoi_id):

        for danh_sach in TraCuuController.CAU_HOI.values():

            for cau_hoi in danh_sach:

                if cau_hoi["id"] == cau_hoi_id:
                    return cau_hoi

        return None

    # ==========================================================
    # KIỂM TRA KHOẢNG NGÀY
    # ==========================================================

    @staticmethod
    def _kiem_tra_khoang_ngay(tu_ngay, den_ngay):

        if not tu_ngay:
            tu_ngay = date.today().isoformat()

        if not den_ngay:
            den_ngay = tu_ngay

        try:

            ngay_bat_dau = date.fromisoformat(
                str(tu_ngay)
            )

            ngay_ket_thuc = date.fromisoformat(
                str(den_ngay)
            )

        except (ValueError, TypeError):

            return (
                None,
                None,
                "Ngày tra cứu không hợp lệ."
            )

        if ngay_bat_dau > ngay_ket_thuc:

            return (
                None,
                None,
                "Ngày bắt đầu không được lớn hơn ngày kết thúc."
            )

        return (
            ngay_bat_dau.isoformat(),
            ngay_ket_thuc.isoformat(),
            None
        )

    # ==========================================================
    # CHUẨN HÓA DANH SÁCH NGƯỜI
    # ==========================================================

    @staticmethod
    def _chuan_hoa_danh_sach_nguoi(
        danh_sach_nguoi_ids
    ):

        if danh_sach_nguoi_ids is None:
            return []

        if not isinstance(
            danh_sach_nguoi_ids,
            (list, tuple, set)
        ):
            danh_sach_nguoi_ids = [
                danh_sach_nguoi_ids
            ]

        ket_qua = []

        for value in danh_sach_nguoi_ids:

            if value is None:
                continue

            try:
                value = int(value)
            except (
                TypeError,
                ValueError
            ):
                continue

            if value not in ket_qua:
                ket_qua.append(value)

        return ket_qua

    # ==========================================================
    # DANH SÁCH NGƯỜI
    # ==========================================================

    @staticmethod
    def lay_danh_sach_nguoi():

        try:

            rows = (
                TraCuuModel
                .lay_danh_sach_nguoi()
            )

            data = []

            for row in rows:

                data.append({
                    "id": row[0],
                    "ho_ten": row[1],
                    "bo_phan_id": row[2],
                    "bo_phan": row[3]
                })

            return {
                "success": True,
                "data": data
            }

        except Exception as e:

            return {
                "success": False,
                "message": (
                    f"Không thể lấy danh sách người: {e}"
                )
            }

    # ==========================================================
    # DANH SÁCH BỘ PHẬN
    # ==========================================================

    @staticmethod
    def lay_danh_sach_bo_phan():

        try:

            rows = (
                TraCuuModel
                .lay_danh_sach_bo_phan()
            )

            data = []

            for row in rows:

                data.append({
                    "id": row[0],
                    "ten": row[1]
                })

            return {
                "success": True,
                "data": data
            }

        except Exception as e:

            return {
                "success": False,
                "message": (
                    f"Không thể lấy danh sách bộ phận: {e}"
                )
            }

    # ==========================================================
    # HỖ TRỢ GỌI MODEL
    # ==========================================================

    @staticmethod
    def _goi_model(
        method_name,
        *args,
        **kwargs
    ):
        """
        Gọi Model an toàn.

        Nếu Model chưa được cập nhật hàm tương ứng,
        Controller không làm app crash mà trả về None.
        """

        try:

            method = getattr(
                TraCuuModel,
                method_name,
                None
            )

            if method is None:
                return None

            return method(
                *args,
                **kwargs
            )

        except Exception:
            return None

    # ==========================================================
    # KIỂM TRA CẦN CHỌN NGƯỜI
    # ==========================================================

    @staticmethod
    def _yeu_cau_nguoi(
        cau_hoi,
        danh_sach_nguoi_ids
    ):

        if not cau_hoi.get(
            "need_person",
            False
        ):
            return None

        if not danh_sach_nguoi_ids:

            return {
                "success": False,
                "type": "warning",
                "message": (
                    "Vui lòng chọn ít nhất một người."
                )
            }

        return None

    # ==========================================================
    # KIỂM TRA CẦN CHỌN BỘ PHẬN
    # ==========================================================

    @staticmethod
    def _yeu_cau_bo_phan(
        cau_hoi,
        bo_phan_id
    ):

        if not cau_hoi.get(
            "need_department",
            False
        ):
            return None

        if bo_phan_id is None:

            return {
                "success": False,
                "type": "warning",
                "message": (
                    "Vui lòng chọn bộ phận."
                )
            }

        return None

    # ==========================================================
    # TRA CỨU CHÍNH
    # ==========================================================

    @staticmethod
    def tra_cuu(
        cau_hoi_id,
        danh_sach_nguoi_ids=None,
        tu_ngay=None,
        den_ngay=None,
        bo_phan_id=None
    ):

        cau_hoi = (
            TraCuuController
            .tim_cau_hoi(cau_hoi_id)
        )

        if not cau_hoi:

            return {
                "success": False,
                "type": "error",
                "message": (
                    "Không tìm thấy câu hỏi tra cứu."
                )
            }

        danh_sach_nguoi_ids = (
            TraCuuController
            ._chuan_hoa_danh_sach_nguoi(
                danh_sach_nguoi_ids
            )
        )

        # ------------------------------------------------------
        # KHOẢNG NGÀY
        # ------------------------------------------------------

        if cau_hoi.get("need_date", True):

            (
                tu_ngay,
                den_ngay,
                loi
            ) = (
                TraCuuController
                ._kiem_tra_khoang_ngay(
                    tu_ngay,
                    den_ngay
                )
            )

            if loi:

                return {
                    "success": False,
                    "type": "error",
                    "message": loi
                }

        # ------------------------------------------------------
        # KIỂM TRA NGƯỜI
        # ------------------------------------------------------

        loi_nguoi = (
            TraCuuController
            ._yeu_cau_nguoi(
                cau_hoi,
                danh_sach_nguoi_ids
            )
        )

        if loi_nguoi:
            return loi_nguoi

        # ------------------------------------------------------
        # KIỂM TRA BỘ PHẬN
        # ------------------------------------------------------

        loi_bo_phan = (
            TraCuuController
            ._yeu_cau_bo_phan(
                cau_hoi,
                bo_phan_id
            )
        )

        if loi_bo_phan:
            return loi_bo_phan

        # ======================================================
        # NHÓM 1 - CHẤM CƠM
        # ======================================================

        if cau_hoi_id == "dem_nguoi_an_hom_nay":

            value = (
                TraCuuController
                ._goi_model(
                    "dem_nguoi_an_theo_khoang",
                    tu_ngay,
                    den_ngay
                )
            )

            return TraCuuController._ket_qua_so(
                value,
                f"Có {value or 0:,} người đã ăn "
                f"trong khoảng {tu_ngay} → {den_ngay}."
            )

        if cau_hoi_id == "nguoi_da_an_hom_nay":

            rows = (
                TraCuuController
                ._goi_model(
                    "lay_nguoi_da_an_theo_khoang",
                    tu_ngay,
                    den_ngay
                )
            )

            return TraCuuController._bang_nguoi_da_an(
                rows
            )

        if cau_hoi_id == "nguoi_chua_an_hom_nay":

            if tu_ngay == den_ngay:

                rows = (
                    TraCuuController
                    ._goi_model(
                        "lay_nguoi_chua_an_theo_ngay",
                        tu_ngay
                    )
                )

                data = []

                for row in rows or []:

                    data.append({
                        "ID": row[0],
                        "Họ tên": row[1],
                        "Bộ phận": row[2]
                    })

            else:

                rows = (
                    TraCuuController
                    ._goi_model(
                        "lay_nguoi_chua_an_theo_khoang",
                        tu_ngay,
                        den_ngay
                    )
                )

                data = []

                if rows is not None:

                    for row in rows:

                        data.append({
                            "ID": row[0],
                            "Họ tên": row[1],
                            "Bộ phận": row[2]
                        })

                else:

                    # Fallback bằng danh sách người đang hoạt động.
                    all_people = (
                        TraCuuModel
                        .lay_danh_sach_nguoi()
                    )

                    for person in all_people:

                        so_lan = (
                            TraCuuModel
                            .dem_so_lan_an(
                                person[0],
                                tu_ngay,
                                den_ngay
                            )
                        )

                        if so_lan == 0:

                            data.append({
                                "ID": person[0],
                                "Họ tên": person[1],
                                "Bộ phận": person[3]
                            })

            return {
                "success": True,
                "type": "table",
                "data": data,
                "message": (
                    f"Có {len(data):,} người chưa ăn "
                    f"trong khoảng đã chọn."
                )
            }

        if cau_hoi_id == "tong_so_suat":

            value = (
                TraCuuController
                ._goi_model(
                    "tong_so_suat_an",
                    tu_ngay,
                    den_ngay
                )
            )

            return TraCuuController._ket_qua_so(
                value,
                f"Tổng số suất ăn: {value or 0:,}."
            )

        if cau_hoi_id == "tong_tien_an_hom_nay":

            value = (
                TraCuuController
                ._goi_model(
                    "tong_tien_an_theo_khoang",
                    tu_ngay,
                    den_ngay
                )
            )

            return TraCuuController._ket_qua_tien(
                value,
                "Tổng tiền ăn trong khoảng thời gian."
            )

        if cau_hoi_id == "nguoi_an_nhieu_lan":

            return TraCuuController._goi_bang_model(
                "lay_nguoi_an_nhieu_lan",
                tu_ngay,
                den_ngay,
                message="Danh sách người ăn nhiều hơn 1 suất."
            )

        if cau_hoi_id == "nguoi_an_mot_suat":

            return TraCuuController._goi_bang_model(
                "lay_nguoi_an_mot_suat",
                tu_ngay,
                den_ngay,
                message="Danh sách người chỉ ăn 1 suất."
            )

        if cau_hoi_id == "nguoi_an_nhieu_nhat":

            return TraCuuController._goi_bang_model(
                "lay_nguoi_an_nhieu_nhat",
                tu_ngay,
                den_ngay,
                message="Người có số suất ăn nhiều nhất."
            )

        if cau_hoi_id == "nguoi_an_it_nhat":

            return TraCuuController._goi_bang_model(
                "lay_nguoi_an_it_nhat",
                tu_ngay,
                den_ngay,
                message="Người có số suất ăn ít nhất."
            )

        if cau_hoi_id == "thong_ke_an_theo_ngay":

            return TraCuuController._goi_bang_model(
                "thong_ke_an_theo_ngay",
                tu_ngay,
                den_ngay,
                message="Thống kê số suất ăn theo ngày."
            )

        if cau_hoi_id == "trung_binh_suat_moi_ngay":

            return TraCuuController._goi_bang_model(
                "trung_binh_suat_moi_ngay",
                tu_ngay,
                den_ngay,
                message="Trung bình số suất ăn mỗi ngày."
            )

        if cau_hoi_id == "nguoi_chua_tung_an":

            return TraCuuController._goi_bang_model(
                "lay_nguoi_chua_tung_an",
                tu_ngay,
                den_ngay,
                message="Người chưa từng ăn trong khoảng."
            )

        if cau_hoi_id == "so_ngay_an_nhieu_nhat":

            return TraCuuController._goi_bang_model(
                "lay_ngay_an_nhieu_nhat",
                tu_ngay,
                den_ngay,
                message="Ngày có nhiều suất ăn nhất."
            )

        if cau_hoi_id == "so_ngay_an_it_nhat":

            return TraCuuController._goi_bang_model(
                "lay_ngay_an_it_nhat",
                tu_ngay,
                den_ngay,
                message="Ngày có ít suất ăn nhất."
            )

        # ======================================================
        # NHÓM 2 - THEO NGƯỜI
        # ======================================================

        if cau_hoi_id == "tong_quan_nguoi":

            data = []

            for person_id in danh_sach_nguoi_ids:

                item = (
                    TraCuuController
                    ._goi_model(
                        "lay_tong_quan_nguoi",
                        person_id,
                        tu_ngay,
                        den_ngay
                    )
                )

                if not item:
                    continue

                data.append({
                    "ID": item.get("id"),
                    "Họ tên": item.get("ho_ten"),
                    "Bộ phận": item.get("bo_phan"),
                    "Tổng phải trả": item.get(
                        "tong_phai_tra", 0
                    ),
                    "Tổng đã nộp": item.get(
                        "tong_da_nop", 0
                    ),
                    "Còn nợ": item.get(
                        "con_no", 0
                    ),
                    "Số lần ăn": item.get(
                        "so_lan_an", 0
                    ),
                    "Đã ăn": (
                        "Có"
                        if item.get("da_an")
                        else "Chưa"
                    )
                })

            return {
                "success": True,
                "type": "table",
                "data": data,
                "message": (
                    "Thông tin tổng quan theo người."
                )
            }

        if cau_hoi_id == "da_an_hom_nay":

            data = []

            for person_id in danh_sach_nguoi_ids:

                nguoi = (
                    TraCuuModel
                    .lay_nguoi_theo_id(
                        person_id
                    )
                )

                if not nguoi:
                    continue

                da_an = (
                    TraCuuModel
                    .kiem_tra_da_an(
                        person_id,
                        tu_ngay,
                        den_ngay
                    )
                )

                data.append({
                    "ID": nguoi[0],
                    "Họ tên": nguoi[1],
                    "Bộ phận": nguoi[3],
                    "Đã ăn": (
                        "Có"
                        if da_an
                        else "Chưa"
                    )
                })

            return {
                "success": True,
                "type": "table",
                "data": data,
                "message": (
                    "Tình trạng ăn của người được chọn."
                )
            }

        if cau_hoi_id == "so_lan_an":

            data = []

            for person_id in danh_sach_nguoi_ids:

                nguoi = (
                    TraCuuModel
                    .lay_nguoi_theo_id(
                        person_id
                    )
                )

                if not nguoi:
                    continue

                so_lan = (
                    TraCuuModel
                    .dem_so_lan_an(
                        person_id,
                        tu_ngay,
                        den_ngay
                    )
                )

                data.append({
                    "ID": nguoi[0],
                    "Họ tên": nguoi[1],
                    "Bộ phận": nguoi[3],
                    "Số lần ăn": so_lan
                })

            return {
                "success": True,
                "type": "table",
                "data": data,
                "message": (
                    "Số lần ăn trong khoảng thời gian."
                )
            }

        if cau_hoi_id == "lich_su_an":

            if len(danh_sach_nguoi_ids) != 1:

                return {
                    "success": False,
                    "type": "warning",
                    "message": (
                        "Vui lòng chọn đúng một người."
                    )
                }

            person_id = danh_sach_nguoi_ids[0]

            rows = (
                TraCuuModel
                .lay_lich_su_an(
                    person_id,
                    tu_ngay,
                    den_ngay
                )
            )

            data = []

            for row in rows or []:

                data.append({
                    "Ngày": row[0],
                    "Đã ăn": (
                        "Có"
                        if row[1]
                        else "Chưa"
                    ),
                    "Tiền phải trả": row[2],
                    "Ghi chú": row[3]
                })

            return {
                "success": True,
                "type": "history",
                "data": data,
                "message": (
                    "Lịch sử ăn của người được chọn."
                )
            }

        if cau_hoi_id == "lich_su_nop_tien":

            if len(danh_sach_nguoi_ids) != 1:

                return {
                    "success": False,
                    "type": "warning",
                    "message": (
                        "Vui lòng chọn đúng một người."
                    )
                }

            person_id = danh_sach_nguoi_ids[0]

            rows = (
                TraCuuModel
                .lay_lich_su_nop_tien(
                    person_id,
                    tu_ngay,
                    den_ngay
                )
            )

            data = []

            for row in rows or []:

                data.append({
                    "Ngày nộp": row[0],
                    "Số tiền": row[1],
                    "Hình thức": row[2],
                    "Ghi chú": row[3]
                })

            return {
                "success": True,
                "type": "payment_history",
                "data": data,
                "message": (
                    "Lịch sử nộp tiền của người được chọn."
                )
            }

        if cau_hoi_id == "tong_da_nop":

            data = []

            for person_id in danh_sach_nguoi_ids:

                nguoi = (
                    TraCuuModel
                    .lay_nguoi_theo_id(
                        person_id
                    )
                )

                if not nguoi:
                    continue

                da_nop = (
                    TraCuuModel
                    .tong_da_nop_nguoi(
                        person_id,
                        tu_ngay,
                        den_ngay
                    )
                )

                data.append({
                    "ID": nguoi[0],
                    "Họ tên": nguoi[1],
                    "Bộ phận": nguoi[3],
                    "Đã nộp": da_nop or 0
                })

            return {
                "success": True,
                "type": "money_table",
                "data": data,
                "message": (
                    "Số tiền đã nộp trong khoảng."
                )
            }

        if cau_hoi_id in (
            "tong_phai_tra_nguoi",
            "cong_no_nguoi",
            "thanh_toan_du",
            "nop_vuot",
            "lan_an_gan_nhat",
            "lan_nop_gan_nhat",
            "ngay_chua_an",
            "an_nhieu_lan_trong_ngay",
            "doi_chieu_nguoi"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                danh_sach_nguoi_ids,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        # ======================================================
        # NHÓM 3 - SO SÁNH NHIỀU NGƯỜI
        # ======================================================

        if cau_hoi_id in (
            "so_sanh_so_suat",
            "so_sanh_phai_tra",
            "so_sanh_da_nop",
            "so_sanh_cong_no",
            "so_sanh_so_ngay_an",
            "ai_an_nhieu_hon",
            "ai_an_it_hon",
            "ai_nop_nhieu_hon",
            "ai_no_nhieu_hon",
            "so_sanh_suat_va_tien"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                danh_sach_nguoi_ids,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        # ======================================================
        # NHÓM 4 - BỘ PHẬN
        # ======================================================

        if cau_hoi_id in (
            "bo_phan_so_nguoi",
            "bo_phan_so_nguoi_an",
            "bo_phan_so_suat",
            "bo_phan_tong_tien",
            "bo_phan_da_thu",
            "bo_phan_cong_no",
            "bo_phan_nguoi_chua_an",
            "bo_phan_nguoi_no",
            "bo_phan_nop_chua_an"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                bo_phan_id,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        if cau_hoi_id in (
            "so_sanh_bo_phan_suat",
            "so_sanh_bo_phan_no",
            "bo_phan_an_nhieu_nhat",
            "bo_phan_no_nhieu_nhat"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        # ======================================================
        # NHÓM 5 - THỜI GIAN
        # ======================================================

        if cau_hoi_id in (
            "thong_ke_theo_ngay",
            "tien_theo_ngay",
            "nguoi_theo_ngay",
            "trung_binh_suat_ngay",
            "trung_binh_tien_ngay",
            "ngay_nhieu_nguoi_nhat",
            "ngay_it_nguoi_nhat",
            "ngay_tien_cao_nhat",
            "ngay_tien_thap_nhat"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        if cau_hoi_id == "lich_su_nguoi_theo_khoang":

            if len(danh_sach_nguoi_ids) != 1:

                return {
                    "success": False,
                    "type": "warning",
                    "message": (
                        "Vui lòng chọn đúng một người."
                    )
                }

            rows = (
                TraCuuModel
                .lay_lich_su_an(
                    danh_sach_nguoi_ids[0],
                    tu_ngay,
                    den_ngay
                )
            )

            return TraCuuController._rows_to_table(
                rows,
                message=cau_hoi["text"]
            )

        # ======================================================
        # NHÓM 6 - CÔNG NỢ
        # ======================================================

        if cau_hoi_id in (
            "dem_nguoi_dang_no",
            "danh_sach_dang_no",
            "tong_cong_no",
            "no_nhieu_nhat",
            "no_it_nhat",
            "an_chua_nop",
            "an_nop_thieu",
            "da_thanh_toan_du",
            "da_nop_vuot",
            "chua_tung_nop",
            "nop_chua_an",
            "an_con_no"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        # ======================================================
        # NHÓM 7 - ĐỐI CHIẾU ĂN / TIỀN
        # ======================================================

        if cau_hoi_id in (
            "doi_chieu_an_tien",
            "an_da_du",
            "tien_khong_khop",
            "suat_khong_khop_tien",
            "an_tien_bang_0",
            "tien_phai_tra_khong_suat"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        # ======================================================
        # NHÓM 8 - BẤT THƯỜNG
        # ======================================================

        if cau_hoi_id in (
            "an_nhieu_lan",
            "du_lieu_an_trung",
            "nguoi_ngung_van_an",
            "nguoi_ngung_van_nop",
            "an_nhung_tien_0",
            "co_tien_nhung_khong_an",
            "du_lieu_thieu_lien_ket",
            "nguoi_khong_bo_phan"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        if cau_hoi_id in (
            "nguoi_co_ten_trung",
            "so_dien_thoai_trung"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                message=cau_hoi["text"]
            )

        # ======================================================
        # NHÓM 9 - KIỂM TRA DỮ LIỆU
        # ======================================================

        if cau_hoi_id in (
            "chi_tiet_khong_co_ngay",
            "giao_dich_khong_co_nguoi",
            "nguoi_thieu_bo_phan",
            "ten_trung",
            "sdt_trung"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                message=cau_hoi["text"]
            )

        if cau_hoi_id in (
            "ngay_du_lieu_bat_thuong",
            "giao_dich_nghi_trung",
            "nguoi_ngung_co_du_lieu",
            "nguoi_chua_tung_an"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        # ======================================================
        # NHÓM 10 - ĐỐI CHIẾU TỔNG HỢP
        # ======================================================

        if cau_hoi_id in (
            "tong_suat_doi_chieu",
            "tong_tien_doi_chieu",
            "tong_thu_doi_chieu",
            "tong_cong_no_doi_chieu",
            "doi_chieu_tong_nguoi",
            "doi_chieu_bo_phan",
            "kiem_tra_chenh_lech",
            "tong_hop_toan_bo"
        ):

            return TraCuuController._goi_bang_model(
                cau_hoi_id,
                tu_ngay,
                den_ngay,
                message=cau_hoi["text"]
            )

        # ======================================================
        # CHƯA CÓ XỬ LÝ
        # ======================================================

        return {
            "success": False,
            "type": "warning",
            "message": (
                "Câu hỏi đã có trong danh sách nhưng "
                "chưa được kết nối với truy vấn dữ liệu."
            )
        }

    # ==========================================================
    # KẾT QUẢ SỐ
    # ==========================================================

    @staticmethod
    def _ket_qua_so(
        value,
        message
    ):

        if value is None:

            return {
                "success": False,
                "type": "warning",
                "message": (
                    "Model chưa có truy vấn tương ứng."
                )
            }

        return {
            "success": True,
            "type": "number",
            "value": value,
            "message": message
        }

    # ==========================================================
    # KẾT QUẢ TIỀN
    # ==========================================================

    @staticmethod
    def _ket_qua_tien(
        value,
        message
    ):

        if value is None:

            return {
                "success": False,
                "type": "warning",
                "message": (
                    "Model chưa có truy vấn tương ứng."
                )
            }

        return {
            "success": True,
            "type": "money",
            "value": value or 0,
            "message": message
        }

    # ==========================================================
    # BẢNG NGƯỜI ĐÃ ĂN
    # ==========================================================

    @staticmethod
    def _bang_nguoi_da_an(rows):

        if rows is None:

            return {
                "success": False,
                "type": "warning",
                "message": (
                    "Không lấy được dữ liệu người đã ăn."
                )
            }

        data = []

        for row in rows:

            if len(row) >= 5:

                data.append({
                    "ID": row[0],
                    "Họ tên": row[1],
                    "Bộ phận": row[2],
                    "Số suất": row[3],
                    "Tổng tiền": row[4]
                })

            elif len(row) >= 3:

                data.append({
                    "ID": row[0],
                    "Họ tên": row[1],
                    "Bộ phận": row[2]
                })

        return {
            "success": True,
            "type": "table",
            "data": data,
            "message": (
                f"Tìm thấy {len(data):,} người."
            )
        }

    # ==========================================================
    # GỌI MODEL TRẢ VỀ BẢNG
    # ==========================================================

    @staticmethod
    def _goi_bang_model(
        cau_hoi_id,
        *args,
        message=None
    ):

        # Map ID câu hỏi -> tên hàm Model
        method_map = {

            # Chấm cơm
            "lay_nguoi_an_nhieu_lan":
                "lay_nguoi_an_nhieu_lan",

            "lay_nguoi_an_mot_suat":
                "lay_nguoi_an_mot_suat",

            "lay_nguoi_an_nhieu_nhat":
                "lay_nguoi_an_nhieu_nhat",

            "lay_nguoi_an_it_nhat":
                "lay_nguoi_an_it_nhat",

            "thong_ke_an_theo_ngay":
                "thong_ke_an_theo_ngay",

            "trung_binh_suat_moi_ngay":
                "trung_binh_suat_moi_ngay",

            "lay_nguoi_chua_tung_an":
                "lay_nguoi_chua_tung_an",

            "lay_ngay_an_nhieu_nhat":
                "lay_ngay_an_nhieu_nhat",

            "lay_ngay_an_it_nhat":
                "lay_ngay_an_it_nhat",

            # Người
            "tong_phai_tra_nguoi":
                "tong_phai_tra_nguoi",

            "cong_no_nguoi":
                "lay_cong_no_nguoi",

            "thanh_toan_du":
                "lay_nguoi_thanh_toan_du",

            "nop_vuot":
                "lay_nguoi_nop_vuot",

            "lan_an_gan_nhat":
                "lay_lan_an_gan_nhat",

            "lan_nop_gan_nhat":
                "lay_lan_nop_gan_nhat",

            "ngay_chua_an":
                "lay_ngay_chua_an",

            "an_nhieu_lan_trong_ngay":
                "lay_an_nhieu_lan_trong_ngay",

            "doi_chieu_nguoi":
                "doi_chieu_nguoi",

            # So sánh
            "so_sanh_so_suat":
                "so_sanh_so_suat",

            "so_sanh_phai_tra":
                "so_sanh_phai_tra",

            "so_sanh_da_nop":
                "so_sanh_da_nop",

            "so_sanh_cong_no":
                "so_sanh_cong_no",

            "so_sanh_so_ngay_an":
                "so_sanh_so_ngay_an",

            "ai_an_nhieu_hon":
                "ai_an_nhieu_hon",

            "ai_an_it_hon":
                "ai_an_it_hon",

            "ai_nop_nhieu_hon":
                "ai_nop_nhieu_hon",

            "ai_no_nhieu_hon":
                "ai_no_nhieu_hon",

            "so_sanh_suat_va_tien":
                "so_sanh_suat_va_tien",

            # Bộ phận
            "bo_phan_so_nguoi":
                "bo_phan_so_nguoi",

            "bo_phan_so_nguoi_an":
                "bo_phan_so_nguoi_an",

            "bo_phan_so_suat":
                "bo_phan_so_suat",

            "bo_phan_tong_tien":
                "bo_phan_tong_tien",

            "bo_phan_da_thu":
                "bo_phan_da_thu",

            "bo_phan_cong_no":
                "bo_phan_cong_no",

            "bo_phan_nguoi_chua_an":
                "bo_phan_nguoi_chua_an",

            "bo_phan_nguoi_no":
                "bo_phan_nguoi_no",

            "bo_phan_nop_chua_an":
                "bo_phan_nop_chua_an",

            "so_sanh_bo_phan_suat":
                "so_sanh_bo_phan_suat",

            "so_sanh_bo_phan_no":
                "so_sanh_bo_phan_no",

            "bo_phan_an_nhieu_nhat":
                "bo_phan_an_nhieu_nhat",

            "bo_phan_no_nhieu_nhat":
                "bo_phan_no_nhieu_nhat",

            # Thời gian
            "thong_ke_theo_ngay":
                "thong_ke_theo_ngay",

            "tien_theo_ngay":
                "tien_theo_ngay",

            "nguoi_theo_ngay":
                "nguoi_theo_ngay",

            "trung_binh_suat_ngay":
                "trung_binh_suat_ngay",

            "trung_binh_tien_ngay":
                "trung_binh_tien_ngay",

            "ngay_nhieu_nguoi_nhat":
                "ngay_nhieu_nguoi_nhat",

            "ngay_it_nguoi_nhat":
                "ngay_it_nguoi_nhat",

            "ngay_tien_cao_nhat":
                "ngay_tien_cao_nhat",

            "ngay_tien_thap_nhat":
                "ngay_tien_thap_nhat",

            # Công nợ
            "dem_nguoi_dang_no":
                "dem_nguoi_dang_no",

            "danh_sach_dang_no":
                "lay_danh_sach_dang_no",

            "tong_cong_no":
                "tong_cong_no",

            "no_nhieu_nhat":
                "lay_nguoi_no_nhieu_nhat",

            "no_it_nhat":
                "lay_nguoi_no_it_nhat",

            "an_chua_nop":
                "lay_nguoi_an_nhung_chua_nop",

            "an_nop_thieu":
                "lay_nguoi_an_nop_thieu",

            "da_thanh_toan_du":
                "lay_nguoi_nop_du",

            "da_nop_vuot":
                "lay_nguoi_nop_vuot",

            "chua_tung_nop":
                "lay_nguoi_chua_tung_nop",

            "nop_chua_an":
                "lay_nguoi_da_nop_nhung_chua_an",

            "an_con_no":
                "lay_nguoi_an_nhung_con_no",

            # Đối chiếu
            "doi_chieu_an_tien":
                "doi_chieu_an_tien",

            "an_da_du":
                "lay_nguoi_an_da_du",

            "tien_khong_khop":
                "lay_nguoi_tien_khong_khop",

            "suat_khong_khop_tien":
                "lay_nguoi_suat_khong_khop_tien",

            "an_tien_bang_0":
                "lay_nguoi_an_tien_bang_0",

            "tien_phai_tra_khong_suat":
                "lay_nguoi_co_tien_nhung_khong_suat",

            # Bất thường
            "an_nhieu_lan":
                "lay_nguoi_an_nhieu_lan",

            "du_lieu_an_trung":
                "lay_du_lieu_an_trung",

            "nguoi_ngung_van_an":
                "lay_nguoi_ngung_hoat_dong_nhung_co_du_lieu",

            "nguoi_ngung_van_nop":
                "lay_nguoi_ngung_hoat_dong_nhung_nop_tien",

            "an_nhung_tien_0":
                "lay_nguoi_an_tien_bang_0",

            "co_tien_nhung_khong_an":
                "lay_nguoi_co_tien_nhung_khong_an",

            "du_lieu_thieu_lien_ket":
                "lay_du_lieu_thieu_lien_ket",

            "nguoi_khong_bo_phan":
                "lay_nguoi_khong_co_bo_phan",

            "nguoi_co_ten_trung":
                "lay_nguoi_trung_ten",

            "so_dien_thoai_trung":
                "lay_so_dien_thoai_trung",

            # Kiểm tra dữ liệu
            "chi_tiet_khong_co_ngay":
                "lay_chi_tiet_khong_co_ngay",

            "giao_dich_khong_co_nguoi":
                "lay_giao_dich_khong_co_nguoi",

            "nguoi_thieu_bo_phan":
                "lay_nguoi_thieu_bo_phan",

            "ten_trung":
                "lay_nguoi_trung_ten",

            "sdt_trung":
                "lay_so_dien_thoai_trung",

            "ngay_du_lieu_bat_thuong":
                "lay_ngay_du_lieu_bat_thuong",

            "giao_dich_nghi_trung":
                "lay_giao_dich_nghi_trung",

            "nguoi_ngung_co_du_lieu":
                "lay_nguoi_ngung_hoat_dong_nhung_co_du_lieu",

            "nguoi_chua_tung_an":
                "lay_nguoi_chua_tung_an",

            # Tổng hợp
            "tong_suat_doi_chieu":
                "doi_chieu_tong_suat",

            "tong_tien_doi_chieu":
                "doi_chieu_tong_tien",

            "tong_thu_doi_chieu":
                "doi_chieu_tong_thu",

            "tong_cong_no_doi_chieu":
                "doi_chieu_tong_cong_no",

            "doi_chieu_tong_nguoi":
                "doi_chieu_tong_nguoi",

            "doi_chieu_bo_phan":
                "doi_chieu_bo_phan",

            "kiem_tra_chenh_lech":
                "kiem_tra_chenh_lech",

            "tong_hop_toan_bo":
                "tong_hop_toan_bo",
        }

        method_name = method_map.get(
            cau_hoi_id
        )

        if not method_name:

            return {
                "success": False,
                "type": "warning",
                "message": (
                    "Chưa xác định được truy vấn cho câu hỏi."
                )
            }

        rows = (
            TraCuuController
            ._goi_model(
                method_name,
                *args
            )
        )

        if rows is None:

            return {
                "success": False,
                "type": "warning",
                "message": (
                    f"Câu hỏi \"{message or cau_hoi_id}\" "
                    "đã được tạo nhưng Model chưa có "
                    "truy vấn tương ứng. "
                    "Cần cập nhật TraCuuModel."
                )
            }

        return TraCuuController._rows_to_table(
            rows,
            message=message
        )

    # ==========================================================
    # CHUYỂN ROWS THÀNH TABLE
    # ==========================================================

    @staticmethod
    def _rows_to_table(
        rows,
        message=None
    ):

        if rows is None:

            return {
                "success": False,
                "type": "warning",
                "message": (
                    "Không có dữ liệu hoặc Model chưa hỗ trợ."
                )
            }

        # Model có thể trả DataFrame
        if isinstance(rows, pd.DataFrame):

            data = rows.to_dict(
                orient="records"
            )

        # Model trả list dict
        elif (
            isinstance(rows, list)
            and (
                not rows
                or isinstance(rows[0], dict)
            )
        ):

            data = rows

        # Model trả list tuple
        else:

            data = []

            for row in rows:

                if isinstance(row, dict):

                    data.append(row)

                else:

                    data.append({
                        f"Cột {i + 1}": value
                        for i, value in enumerate(row)
                    })

        return {
            "success": True,
            "type": "table",
            "data": data,
            "message": (
                message
                or f"Có {len(data):,} dòng dữ liệu."
            )
        }

    # ==========================================================
    # TẠO DATAFRAME
    # ==========================================================

    @staticmethod
    def tao_dataframe(
        data,
        columns=None
    ):

        if data is None:
            return pd.DataFrame()

        if isinstance(
            data,
            pd.DataFrame
        ):
            return data

        if isinstance(
            data,
            list
        ):

            if not data:

                return pd.DataFrame(
                    columns=columns
                )

            if isinstance(
                data[0],
                dict
            ):

                return pd.DataFrame(data)

            return pd.DataFrame(
                data,
                columns=columns
            )

        return pd.DataFrame(data)