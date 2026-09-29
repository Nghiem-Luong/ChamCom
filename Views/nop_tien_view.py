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


def _money(value):
    try:
        return f"{float(value or 0):,.0f} đ"
    except Exception:
        return "0 đ"


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
            return values[index] if index < len(values) else default

        return row[index]
    except Exception:
        return default


def _month_range(year, month):
    last_day = calendar.monthrange(year, month)[1]

    return (
        date(year, month, 1),
        date(year, month, last_day)
    )


def _week_range(day):
    day = _date_value(day)

    if not day:
        return None, None

    monday = day - timedelta(days=day.weekday())
    saturday = monday + timedelta(days=5)

    return monday, saturday

def _weeks_in_month(year, month):
    first_day, last_day = _month_range(year, month)

    first_monday = first_day - timedelta(days=first_day.weekday())
    last_saturday = last_day + timedelta(days=5 - last_day.weekday())

    weeks = []
    current_monday = first_monday

    while current_monday <= last_saturday:
        current_saturday = current_monday + timedelta(days=5)
        weeks.append((current_monday, current_saturday))
        current_monday += timedelta(days=7)

    return weeks


def _status(balance):
    balance = float(balance or 0)

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


def _same_id(value1, value2):
    if value1 is None or value2 is None:
        return value1 is None and value2 is None

    return str(value1).strip() == str(value2).strip()


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

            data = result.get("data", [])
            return data or []

        return result or []

    except Exception as e:
        st.error(
            f"Không thể tải danh sách người ăn: {e}"
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
        "department_id": _get(row, 5),
        "department_name": _get(row, 6, "")
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

        return department_id, department_name or ""

    return (
        _get(row, 0),
        _get(row, 1, "")
    )


def _filter_people(people, department_id):
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
            result = NopTienController.tinh_cong_no_luy_ke(
                nguoi_an_id=info["id"],
                tu_ngay=tu_ngay,
                den_ngay=den_ngay
            )
        except Exception:
            continue

        if not isinstance(result, dict):
            continue

        if not result.get("success"):
            continue

        opening = _safe_float(
            result.get("opening_balance", 0)
        )

        due = _safe_float(
            result.get("period_due", 0)
        )

        paid = _safe_float(
            result.get("period_paid", 0)
        )

        closing = _safe_float(
            result.get("closing_balance", 0)
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

    return data, total_due, total_paid


def _xuat_excel(
    people,
    tu_ngay,
    den_ngay,
    filter_type
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
        NopTienController.tao_dataframe_tong_hop(
            people,
            from_date,
            to_date
        )
    )

    tong_hop_tuan = pd.DataFrame()

    if tu_ngay and den_ngay:
        tong_hop_tuan = (
            NopTienController.tao_dataframe_tong_hop_tuan(
                people,
                from_date,
                to_date
            )
        )

    chi_tiet_ca_nhan = (
        NopTienController.tao_dataframe_chi_tiet_ca_nhan(
            people,
            from_date,
            to_date
        )
    )

    chi_tiet_tien_com = (
        NopTienController.tao_dataframe_chi_tiet_tien_com(
            people,
            from_date,
            to_date
        )
    )

    lich_su_nop_tien = (
        NopTienController.tao_dataframe_lich_su_nop_tien(
            people,
            from_date,
            to_date
        )
    )

    van_de_phat_sinh = (
        NopTienController.tao_dataframe_van_de(
            people,
            from_date,
            to_date
        )
    )

    extra_df = (
        NopTienController.tao_dataframe_suat_an_phat_sinh(
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
                "Người ID": pd.Series(
                    [pd.NA] * len(extra_df),
                    dtype="Int64"
                ),
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
    st.subheader("📊 Tổng quan")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Phải trả trong kỳ",
            _money(total_due)
        )

    with c2:
        st.metric(
            "Đã nộp trong kỳ",
            _money(total_paid)
        )

    with c3:
        if total_closing < 0:
            st.metric(
                "Công nợ cuối kỳ",
                _money(abs(total_closing))
            )
        elif total_closing > 0:
            st.metric(
                "Tiền dư cuối kỳ",
                _money(total_closing)
            )
        else:
            st.metric(
                "Đã cân bằng",
                "0 đ"
            )

    with c4:
        st.metric(
            "Người còn nợ",
            f"{debt_people} người"
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
    st.subheader("📈 Công nợ lũy kế")

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

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Nợ đầu kỳ",
            _money(opening_debt)
        )

        if opening_credit > 0:
            st.caption(
                f"Dư đầu kỳ: {_money(opening_credit)}"
            )

    with c2:
        st.metric(
            "Phải trả",
            _money(total_due)
        )

    with c3:
        st.metric(
            "Đã nộp",
            _money(total_paid)
        )

    with c4:
        if total_closing < 0:
            st.metric(
                "Nợ cuối kỳ",
                _money(abs(total_closing))
            )
        elif total_closing > 0:
            st.metric(
                "Dư cuối kỳ",
                _money(total_closing)
            )
        else:
            st.metric(
                "Cân bằng",
                "0 đ"
            )


def _hien_thi_tong_hop_tuan(
    people,
    tu_ngay,
    den_ngay
):
    st.subheader("📅 Tổng hợp theo tuần")

    week_df = (
        NopTienController.tao_dataframe_tong_hop_tuan(
            people,
            tu_ngay.isoformat(),
            den_ngay.isoformat()
        )
    )

    if week_df is None or week_df.empty:
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


def _hien_thi_chi_tiet_nguoi(
    item,
    filter_type,
    tu_ngay,
    den_ngay,
    today
):
    with st.expander(
        f"Chi tiết — {item['name']} #{item['id']}",
        expanded=False
    ):
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
                    NopTienController.tong_hop_theo_tuan(
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

                    config = {}

                    for column in [
                        "Nợ đầu kỳ",
                        "Phải trả",
                        "Đã nộp",
                        "Còn nợ",
                        "Nộp thừa"
                    ]:
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
                NopTienController.lay_chi_tiet_tien_com(
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
                                4,
                                ""
                            ),
                            "Đã ăn": (
                                "Có"
                                if _get(
                                    row,
                                    5,
                                    0
                                )
                                else "Không"
                            ),
                            "Số tiền": _safe_float(
                                _get(
                                    row,
                                    6,
                                    0
                                )
                            ),
                            "Trạng thái": (
                                "Đã ăn"
                                if _get(
                                    row,
                                    5,
                                    0
                                )
                                else "Đăng ký"
                            ),
                            "Ghi chú": _get(
                                row,
                                7,
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
                NopTienController.lay_theo_nguoi(
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
                options = []

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

                    options.append(
                        (
                            label,
                            transaction_id
                        )
                    )

                selected_transaction = st.selectbox(
                    "Giao dịch",
                    options,
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
                    NopTienController.tim_theo_id(
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

                ec1, ec2 = st.columns(2)

                with ec1:
                    edit_date = st.date_input(
                        "Ngày nộp",
                        value=transaction_date,
                        key=(
                            f"edit_date_"
                            f"{transaction_id}"
                        )
                    )

                with ec2:
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

                ec1, ec2 = st.columns(2)

                with ec1:
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

                with ec2:
                    if st.button(
                        "🗑️ Xóa giao dịch",
                        width="stretch",
                        key=(
                            f"delete_"
                            f"{transaction_id}"
                        )
                    ):
                        result = (
                            NopTienController.xoa(
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


def _hien_thi_form_nop_tien(
    filtered_people,
    today
):
    with st.expander(
        "➕ Ghi nhận giao dịch nộp tiền",
        expanded=False
    ):
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

        selected_person = st.selectbox(
            "Người nộp",
            person_options,
            format_func=lambda x: x[0],
            key="payment_person_new"
        )

        selected_person_id = selected_person[1]

        c1, c2, c3 = st.columns(3)

        with c1:
            payment_date = st.date_input(
                "Ngày nộp",
                value=today,
                key="payment_date_new"
            )

        with c2:
            payment_amount = st.number_input(
                "Số tiền",
                min_value=0,
                value=0,
                step=10000,
                key="payment_amount_new"
            )

        with c3:
            payment_method = st.selectbox(
                "Hình thức",
                [
                    "Tiền mặt",
                    "Chuyển khoản"
                ],
                key="payment_method_new"
            )

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

            result = NopTienController.them_giao_dich(
                nguoi_an_id=selected_person_id,
                ngay_nop=payment_date.isoformat(),
                so_tien=payment_amount,
                hinh_thuc=payment_method,
                ghi_chu=payment_note.strip() or None
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


def _hien_thi_hinh_thuc_nop(
    tu_ngay,
    den_ngay
):
    st.subheader("💳 Hình thức nộp tiền")

    result = NopTienController.tong_tien_theo_hinh_thuc(
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
            method = _get(
                item,
                0,
                ""
            )

            total = _safe_float(
                _get(
                    item,
                    1,
                    0
                )
            )

            rows.append(
                {
                    "Hình thức": method,
                    "Số giao dịch": 0,
                    "Tổng tiền": total
                }
            )

    df = pd.DataFrame(rows)

    if df.empty:
        st.info(
            "Chưa có dữ liệu giao dịch."
        )
        return

    if "Hình thức" in df.columns:
        df["Hình thức"] = df["Hình thức"].fillna("")

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
        NopTienController.tao_dataframe_van_de(
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
        return

    st.subheader("⚠️ Cần đối chiếu")

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
    st.title("💰 Nộp tiền & Công nợ")

    st.caption(
        "Quản lý tiền cơm, giao dịch và công nợ theo kỳ."
    )

    st.divider()

    people = _people()
    departments = _departments()

    if not people:
        st.info(
            "Chưa có người ăn."
        )
        return

    st.subheader("🔎 Bộ lọc")

    c1, c2, c3 = st.columns(
        [1.15, 1.25, 1.4]
    )

    today = date.today()

    with c1:
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

    with c2:
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
                "Chọn ngày",
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

    with c3:
        department_options = [
            (
                "Tất cả bộ phận",
                None
            )
        ]

        for dep in departments:
            department_id, department_name = (
                _department_info(dep)
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
        summary_people = []

        total_due = 0
        total_paid = 0

        for person in filtered_people:
            info = _person_info(person)

            if info["id"] is None:
                continue

            result = NopTienController.tinh_so_du(
                info["id"]
            )

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

            summary_people.append(
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
        NopTienController.tong_tien_suat_an_phat_sinh(
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
            f"Khoản này được theo dõi riêng vì chưa gắn "
            f"với người ăn và không tự cộng vào công nợ cá nhân."
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

    st.subheader("📊 Báo cáo Excel")

    st.caption(
        "Báo cáo gồm tổng hợp công nợ, công nợ theo tuần, "
        "chi tiết cá nhân, tiền cơm, lịch sử nộp tiền "
        "và các vấn đề cần đối chiếu."
    )

    export_col1, export_col2 = st.columns(
        [1, 3]
    )

    with export_col1:
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
                den_ngay,
                filter_type
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
                if isinstance(result, dict)
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
        with export_col2:
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

    _hien_thi_form_nop_tien(
        filtered_people,
        today
    )

    st.subheader("👥 Công nợ từng người")

    fc1, fc2, fc3 = st.columns(
        [1.5, 1, 1]
    )

    with fc1:
        search = st.text_input(
            "Tìm kiếm",
            placeholder="Tên hoặc ID người ăn...",
            key="finance_search"
        )

    with fc2:
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

    with fc3:
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

    for item in display:
        st.markdown(
            f"### {_status_icon(item['status'])} "
            f"{item['name']} #{item['id']}"
        )

        st.caption(
            item["department_name"]
            or "Chưa có bộ phận"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.caption("Nợ đầu kỳ")

            if item["opening"] < 0:
                st.write(
                    _money(
                        abs(item["opening"])
                    )
                )
            elif item["opening"] > 0:
                st.write(
                    "Dư "
                    + _money(item["opening"])
                )
            else:
                st.write("0 đ")

        with c2:
            st.caption("Phải trả")

            st.write(
                _money(item["due"])
            )

        with c3:
            st.caption("Đã nộp")

            st.write(
                _money(item["paid"])
            )

        with c4:
            st.caption("Cuối kỳ")

            if item["closing"] < 0:
                st.write(
                    f"Còn nợ "
                    f"{_money(abs(item['closing']))}"
                )
            elif item["closing"] > 0:
                st.write(
                    f"Dư "
                    f"{_money(item['closing'])}"
                )
            else:
                st.write("Đã đủ")

        _hien_thi_chi_tiet_nguoi(
            item,
            filter_type,
            tu_ngay,
            den_ngay,
            today
        )

        st.divider()

    _hien_thi_hinh_thuc_nop(
        tu_ngay,
        den_ngay
    )

    _hien_thi_van_de(
        filtered_people,
        tu_ngay,
        den_ngay
    )