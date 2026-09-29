import streamlit as st
from datetime import date

from Controllers.nguoi_an_controller import NguoiAnController
from Controllers.nop_tien_controller import NopTienController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section
)


def hien_thi_nop_tien():

    # ==========================================================
    # 1. HEADER
    # ==========================================================

    hien_thi_header(
        "💰 Nộp tiền & Bảng công nợ",
        "Theo dõi tiền đã nộp, tiền phải trả và số dư của từng người."
    )

    # ==========================================================
    # 2. LẤY DANH SÁCH NGƯỜI ĂN
    # ==========================================================

    result_nguoi = NguoiAnController.lay_danh_sach()

    if not result_nguoi["success"]:

        st.error(
            result_nguoi["message"]
        )

        return

    danh_sach = result_nguoi["data"]

    if not danh_sach:

        st.info(
            "🌷 Chưa có người ăn. Hãy thêm người ăn trước."
        )

        return

    # ==========================================================
    # 3. TÍNH TỔNG QUAN
    # ==========================================================

    tong_da_nop = 0
    tong_phai_tra = 0
    tong_so_du = 0

    danh_sach_cong_no = []

    for nguoi in danh_sach:

        nguoi_id = nguoi[0]
        ho_ten = nguoi[1]

        result = NopTienController.tinh_so_du(
            nguoi_id
        )

        if result["success"]:

            da_nop = result["tong_da_nop"]
            phai_tra = result["tong_phai_tra"]
            so_du = result["data"]

        else:

            da_nop = 0
            phai_tra = 0
            so_du = 0

        tong_da_nop += da_nop
        tong_phai_tra += phai_tra
        tong_so_du += so_du

        danh_sach_cong_no.append({
            "id": nguoi_id,
            "ho_ten": ho_ten,
            "da_nop": da_nop,
            "phai_tra": phai_tra,
            "so_du": so_du,
            "dang_hoat_dong": nguoi[3]
        })

    # ==========================================================
    # 4. TỔNG QUAN TÀI CHÍNH
    # ==========================================================

    hien_thi_tieu_de_section(
        "Tổng quan tài chính",
        "📊"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        hien_thi_the(
            "Tổng tiền đã nộp",
            f"{tong_da_nop:,.0f} đ",
            "💵"
        )

    with col2:

        hien_thi_the(
            "Tổng tiền phải trả",
            f"{tong_phai_tra:,.0f} đ",
            "🍚"
        )

    with col3:

        hien_thi_the(
            "Tổng số dư",
            f"{tong_so_du:,.0f} đ",
            "💳"
        )

    st.markdown("")

    # ==========================================================
    # 5. GHI NHẬN NỘP TIỀN
    # ==========================================================

    hien_thi_tieu_de_section(
        "Ghi nhận nộp tiền",
        "💵"
    )

    with st.container(border=True):

        st.markdown(
            "### 💰 Khoản nộp mới"
        )

        st.caption(
            "Nhập thông tin khoản tiền người ăn vừa nộp."
        )

        danh_sach_chon = [
            nguoi
            for nguoi in danh_sach
            if nguoi[3] == 1
        ]

        if not danh_sach_chon:

            st.warning(
                "Không có người ăn đang hoạt động."
            )

        else:

            col1, col2 = st.columns(2)

            with col1:

                lua_chon = st.selectbox(
                    "👤 Người nộp tiền",
                    danh_sach_chon,
                    format_func=lambda x: x[1]
                )

            with col2:

                ngay_nop = st.date_input(
                    "📅 Ngày nộp",
                    value=date.today(),
                    format="DD/MM/YYYY"
                )

            col1, col2 = st.columns(2)

            with col1:

                so_tien = st.number_input(
                    "💰 Số tiền",
                    min_value=0,
                    step=10000,
                    value=0,
                    format="%d"
                )

            with col2:

                hinh_thuc = st.selectbox(
                    "💳 Hình thức",
                    [
                        "Tiền mặt",
                        "Chuyển khoản"
                    ]
                )

            ghi_chu = st.text_input(
                "📝 Ghi chú",
                placeholder="Ví dụ: Nộp tiền tháng 10..."
            )

            if st.button(
                "💾 Lưu khoản nộp",
                type="primary",
                width="stretch"
            ):

                if so_tien <= 0:

                    st.warning(
                        "Số tiền phải lớn hơn 0."
                    )

                else:

                    result = (
                        NopTienController.them_giao_dich(
                            nguoi_an_id=lua_chon[0],
                            ngay_nop=ngay_nop.strftime(
                                "%Y-%m-%d"
                            ),
                            so_tien=so_tien,
                            hinh_thuc=hinh_thuc,
                            ghi_chu=ghi_chu
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
    # 6. BẢNG CÔNG NỢ
    # ==========================================================

    hien_thi_tieu_de_section(
        "Bảng công nợ",
        "📋"
    )

    col1, col2 = st.columns([2, 1])

    with col1:

        tu_khoa = st.text_input(
            "🔎 Tìm người",
            placeholder="Nhập tên người ăn..."
        )

    with col2:

        st.write("")

        st.caption(
            f"👥 Tổng số: {len(danh_sach_cong_no)} người"
        )

    danh_sach_hien_thi = danh_sach_cong_no

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
            in x["ho_ten"].lower()
        ]

    if not danh_sach_hien_thi:

        st.info(
            "🌷 Không tìm thấy người phù hợp."
        )

        return

    # ==========================================================
    # 7. HIỂN THỊ CÔNG NỢ
    # ==========================================================

    for nguoi in danh_sach_hien_thi:

        nguoi_id = nguoi["id"]
        ho_ten = nguoi["ho_ten"]
        da_nop = nguoi["da_nop"]
        phai_tra = nguoi["phai_tra"]
        so_du = nguoi["so_du"]

        if so_du > 0:

            trang_thai = "🟢 Còn dư tiền"

        elif so_du == 0:

            trang_thai = "⚪ Đã đủ"

        else:

            trang_thai = "🟠 Còn thiếu"

        with st.container(border=True):

            # --------------------------------------------------
            # THÔNG TIN TỔNG QUAN
            # --------------------------------------------------

            st.markdown(
                f"### 👤 {ho_ten}"
            )

            st.caption(
                trang_thai
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.caption(
                    "💵 Đã nộp"
                )

                st.markdown(
                    f"**{da_nop:,.0f} đ**"
                )

            with col2:

                st.caption(
                    "🍚 Phải trả"
                )

                st.markdown(
                    f"**{phai_tra:,.0f} đ**"
                )

            with col3:

                st.caption(
                    "💳 Số dư"
                )

                st.markdown(
                    f"**{so_du:,.0f} đ**"
                )

            # --------------------------------------------------
            # CHI TIẾT
            # --------------------------------------------------

            with st.expander(
                "📋 Xem chi tiết"
            ):

                # ==============================================
                # CHI TIẾT TIỀN CƠM
                # ==============================================

                st.markdown(
                    "#### 🍚 Chi tiết tiền cơm"
                )

                result_tien_com = (
                    NopTienController.lay_chi_tiet_tien_com(
                        nguoi_id
                    )
                )

                if result_tien_com["success"]:

                    chi_tiet_tien_com = (
                        result_tien_com["data"]
                    )

                    tong_tien_com = 0

                    if chi_tiet_tien_com:

                        for item in chi_tiet_tien_com:

                            (
                                chi_tiet_id,
                                _,
                                _,
                                _,
                                ngay_an,
                                da_an,
                                so_tien_phai_tra,
                                ghi_chu_an
                            ) = item

                            if da_an == 1:

                                tong_tien_com += (
                                    so_tien_phai_tra
                                )

                                st.write(
                                    f"📅 **{ngay_an}** — "
                                    f"🍚 Đã ăn — "
                                    f"**{so_tien_phai_tra:,.0f} đ**"
                                )

                                if ghi_chu_an:

                                    st.caption(
                                        f"📝 {ghi_chu_an}"
                                    )

                            else:

                                st.write(
                                    f"📅 **{ngay_an}** — "
                                    f"Không ăn"
                                )

                        st.divider()

                        st.markdown(
                            f"**Tổng tiền cơm: "
                            f"{tong_tien_com:,.0f} đ**"
                        )

                        # ======================================
                        # TỔNG KẾT TÀI CHÍNH
                        # ======================================

                        st.markdown(
                            "#### 💳 Tổng kết tài chính"
                        )

                        col_tc1, col_tc2, col_tc3 = (
                            st.columns(3)
                        )

                        with col_tc1:

                            st.caption(
                                "🍚 Phải trả"
                            )

                            st.write(
                                f"**{phai_tra:,.0f} đ**"
                            )

                        with col_tc2:

                            st.caption(
                                "💵 Đã nộp"
                            )

                            st.write(
                                f"**{da_nop:,.0f} đ**"
                            )

                        with col_tc3:

                            st.caption(
                                "💳 Số dư"
                            )

                            st.write(
                                f"**{so_du:,.0f} đ**"
                            )

                    else:

                        st.info(
                            "Người này chưa có dữ liệu chấm cơm."
                        )

                else:

                    st.error(
                        result_tien_com["message"]
                    )

                # ==============================================
                # LỊCH SỬ NỘP TIỀN
                # ==============================================

                st.markdown(
                    "#### 💰 Lịch sử nộp tiền"
                )

                result_giao_dich = (
                    NopTienController.lay_theo_nguoi(
                        nguoi_id
                    )
                )

                if result_giao_dich["success"]:

                    giao_dich = (
                        result_giao_dich["data"]
                    )

                    if giao_dich:

                        for giao_dich_item in giao_dich:

                            (
                                giao_dich_id,
                                _,
                                _,
                                ngay_nop,
                                tien,
                                hinh_thuc_item,
                                ghi_chu_item
                            ) = giao_dich_item

                            with st.container(
                                border=True
                            ):

                                col1, col2 = st.columns(
                                    [4, 1]
                                )

                                with col1:

                                    st.write(
                                        f"📅 **{ngay_nop}**"
                                    )

                                    st.write(
                                        f"💵 **{tien:,.0f} đ**"
                                    )

                                    st.caption(
                                        f"💳 {hinh_thuc_item}"
                                    )

                                    if ghi_chu_item:

                                        st.caption(
                                            f"📝 {ghi_chu_item}"
                                        )

                                with col2:

                                    if st.button(
                                        "🗑️ Xóa",
                                        key=(
                                            f"xoa_gd_"
                                            f"{giao_dich_id}"
                                        ),
                                        width="stretch"
                                    ):

                                        result_xoa = (
                                            NopTienController.xoa(
                                                giao_dich_id
                                            )
                                        )

                                        if result_xoa["success"]:

                                            st.success(
                                                result_xoa["message"]
                                            )

                                            st.rerun()

                                        else:

                                            st.error(
                                                result_xoa["message"]
                                            )

                    else:

                        st.info(
                            "Người này chưa có khoản nộp tiền nào."
                        )

                else:

                    st.error(
                        result_giao_dich["message"]
                    )