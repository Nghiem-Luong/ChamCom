import streamlit as st
from datetime import date, timedelta

from Controllers.thong_ke_controller import ThongKeController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section
)


def hien_thi_thong_ke():

    # ==========================================================
    # 1. HEADER
    # ==========================================================

    hien_thi_header(
        "📊 Thống kê",
        "Theo dõi tình hình ăn uống và chi phí theo thời gian."
    )

    # ==========================================================
    # 2. CHỌN KHOẢNG THỜI GIAN
    # ==========================================================

    hien_thi_tieu_de_section(
        "Khoảng thời gian thống kê",
        "📅"
    )

    with st.container(border=True):

        che_do = st.selectbox(
            "Kiểu thống kê",
            [
                "Hôm nay",
                "7 ngày gần nhất",
                "Tháng này",
                "Tùy chọn"
            ]
        )

        hom_nay = date.today()

        if che_do == "Hôm nay":

            tu_ngay = hom_nay
            den_ngay = hom_nay

        elif che_do == "7 ngày gần nhất":

            tu_ngay = hom_nay - timedelta(days=6)
            den_ngay = hom_nay

        elif che_do == "Tháng này":

            tu_ngay = hom_nay.replace(day=1)
            den_ngay = hom_nay

        else:

            col1, col2 = st.columns(2)

            with col1:

                tu_ngay = st.date_input(
                    "Từ ngày",
                    value=hom_nay.replace(day=1),
                    format="DD/MM/YYYY"
                )

            with col2:

                den_ngay = st.date_input(
                    "Đến ngày",
                    value=hom_nay,
                    format="DD/MM/YYYY"
                )

        if tu_ngay > den_ngay:

            st.error(
                "⚠️ Ngày bắt đầu không được lớn hơn ngày kết thúc."
            )

            return

    tu_ngay_str = tu_ngay.strftime(
        "%Y-%m-%d"
    )

    den_ngay_str = den_ngay.strftime(
        "%Y-%m-%d"
    )

    st.caption(
        f"📌 Đang thống kê từ "
        f"**{tu_ngay.strftime('%d/%m/%Y')}** "
        f"đến "
        f"**{den_ngay.strftime('%d/%m/%Y')}**"
    )

    # ==========================================================
    # 3. LẤY THỐNG KÊ TỔNG QUAN
    # ==========================================================

    result = (
        ThongKeController.thong_ke_theo_khoang_ngay(
            tu_ngay_str,
            den_ngay_str
        )
    )

    if not result["success"]:

        st.error(
            result["message"]
        )

        return

    data = result["data"]

    # ==========================================================
    # 4. TỔNG QUAN
    # ==========================================================

    hien_thi_tieu_de_section(
        "Tổng quan",
        "📌"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        hien_thi_the(
            "Số ngày",
            data["so_ngay"],
            "📅"
        )

    with col2:

        hien_thi_the(
            "Tổng lượt ăn",
            data["tong_luot_an"],
            "👥"
        )

    with col3:

        hien_thi_the(
            "Tổng tiền",
            f"{data['tong_tien']:,.0f} đ",
            "💰"
        )

    with col4:

        hien_thi_the(
            "Trung bình / lượt",
            f"{data['trung_binh']:,.0f} đ",
            "📌"
        )

    st.markdown("")

    # ==========================================================
    # 5. THỐNG KÊ TỪNG NGÀY
    # ==========================================================

    hien_thi_tieu_de_section(
        "Thống kê từng ngày",
        "📈"
    )

    result_ngay = (
        ThongKeController.thong_ke_tung_ngay(
            tu_ngay_str,
            den_ngay_str
        )
    )

    if not result_ngay["success"]:

        st.error(
            result_ngay["message"]
        )

    else:

        du_lieu_ngay = result_ngay["data"]

        if not du_lieu_ngay:

            st.info(
                "🌷 Chưa có dữ liệu trong khoảng thời gian này."
            )

        else:

            bang_ngay = []

            for row in du_lieu_ngay:

                ngay = row[0]
                so_nguoi = row[1]
                tong_tien = row[2]

                bang_ngay.append({
                    "Ngày": ngay,
                    "Số người ăn": so_nguoi,
                    "Tổng tiền": tong_tien
                })

            st.dataframe(
                bang_ngay,
                width="stretch",
                hide_index=True,
                column_config={
                    "Tổng tiền": st.column_config.NumberColumn(
                        "Tổng tiền",
                        format="%,.0f đ"
                    )
                }
            )

    # ==========================================================
    # 6. BIỂU ĐỒ
    # ==========================================================

    if (
        result_ngay["success"]
        and result_ngay["data"]
    ):

        hien_thi_tieu_de_section(
            "Biểu đồ theo ngày",
            "📊"
        )

        # ------------------------------------------------------
        # BIỂU ĐỒ SỐ NGƯỜI ĂN
        # ------------------------------------------------------

        st.markdown(
            "#### 👥 Số người ăn theo ngày"
        )

        du_lieu_bieu_do = {
            "Ngày": [],
            "Số người ăn": []
        }

        for row in result_ngay["data"]:

            du_lieu_bieu_do["Ngày"].append(
                row[0]
            )

            du_lieu_bieu_do["Số người ăn"].append(
                row[1]
            )

        st.line_chart(
            du_lieu_bieu_do,
            x="Ngày",
            y="Số người ăn"
        )

        # ------------------------------------------------------
        # BIỂU ĐỒ TIỀN
        # ------------------------------------------------------

        st.markdown(
            "#### 💰 Tổng tiền theo ngày"
        )

        du_lieu_tien = {
            "Ngày": [],
            "Tổng tiền": []
        }

        for row in result_ngay["data"]:

            du_lieu_tien["Ngày"].append(
                row[0]
            )

            du_lieu_tien["Tổng tiền"].append(
                row[2]
            )

        st.line_chart(
            du_lieu_tien,
            x="Ngày",
            y="Tổng tiền"
        )

    # ==========================================================
    # 7. THỐNG KÊ THEO NGƯỜI
    # ==========================================================

    hien_thi_tieu_de_section(
        "Thống kê theo người",
        "👩‍🍳"
    )

    result_nguoi = (
        ThongKeController.thong_ke_theo_nguoi(
            tu_ngay_str,
            den_ngay_str
        )
    )

    if not result_nguoi["success"]:

        st.error(
            result_nguoi["message"]
        )

    else:

        du_lieu_nguoi = result_nguoi["data"]

        bang_nguoi = []

        for row in du_lieu_nguoi:

            bang_nguoi.append({
                "Họ tên": row[1],
                "Số lần ăn": row[2],
                "Tổng tiền": row[3]
            })

        if bang_nguoi:

            st.dataframe(
                bang_nguoi,
                width="stretch",
                hide_index=True,
                column_config={
                    "Tổng tiền": st.column_config.NumberColumn(
                        "Tổng tiền",
                        format="%,.0f đ"
                    )
                }
            )

        else:

            st.info(
                "🌷 Chưa có dữ liệu theo người."
            )