import streamlit as st
from datetime import date

from Controllers.bao_cao_controller import BaoCaoController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section
)


def hien_thi_bao_cao():

    hien_thi_header(
        "📑 Xuất báo cáo",
        "Xem dữ liệu và xuất báo cáo theo khoảng thời gian và người ăn."
    )

    # ==========================================================
    # 1. BỘ LỌC
    # ==========================================================

    hien_thi_tieu_de_section(
        "Bộ lọc báo cáo",
        "🔎"
    )

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            tu_ngay = st.date_input(
                "📅 Từ ngày",
                value=date.today().replace(day=1),
                format="DD/MM/YYYY"
            )

        with col2:
            den_ngay = st.date_input(
                "📅 Đến ngày",
                value=date.today(),
                format="DD/MM/YYYY"
            )

        ten_nguoi = st.text_input(
            "👤 Tìm theo tên",
            placeholder="Nhập tên người ăn cần tìm..."
        )

    if tu_ngay > den_ngay:

        st.error(
            "⚠️ Ngày bắt đầu không được lớn hơn ngày kết thúc."
        )

        return

    tu_ngay_str = tu_ngay.strftime("%Y-%m-%d")
    den_ngay_str = den_ngay.strftime("%Y-%m-%d")

    st.caption(
        f"📌 Khoảng thời gian: "
        f"**{tu_ngay.strftime('%d/%m/%Y')}** "
        f"→ "
        f"**{den_ngay.strftime('%d/%m/%Y')}**"
    )

    if ten_nguoi.strip():

        st.info(
            f"🔎 Đang lọc báo cáo của: "
            f"**{ten_nguoi.strip()}**"
        )

    # ==========================================================
    # 2. LẤY DỮ LIỆU
    # ==========================================================

    result = BaoCaoController.lay_du_lieu_bao_cao(
        tu_ngay_str,
        den_ngay_str,
        ten_nguoi
    )

    if not result["success"]:

        st.error(result["message"])

        return

    du_lieu = result["data"]

    # ==========================================================
    # 3. TỔNG QUAN
    # ==========================================================

    tong_ban_ghi = len(du_lieu)

    tong_tien = sum(
        (row[4] or 0)
        for row in du_lieu
        if row[3] == 1
    )

    so_luot_an = sum(
        1
        for row in du_lieu
        if row[3] == 1
    )

    hien_thi_tieu_de_section(
        "Tổng quan báo cáo",
        "📊"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        hien_thi_the(
            "Tổng bản ghi",
            tong_ban_ghi,
            "📋"
        )

    with col2:
        hien_thi_the(
            "Tổng lượt ăn",
            so_luot_an,
            "👥"
        )

    with col3:
        hien_thi_the(
            "Tổng tiền",
            f"{tong_tien:,.0f} đ",
            "💰"
        )

    st.markdown("")

    # ==========================================================
    # 4. DỮ LIỆU
    # ==========================================================

    hien_thi_tieu_de_section(
        "Dữ liệu báo cáo",
        "📋"
    )

    if du_lieu:

        bang_du_lieu = []

        for row in du_lieu:

            ngay = row[0]
            ho_ten = row[1]
            sdt = row[2] or ""
            da_an = row[3]
            so_tien = row[4] or 0
            ghi_chu = row[5] or ""

            try:

                ngay_hien_thi = (
                    f"{ngay[8:10]}/"
                    f"{ngay[5:7]}/"
                    f"{ngay[0:4]}"
                )

            except Exception:

                ngay_hien_thi = ngay

            bang_du_lieu.append({
                "Ngày": ngay_hien_thi,
                "Họ tên": ho_ten,
                "SĐT": sdt,
                "Đã ăn": (
                    "Có"
                    if da_an == 1
                    else "Không"
                ),
                "Số tiền phải trả": so_tien,
                "Ghi chú": ghi_chu
            })

        st.caption(
            f"Hiển thị {len(bang_du_lieu)} bản ghi."
        )

        st.dataframe(
            bang_du_lieu,
            width="stretch",
            hide_index=True,
            column_config={
                "Số tiền phải trả": st.column_config.NumberColumn(
                    "Số tiền phải trả",
                    format="%,.0f đ"
                )
            }
        )

    else:

        st.info(
            "🌷 Không có dữ liệu phù hợp với "
            "khoảng thời gian và tên đã chọn."
        )

    # ==========================================================
    # 5. XUẤT BÁO CÁO
    # ==========================================================

    hien_thi_tieu_de_section(
        "Xuất dữ liệu",
        "📤"
    )

    st.caption(
        "Tạo file báo cáo rồi tải file về máy."
    )

    # ==========================================================
    # 5.1. EXCEL
    # ==========================================================

    hien_thi_tieu_de_section(
        "Báo cáo Excel",
        "📊"
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        if st.button(
            "📊 Tạo file Excel",
            type="primary",
            width="stretch",
            key="tao_excel_bao_cao"
        ):

            file_path_excel = (
                f"BaoCao_"
                f"{tu_ngay_str}_"
                f"{den_ngay_str}.xlsx"
            )

            result_excel = BaoCaoController.xuat_excel(
                tu_ngay_str,
                den_ngay_str,
                file_path_excel,
                ten_nguoi
            )

            if result_excel["success"]:

                st.session_state["bao_cao_excel_path"] = (
                    result_excel["file_path"]
                )

                st.session_state["bao_cao_excel_name"] = (
                    file_path_excel
                )

                st.success(
                    "✅ Đã tạo file Excel."
                )

            else:

                st.error(
                    result_excel["message"]
                )

    with col2:

        excel_path = st.session_state.get(
            "bao_cao_excel_path"
        )

        excel_name = st.session_state.get(
            "bao_cao_excel_name",
            "BaoCao.xlsx"
        )

        if excel_path:

            try:

                with open(
                    excel_path,
                    "rb"
                ) as file:

                    excel_data = file.read()

                st.download_button(
                    "⬇️ Tải file Excel",
                    data=excel_data,
                    file_name=excel_name,
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    width="stretch",
                    key="tai_excel_bao_cao"
                )

            except Exception as error:

                st.error(
                    f"Không thể đọc file Excel: {error}"
                )

    st.markdown("")

    # ==========================================================
    # 5.2. CSV
    # ==========================================================

    hien_thi_tieu_de_section(
        "Báo cáo CSV",
        "📄"
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        if st.button(
            "📄 Tạo file CSV",
            width="stretch",
            key="tao_csv_bao_cao"
        ):

            file_path_csv = (
                f"BaoCao_"
                f"{tu_ngay_str}_"
                f"{den_ngay_str}.csv"
            )

            result_csv = BaoCaoController.xuat_csv(
                tu_ngay_str,
                den_ngay_str,
                file_path_csv,
                ten_nguoi
            )

            if result_csv["success"]:

                st.session_state["bao_cao_csv_path"] = (
                    result_csv["file_path"]
                )

                st.session_state["bao_cao_csv_name"] = (
                    file_path_csv
                )

                st.success(
                    "✅ Đã tạo file CSV."
                )

            else:

                st.error(
                    result_csv["message"]
                )

    with col2:

        csv_path = st.session_state.get(
            "bao_cao_csv_path"
        )

        csv_name = st.session_state.get(
            "bao_cao_csv_name",
            "BaoCao.csv"
        )

        if csv_path:

            try:

                with open(
                    csv_path,
                    "rb"
                ) as file:

                    csv_data = file.read()

                st.download_button(
                    "⬇️ Tải file CSV",
                    data=csv_data,
                    file_name=csv_name,
                    mime="text/csv",
                    width="stretch",
                    key="tai_csv_bao_cao"
                )

            except Exception as error:

                st.error(
                    f"Không thể đọc file CSV: {error}"
                )