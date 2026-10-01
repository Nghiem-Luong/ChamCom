# -*- coding: utf-8 -*-

import calendar
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

from Controllers.nop_tien_controller import NopTienController
from Controllers.nguoi_an_controller import NguoiAnController
from Controllers.bo_phan_controller import BoPhanController
from Utils.nop_tien_excel import xuat_bao_cao_cong_no_excel
from Views.layout import (
    hien_thi_header,
    hien_thi_tieu_de_section,
    hien_thi_the,
    hien_thi_info_card
)


def _money(value):
    try:
        return f"{float(value or 0):,.0f} đ"
    except Exception:
        return "0 đ"


def _safe_float(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def _safe_int(value):
    try:
        return int(float(value or 0))
    except Exception:
        return 0


def _date_value(value):
    if isinstance(value, date):
        return value

    try:
        return date.fromisoformat(str(value)[:10])
    except Exception:
        return None


def _get(row, index, default=None):
    try:
        if isinstance(row, dict):
            values = list(row.values())

            if index < len(values):
                return values[index]

            return default

        return row[index]

    except Exception:
        return default


def _month_range(year, month):
    last_day = calendar.monthrange(
        int(year),
        int(month)
    )[1]

    return (
        date(int(year), int(month), 1),
        date(
            int(year),
            int(month),
            last_day
        )
    )


def _week_range(day):
    day = _date_value(day)

    if not day:
        return None, None

    monday = day - timedelta(
        days=day.weekday()
    )

    sunday = monday + timedelta(days=6)

    return monday, sunday


def _status(balance):
    balance = _safe_float(balance)

    if abs(balance) < 0.01:
        return "Đã đủ"

    if balance < 0:
        return "Còn nợ"

    return "Nộp thừa"


def _status_icon(status):
    if status == "Còn nợ":
        return "🔴"

    if status == "Nộp thừa":
        return "🟢"

    return "🔵"


def _same_id(value1, value2):
    if value1 is None or value2 is None:
        return value1 is None and value2 is None

    return (
        str(value1).strip()
        == str(value2).strip()
    )


def _people():
    try:
        result = NguoiAnController.lay_danh_sach()

        if isinstance(result, dict):
            if not result.get("success", True):
                st.error(
                    result.get(
                        "message",
                        "Không thể tải danh sách người ăn."
                    )
                )
                return []

            return result.get("data", []) or []

        return result or []

    except Exception as error:
        st.error(
            f"Không thể tải danh sách người ăn: {error}"
        )
        return []


def _departments():
    try:
        result = BoPhanController.lay_danh_sach()

        if isinstance(result, dict):
            if not result.get("success", True):
                return []

            return result.get("data", []) or []

        return result or []

    except Exception:
        return []


def _person_info(row):
    if isinstance(row, dict):
        person_id = (
            row.get("id")
            if "id" in row
            else row.get("Id")
        )

        name = (
            row.get("name")
            if "name" in row
            else row.get("HoTen", "")
        )

        department_id = (
            row.get("department_id")
            if "department_id" in row
            else row.get("BoPhanId")
        )

        department_name = (
            row.get("department_name")
            if "department_name" in row
            else row.get("TenBoPhan", "")
        )

        return {
            "id": person_id,
            "name": name or "",
            "department_id": department_id,
            "department_name": department_name or ""
        }

    return {
        "id": _get(row, 0),
        "name": _get(row, 1, ""),
        "department_id": _get(row, 3),
        "department_name": _get(row, 4, "")
    }


def _department_info(row):
    if isinstance(row, dict):
        department_id = (
            row.get("id")
            if "id" in row
            else row.get("Id")
        )

        department_name = (
            row.get("name")
            if "name" in row
            else row.get("TenBoPhan", "")
        )

        return (
            department_id,
            department_name or ""
        )

    return (
        _get(row, 0),
        _get(row, 1, "")
    )


def _filter_people(
    people,
    department_id
):
    if department_id is None:
        return list(people)

    result = []

    for person in people:
        info = _person_info(person)

        if _same_id(
            info["department_id"],
            department_id
        ):
            result.append(person)

    return result


def _summary_people(
    people,
    tu_ngay,
    den_ngay
):
    data = []

    total_due = 0
    total_paid = 0

    for person in people:
        info = _person_info(person)

        if info["id"] is None:
            continue

        try:
            result = (
                NopTienController
                .tinh_cong_no_luy_ke(
                    nguoi_an_id=info["id"],
                    tu_ngay=tu_ngay,
                    den_ngay=den_ngay
                )
            )
        except Exception:
            continue

        if not isinstance(result, dict):
            continue

        if not result.get("success"):
            continue

        opening = _safe_float(
            result.get(
                "opening_balance",
                0
            )
        )

        due = _safe_float(
            result.get(
                "period_due",
                0
            )
        )

        paid = _safe_float(
            result.get(
                "period_paid",
                0
            )
        )

        closing = _safe_float(
            result.get(
                "closing_balance",
                0
            )
        )

        status = result.get(
            "status",
            _status(closing)
        )

        data.append(
            {
                "id": info["id"],
                "name": info["name"],
                "department_id": info["department_id"],
                "department_name": info["department_name"],
                "opening": opening,
                "due": due,
                "paid": paid,
                "closing": closing,
                "status": status
            }
        )

        total_due += due
        total_paid += paid

    return (
        data,
        total_due,
        total_paid
    )


def _summary_people_all(
    people
):
    data = []

    total_due = 0
    total_paid = 0

    for person in people:
        info = _person_info(person)

        if info["id"] is None:
            continue

        try:
            result = (
                NopTienController
                .tinh_so_du(
                    info["id"]
                )
            )
        except Exception:
            continue

        if not isinstance(result, dict):
            continue

        if not result.get("success"):
            continue

        due = _safe_float(
            result.get(
                "tong_phai_tra",
                0
            )
        )

        paid = _safe_float(
            result.get(
                "tong_da_nop",
                0
            )
        )

        balance = _safe_float(
            result.get(
                "data",
                0
            )
        )

        data.append(
            {
                "id": info["id"],
                "name": info["name"],
                "department_id": info["department_id"],
                "department_name": info["department_name"],
                "opening": 0,
                "due": due,
                "paid": paid,
                "closing": balance,
                "status": _status(balance)
            }
        )

        total_due += due
        total_paid += paid

    return (
        data,
        total_due,
        total_paid
    )


def _xuat_excel(
    people,
    tu_ngay,
    den_ngay
):
    if tu_ngay and den_ngay:
        from_date = tu_ngay.isoformat()
        to_date = den_ngay.isoformat()

        ky_bao_cao = (
            f"{tu_ngay.strftime('%d/%m/%Y')} - "
            f"{den_ngay.strftime('%d/%m/%Y')}"
        )
    else:
        from_date = None
        to_date = None
        ky_bao_cao = "Toàn bộ dữ liệu"

    tong_hop_thang = (
        NopTienController
        .tao_dataframe_tong_hop(
            people,
            from_date,
            to_date
        )
    )

    tong_hop_tuan = pd.DataFrame()

    if tu_ngay and den_ngay:
        tong_hop_tuan = (
            NopTienController
            .tao_dataframe_tong_hop_tuan(
                people,
                from_date,
                to_date
            )
        )

    chi_tiet_ca_nhan = (
        NopTienController
        .tao_dataframe_chi_tiet_ca_nhan(
            people,
            from_date,
            to_date
        )
    )

    chi_tiet_tien_com = (
        NopTienController
        .tao_dataframe_chi_tiet_tien_com(
            people,
            from_date,
            to_date
        )
    )

    lich_su_nop_tien = (
        NopTienController
        .tao_dataframe_lich_su_nop_tien(
            people,
            from_date,
            to_date
        )
    )

    van_de_phat_sinh = (
        NopTienController
        .tao_dataframe_van_de(
            people,
            from_date,
            to_date
        )
    )

    extra_df = (
        NopTienController
        .tao_dataframe_suat_an_phat_sinh(
            from_date,
            to_date
        )
    )

    if (
        isinstance(extra_df, pd.DataFrame)
        and not extra_df.empty
    ):
        extra_rows = pd.DataFrame(
            {
                "Người ID": "",
                "Người": extra_df["Họ tên"],
                "Bộ phận": extra_df["Đơn vị"],
                "Ngày": extra_df["Ngày ăn"],
                "Đã ăn": "Phát sinh",
                "Số tiền": extra_df["Số tiền"],
                "Trạng thái": "Suất phát sinh",
                "Ghi chú": extra_df["Ghi chú"]
            }
        )

        if chi_tiet_tien_com is None:
            chi_tiet_tien_com = extra_rows

        elif (
            isinstance(
                chi_tiet_tien_com,
                pd.DataFrame
            )
            and chi_tiet_tien_com.empty
        ):
            chi_tiet_tien_com = extra_rows

        else:
            chi_tiet_tien_com = pd.concat(
                [
                    chi_tiet_tien_com,
                    extra_rows
                ],
                ignore_index=True
            )

    if tu_ngay and den_ngay:
        file_name = (
            "BaoCao_CongNo_"
            f"{tu_ngay.strftime('%Y%m%d')}_"
            f"{den_ngay.strftime('%Y%m%d')}.xlsx"
        )
    else:
        file_name = (
            "BaoCao_CongNo_ToanBo_"
            f"{date.today().strftime('%Y%m%d')}.xlsx"
        )

    return xuat_bao_cao_cong_no_excel(
        tong_hop_thang=tong_hop_thang,
        tong_hop_tuan=tong_hop_tuan,
        chi_tiet_ca_nhan=chi_tiet_ca_nhan,
        chi_tiet_tien_com=chi_tiet_tien_com,
        lich_su_nop_tien=lich_su_nop_tien,
        van_de_phat_sinh=van_de_phat_sinh,
        ten_bao_cao=file_name,
        ky_bao_cao=ky_bao_cao
    )


def _hien_thi_tong_quan(
    total_due,
    total_paid,
    total_closing,
    debt_people,
    enough_people,
    overpaid_people
):
    hien_thi_tieu_de_section(
        "Tổng quan công nợ",
        "📊"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        hien_thi_the(
            "Phải trả trong kỳ",
            _money(total_due),
            "💰"
        )

    with col2:
        hien_thi_the(
            "Đã nộp trong kỳ",
            _money(total_paid),
            "💵"
        )

    with col3:
        if total_closing < 0:
            hien_thi_the(
                "Còn nợ cuối kỳ",
                _money(abs(total_closing)),
                "🔴"
            )
        elif total_closing > 0:
            hien_thi_the(
                "Nộp thừa cuối kỳ",
                _money(total_closing),
                "🟢"
            )
        else:
            hien_thi_the(
                "Đã cân bằng",
                "0 đ",
                "🔵"
            )

    with col4:
        hien_thi_the(
            "Người còn nợ",
            f"{debt_people} người",
            "👥"
        )

        st.caption(
            f"{enough_people} đủ · "
            f"{overpaid_people} dư"
        )


def _hien_thi_luy_ke(
    summary_people,
    total_due,
    total_paid,
    total_closing
):
    hien_thi_tieu_de_section(
        "Công nợ lũy kế",
        "📈"
    )

    opening_balance = sum(
        item["opening"]
        for item in summary_people
    )

    opening_debt = max(
        -opening_balance,
        0
    )

    opening_credit = max(
        opening_balance,
        0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        hien_thi_info_card(
            "Nợ đầu kỳ",
            _money(opening_debt)
        )

        if opening_credit > 0:
            st.caption(
                f"Dư đầu kỳ: "
                f"{_money(opening_credit)}"
            )

    with col2:
        hien_thi_info_card(
            "Phải trả",
            _money(total_due)
        )

    with col3:
        hien_thi_info_card(
            "Đã nộp",
            _money(total_paid)
        )

    with col4:
        if total_closing < 0:
            hien_thi_info_card(
                "Nợ cuối kỳ",
                _money(abs(total_closing))
            )
        elif total_closing > 0:
            hien_thi_info_card(
                "Dư cuối kỳ",
                _money(total_closing)
            )
        else:
            hien_thi_info_card(
                "Cân bằng",
                "0 đ"
            )


def _hien_thi_tong_hop_tuan(
    people,
    tu_ngay,
    den_ngay
):
    hien_thi_tieu_de_section(
        "Tổng hợp theo tuần",
        "📅"
    )

    week_df = (
        NopTienController
        .tao_dataframe_tong_hop_tuan(
            people,
            tu_ngay.isoformat(),
            den_ngay.isoformat()
        )
    )

    if (
        week_df is None
        or week_df.empty
    ):
        st.info(
            "Không có dữ liệu theo tuần."
        )
        return

    config = {}

    for column in [
        "Nợ đầu kỳ",
        "Phải trả",
        "Đã nộp",
        "Còn nợ",
        "Nộp thừa"
    ]:
        if column in week_df.columns:
            config[column] = (
                st.column_config.NumberColumn(
                    format="%,d đ"
                )
            )

    st.dataframe(
        week_df,
        width="stretch",
        hide_index=True,
        column_config=config
    )


def _hien_thi_form_nop_tien(
    filtered_people,
    today
):
    hien_thi_tieu_de_section(
        "Ghi nhận nộp tiền",
        "💵"
    )

    with st.container(border=True):
        person_options = []

        for person in filtered_people:
            info = _person_info(person)

            label = (
                f"{info['name']} — "
                f"{info['department_name'] or 'Chưa có bộ phận'} "
                f"— ID {info['id']}"
            )

            person_options.append(
                (
                    label,
                    info["id"]
                )
            )

        if not person_options:
            st.info(
                "Không có người để ghi nhận giao dịch."
            )
            return

        col1, col2 = st.columns(
            [2.2, 1]
        )

        with col1:
            selected_person = st.selectbox(
                "Người nộp",
                person_options,
                format_func=lambda x: x[0],
                key="payment_person_new"
            )

        with col2:
            payment_date = st.date_input(
                "Ngày nộp",
                value=today,
                key="payment_date_new"
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            payment_amount = st.number_input(
                "Số tiền",
                min_value=0,
                value=0,
                step=10000,
                key="payment_amount_new"
            )

        with col2:
            payment_method = st.selectbox(
                "Hình thức",
                [
                    "Tiền mặt",
                    "Chuyển khoản"
                ],
                key="payment_method_new"
            )

        with col3:
            payment_note = st.text_input(
                "Ghi chú",
                placeholder="Ví dụ: Nộp tiền cơm tháng 09",
                key="payment_note_new"
            )

        if st.button(
            "💾 Lưu giao dịch",
            type="primary",
            width="stretch",
            key="payment_save_new"
        ):
            if payment_amount <= 0:
                st.error(
                    "Số tiền phải lớn hơn 0."
                )
                return

            result = (
                NopTienController
                .them_giao_dich(
                    nguoi_an_id=selected_person[1],
                    ngay_nop=payment_date.isoformat(),
                    so_tien=payment_amount,
                    hinh_thuc=payment_method,
                    ghi_chu=(
                        payment_note.strip()
                        or None
                    )
                )
            )

            if result.get("success"):
                st.success(
                    result.get(
                        "message",
                        "Đã lưu giao dịch."
                    )
                )
                st.rerun()
            else:
                st.error(
                    result.get(
                        "message",
                        "Không thể lưu giao dịch."
                    )
                )


def _hien_thi_bang_cong_no(
    summary_people,
    filter_type,
    tu_ngay,
    den_ngay,
    today
):
    hien_thi_tieu_de_section(
        "Công nợ từng người",
        "👥"
    )

    col1, col2, col3 = st.columns(
        [1.6, 1, 1]
    )

    with col1:
        search = st.text_input(
            "Tìm kiếm",
            placeholder="Tên hoặc ID người ăn...",
            key="finance_search"
        )

    with col2:
        status_filter = st.selectbox(
            "Trạng thái",
            [
                "Tất cả",
                "Còn nợ",
                "Đã đủ",
                "Nộp thừa"
            ],
            key="finance_status_filter"
        )

    with col3:
        sort_type = st.selectbox(
            "Sắp xếp",
            [
                "Nợ nhiều nhất",
                "Tên A → Z",
                "Phải trả nhiều nhất",
                "Đã nộp nhiều nhất"
            ],
            key="finance_sort"
        )

    display = []

    search_lower = search.strip().lower()

    for item in summary_people:
        if search_lower:
            text = (
                f"{item['name']} "
                f"{item['id']}"
            ).lower()

            if search_lower not in text:
                continue

        if (
            status_filter != "Tất cả"
            and item["status"] != status_filter
        ):
            continue

        display.append(item)

    if sort_type == "Nợ nhiều nhất":
        display.sort(
            key=lambda x: max(
                -x["closing"],
                0
            ),
            reverse=True
        )

    elif sort_type == "Tên A → Z":
        display.sort(
            key=lambda x: str(
                x["name"] or ""
            ).lower()
        )

    elif sort_type == "Phải trả nhiều nhất":
        display.sort(
            key=lambda x: x["due"],
            reverse=True
        )

    elif sort_type == "Đã nộp nhiều nhất":
        display.sort(
            key=lambda x: x["paid"],
            reverse=True
        )

    st.caption(
        f"Hiển thị {len(display)} người."
    )

    if not display:
        st.info(
            "Không có người phù hợp với bộ lọc."
        )
        return

    rows = []

    for item in display:
        closing = item["closing"]

        rows.append(
            {
                "ID": item["id"],
                "Người": item["name"],
                "Bộ phận": (
                    item["department_name"]
                    or "Chưa có bộ phận"
                ),
                "Nợ đầu kỳ": (
                    abs(item["opening"])
                    if item["opening"] < 0
                    else 0
                ),
                "Phải trả": item["due"],
                "Đã nộp": item["paid"],
                "Còn nợ": (
                    abs(closing)
                    if closing < 0
                    else 0
                ),
                "Nộp thừa": (
                    closing
                    if closing > 0
                    else 0
                ),
                "Trạng thái": (
                    f"{_status_icon(item['status'])} "
                    f"{item['status']}"
                )
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn(
                format="%d"
            ),
            "Nợ đầu kỳ": st.column_config.NumberColumn(
                format="%,d đ"
            ),
            "Phải trả": st.column_config.NumberColumn(
                format="%,d đ"
            ),
            "Đã nộp": st.column_config.NumberColumn(
                format="%,d đ"
            ),
            "Còn nợ": st.column_config.NumberColumn(
                format="%,d đ"
            ),
            "Nộp thừa": st.column_config.NumberColumn(
                format="%,d đ"
            )
        }
    )

    st.markdown("")

    person_options = []

    for item in display:
        person_options.append(
            (
                f"{_status_icon(item['status'])} "
                f"{item['name']} "
                f"— ID {item['id']}",
                item
            )
        )

    selected = st.selectbox(
        "Chọn người để xem chi tiết",
        person_options,
        format_func=lambda x: x[0],
        key="finance_person_detail"
    )

    if selected:
        _hien_thi_chi_tiet_nguoi(
            selected[1],
            filter_type,
            tu_ngay,
            den_ngay,
            today
        )


def _hien_thi_chi_tiet_nguoi(
    item,
    filter_type,
    tu_ngay,
    den_ngay,
    today
):
    hien_thi_tieu_de_section(
        f"Chi tiết {item['name']} #{item['id']}",
        "🔎"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        hien_thi_info_card(
            "Nợ đầu kỳ",
            (
                _money(abs(item["opening"]))
                if item["opening"] < 0
                else "0 đ"
            )
        )

    with col2:
        hien_thi_info_card(
            "Phải trả",
            _money(item["due"])
        )

    with col3:
        hien_thi_info_card(
            "Đã nộp",
            _money(item["paid"])
        )

    with col4:
        if item["closing"] < 0:
            hien_thi_info_card(
                "Còn nợ",
                _money(abs(item["closing"]))
            )
        elif item["closing"] > 0:
            hien_thi_info_card(
                "Nộp thừa",
                _money(item["closing"])
            )
        else:
            hien_thi_info_card(
                "Trạng thái",
                "Đã đủ"
            )

    st.caption(
        item["department_name"]
        or "Chưa có bộ phận"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "📅 Công nợ tuần",
            "🍚 Tiền cơm",
            "💵 Giao dịch"
        ]
    )

    with tab1:
        if filter_type == "Toàn bộ":
            st.info(
                "Chọn Tháng, Tuần hoặc Khoảng ngày "
                "để xem công nợ theo tuần."
            )
        else:
            weekly = (
                NopTienController
                .tong_hop_theo_tuan(
                    nguoi_an_id=item["id"],
                    tu_ngay=tu_ngay.isoformat(),
                    den_ngay=den_ngay.isoformat()
                )
            )

            weekly_data = (
                weekly.get("data", [])
                if isinstance(weekly, dict)
                else []
            )

            if not weekly_data:
                st.info(
                    "Không có dữ liệu theo tuần."
                )
            else:
                rows = []

                for week in weekly_data:
                    closing = _safe_float(
                        week.get(
                            "closing_balance",
                            0
                        )
                    )

                    rows.append(
                        {
                            "Từ ngày": (
                                week["tu_ngay"].strftime(
                                    "%d/%m/%Y"
                                )
                                if hasattr(
                                    week["tu_ngay"],
                                    "strftime"
                                )
                                else str(
                                    week["tu_ngay"]
                                )
                            ),
                            "Đến ngày": (
                                week["den_ngay"].strftime(
                                    "%d/%m/%Y"
                                )
                                if hasattr(
                                    week["den_ngay"],
                                    "strftime"
                                )
                                else str(
                                    week["den_ngay"]
                                )
                            ),
                            "Nợ đầu kỳ": _safe_float(
                                week.get(
                                    "opening_balance",
                                    0
                                )
                            ),
                            "Phải trả": _safe_float(
                                week.get(
                                    "period_due",
                                    0
                                )
                            ),
                            "Đã nộp": _safe_float(
                                week.get(
                                    "period_paid",
                                    0
                                )
                            ),
                            "Còn nợ": (
                                abs(closing)
                                if closing < 0
                                else 0
                            ),
                            "Nộp thừa": (
                                closing
                                if closing > 0
                                else 0
                            ),
                            "Trạng thái": week.get(
                                "status",
                                _status(closing)
                            )
                        }
                    )

                weekly_df = pd.DataFrame(rows)

                money_columns = [
                    "Nợ đầu kỳ",
                    "Phải trả",
                    "Đã nộp",
                    "Còn nợ",
                    "Nộp thừa"
                ]

                config = {}

                for column in money_columns:
                    config[column] = (
                        st.column_config.NumberColumn(
                            format="%,d đ"
                        )
                    )

                st.dataframe(
                    weekly_df,
                    width="stretch",
                    hide_index=True,
                    column_config=config
                )

    with tab2:
        result = (
            NopTienController
            .lay_chi_tiet_tien_com(
                item["id"],
                (
                    tu_ngay.isoformat()
                    if tu_ngay
                    else None
                ),
                (
                    den_ngay.isoformat()
                    if den_ngay
                    else None
                )
            )
        )

        meal_data = (
            result.get("data", [])
            if isinstance(result, dict)
            else []
        )

        if not meal_data:
            st.info(
                "Chưa có dữ liệu tiền cơm."
            )
        else:
            rows = []

            for row in meal_data:
                rows.append(
                    {
                        "Ngày": _get(
                            row,
                            2,
                            ""
                        ),
                        "Đã ăn": (
                            "Có"
                            if _get(
                                row,
                                4,
                                0
                            )
                            else "Không"
                        ),
                        "Số tiền": _safe_float(
                            _get(
                                row,
                                5,
                                0
                            )
                        ),
                        "Trạng thái": _get(
                            row,
                            8,
                            "Đăng ký"
                        ),
                        "Ghi chú": _get(
                            row,
                            9,
                            ""
                        )
                    }
                )

            meal_df = pd.DataFrame(rows)

            st.dataframe(
                meal_df,
                width="stretch",
                hide_index=True,
                column_config={
                    "Số tiền":
                        st.column_config.NumberColumn(
                            format="%,d đ"
                        )
                }
            )

    with tab3:
        result = (
            NopTienController
            .lay_theo_nguoi(
                item["id"]
            )
        )

        transactions = (
            result.get("data", [])
            if isinstance(result, dict)
            else []
        )

        if not transactions:
            st.info(
                "Chưa có giao dịch."
            )
        else:
            transaction_options = []

            for row in transactions:
                transaction_id = _get(
                    row,
                    0
                )

                payment_date = _get(
                    row,
                    3,
                    ""
                )

                amount = _safe_float(
                    _get(
                        row,
                        4,
                        0
                    )
                )

                method = _get(
                    row,
                    5,
                    ""
                )

                label = (
                    f"#{transaction_id} · "
                    f"{payment_date} · "
                    f"{_money(amount)} · "
                    f"{method}"
                )

                transaction_options.append(
                    (
                        label,
                        transaction_id
                    )
                )

            selected_transaction = st.selectbox(
                "Giao dịch",
                transaction_options,
                format_func=lambda x: x[0],
                key=(
                    f"transaction_select_"
                    f"{item['id']}"
                )
            )

            transaction_id = (
                selected_transaction[1]
            )

            transaction_result = (
                NopTienController
                .tim_theo_id(
                    transaction_id
                )
            )

            transaction = (
                transaction_result.get("data")
                if isinstance(
                    transaction_result,
                    dict
                )
                else None
            )

            if not transaction:
                st.warning(
                    "Không tìm thấy giao dịch."
                )
                return

            transaction_date = (
                _date_value(
                    _get(
                        transaction,
                        5,
                        today
                    )
                )
                or today
            )

            transaction_amount = _safe_int(
                _get(
                    transaction,
                    6,
                    0
                )
            )

            transaction_method = (
                _get(
                    transaction,
                    7,
                    "Tiền mặt"
                )
                or "Tiền mặt"
            )

            transaction_note = (
                _get(
                    transaction,
                    8,
                    ""
                )
                or ""
            )

            col1, col2 = st.columns(2)

            with col1:
                edit_date = st.date_input(
                    "Ngày nộp",
                    value=transaction_date,
                    key=(
                        f"edit_date_"
                        f"{transaction_id}"
                    )
                )

            with col2:
                edit_amount = st.number_input(
                    "Số tiền",
                    min_value=0,
                    value=transaction_amount,
                    step=10000,
                    key=(
                        f"edit_amount_"
                        f"{transaction_id}"
                    )
                )

            edit_method = st.selectbox(
                "Hình thức",
                [
                    "Tiền mặt",
                    "Chuyển khoản"
                ],
                index=(
                    1
                    if transaction_method
                    == "Chuyển khoản"
                    else 0
                ),
                key=(
                    f"edit_method_"
                    f"{transaction_id}"
                )
            )

            edit_note = st.text_input(
                "Ghi chú",
                value=transaction_note,
                key=(
                    f"edit_note_"
                    f"{transaction_id}"
                )
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "💾 Lưu thay đổi",
                    type="primary",
                    width="stretch",
                    key=(
                        f"edit_save_"
                        f"{transaction_id}"
                    )
                ):
                    if edit_amount <= 0:
                        st.error(
                            "Số tiền phải lớn hơn 0."
                        )
                    else:
                        result = (
                            NopTienController
                            .cap_nhat_giao_dich(
                                giao_dich_id=transaction_id,
                                nguoi_an_id=item["id"],
                                ngay_nop=edit_date.isoformat(),
                                so_tien=edit_amount,
                                hinh_thuc=edit_method,
                                ghi_chu=(
                                    edit_note.strip()
                                    or None
                                )
                            )
                        )

                        if result.get("success"):
                            st.success(
                                "Đã cập nhật giao dịch."
                            )
                            st.rerun()
                        else:
                            st.error(
                                result.get(
                                    "message",
                                    "Không thể cập nhật."
                                )
                            )

            with col2:
                if st.button(
                    "🗑️ Xóa giao dịch",
                    width="stretch",
                    key=(
                        f"delete_"
                        f"{transaction_id}"
                    )
                ):
                    result = (
                        NopTienController
                        .xoa(
                            transaction_id
                        )
                    )

                    if result.get("success"):
                        st.success(
                            "Đã xóa giao dịch."
                        )
                        st.rerun()
                    else:
                        st.error(
                            result.get(
                                "message",
                                "Không thể xóa."
                            )
                        )


def _hien_thi_excel(
    filtered_people,
    tu_ngay,
    den_ngay
):
    hien_thi_tieu_de_section(
        "Xuất báo cáo",
        "📑"
    )

    st.caption(
        "Báo cáo gồm công nợ, công nợ tuần, "
        "chi tiết cá nhân, tiền cơm, lịch sử nộp tiền "
        "và các vấn đề cần đối chiếu."
    )

    col1, col2 = st.columns(
        [1, 2]
    )

    with col1:
        export_clicked = st.button(
            "📥 Tạo báo cáo Excel",
            type="primary",
            width="stretch",
            key="finance_export_excel"
        )

    if export_clicked:
        with st.spinner(
            "Đang tổng hợp dữ liệu và tạo Excel..."
        ):
            result = _xuat_excel(
                filtered_people,
                tu_ngay,
                den_ngay
            )

        if (
            isinstance(result, dict)
            and result.get("success")
        ):
            file_path = result.get(
                "file_path"
            )

            if (
                file_path
                and Path(file_path).exists()
            ):
                with open(
                    file_path,
                    "rb"
                ) as file:
                    file_bytes = file.read()

                st.session_state[
                    "finance_excel_bytes"
                ] = file_bytes

                st.session_state[
                    "finance_excel_name"
                ] = Path(file_path).name

                st.success(
                    "Đã tạo báo cáo Excel."
                )
            else:
                st.error(
                    "Đã tạo báo cáo nhưng không tìm thấy file."
                )
        else:
            message = (
                result.get("message")
                if isinstance(
                    result,
                    dict
                )
                else "Không thể xuất báo cáo."
            )

            st.error(message)

    if (
        st.session_state.get(
            "finance_excel_bytes"
        )
        and st.session_state.get(
            "finance_excel_name"
        )
    ):
        with col2:
            st.download_button(
                "⬇️ Tải báo cáo Excel",
                data=st.session_state[
                    "finance_excel_bytes"
                ],
                file_name=st.session_state[
                    "finance_excel_name"
                ],
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                ),
                width="stretch",
                key="finance_download_excel"
            )


def _hien_thi_hinh_thuc_nop(
    tu_ngay,
    den_ngay
):
    with st.expander(
        "💳 Thống kê hình thức nộp tiền",
        expanded=False
    ):
        result = (
            NopTienController
            .tong_tien_theo_hinh_thuc(
                tu_ngay=(
                    tu_ngay.isoformat()
                    if tu_ngay
                    else None
                ),
                den_ngay=(
                    den_ngay.isoformat()
                    if den_ngay
                    else None
                )
            )
        )

        method_data = (
            result.get("data", [])
            if isinstance(result, dict)
            else []
        )

        if not method_data:
            st.info(
                "Chưa có dữ liệu giao dịch."
            )
            return

        rows = []

        for item in method_data:
            if isinstance(item, dict):
                rows.append(
                    {
                        "Hình thức": item.get(
                            "hinh_thuc",
                            item.get(
                                "Hình thức",
                                ""
                            )
                        ),
                        "Số giao dịch": _safe_int(
                            item.get(
                                "so_giao_dich",
                                item.get(
                                    "Số giao dịch",
                                    0
                                )
                            )
                        ),
                        "Tổng tiền": _safe_float(
                            item.get(
                                "tong_tien",
                                item.get(
                                    "Tổng tiền",
                                    0
                                )
                            )
                        )
                    }
                )
            else:
                rows.append(
                    {
                        "Hình thức": _get(
                            item,
                            0,
                            ""
                        ),
                        "Số giao dịch": 0,
                        "Tổng tiền": _safe_float(
                            _get(
                                item,
                                1,
                                0
                            )
                        )
                    }
                )

        df = pd.DataFrame(rows)

        if df.empty:
            st.info(
                "Chưa có dữ liệu giao dịch."
            )
            return

        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "Số giao dịch":
                    st.column_config.NumberColumn(
                        format="%d"
                    ),
                "Tổng tiền":
                    st.column_config.NumberColumn(
                        format="%,d đ"
                    )
            }
        )


def _hien_thi_van_de(
    people,
    tu_ngay,
    den_ngay
):
    issue_df = (
        NopTienController
        .tao_dataframe_van_de(
            people,
            (
                tu_ngay.isoformat()
                if tu_ngay
                else None
            ),
            (
                den_ngay.isoformat()
                if den_ngay
                else None
            )
        )
    )

    if (
        issue_df is None
        or issue_df.empty
    ):
        with st.expander(
            "⚠️ Cần đối chiếu",
            expanded=False
        ):
            st.success(
                "Không có vấn đề cần đối chiếu."
            )
        return

    with st.expander(
        "⚠️ Cần đối chiếu",
        expanded=True
    ):
        config = {}

        if "Số tiền" in issue_df.columns:
            config["Số tiền"] = (
                st.column_config.NumberColumn(
                    format="%,d đ"
                )
            )

        st.dataframe(
            issue_df,
            width="stretch",
            hide_index=True,
            column_config=config
        )


def hien_thi_nop_tien(
    language="vi"
):
    hien_thi_header(
        "💰 Nộp tiền & Công nợ",
        "Quản lý tiền cơm, giao dịch và công nợ theo kỳ."
    )

    people = _people()
    departments = _departments()

    if not people:
        st.info(
            "Chưa có người ăn."
        )
        return

    today = date.today()

    hien_thi_tieu_de_section(
        "Bộ lọc dữ liệu",
        "🔎"
    )

    col1, col2, col3 = st.columns(
        [1, 1.3, 1.3]
    )

    with col1:
        filter_type = st.selectbox(
            "Kỳ xem",
            [
                "Tháng",
                "Tuần",
                "Khoảng ngày",
                "Toàn bộ"
            ],
            key="finance_period_type"
        )

    with col2:
        if filter_type == "Tháng":
            selected_month = st.date_input(
                "Chọn tháng",
                value=today.replace(day=1),
                key="finance_month"
            )

            tu_ngay, den_ngay = _month_range(
                selected_month.year,
                selected_month.month
            )

        elif filter_type == "Tuần":
            selected_day = st.date_input(
                "Chọn ngày trong tuần",
                value=today,
                key="finance_week_day"
            )

            tu_ngay, den_ngay = _week_range(
                selected_day
            )

        elif filter_type == "Khoảng ngày":
            tu_ngay = st.date_input(
                "Từ ngày",
                value=today.replace(day=1),
                key="finance_from"
            )

            den_ngay = st.date_input(
                "Đến ngày",
                value=today,
                key="finance_to"
            )

        else:
            tu_ngay = None
            den_ngay = None

    with col3:
        department_options = [
            (
                "Tất cả bộ phận",
                None
            )
        ]

        for department in departments:
            department_id, department_name = (
                _department_info(department)
            )

            if department_id is None:
                continue

            department_options.append(
                (
                    department_name,
                    department_id
                )
            )

        selected_department = st.selectbox(
            "Bộ phận",
            department_options,
            format_func=lambda x: x[0],
            key="finance_department"
        )

        selected_department_id = (
            selected_department[1]
        )

    if (
        tu_ngay
        and den_ngay
        and tu_ngay > den_ngay
    ):
        st.error(
            "Từ ngày không được lớn hơn đến ngày."
        )
        return

    filtered_people = _filter_people(
        people,
        selected_department_id
    )

    if not filtered_people:
        st.info(
            "Không có người thuộc bộ phận đã chọn."
        )
        return

    if filter_type == "Toàn bộ":
        (
            summary_people,
            total_due,
            total_paid
        ) = _summary_people_all(
            filtered_people
        )
    else:
        (
            summary_people,
            total_due,
            total_paid
        ) = _summary_people(
            filtered_people,
            tu_ngay.isoformat(),
            den_ngay.isoformat()
        )

    extra_total = (
        NopTienController
        .tong_tien_suat_an_phat_sinh(
            (
                tu_ngay.isoformat()
                if tu_ngay
                else None
            ),
            (
                den_ngay.isoformat()
                if den_ngay
                else None
            )
        )
    )

    extra_total = _safe_float(
        extra_total
    )

    total_closing = sum(
        item["closing"]
        for item in summary_people
    )

    debt_people = sum(
        1
        for item in summary_people
        if item["closing"] < 0
    )

    enough_people = sum(
        1
        for item in summary_people
        if abs(item["closing"]) < 0.01
    )

    overpaid_people = sum(
        1
        for item in summary_people
        if item["closing"] > 0
    )

    _hien_thi_tong_quan(
        total_due,
        total_paid,
        total_closing,
        debt_people,
        enough_people,
        overpaid_people
    )

    if extra_total > 0:
        st.info(
            f"🍚 Suất ăn phát sinh trong kỳ: "
            f"**{_money(extra_total)}**. "
            f"Khoản này được theo dõi riêng và không tự "
            f"cộng vào công nợ cá nhân."
        )

    if filter_type != "Toàn bộ":
        _hien_thi_luy_ke(
            summary_people,
            total_due,
            total_paid,
            total_closing
        )

    if filter_type == "Tháng":
        _hien_thi_tong_hop_tuan(
            filtered_people,
            tu_ngay,
            den_ngay
        )

    _hien_thi_form_nop_tien(
        filtered_people,
        today
    )

    _hien_thi_bang_cong_no(
        summary_people,
        filter_type,
        tu_ngay,
        den_ngay,
        today
    )

    _hien_thi_excel(
        filtered_people,
        tu_ngay,
        den_ngay
    )

    _hien_thi_hinh_thuc_nop(
        tu_ngay,
        den_ngay
    )

    _hien_thi_van_de(
        filtered_people,
        tu_ngay,
        den_ngay
    )
