import streamlit as st
from datetime import date

from Controllers.nguoi_an_controller import NguoiAnController
from Controllers.ngay_an_controller import NgayAnController
from Controllers.chi_tiet_an_controller import ChiTietAnController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section,
    hien_thi_info_card
)


def hien_thi_cham_com():

    # ==========================================================
    # 1. HEADER
    # ==========================================================

    hien_thi_header(
        "🍚 Chấm cơm hôm nay",
        "Đăng ký suất ăn và theo dõi số tiền phải trả theo từng ngày."
    )

    # ==========================================================
    # 2. CHỌN NGÀY
    # ==========================================================

    hien_thi_tieu_de_section(
        "Chọn ngày ăn",
        "📅"
    )

    col1, col2 = st.columns([1.3, 2])

    with col1:

        ngay_chon = st.date_input(
            "Ngày ăn",
            value=date.today(),
            format="DD/MM/YYYY"
        )

    ngay_str = ngay_chon.strftime(
        "%Y-%m-%d"
    )

    # ==========================================================
    # 3. TÌM NGÀY ĂN
    # ==========================================================

    result_ngay = NgayAnController.tim_theo_ngay(
        ngay_str
    )

    if not result_ngay.get(
        "success",
        False
    ):

        st.error(
            result_ngay.get(
                "message",
                "Không thể lấy thông tin ngày ăn."
            )
        )

        return

    ngay_an = result_ngay.get(
        "data"
    )

    # ==========================================================
    # 4. NGÀY CHƯA ĐƯỢC TẠO
    # ==========================================================

    if not ngay_an:

        st.info(
            "🌷 Ngày này chưa được tạo. "
            "Hãy kiểm tra đơn giá trước khi tạo ngày ăn."
        )

        # ------------------------------------------------------
        # ĐƠN GIÁ MẶC ĐỊNH
        # ------------------------------------------------------

        don_gia_mac_dinh = 30000

        try:

            result_truoc = (
                NgayAnController.lay_ngay_truoc_do(
                    ngay_str
                )
            )

            if result_truoc.get(
                "success",
                False
            ):

                ngay_truoc = result_truoc.get(
                    "data"
                )

                if ngay_truoc:

                    don_gia_truoc = ngay_truoc[2]

                    if don_gia_truoc is not None:

                        don_gia_mac_dinh = int(
                            don_gia_truoc
                        )

        except Exception:

            don_gia_mac_dinh = 30000

        # ------------------------------------------------------
        # THÔNG TIN TẠO NGÀY
        # ------------------------------------------------------

        hien_thi_tieu_de_section(
            "Thông tin ngày ăn",
            "⚙️"
        )

        col1, col2 = st.columns(2)

        with col1:

            don_gia = st.number_input(
                "💰 Đơn giá",
                min_value=0,
                step=1000,
                value=don_gia_mac_dinh,
                format="%d"
            )

        with col2:

            ghi_chu = st.text_input(
                "📝 Ghi chú ngày",
                placeholder="Ví dụ: Suất ăn tháng 10..."
            )

        st.caption(
            f"💡 Đơn giá đề xuất từ ngày trước: "
            f"{don_gia_mac_dinh:,.0f} đ"
        )

        st.markdown("")

        if st.button(
            "✨ Tạo ngày ăn",
            width="stretch",
            type="primary"
        ):

            result = NgayAnController.tao_ngay_an(
                ngay=ngay_str,
                don_gia_mac_dinh=don_gia,
                ghi_chu=ghi_chu
            )

            if result.get(
                "success",
                False
            ):

                st.success(
                    result.get(
                        "message",
                        "Đã tạo ngày ăn."
                    )
                )

                st.rerun()

            else:

                st.error(
                    result.get(
                        "message",
                        "Không thể tạo ngày ăn."
                    )
                )

        return

    # ==========================================================
    # 5. THÔNG TIN NGÀY ĐÃ CÓ
    # ==========================================================

    ngay_an_id = ngay_an[0]

    don_gia = ngay_an[2]

    if don_gia is None:
        don_gia = 0

    don_gia = int(
        don_gia
    )

    hien_thi_tieu_de_section(
        "Thông tin ngày ăn",
        "📌"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        hien_thi_the(
            "Ngày ăn",
            ngay_chon.strftime(
                "%d/%m/%Y"
            ),
            "📅"
        )

    with col2:

        hien_thi_the(
            "Đơn giá",
            f"{don_gia:,.0f} đ",
            "💰"
        )

    with col3:

        hien_thi_the(
            "Trạng thái",
            "Đăng ký ăn",
            "🟢"
        )

    st.markdown("")

    # ==========================================================
    # 6. LẤY DANH SÁCH NGƯỜI HOẠT ĐỘNG
    # ==========================================================

    result_nguoi = (
        NguoiAnController
        .lay_danh_sach_dang_hoat_dong()
    )

    if not result_nguoi.get(
        "success",
        False
    ):

        st.error(
            result_nguoi.get(
                "message",
                "Không thể lấy danh sách người ăn."
            )
        )

        return

    danh_sach = result_nguoi.get(
        "data",
        []
    )

    if not danh_sach:

        st.warning(
            "👥 Chưa có người ăn đang hoạt động."
        )

        return

    # ==========================================================
    # 7. LẤY DỮ LIỆU ĐÃ ĐĂNG KÝ
    # ==========================================================

    result_cham = (
        ChiTietAnController
        .lay_theo_ngay(
            ngay_an_id
        )
    )

    if not result_cham.get(
        "success",
        False
    ):

        st.error(
            result_cham.get(
                "message",
                "Không thể lấy dữ liệu đăng ký."
            )
        )

        return

    du_lieu_da_cham = result_cham.get(
        "data",
        []
    )

    # ==========================================================
    # 8. TẠO DICTIONARY TRẠNG THÁI
    # ==========================================================

    da_dang_ky = {}

    for item in du_lieu_da_cham:

        try:

            nguoi_an_id = item[1]

            da_an = item[5]

            da_dang_ky[nguoi_an_id] = bool(
                da_an
            )

        except (
            IndexError,
            TypeError,
            ValueError
        ):

            continue

    # ==========================================================
    # 9. KHỞI TẠO CHECKBOX
    # ==========================================================

    for nguoi in danh_sach:

        nguoi_an_id = nguoi[0]

        key = (
            f"dang_ky_"
            f"{ngay_str}_"
            f"{nguoi_an_id}"
        )

        if key not in st.session_state:

            if nguoi_an_id in da_dang_ky:

                st.session_state[key] = (
                    da_dang_ky[nguoi_an_id]
                )

            else:

                st.session_state[key] = True

    # ==========================================================
    # 10. KHU VỰC ĐĂNG KÝ
    # ==========================================================

    hien_thi_tieu_de_section(
        "Danh sách đăng ký",
        "👥"
    )

    tu_khoa = st.text_input(
        "🔎 Tìm người",
        placeholder="Nhập tên để tìm nhanh..."
    )

    danh_sach_hien_thi = danh_sach

    if tu_khoa.strip():

        tu_khoa_lower = (
            tu_khoa
            .strip()
            .lower()
        )

        danh_sach_hien_thi = [
            nguoi
            for nguoi in danh_sach
            if tu_khoa_lower
            in str(
                nguoi[1]
            ).lower()
        ]

    if not danh_sach_hien_thi:

        st.info(
            "Không tìm thấy người phù hợp."
        )

        return

    # ==========================================================
    # 11. CHỌN / BỎ CHỌN
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "☑️ Chọn tất cả",
            width="stretch"
        ):

            for nguoi in danh_sach:

                nguoi_an_id = nguoi[0]

                key = (
                    f"dang_ky_"
                    f"{ngay_str}_"
                    f"{nguoi_an_id}"
                )

                st.session_state[key] = True

            st.rerun()

    with col2:

        if st.button(
            "⬜ Bỏ chọn tất cả",
            width="stretch"
        ):

            for nguoi in danh_sach:

                nguoi_an_id = nguoi[0]

                key = (
                    f"dang_ky_"
                    f"{ngay_str}_"
                    f"{nguoi_an_id}"
                )

                st.session_state[key] = False

            st.rerun()

    # ==========================================================
    # 12. DANH SÁCH NGƯỜI
    # ==========================================================

    so_nguoi_dang_ky = 0

    for nguoi in danh_sach_hien_thi:

        nguoi_an_id = nguoi[0]

        ho_ten = nguoi[1]

        key = (
            f"dang_ky_"
            f"{ngay_str}_"
            f"{nguoi_an_id}"
        )

        trang_thai = st.checkbox(
            ho_ten,
            key=key
        )

        if trang_thai:

            so_nguoi_dang_ky += 1

    # ==========================================================
    # 13. TỔNG TẠM TÍNH
    # ==========================================================

    tong_nguoi_dang_ky = 0

    for nguoi in danh_sach:

        nguoi_an_id = nguoi[0]

        key = (
            f"dang_ky_"
            f"{ngay_str}_"
            f"{nguoi_an_id}"
        )

        if st.session_state.get(
            key,
            False
        ):

            tong_nguoi_dang_ky += 1

    tong_tien = (
        tong_nguoi_dang_ky
        * don_gia
    )

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:

        hien_thi_the(
            "Số người đăng ký",
            tong_nguoi_dang_ky,
            "👥"
        )

    with col2:

        hien_thi_the(
            "Tổng tiền",
            f"{tong_tien:,.0f} đ",
            "💰"
        )

    # ==========================================================
    # 14. LƯU ĐĂNG KÝ
    # ==========================================================

    st.markdown("")

    if st.button(
        "💾 LƯU ĐĂNG KÝ",
        width="stretch",
        type="primary"
    ):

        danh_sach_dang_ky = []

        for nguoi in danh_sach:

            nguoi_an_id = nguoi[0]

            key = (
                f"dang_ky_"
                f"{ngay_str}_"
                f"{nguoi_an_id}"
            )

            if st.session_state.get(
                key,
                False
            ):

                danh_sach_dang_ky.append(
                    nguoi_an_id
                )

        result = (
            ChiTietAnController
            .luu_danh_sach_dang_ky(
                ngay_an_id=ngay_an_id,
                danh_sach_nguoi_an=danh_sach_dang_ky,
                don_gia=don_gia
            )
        )

        if result.get(
            "success",
            False
        ):

            st.success(
                result.get(
                    "message",
                    "Đã lưu đăng ký."
                )
            )

            st.rerun()

        else:

            st.error(
                result.get(
                    "message",
                    "Không thể lưu đăng ký."
                )
            )

    # ==========================================================
    # 15. DANH SÁCH ĐÃ LƯU
    # ==========================================================

    hien_thi_tieu_de_section(
        "Danh sách đã đăng ký",
        "🍚"
    )

    result_sau_luu = (
        ChiTietAnController
        .lay_theo_ngay(
            ngay_an_id
        )
    )

    if result_sau_luu.get(
        "success",
        False
    ):

        du_lieu_sau_luu = (
            result_sau_luu.get(
                "data",
                []
            )
        )

        danh_sach_da_dang_ky = [
            item
            for item in du_lieu_sau_luu
            if bool(item[5])
        ]

        if danh_sach_da_dang_ky:

            so_luong = len(
                danh_sach_da_dang_ky
            )

            tong_tien_da_dang_ky = (
                so_luong
                * don_gia
            )

            col1, col2 = st.columns(2)

            with col1:

                hien_thi_the(
                    "Tổng số người",
                    f"{so_luong} người",
                    "👥"
                )

            with col2:

                hien_thi_the(
                    "Tổng tiền",
                    f"{tong_tien_da_dang_ky:,.0f} đ",
                    "💰"
                )

            st.markdown("")

            for index, item in enumerate(
                danh_sach_da_dang_ky,
                start=1
            ):

                ho_ten = item[2]

                col1, col2, col3 = st.columns(
                    [0.8, 5, 2]
                )

                with col1:

                    st.write(
                        f"**{index}**"
                    )

                with col2:

                    st.write(
                        f"**{ho_ten}**"
                    )

                with col3:

                    st.write(
                        f"{don_gia:,.0f} đ"
                    )

                if index < so_luong:

                    st.divider()

        else:

            st.info(
                "🍚 Chưa có ai đăng ký ăn trong ngày này."
            )

    else:

        st.error(
            result_sau_luu.get(
                "message",
                "Không thể tải danh sách đăng ký."
            )
        )