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
            "header": "📑 Báo cáo & Quyết toán",
            "header_desc": "Theo dõi chấm cơm, thanh toán và công nợ theo từng kỳ.",

            "filter": "Bộ lọc",
            "from_date": "📅 Từ ngày",
            "to_date": "📅 Đến ngày",
            "department": "🏢 Bộ phận",
            "all_department": "Tất cả bộ phận",
            "search_name": "👤 Tìm người ăn",
            "search_placeholder": "Nhập tên cần tìm...",
            "date_error": "⚠️ Ngày bắt đầu không được lớn hơn ngày kết thúc.",

            "overview": "Tổng quan thanh toán",
            "due": "Phải trả",
            "paid": "Đã nộp",
            "debt": "Còn nợ",
            "overpaid": "Nộp thừa",
            "enough": "Đã đủ",
            "people": "người",

            "payment": "Tình trạng công nợ",
            "payment_note": "Đã đủ bao gồm người nộp đúng và người nộp thừa. Nộp thừa được hiển thị riêng để dễ theo dõi.",

            "tab_all": "Tất cả",
            "tab_debt": "Còn nợ",
            "tab_over": "Nộp thừa",
            "tab_enough": "Đã đủ",

            "name": "Họ tên",
            "department_name": "Bộ phận",
            "opening": "Nợ đầu kỳ",
            "period_due": "Phải trả kỳ",
            "period_paid": "Đã nộp kỳ",
            "period_balance": "Số dư kỳ",
            "debt_amount": "Còn nợ",
            "over_amount": "Nộp thừa",
            "closing_balance": "Số dư lũy kế",
            "status": "Trạng thái",

            "no_data": "🌷 Không có dữ liệu phù hợp.",
            "no_debt": "✅ Hiện không có người còn nợ.",
            "no_over": "✅ Hiện không có người nộp thừa.",
            "no_enough": "🌷 Chưa có người đã đủ.",

            "settlement": "Quyết toán",
            "weekly": "📆 Theo tuần",
            "weekly_desc": "Các bộ phận thông thường quyết toán theo tuần, từ Thứ 2 đến Thứ 7.",
            "monthly": "📅 Theo tháng",
            "monthly_desc": "Bộ phận Vệ sinh quyết toán theo tháng.",
            "vs_notice": "🏢 Bộ phận Vệ sinh đang áp dụng quyết toán theo tháng. Dữ liệu tuần vẫn được giữ để theo dõi.",
            "weekly_tracking": "Theo dõi tuần",

            "week": "Tuần",
            "from": "Từ ngày",
            "to": "Đến ngày",
            "week_due": "Phải trả tuần",
            "week_paid": "Đã nộp tuần",
            "week_debt": "Còn nợ tuần",
            "week_over": "Nộp thừa tuần",
            "week_status": "Trạng thái tuần",
            "week_detail": "Chi tiết tuần",

            "month": "Tháng",
            "month_due": "Phải trả tháng",
            "month_paid": "Đã nộp tháng",
            "month_debt": "Còn nợ tháng",
            "month_over": "Nộp thừa tháng",
            "month_status": "Trạng thái tháng",
            "month_detail": "Chi tiết tháng",

            "daily_report": "Chi tiết chấm cơm",
            "records": "bản ghi",
            "date": "Ngày",
            "phone": "SĐT",
            "ate": "Đã ăn",
            "amount_due": "Số tiền phải trả",
            "note": "Ghi chú",
            "yes": "Có",
            "no": "Không",

            "export": "Xuất báo cáo",
            "export_desc": "Xuất dữ liệu theo khoảng thời gian đang chọn.",
            "excel": "📊 Excel",
            "create_excel": "Tạo file Excel",
            "download_excel": "⬇️ Tải Excel",
            "excel_created": "✅ Đã tạo file Excel.",
            "excel_error": "Không thể đọc file Excel: {}",

            "csv": "📄 CSV",
            "create_csv": "Tạo file CSV",
            "download_csv": "⬇️ Tải CSV",
            "csv_created": "✅ Đã tạo file CSV.",
            "csv_error": "Không thể đọc file CSV: {}",

            "total_people": "Tổng người",
            "total_due": "Tổng phải trả",
            "total_paid": "Tổng đã nộp",
            "total_debt": "Tổng còn nợ",
            "total_over": "Tổng nộp thừa",
            "period": "Khoảng thời gian",
            "selected_department": "Bộ phận đang xem",
            "searched_person": "Đang lọc người",

            "settled": "Đã đủ",
            "unsettled": "Còn nợ"
        },

        "en": {
            "header": "📑 Reports & Settlement",
            "header_desc": "Track meals, payments and outstanding balances by period.",

            "filter": "Filters",
            "from_date": "📅 From date",
            "to_date": "📅 To date",
            "department": "🏢 Department",
            "all_department": "All departments",
            "search_name": "👤 Search participant",
            "search_placeholder": "Enter a name...",
            "date_error": "⚠️ The start date cannot be later than the end date.",

            "overview": "Payment Overview",
            "due": "Amount due",
            "paid": "Paid",
            "debt": "Outstanding",
            "overpaid": "Overpaid",
            "enough": "Paid in full",
            "people": "people",

            "payment": "Payment Status",
            "payment_note": "Paid in full includes exact payments and overpayments. Overpaid amounts are shown separately.",

            "tab_all": "All",
            "tab_debt": "Outstanding",
            "tab_over": "Overpaid",
            "tab_enough": "Paid in full",

            "name": "Name",
            "department_name": "Department",
            "opening": "Opening balance",
            "period_due": "Period due",
            "period_paid": "Period paid",
            "period_balance": "Period balance",
            "debt_amount": "Outstanding",
            "over_amount": "Overpaid",
            "closing_balance": "Cumulative balance",
            "status": "Status",

            "no_data": "🌷 No matching data.",
            "no_debt": "✅ No outstanding balances.",
            "no_over": "✅ No overpayments.",
            "no_enough": "🌷 No fully paid participants.",

            "settlement": "Settlement",
            "weekly": "📆 Weekly",
            "weekly_desc": "Regular departments are settled weekly, Monday to Saturday.",
            "monthly": "📅 Monthly",
            "monthly_desc": "The Vệ sinh department is settled monthly.",
            "vs_notice": "🏢 Vệ sinh uses monthly settlement. Weekly figures remain available for tracking.",
            "weekly_tracking": "Weekly tracking",

            "week": "Week",
            "from": "From",
            "to": "To",
            "week_due": "Weekly due",
            "week_paid": "Weekly paid",
            "week_debt": "Weekly outstanding",
            "week_over": "Weekly overpaid",
            "week_status": "Weekly status",
            "week_detail": "Weekly details",

            "month": "Month",
            "month_due": "Monthly due",
            "month_paid": "Monthly paid",
            "month_debt": "Monthly outstanding",
            "month_over": "Monthly overpaid",
            "month_status": "Monthly status",
            "month_detail": "Monthly details",

            "daily_report": "Meal Details",
            "records": "records",
            "date": "Date",
            "phone": "Phone",
            "ate": "Ate",
            "amount_due": "Amount due",
            "note": "Note",
            "yes": "Yes",
            "no": "No",

            "export": "Export Reports",
            "export_desc": "Export data for the selected period.",
            "excel": "📊 Excel",
            "create_excel": "Create Excel",
            "download_excel": "⬇️ Download Excel",
            "excel_created": "✅ Excel file created.",
            "excel_error": "Unable to read Excel file: {}",

            "csv": "📄 CSV",
            "create_csv": "Create CSV",
            "download_csv": "⬇️ Download CSV",
            "csv_created": "✅ CSV file created.",
            "csv_error": "Unable to read CSV file: {}",

            "total_people": "Total people",
            "total_due": "Total due",
            "total_paid": "Total paid",
            "total_debt": "Total outstanding",
            "total_over": "Total overpaid",
            "period": "Date range",
            "selected_department": "Department",
            "searched_person": "Filtering participant",

            "settled": "Paid in full",
            "unsettled": "Outstanding"
        },

        "zh": {
            "header": "📑 报告与结算",
            "header_desc": "按时间查看用餐、付款和欠款情况。",

            "filter": "筛选",
            "from_date": "📅 开始日期",
            "to_date": "📅 结束日期",
            "department": "🏢 部门",
            "all_department": "全部部门",
            "search_name": "👤 搜索人员",
            "search_placeholder": "输入姓名...",
            "date_error": "⚠️ 开始日期不能晚于结束日期。",

            "overview": "付款概览",
            "due": "应付",
            "paid": "已付",
            "debt": "欠款",
            "overpaid": "多付",
            "enough": "已付清",
            "people": "人",

            "payment": "账务状态",
            "payment_note": "已付清包括刚好付清和多付。多付金额单独显示。",

            "tab_all": "全部",
            "tab_debt": "欠款",
            "tab_over": "多付",
            "tab_enough": "已付清",

            "name": "姓名",
            "department_name": "部门",
            "opening": "期初余额",
            "period_due": "期间应付",
            "period_paid": "期间已付",
            "period_balance": "期间余额",
            "debt_amount": "欠款",
            "over_amount": "多付",
            "closing_balance": "累计余额",
            "status": "状态",

            "no_data": "🌷 没有符合条件的数据。",
            "no_debt": "✅ 当前没有欠款人员。",
            "no_over": "✅ 当前没有多付人员。",
            "no_enough": "🌷 暂无已付清人员。",

            "settlement": "结算",
            "weekly": "📆 按周",
            "weekly_desc": "普通部门按周结算，周一至周六。",
            "monthly": "📅 按月",
            "monthly_desc": "Vệ sinh 部门按月结算。",
            "vs_notice": "🏢 Vệ sinh 部门按月结算，同时保留按周数据用于跟踪。",
            "weekly_tracking": "按周跟踪",

            "week": "周",
            "from": "开始",
            "to": "结束",
            "week_due": "本周应付",
            "week_paid": "本周已付",
            "week_debt": "本周欠款",
            "week_over": "本周多付",
            "week_status": "本周状态",
            "week_detail": "本周明细",

            "month": "月份",
            "month_due": "本月应付",
            "month_paid": "本月已付",
            "month_debt": "本月欠款",
            "month_over": "本月多付",
            "month_status": "本月状态",
            "month_detail": "本月明细",

            "daily_report": "用餐明细",
            "records": "条记录",
            "date": "日期",
            "phone": "电话",
            "ate": "已用餐",
            "amount_due": "应付金额",
            "note": "备注",
            "yes": "是",
            "no": "否",

            "export": "导出报告",
            "export_desc": "导出当前时间范围的数据。",
            "excel": "📊 Excel",
            "create_excel": "创建 Excel",
            "download_excel": "⬇️ 下载 Excel",
            "excel_created": "✅ Excel 文件已创建。",
            "excel_error": "无法读取 Excel 文件：{}",

            "csv": "📄 CSV",
            "create_csv": "创建 CSV",
            "download_csv": "⬇️ 下载 CSV",
            "csv_created": "✅ CSV 已创建。",
            "csv_error": "无法读取 CSV 文件：{}",

            "total_people": "总人数",
            "total_due": "应付总额",
            "total_paid": "已付总额",
            "total_debt": "欠款总额",
            "total_over": "多付总额",
            "period": "时间范围",
            "selected_department": "当前部门",
            "searched_person": "当前人员",

            "settled": "已付清",
            "unsettled": "欠款"
        }
    }

    text = texts.get(
        language,
        texts["vi"]
    )

    def trang_thai_ky(balance):
        if balance < -0.01:
            return text["unsettled"]

        return text["settled"]

    def hien_thi_bang_tien(
        rows,
        include_opening=True,
        include_period=True,
        include_debt=True,
        include_over=True,
        include_closing=True
    ):
        if not rows:
            st.info(text["no_data"])
            return

        table = []

        for row in rows:
            item = {
                text["name"]: row["HoTen"],
                text["department_name"]: row["BoPhan"]
            }

            if include_opening:
                item[text["opening"]] = row["NoDauKy"]

            if include_period:
                item[text["period_due"]] = row["PhaiTra"]
                item[text["period_paid"]] = row["DaNop"]
                item[text["period_balance"]] = row["SoDuKy"]

            if include_debt:
                item[text["debt_amount"]] = row["ConNo"]

            if include_over:
                item[text["over_amount"]] = row["NopThua"]

            if include_closing:
                item[text["closing_balance"]] = row[
                    "SoDuCuoiKy"
                ]

            item[text["status"]] = row["TrangThai"]

            table.append(item)

        column_config = {}

        money_columns = [
            text["opening"],
            text["period_due"],
            text["period_paid"],
            text["period_balance"],
            text["debt_amount"],
            text["over_amount"],
            text["closing_balance"]
        ]

        for column in money_columns:
            if column in table[0]:
                column_config[column] = (
                    st.column_config.NumberColumn(
                        column,
                        format="%,.0f đ"
                    )
                )

        st.dataframe(
            table,
            width="stretch",
            hide_index=True,
            column_config=column_config
        )

    def tao_bang_quyet_toan_tuan(items):
        table = []

        for item in items:
            week_rows = item["ChiTiet"]

            if ten_nguoi.strip():
                keyword = (
                    ten_nguoi
                    .strip()
                    .casefold()
                )

                week_rows = [
                    row
                    for row in week_rows
                    if keyword
                    in row["HoTen"].casefold()
                ]

            due = sum(
                row["PhaiTra"]
                for row in week_rows
            )

            paid = sum(
                row["DaNop"]
                for row in week_rows
            )

            debt = sum(
                row["ConNoKy"]
                for row in week_rows
            )

            over = sum(
                row["NopThuaKy"]
                for row in week_rows
            )

            status = (
                text["unsettled"]
                if debt > 0.01
                else text["settled"]
            )

            table.append({
                text["week"]:
                    item["Tuan"],

                text["from"]:
                    item["TuNgay"].strftime(
                        "%d/%m/%Y"
                    ),

                text["to"]:
                    item["DenNgay"].strftime(
                        "%d/%m/%Y"
                    ),

                text["week_due"]:
                    due,

                text["week_paid"]:
                    paid,

                text["week_debt"]:
                    debt,

                text["week_over"]:
                    over,

                text["week_status"]:
                    status
            })

        return table

    def tao_bang_quyet_toan_thang(items):
        table = []

        for item in items:
            month_rows = item["ChiTiet"]

            if ten_nguoi.strip():
                keyword = (
                    ten_nguoi
                    .strip()
                    .casefold()
                )

                month_rows = [
                    row
                    for row in month_rows
                    if keyword
                    in row["HoTen"].casefold()
                ]

            due = sum(
                row["PhaiTra"]
                for row in month_rows
            )

            paid = sum(
                row["DaNop"]
                for row in month_rows
            )

            debt = sum(
                row["ConNoKy"]
                for row in month_rows
            )

            over = sum(
                row["NopThuaKy"]
                for row in month_rows
            )

            status = (
                text["unsettled"]
                if debt > 0.01
                else text["settled"]
            )

            table.append({
                text["month"]:
                    f"{item['Nam']:04d}/{item['Thang']:02d}",

                text["from"]:
                    item["TuNgay"].strftime(
                        "%d/%m/%Y"
                    ),

                text["to"]:
                    item["DenNgay"].strftime(
                        "%d/%m/%Y"
                    ),

                text["month_due"]:
                    due,

                text["month_paid"]:
                    paid,

                text["month_debt"]:
                    debt,

                text["month_over"]:
                    over,

                text["month_status"]:
                    status
            })

        return table

    department_rows = (
        BaoCaoController.lay_bo_phan()
    )

    department_options = [
        (None, text["all_department"])
    ]

    department_options.extend(
        (row[0], row[1])
        for row in department_rows
    )

    department_labels = [
        item[1]
        for item in department_options
    ]

    hien_thi_header(
        text["header"],
        text["header_desc"]
    )

    hien_thi_tieu_de_section(
        text["filter"],
        "🔎"
    )

    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(
            [1.05, 1.05, 1.35, 1.75]
        )

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

        with col3:
            selected_department = st.selectbox(
                text["department"],
                department_labels,
                index=0
            )

        with col4:
            ten_nguoi = st.text_input(
                text["search_name"],
                placeholder=text["search_placeholder"]
            )

    if tu_ngay > den_ngay:
        st.error(
            text["date_error"]
        )
        return

    bo_phan_id = next(
        item_id
        for item_id, item_name in department_options
        if item_name == selected_department
    )

    tu_ngay_str = tu_ngay.strftime(
        "%Y-%m-%d"
    )

    den_ngay_str = den_ngay.strftime(
        "%Y-%m-%d"
    )

    context_cols = st.columns(3)

    with context_cols[0]:
        st.caption(
            f"📌 {text['period']}"
        )
        st.write(
            f"{tu_ngay:%d/%m/%Y} → {den_ngay:%d/%m/%Y}"
        )

    with context_cols[1]:
        st.caption(
            f"🏢 {text['selected_department']}"
        )
        st.write(
            selected_department
        )

    with context_cols[2]:
        st.caption(
            f"👤 {text['searched_person']}"
        )
        st.write(
            ten_nguoi.strip()
            if ten_nguoi.strip()
            else "—"
        )

    daily_result = (
        BaoCaoController
        .lay_du_lieu_bao_cao(
            tu_ngay_str,
            den_ngay_str,
            ten_nguoi
        )
    )

    if not daily_result["success"]:
        st.error(
            daily_result["message"]
        )
        return

    du_lieu = daily_result["data"]

    if bo_phan_id is not None:
        department_people = (
            BaoCaoController
            .lay_danh_sach_nguoi_an(
                bo_phan_id
            )
        )

        department_names = {
            str(row[1])
            .strip()
            .casefold()
            for row in department_people
            if row[1]
        }

        du_lieu = [
            row
            for row in du_lieu
            if str(row[1])
            .strip()
            .casefold()
            in department_names
        ]

    payment_result = (
        BaoCaoController
        .lay_tong_quan_thanh_toan(
            tu_ngay_str,
            den_ngay_str,
            bo_phan_id
        )
    )

    if not payment_result["success"]:
        st.error(
            payment_result["message"]
        )
        return

    payment_rows = payment_result[
        "data"
    ]

    if ten_nguoi.strip():
        keyword = (
            ten_nguoi
            .strip()
            .casefold()
        )

        payment_rows = [
            row
            for row in payment_rows
            if keyword in row["HoTen"].casefold()
        ]

    tong_phai_tra = sum(
        row["PhaiTra"]
        for row in payment_rows
    )

    tong_da_nop = sum(
        row["DaNop"]
        for row in payment_rows
    )

    tong_con_no = sum(
        row["ConNo"]
        for row in payment_rows
    )

    tong_nop_thua = sum(
        row["NopThua"]
        for row in payment_rows
    )

    so_da_du = sum(
        1
        for row in payment_rows
        if row["TrangThai"] == "Đã đủ"
    )

    so_con_no = sum(
        1
        for row in payment_rows
        if row["TrangThai"] == "Còn nợ"
    )

    so_nop_thua = sum(
        1
        for row in payment_rows
        if row["NopThua"] > 0.01
    )

    so_luot_an = sum(
        1
        for row in du_lieu
        if row[3] == 1
    )

    hien_thi_tieu_de_section(
        text["overview"],
        "📊"
    )

    overview_cols = st.columns(5)

    overview_cards = [
        (
            overview_cols[0],
            text["due"],
            f"{tong_phai_tra:,.0f} đ",
            "💳"
        ),
        (
            overview_cols[1],
            text["paid"],
            f"{tong_da_nop:,.0f} đ",
            "💰"
        ),
        (
            overview_cols[2],
            text["debt"],
            f"{tong_con_no:,.0f} đ",
            "🔴"
        ),
        (
            overview_cols[3],
            text["overpaid"],
            f"{tong_nop_thua:,.0f} đ",
            "🟢"
        ),
        (
            overview_cols[4],
            text["enough"],
            f"{so_da_du} {text['people']}",
            "✅"
        )
    ]

    for column, title, value, icon in overview_cards:
        with column:
            hien_thi_the(
                title,
                value,
                icon
            )

    hien_thi_tieu_de_section(
        text["payment"],
        "💰"
    )

    st.caption(
        text["payment_note"]
    )

    all_rows = payment_rows

    debt_rows = [
        row
        for row in payment_rows
        if row["ConNo"] > 0.01
    ]

    over_rows = [
        row
        for row in payment_rows
        if row["NopThua"] > 0.01
    ]

    enough_rows = [
        row
        for row in payment_rows
        if row["TrangThai"] == "Đã đủ"
    ]

    tabs = st.tabs([
        f"📋 {text['tab_all']} ({len(all_rows)})",
        f"🔴 {text['tab_debt']} ({len(debt_rows)})",
        f"🟢 {text['tab_over']} ({len(over_rows)})",
        f"✅ {text['tab_enough']} ({len(enough_rows)})"
    ])

    with tabs[0]:
        if all_rows:
            hien_thi_bang_tien(
                all_rows,
                include_opening=True,
                include_period=True,
                include_debt=True,
                include_over=True,
                include_closing=True
            )
        else:
            st.info(text["no_data"])

    with tabs[1]:
        if debt_rows:
            hien_thi_bang_tien(
                debt_rows,
                include_opening=False,
                include_period=True,
                include_debt=True,
                include_over=False,
                include_closing=True
            )
        else:
            st.success(text["no_debt"])

    with tabs[2]:
        if over_rows:
            hien_thi_bang_tien(
                over_rows,
                include_opening=False,
                include_period=True,
                include_debt=False,
                include_over=True,
                include_closing=True
            )
        else:
            st.success(text["no_over"])

    with tabs[3]:
        if enough_rows:
            hien_thi_bang_tien(
                enough_rows,
                include_opening=False,
                include_period=True,
                include_debt=True,
                include_over=True,
                include_closing=True
            )
        else:
            st.info(text["no_enough"])

    is_ve_sinh = (
        BaoCaoController
        .la_bo_phan_ve_sinh(
            selected_department
        )
    )

    hien_thi_tieu_de_section(
        text["settlement"],
        "📅"
    )

    if is_ve_sinh:
        st.info(
            text["vs_notice"]
        )

        settlement_tabs = st.tabs([
            text["monthly"],
            text["weekly_tracking"]
        ])

        with settlement_tabs[0]:
            st.caption(
                text["monthly_desc"]
            )

            monthly_result = (
                BaoCaoController
                .lay_bao_cao_thang_theo_khoang(
                    tu_ngay_str,
                    den_ngay_str,
                    bo_phan_id
                )
            )

            if not monthly_result["success"]:
                st.error(
                    monthly_result["message"]
                )

            elif not monthly_result["data"]:
                st.info(
                    text["no_data"]
                )

            else:
                monthly_table = (
                    tao_bang_quyet_toan_thang(
                        monthly_result["data"]
                    )
                )

                if monthly_table:
                    st.dataframe(
                        monthly_table,
                        width="stretch",
                        hide_index=True,
                        column_config={
                            text["month_due"]:
                                st.column_config.NumberColumn(
                                    text["month_due"],
                                    format="%,.0f đ"
                                ),
                            text["month_paid"]:
                                st.column_config.NumberColumn(
                                    text["month_paid"],
                                    format="%,.0f đ"
                                ),
                            text["month_debt"]:
                                st.column_config.NumberColumn(
                                    text["month_debt"],
                                    format="%,.0f đ"
                                ),
                            text["month_over"]:
                                st.column_config.NumberColumn(
                                    text["month_over"],
                                    format="%,.0f đ"
                                )
                        }
                    )

                for item in monthly_result["data"]:
                    month_rows = item["ChiTiet"]

                    if ten_nguoi.strip():
                        keyword = (
                            ten_nguoi
                            .strip()
                            .casefold()
                        )

                        month_rows = [
                            row
                            for row in month_rows
                            if keyword
                            in row["HoTen"].casefold()
                        ]

                    if not month_rows:
                        continue

                    due = sum(
                        row["PhaiTra"]
                        for row in month_rows
                    )

                    paid = sum(
                        row["DaNop"]
                        for row in month_rows
                    )

                    debt = sum(
                        row["ConNoKy"]
                        for row in month_rows
                    )

                    over = sum(
                        row["NopThuaKy"]
                        for row in month_rows
                    )

                    status = (
                        text["unsettled"]
                        if debt > 0.01
                        else text["settled"]
                    )

                    with st.expander(
                        f"📅 "
                        f"{item['Nam']:04d}/"
                        f"{item['Thang']:02d}"
                        f"  ·  "
                        f"{status}"
                    ):
                        summary_cols = st.columns(4)

                        with summary_cols[0]:
                            hien_thi_the(
                                text["month_due"],
                                f"{due:,.0f} đ",
                                "💳"
                            )

                        with summary_cols[1]:
                            hien_thi_the(
                                text["month_paid"],
                                f"{paid:,.0f} đ",
                                "💰"
                            )

                        with summary_cols[2]:
                            hien_thi_the(
                                text["month_debt"],
                                f"{debt:,.0f} đ",
                                "🔴"
                            )

                        with summary_cols[3]:
                            hien_thi_the(
                                text["month_over"],
                                f"{over:,.0f} đ",
                                "🟢"
                            )

                        st.caption(
                            text["month_detail"]
                        )

                        hien_thi_bang_tien(
                            month_rows,
                            include_opening=False,
                            include_period=True,
                            include_debt=True,
                            include_over=True,
                            include_closing=False
                        )

        with settlement_tabs[1]:
            st.caption(
                text["weekly_desc"]
            )

            weekly_result = (
                BaoCaoController
                .lay_bao_cao_tuan_theo_khoang(
                    tu_ngay_str,
                    den_ngay_str,
                    bo_phan_id
                )
            )

            if not weekly_result["success"]:
                st.error(
                    weekly_result["message"]
                )

            elif not weekly_result["data"]:
                st.info(
                    text["no_data"]
                )

            else:
                weekly_table = (
                    tao_bang_quyet_toan_tuan(
                        weekly_result["data"]
                    )
                )

                if weekly_table:
                    st.dataframe(
                        weekly_table,
                        width="stretch",
                        hide_index=True,
                        column_config={
                            text["week_due"]:
                                st.column_config.NumberColumn(
                                    text["week_due"],
                                    format="%,.0f đ"
                                ),
                            text["week_paid"]:
                                st.column_config.NumberColumn(
                                    text["week_paid"],
                                    format="%,.0f đ"
                                ),
                            text["week_debt"]:
                                st.column_config.NumberColumn(
                                    text["week_debt"],
                                    format="%,.0f đ"
                                ),
                            text["week_over"]:
                                st.column_config.NumberColumn(
                                    text["week_over"],
                                    format="%,.0f đ"
                                )
                        }
                    )

    else:
        st.caption(
            text["weekly_desc"]
        )

        weekly_result = (
            BaoCaoController
            .lay_bao_cao_tuan_theo_khoang(
                tu_ngay_str,
                den_ngay_str,
                bo_phan_id
            )
        )

        if not weekly_result["success"]:
            st.error(
                weekly_result["message"]
            )

        elif not weekly_result["data"]:
            st.info(
                text["no_data"]
            )

        else:
            weekly_table = (
                tao_bang_quyet_toan_tuan(
                    weekly_result["data"]
                )
            )

            if weekly_table:
                st.dataframe(
                    weekly_table,
                    width="stretch",
                    hide_index=True,
                    column_config={
                        text["week_due"]:
                            st.column_config.NumberColumn(
                                text["week_due"],
                                format="%,.0f đ"
                            ),
                        text["week_paid"]:
                            st.column_config.NumberColumn(
                                text["week_paid"],
                                format="%,.0f đ"
                            ),
                        text["week_debt"]:
                            st.column_config.NumberColumn(
                                text["week_debt"],
                                format="%,.0f đ"
                            ),
                        text["week_over"]:
                            st.column_config.NumberColumn(
                                text["week_over"],
                                format="%,.0f đ"
                            )
                    }
                )

            for item in weekly_result["data"]:
                week_rows = item["ChiTiet"]

                if ten_nguoi.strip():
                    keyword = (
                        ten_nguoi
                        .strip()
                        .casefold()
                    )

                    week_rows = [
                        row
                        for row in week_rows
                        if keyword
                        in row["HoTen"].casefold()
                    ]

                if not week_rows:
                    continue

                due = sum(
                    row["PhaiTra"]
                    for row in week_rows
                )

                paid = sum(
                    row["DaNop"]
                    for row in week_rows
                )

                debt = sum(
                    row["ConNoKy"]
                    for row in week_rows
                )

                over = sum(
                    row["NopThuaKy"]
                    for row in week_rows
                )

                status = (
                    text["unsettled"]
                    if debt > 0.01
                    else text["settled"]
                )

                with st.expander(
                    f"📆 "
                    f"{text['week']} "
                    f"{item['Tuan']:02d}"
                    f"  ·  "
                    f"{item['TuNgay'].strftime('%d/%m/%Y')}"
                    f" - "
                    f"{item['DenNgay'].strftime('%d/%m/%Y')}"
                    f"  ·  "
                    f"{status}"
                ):
                    summary_cols = st.columns(4)

                    with summary_cols[0]:
                        hien_thi_the(
                            text["week_due"],
                            f"{due:,.0f} đ",
                            "💳"
                        )

                    with summary_cols[1]:
                        hien_thi_the(
                            text["week_paid"],
                            f"{paid:,.0f} đ",
                            "💰"
                        )

                    with summary_cols[2]:
                        hien_thi_the(
                            text["week_debt"],
                            f"{debt:,.0f} đ",
                            "🔴"
                        )

                    with summary_cols[3]:
                        hien_thi_the(
                            text["week_over"],
                            f"{over:,.0f} đ",
                            "🟢"
                        )

                    st.caption(
                        text["week_detail"]
                    )

                    hien_thi_bang_tien(
                        week_rows,
                        include_opening=False,
                        include_period=True,
                        include_debt=True,
                        include_over=True,
                        include_closing=False
                    )

    with st.expander(
        f"📋 {text['daily_report']}"
    ):
        st.caption(
            f"{len(du_lieu)} {text['records']}"
        )

        if du_lieu:
            daily_table = [
                {
                    text["date"]:
                        BaoCaoController._format_ngay(
                            row[0]
                        ),

                    text["name"]:
                        row[1],

                    text["phone"]:
                        row[2] or "",

                    text["ate"]:
                        (
                            text["yes"]
                            if row[3] == 1
                            else text["no"]
                        ),

                    text["amount_due"]:
                        row[4] or 0,

                    text["note"]:
                        row[5] or ""
                }
                for row in du_lieu
            ]

            st.dataframe(
                daily_table,
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
            st.info(
                text["no_data"]
            )

    with st.expander(
        f"📤 {text['export']}"
    ):
        st.caption(
            text["export_desc"]
        )

        export_cols = st.columns(2)

        with export_cols[0]:
            hien_thi_tieu_de_section(
                text["excel"],
                "📊"
            )

            if st.button(
                text["create_excel"],
                type="primary",
                width="stretch",
                key="tao_excel_bao_cao_tong_hop"
            ):
                file_name = (
                    "BaoCao_TongHop_"
                    f"{tu_ngay_str}_"
                    f"{den_ngay_str}.xlsx"
                )

                result_excel = (
                    BaoCaoController.xuat_excel(
                        tu_ngay_str,
                        den_ngay_str,
                        file_name,
                        ten_nguoi
                    )
                )

                if result_excel["success"]:
                    st.session_state[
                        "bao_cao_excel_path"
                    ] = result_excel["file_path"]

                    st.session_state[
                        "bao_cao_excel_name"
                    ] = file_name

                    st.success(
                        text["excel_created"]
                    )
                else:
                    st.error(
                        result_excel["message"]
                    )

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
                        text["excel_error"].format(
                            error
                        )
                    )

        with export_cols[1]:
            hien_thi_tieu_de_section(
                text["csv"],
                "📄"
            )

            if st.button(
                text["create_csv"],
                width="stretch",
                key="tao_csv_bao_cao"
            ):
                file_path_csv = (
                    "BaoCao_"
                    f"{tu_ngay_str}_"
                    f"{den_ngay_str}.csv"
                )

                result_csv = (
                    BaoCaoController.xuat_csv(
                        tu_ngay_str,
                        den_ngay_str,
                        file_path_csv,
                        ten_nguoi
                    )
                )

                if result_csv["success"]:
                    st.session_state[
                        "bao_cao_csv_path"
                    ] = result_csv["file_path"]

                    st.session_state[
                        "bao_cao_csv_name"
                    ] = file_path_csv

                    st.success(
                        text["csv_created"]
                    )
                else:
                    st.error(
                        result_csv["message"]
                    )

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
                        text["csv_error"].format(
                            error
                        )
                    )