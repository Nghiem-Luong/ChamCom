import streamlit as st
from datetime import datetime

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section,
    hien_thi_info_card
)

from Controllers.nguoi_an_controller import NguoiAnController


def hien_thi_trang_chu():

    # ==========================================================
    # 1. HEADER
    # ==========================================================

    hien_thi_header(
        "🏠 Trang chủ",
        "Tổng quan nhanh về hệ thống Quản lý Chấm Cơm."
    )

    # ==========================================================
    # 2. THÔNG TIN NGÀY
    # ==========================================================

    ngay_hien_tai = datetime.now().strftime(
        "%d/%m/%Y"
    )

    gio_hien_tai = datetime.now().strftime(
        "%H:%M"
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        st.info(
            f"📅 Hôm nay: **{ngay_hien_tai}**  •  🕐 {gio_hien_tai}"
        )

    with col2:
        st.success(
            "🟢 Hệ thống hoạt động"
        )

    # ==========================================================
    # 3. LẤY DỮ LIỆU NGƯỜI ĂN
    # ==========================================================

    result = NguoiAnController.lay_danh_sach()

    if result["success"]:

        danh_sach = result["data"]

        tong_nguoi = len(danh_sach)

        dang_hoat_dong = len(
            [
                nguoi
                for nguoi in danh_sach
                if nguoi[3] == 1
            ]
        )

        da_ngung = len(
            [
                nguoi
                for nguoi in danh_sach
                if nguoi[3] == 0
            ]
        )

    else:

        tong_nguoi = 0
        dang_hoat_dong = 0
        da_ngung = 0

        st.warning(
            "⚠️ Không thể lấy dữ liệu người ăn."
        )

    # ==========================================================
    # 4. TỔNG QUAN
    # ==========================================================

    hien_thi_tieu_de_section(
        "Tổng quan hệ thống",
        "📊"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        hien_thi_the(
            "Tổng số người ăn",
            tong_nguoi,
            "👥"
        )

    with col2:
        hien_thi_the(
            "Đang hoạt động",
            dang_hoat_dong,
            "🟢"
        )

    with col3:
        hien_thi_the(
            "Đã ngừng",
            da_ngung,
            "⚪"
        )

    st.markdown("")

    # ==========================================================
    # 5. TÌNH TRẠNG NGƯỜI ĂN
    # ==========================================================

    hien_thi_tieu_de_section(
        "Tình trạng người ăn",
        "👥"
    )

    if tong_nguoi > 0:

        ty_le_hoat_dong = (
            dang_hoat_dong
            / tong_nguoi
            * 100
        )

    else:

        ty_le_hoat_dong = 0

    col1, col2 = st.columns([2, 1])

    with col1:

        hien_thi_info_card(
            "🟢 Người ăn đang hoạt động",
            (
                f"Có {dang_hoat_dong} người đang hoạt động "
                f"trên tổng số {tong_nguoi} người."
            )
        )

        st.progress(
            ty_le_hoat_dong / 100,
            text=f"Tỷ lệ hoạt động: {ty_le_hoat_dong:.1f}%"
        )

    with col2:

        hien_thi_info_card(
            "⚪ Đã ngừng hoạt động",
            f"{da_ngung} người"
        )

    st.markdown("")

    # ==========================================================
    # 6. CHỨC NĂNG CHÍNH
    # ==========================================================

    hien_thi_tieu_de_section(
        "Chức năng chính",
        "✨"
    )

    col1, col2 = st.columns(2)

    with col1:

        hien_thi_info_card(
            "🍚 Chấm cơm",
            (
                "Quản lý người ăn, đăng ký suất ăn, "
                "đơn giá và số tiền phải trả theo từng ngày."
            )
        )

    with col2:

        hien_thi_info_card(
            "👩‍🍳 Quản lý người ăn",
            (
                "Thêm, chỉnh sửa, tìm kiếm, "
                "ngừng hoạt động hoặc kích hoạt lại người ăn."
            )
        )

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:

        hien_thi_info_card(
            "💰 Nộp tiền & công nợ",
            (
                "Theo dõi tiền đã nộp, tiền phải trả "
                "và tình trạng công nợ của từng người."
            )
        )

    with col2:

        hien_thi_info_card(
            "📊 Thống kê & báo cáo",
            (
                "Theo dõi dữ liệu theo thời gian "
                "và xuất báo cáo phục vụ quản lý."
            )
        )

    st.markdown("")

    # ==========================================================
    # 7. TRỢ LÝ AI
    # ==========================================================

    hien_thi_tieu_de_section(
        "Trợ lý thông minh",
        "🤖"
    )

    with st.container(border=True):

        st.markdown(
            "### 🤖 Dâu Tây"
        )

        st.write(
            "Trợ lý AI hỗ trợ tra cứu thông tin "
            "và dữ liệu trong hệ thống bằng "
            "câu hỏi tiếng Việt tự nhiên."
        )

        st.info(
            "💡 Bạn có thể sử dụng robot ở góc "
            "màn hình để đặt câu hỏi."
        )

    st.markdown("")

    # ==========================================================
    # 8. QUY TRÌNH SỬ DỤNG
    # ==========================================================

    hien_thi_tieu_de_section(
        "Quy trình sử dụng",
        "📌"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        hien_thi_info_card(
            "① 👩‍🍳 Quản lý người ăn",
            (
                "Thêm và quản lý danh sách "
                "người sử dụng suất ăn."
            )
        )

    with col2:

        hien_thi_info_card(
            "② 🍚 Chấm cơm",
            (
                "Ghi nhận người ăn và "
                "số tiền phải trả."
            )
        )

    with col3:

        hien_thi_info_card(
            "③ 📊 Theo dõi",
            (
                "Kiểm tra công nợ, "
                "thống kê và báo cáo."
            )
        )