import streamlit as st

from Controllers.nguoi_an_controller import NguoiAnController
from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section,
    hien_thi_info_card
)


def hien_thi_nguoi_an():

    # ==========================================================
    # 1. HEADER
    # ==========================================================

    hien_thi_header(
        "👩‍🍳 Quản lý người ăn",
        "Thêm, chỉnh sửa và quản lý danh sách người ăn."
    )

    # ==========================================================
    # 2. LẤY DANH SÁCH
    # ==========================================================

    result = NguoiAnController.lay_danh_sach()

    if not result["success"]:

        st.error(
            result["message"]
        )

        return

    danh_sach = result["data"]

    dang_hoat_dong = [
        x
        for x in danh_sach
        if x[3] == 1
    ]

    da_ngung = [
        x
        for x in danh_sach
        if x[3] == 0
    ]

    # ==========================================================
    # 3. THỐNG KÊ NHANH
    # ==========================================================

    hien_thi_tieu_de_section(
        "Tổng quan người ăn",
        "📊"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        hien_thi_the(
            "Tổng số người",
            len(danh_sach),
            "👥"
        )

    with col2:

        hien_thi_the(
            "Đang hoạt động",
            len(dang_hoat_dong),
            "🟢"
        )

    with col3:

        hien_thi_the(
            "Đã ngừng",
            len(da_ngung),
            "⚪"
        )

    st.markdown("")

    # ==========================================================
    # 4. THÊM NGƯỜI ĂN
    # ==========================================================

    hien_thi_tieu_de_section(
        "Thêm người ăn",
        "➕"
    )

    with st.container(border=True):

        st.markdown(
            "### 👤 Thông tin người ăn mới"
        )

        st.caption(
            "Nhập thông tin cơ bản. Họ và tên là trường bắt buộc."
        )

        col1, col2 = st.columns(2)

        with col1:

            ho_ten = st.text_input(
                "Họ và tên *",
                placeholder="Ví dụ: Nguyễn Văn A"
            )

        with col2:

            sdt = st.text_input(
                "Số điện thoại",
                placeholder="Không bắt buộc"
            )

        if st.button(
            "✨ Thêm người ăn",
            type="primary",
            width="stretch"
        ):

            if not ho_ten.strip():

                st.warning(
                    "Vui lòng nhập họ và tên."
                )

            else:

                result = (
                    NguoiAnController.them_nguoi_an(
                        ho_ten=ho_ten,
                        sdt=sdt
                    )
                )

                if result["success"]:

                    st.success(
                        result["message"]
                    )

                    st.rerun()

                else:

                    st.error(
                        result["message"]
                    )

    st.markdown("")

    # ==========================================================
    # 5. TÌM KIẾM & LỌC
    # ==========================================================

    hien_thi_tieu_de_section(
        "Danh sách người ăn",
        "👥"
    )

    col1, col2 = st.columns([2, 1])

    with col1:

        tu_khoa = st.text_input(
            "🔎 Tìm kiếm",
            placeholder="Nhập tên người ăn..."
        )

    with col2:

        trang_thai = st.selectbox(
            "Trạng thái",
            [
                "Tất cả",
                "Đang hoạt động",
                "Đã ngừng"
            ]
        )

    # ==========================================================
    # 6. LỌC DỮ LIỆU
    # ==========================================================

    danh_sach_hien_thi = danh_sach

    if tu_khoa.strip():

        tu_khoa_lower = (
            tu_khoa
            .strip()
            .lower()
        )

        danh_sach_hien_thi = [
            x
            for x in danh_sach_hien_thi
            if tu_khoa_lower
            in str(x[1]).lower()
        ]

    if trang_thai == "Đang hoạt động":

        danh_sach_hien_thi = [
            x
            for x in danh_sach_hien_thi
            if x[3] == 1
        ]

    elif trang_thai == "Đã ngừng":

        danh_sach_hien_thi = [
            x
            for x in danh_sach_hien_thi
            if x[3] == 0
        ]

    # ==========================================================
    # 7. KẾT QUẢ LỌC
    # ==========================================================

    st.caption(
        f"Hiển thị {len(danh_sach_hien_thi)} / "
        f"{len(danh_sach)} người ăn"
    )

    if not danh_sach_hien_thi:

        st.info(
            "🌷 Không tìm thấy người ăn phù hợp."
        )

        return

    # ==========================================================
    # 8. DANH SÁCH
    # ==========================================================

    for nguoi in danh_sach_hien_thi:

        nguoi_id = nguoi[0]

        ho_ten_hien_tai = nguoi[1]

        sdt_hien_tai = nguoi[2] or ""

        dang_hoat_dong = nguoi[3]

        if dang_hoat_dong:

            trang_thai_text = (
                "🟢 Đang hoạt động"
            )

        else:

            trang_thai_text = (
                "⚪ Đã ngừng"
            )

        with st.container(border=True):

            # --------------------------------------------------
            # THÔNG TIN
            # --------------------------------------------------

            col1, col2, col3 = st.columns(
                [3.5, 2, 1.4]
            )

            with col1:

                st.markdown(
                    f"### 👤 {ho_ten_hien_tai}"
                )

                st.caption(
                    f"📞 SĐT: "
                    f"{sdt_hien_tai or 'Chưa cập nhật'}"
                )

            with col2:

                st.write(
                    trang_thai_text
                )

                st.caption(
                    f"ID người ăn: {nguoi_id}"
                )

            with col3:

                if dang_hoat_dong:

                    if st.button(
                        "✏️ Sửa",
                        key=f"sua_{nguoi_id}",
                        width="stretch"
                    ):

                        st.session_state[
                            f"edit_{nguoi_id}"
                        ] = True

                        st.rerun()

                    if st.button(
                        "⏸️ Ngừng",
                        key=f"ngung_{nguoi_id}",
                        width="stretch"
                    ):

                        result = (
                            NguoiAnController
                            .ngung_hoat_dong(
                                nguoi_id
                            )
                        )

                        if result["success"]:

                            st.success(
                                result["message"]
                            )

                            st.rerun()

                        else:

                            st.error(
                                result["message"]
                            )

                else:

                    if st.button(
                        "🔄 Kích hoạt",
                        key=f"kich_hoat_{nguoi_id}",
                        width="stretch"
                    ):

                        result = (
                            NguoiAnController
                            .kich_hoat_lai(
                                nguoi_id
                            )
                        )

                        if result["success"]:

                            st.success(
                                result["message"]
                            )

                            st.rerun()

                        else:

                            st.error(
                                result["message"]
                            )

            # --------------------------------------------------
            # FORM SỬA
            # --------------------------------------------------

            if st.session_state.get(
                f"edit_{nguoi_id}",
                False
            ):

                st.divider()

                st.markdown(
                    "### ✏️ Chỉnh sửa thông tin"
                )

                col1, col2 = st.columns(2)

                with col1:

                    ten_moi = st.text_input(
                        "Họ và tên",
                        value=ho_ten_hien_tai,
                        key=f"ten_moi_{nguoi_id}"
                    )

                with col2:

                    sdt_moi = st.text_input(
                        "Số điện thoại",
                        value=sdt_hien_tai,
                        key=f"sdt_moi_{nguoi_id}"
                    )

                col_a, col_b = st.columns(2)

                with col_a:

                    if st.button(
                        "💾 Lưu thay đổi",
                        key=f"luu_{nguoi_id}",
                        type="primary",
                        width="stretch"
                    ):

                        result = (
                            NguoiAnController.cap_nhat(
                                nguoi_an_id=nguoi_id,
                                ho_ten=ten_moi,
                                sdt=sdt_moi
                            )
                        )

                        if result["success"]:

                            st.success(
                                result["message"]
                            )

                            st.session_state[
                                f"edit_{nguoi_id}"
                            ] = False

                            st.rerun()

                        else:

                            st.error(
                                result["message"]
                            )

                with col_b:

                    if st.button(
                        "Hủy",
                        key=f"huy_{nguoi_id}",
                        width="stretch"
                    ):

                        st.session_state[
                            f"edit_{nguoi_id}"
                        ] = False

                        st.rerun()