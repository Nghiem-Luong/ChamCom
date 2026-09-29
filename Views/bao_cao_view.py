import streamlit as st
from datetime import date

from Controllers.bao_cao_controller import BaoCaoController
from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section
)


def hien_thi_bao_cao(language="vi"):
    texts = {
        "vi": {
            "header": "📑 Xuất báo cáo",
            "header_desc": "Xem và xuất báo cáo chấm cơm theo khoảng thời gian.",
            "filter": "Bộ lọc báo cáo",
            "from_date": "📅 Từ ngày",
            "to_date": "📅 Đến ngày",
            "search_name": "👤 Tìm theo tên",
            "search_placeholder": "Nhập tên người ăn...",
            "date_error": "⚠️ Ngày bắt đầu không được lớn hơn ngày kết thúc.",
            "period": "📌 Khoảng thời gian",
            "filtering_person": "🔎 Đang lọc người ăn",
            "overview": "Tổng quan báo cáo",
            "total_records": "Tổng bản ghi",
            "total_meals": "Tổng lượt ăn",
            "total_money": "Tổng tiền cơm",
            "data": "Dữ liệu báo cáo",
            "display_records": "Hiển thị {} bản ghi.",
            "date": "Ngày",
            "name": "Họ tên",
            "phone": "SĐT",
            "ate": "Đã ăn",
            "amount_due": "Số tiền phải trả",
            "note": "Ghi chú",
            "yes": "Có",
            "no": "Không",
            "no_data": "🌷 Không có dữ liệu phù hợp.",
            "export": "Xuất dữ liệu",
            "export_desc": "Một file Excel duy nhất sẽ tổng hợp toàn bộ báo cáo thành nhiều sheet.",
            "excel_report": "📊 File Excel tổng hợp",
            "create_excel": "📊 Xuất file Excel tổng hợp",
            "download_excel": "⬇️ Tải file Excel",
            "excel_created": "✅ Đã tạo file Excel tổng hợp.",
            "excel_error": "Không thể đọc file Excel: {}",
            "csv_report": "📄 Báo cáo CSV",
            "csv_desc": "CSV giữ nguyên chức năng xuất dữ liệu chi tiết hiện tại.",
            "create_csv": "📄 Tạo file CSV",
            "download_csv": "⬇️ Tải file CSV",
            "csv_created": "✅ Đã tạo file CSV.",
            "csv_error": "Không thể đọc file CSV: {}",
        },
        "en": {
            "header": "📑 Reports",
            "header_desc": "View and export meal reports by date range.",
            "filter": "Report Filters",
            "from_date": "📅 From date",
            "to_date": "📅 To date",
            "search_name": "👤 Search by name",
            "search_placeholder": "Enter participant name...",
            "date_error": "⚠️ The start date cannot be later than the end date.",
            "period": "📌 Date range",
            "filtering_person": "🔎 Filtering participant",
            "overview": "Report Overview",
            "total_records": "Total records",
            "total_meals": "Total meals",
            "total_money": "Total meal amount",
            "data": "Report Data",
            "display_records": "Showing {} records.",
            "date": "Date",
            "name": "Name",
            "phone": "Phone",
            "ate": "Ate",
            "amount_due": "Amount due",
            "note": "Note",
            "yes": "Yes",
            "no": "No",
            "no_data": "🌷 No matching data.",
            "export": "Export",
            "export_desc": "One Excel file will contain all reports in multiple sheets.",
            "excel_report": "📊 Combined Excel Report",
            "create_excel": "📊 Export Combined Excel",
            "download_excel": "⬇️ Download Excel",
            "excel_created": "✅ Combined Excel file created.",
            "excel_error": "Unable to read Excel file: {}",
            "csv_report": "📄 CSV Report",
            "csv_desc": "CSV keeps the existing detailed export function.",
            "create_csv": "📄 Create CSV",
            "download_csv": "⬇️ Download CSV",
            "csv_created": "✅ CSV file created.",
            "csv_error": "Unable to read CSV file: {}",
        },
        "zh": {
            "header": "📑 导出报告",
            "header_desc": "按时间范围查看和导出用餐报告。",
            "filter": "报告筛选",
            "from_date": "📅 开始日期",
            "to_date": "📅 结束日期",
            "search_name": "👤 按姓名搜索",
            "search_placeholder": "输入姓名...",
            "date_error": "⚠️ 开始日期不能晚于结束日期。",
            "period": "📌 时间范围",
            "filtering_person": "🔎 当前筛选人员",
            "overview": "报告概览",
            "total_records": "记录总数",
            "total_meals": "用餐总次数",
            "total_money": "餐费总额",
            "data": "报告数据",
            "display_records": "显示 {} 条记录。",
            "date": "日期",
            "name": "姓名",
            "phone": "电话",
            "ate": "已用餐",
            "amount_due": "应付金额",
            "note": "备注",
            "yes": "是",
            "no": "否",
            "no_data": "🌷 没有符合条件的数据。",
            "export": "导出数据",
            "export_desc": "一个 Excel 文件包含多个报告工作表。",
            "excel_report": "📊 Excel 综合报告",
            "create_excel": "📊 导出 Excel 综合报告",
            "download_excel": "⬇️ 下载 Excel",
            "excel_created": "✅ Excel 综合报告已创建。",
            "excel_error": "无法读取 Excel 文件：{}",
            "csv_report": "📄 CSV 报告",
            "csv_desc": "CSV 保留现有详细导出功能。",
            "create_csv": "📄 创建 CSV",
            "download_csv": "⬇️ 下载 CSV",
            "csv_created": "✅ CSV 已创建。",
            "csv_error": "无法读取 CSV 文件：{}",
        }
    }

    text = texts.get(language, texts["vi"])

    hien_thi_header(text["header"], text["header_desc"])

    hien_thi_tieu_de_section(text["filter"], "🔎")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            tu_ngay = st.date_input(
                text["from_date"],
                value=date.today().replace(day=1),
                format="DD/MM/YYYY"
            )

        with col2:
            den_ngay = st.date_input(
                text["to_date"],
                value=date.today(),
                format="DD/MM/YYYY"
            )

        ten_nguoi = st.text_input(
            text["search_name"],
            placeholder=text["search_placeholder"]
        )

    if tu_ngay > den_ngay:
        st.error(text["date_error"])
        return

    tu_ngay_str = tu_ngay.strftime("%Y-%m-%d")
    den_ngay_str = den_ngay.strftime("%Y-%m-%d")

    st.caption(
        f"{text['period']}: "
        f"**{tu_ngay.strftime('%d/%m/%Y')}** → "
        f"**{den_ngay.strftime('%d/%m/%Y')}**"
    )

    if ten_nguoi.strip():
        st.info(
            f"{text['filtering_person']}: "
            f"**{ten_nguoi.strip()}**"
        )

    result = BaoCaoController.lay_du_lieu_bao_cao(
        tu_ngay_str,
        den_ngay_str,
        ten_nguoi
    )

    if not result["success"]:
        st.error(result["message"])
        return

    du_lieu = result["data"]

    tong_ban_ghi = len(du_lieu)

    so_luot_an = sum(
        1
        for row in du_lieu
        if row[3] == 1
    )

    tong_tien = sum(
        (row[4] or 0)
        for row in du_lieu
        if row[3] == 1
    )

    hien_thi_tieu_de_section(
        text["overview"],
        "📊"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        hien_thi_the(
            text["total_records"],
            tong_ban_ghi,
            "📋"
        )

    with col2:
        hien_thi_the(
            text["total_meals"],
            so_luot_an,
            "👥"
        )

    with col3:
        hien_thi_the(
            text["total_money"],
            f"{tong_tien:,.0f} đ",
            "💰"
        )

    hien_thi_tieu_de_section(
        text["data"],
        "📋"
    )

    if du_lieu:
        bang_du_lieu = []

        for row in du_lieu:
            bang_du_lieu.append({
                text["date"]: BaoCaoController._format_ngay(row[0]),
                text["name"]: row[1],
                text["phone"]: row[2] or "",
                text["ate"]: (
                    text["yes"]
                    if row[3] == 1
                    else text["no"]
                ),
                text["amount_due"]: row[4] or 0,
                text["note"]: row[5] or ""
            })

        st.caption(
            text["display_records"].format(
                len(bang_du_lieu)
            )
        )

        st.dataframe(
            bang_du_lieu,
            width="stretch",
            hide_index=True,
            column_config={
                text["amount_due"]:
                    st.column_config.NumberColumn(
                        text["amount_due"],
                        format="%,.0f đ"
                    )
            }
        )

    else:
        st.info(text["no_data"])

    hien_thi_tieu_de_section(
        text["export"],
        "📤"
    )

    st.caption(text["export_desc"])

    hien_thi_tieu_de_section(
        text["excel_report"],
        "📊"
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button(
            text["create_excel"],
            type="primary",
            width="stretch",
            key="tao_excel_bao_cao_tong_hop"
        ):
            file_name = (
                f"BaoCao_TongHop_"
                f"{tu_ngay_str}_"
                f"{den_ngay_str}.xlsx"
            )

            result_excel = BaoCaoController.xuat_excel(
                tu_ngay_str,
                den_ngay_str,
                file_name,
                ten_nguoi
            )

            if result_excel["success"]:
                st.session_state["bao_cao_excel_path"] = (
                    result_excel["file_path"]
                )

                st.session_state["bao_cao_excel_name"] = (
                    file_name
                )

                st.success(
                    text["excel_created"]
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
            "BaoCao_TongHop.xlsx"
        )

        if excel_path:
            try:
                with open(
                    excel_path,
                    "rb"
                ) as file:
                    excel_data = file.read()

                st.download_button(
                    text["download_excel"],
                    data=excel_data,
                    file_name=excel_name,
                    mime=(
                        "application/"
                        "vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    width="stretch",
                    key="tai_excel_bao_cao_tong_hop"
                )

            except Exception as error:
                st.error(
                    text["excel_error"].format(error)
                )

    hien_thi_tieu_de_section(
        text["csv_report"],
        "📄"
    )

    st.caption(text["csv_desc"])

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button(
            text["create_csv"],
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
                    text["csv_created"]
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
                    text["download_csv"],
                    data=csv_data,
                    file_name=csv_name,
                    mime="text/csv",
                    width="stretch",
                    key="tai_csv_bao_cao"
                )

            except Exception as error:
                st.error(
                    text["csv_error"].format(error)
                )