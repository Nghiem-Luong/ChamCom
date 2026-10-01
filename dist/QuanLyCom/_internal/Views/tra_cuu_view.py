# -*- coding: utf-8 -*-

from datetime import date, timedelta

import streamlit as st

from Controllers.tra_cuu_controller import TraCuuController


# ==========================================================
# HÀM TIỆN ÍCH
# ==========================================================

def _money(value):

    try:
        return f"{float(value or 0):,.0f} đ"

    except (TypeError, ValueError):

        return "0 đ"


def _number(value):

    try:
        return f"{int(value or 0):,}"

    except (TypeError, ValueError):

        return "0"


def _float_number(value):

    try:
        return f"{float(value or 0):,.0f}"

    except (TypeError, ValueError):

        return "0"


def _lay_khoang_thoi_gian():

    """
    Lấy khoảng thời gian người dùng đang chọn.

    Tất cả câu hỏi tra cứu đều sử dụng khoảng thời gian này.
    """

    lua_chon = st.session_state.get(
        "tra_cuu_thoi_gian",
        "Hôm nay"
    )

    hom_nay = date.today()

    # ------------------------------------------------------
    # HÔM NAY
    # ------------------------------------------------------

    if lua_chon == "Hôm nay":

        return (
            hom_nay,
            hom_nay
        )

    # ------------------------------------------------------
    # HÔM QUA
    # ------------------------------------------------------

    if lua_chon == "Hôm qua":

        ngay = (
            hom_nay -
            timedelta(days=1)
        )

        return (
            ngay,
            ngay
        )

    # ------------------------------------------------------
    # 7 NGÀY GẦN ĐÂY
    # ------------------------------------------------------

    if lua_chon == "7 ngày gần đây":

        return (
            hom_nay -
            timedelta(days=6),
            hom_nay
        )

    # ------------------------------------------------------
    # THÁNG NÀY
    # ------------------------------------------------------

    if lua_chon == "Tháng này":

        return (
            date(
                hom_nay.year,
                hom_nay.month,
                1
            ),
            hom_nay
        )

    # ------------------------------------------------------
    # KHOẢNG THỜI GIAN TỰ CHỌN
    # ------------------------------------------------------

    tu_ngay = st.session_state.get(
        "tra_cuu_tu_ngay",
        hom_nay
    )

    den_ngay = st.session_state.get(
        "tra_cuu_den_ngay",
        hom_nay
    )

    return (
        tu_ngay,
        den_ngay
    )


# ==========================================================
# FORMAT BẢNG
# ==========================================================

def _tao_column_config(data):

    """
    Tự động nhận diện một số cột tiền / số
    để định dạng đẹp trên dataframe.
    """

    if not data:

        return {}

    if not isinstance(data, list):

        return {}

    if not isinstance(data[0], dict):

        return {}

    column_config = {}

    # ------------------------------------------------------
    # CỘT TIỀN
    # ------------------------------------------------------

    money_columns = [
        "Tiền ăn",
        "Tổng tiền",
        "Tổng tiền ăn",
        "Đã nộp",
        "Đã thu",
        "Phải trả",
        "Tổng phải trả",
        "Còn nợ",
        "Công nợ",
        "Dư",
        "Tiền phải trả",
        "Số tiền",
        "Tổng đã nộp",
        "Tổng công nợ",
        "Số tiền nợ",
        "Tiền nợ",
        "Chênh lệch"
    ]

    # ------------------------------------------------------
    # CỘT SỐ
    # ------------------------------------------------------

    number_columns = [
        "Số người",
        "Số suất",
        "Tổng suất",
        "Số lần ăn",
        "Số lần",
        "Số giao dịch",
        "Số ngày",
        "Số lần trùng"
    ]

    for column in money_columns:

        if column in data[0]:

            column_config[column] = (
                st.column_config.NumberColumn(
                    column,
                    format="%,d đ"
                )
            )

    for column in number_columns:

        if column in data[0]:

            column_config[column] = (
                st.column_config.NumberColumn(
                    column,
                    format="%,d"
                )
            )

    return column_config


# ==========================================================
# HIỂN THỊ DATAFRAME
# ==========================================================

def _hien_thi_dataframe(
    data,
    result_type="table"
):

    if data is None:

        data = []

    if not data:

        st.info(
            "Không có dữ liệu phù hợp với điều kiện tra cứu."
        )

        return

    # ------------------------------------------------------
    # TẠO CONFIG
    # ------------------------------------------------------

    column_config = _tao_column_config(data)

    # ------------------------------------------------------
    # BẢNG
    # ------------------------------------------------------

    st.dataframe(
        data,
        width="stretch",
        hide_index=True,
        column_config=column_config
    )


# ==========================================================
# HIỂN THỊ TÓM TẮT
# ==========================================================

def _hien_thi_summary(result):

    data = result.get(
        "data",
        {}
    )

    if not data:

        return

    if not isinstance(data, dict):

        return

    # ------------------------------------------------------
    # LẤY CÁC GIÁ TRỊ PHỔ BIẾN
    # ------------------------------------------------------

    metrics = []

    money_keys = {
        "tong_tien",
        "tong_tien_an",
        "tong_phai_tra",
        "tong_da_nop",
        "tong_da_thu",
        "tong_cong_no",
        "con_no",
        "du"
    }

    number_keys = {
        "so_nguoi",
        "so_nguoi_an",
        "so_nguoi_no",
        "so_suat",
        "tong_so_suat",
        "so_lan_an",
        "so_giao_dich"
    }

    labels = {
        "so_nguoi": "Số người",
        "so_nguoi_an": "Người đã ăn",
        "so_nguoi_no": "Người đang nợ",
        "so_suat": "Số suất",
        "tong_so_suat": "Tổng suất",
        "so_lan_an": "Số lần ăn",
        "so_giao_dich": "Số giao dịch",
        "tong_tien": "Tổng tiền",
        "tong_tien_an": "Tổng tiền ăn",
        "tong_phai_tra": "Tổng phải trả",
        "tong_da_nop": "Tổng đã nộp",
        "tong_da_thu": "Tổng đã thu",
        "tong_cong_no": "Tổng công nợ",
        "con_no": "Còn nợ",
        "du": "Dư"
    }

    for key, value in data.items():

        if key not in labels:
            continue

        if key in money_keys:

            display_value = _money(value)

        elif key in number_keys:

            display_value = _number(value)

        else:

            display_value = str(value)

        metrics.append(
            (
                labels[key],
                display_value
            )
        )

    # ------------------------------------------------------
    # HIỂN THỊ 4 METRIC / HÀNG
    # ------------------------------------------------------

    if metrics:

        for start in range(
            0,
            len(metrics),
            4
        ):

            current = metrics[
                start:start + 4
            ]

            columns = st.columns(
                len(current)
            )

            for column, item in zip(
                columns,
                current
            ):

                with column:

                    st.metric(
                        item[0],
                        item[1]
                    )


# ==========================================================
# HIỂN THỊ KẾT QUẢ
# ==========================================================

def _hien_thi_ket_qua(result):

    if not result:

        return

    # ======================================================
    # KIỂM TRA THÀNH CÔNG
    # ======================================================

    if not result.get(
        "success",
        False
    ):

        message = result.get(
            "message",
            "Không thể tra cứu."
        )

        if result.get(
            "type"
        ) == "warning":

            st.warning(message)

        else:

            st.error(message)

        return

    # ======================================================
    # THÔNG BÁO
    # ======================================================

    message = result.get(
        "message"
    )

    if message:

        st.success(message)

    result_type = result.get(
        "type",
        "table"
    )

    # ======================================================
    # TÓM TẮT
    # ======================================================

    if result_type in [
        "summary",
        "summary_table"
    ]:

        _hien_thi_summary(
            result
        )

        # Nếu vẫn có bảng chi tiết
        data = result.get(
            "data_table",
            []
        )

        if data:

            st.divider()

            _hien_thi_dataframe(
                data,
                result_type
            )

        return

    # ======================================================
    # SỐ
    # ======================================================

    if result_type == "number":

        value = result.get(
            "value",
            0
        )

        st.metric(
            "Kết quả",
            _number(value)
        )

        return

    # ======================================================
    # TIỀN
    # ======================================================

    if result_type == "money":

        value = result.get(
            "value",
            0
        )

        st.metric(
            "Số tiền",
            _money(value)
        )

        return

    # ======================================================
    # VĂN BẢN
    # ======================================================

    if result_type in [
        "text",
        "message"
    ]:

        value = result.get(
            "value",
            result.get(
                "message",
                ""
            )
        )

        st.info(str(value))

        return

    # ======================================================
    # DANH SÁCH CẢNH BÁO
    # ======================================================

    if result_type == "warning_table":

        data = result.get(
            "data",
            []
        )

        if data:

            st.warning(
                result.get(
                    "warning_message",
                    "Có dữ liệu cần kiểm tra."
                )
            )

            _hien_thi_dataframe(
                data,
                result_type
            )

        else:

            st.success(
                result.get(
                    "empty_message",
                    "Không phát hiện trường hợp bất thường."
                )
            )

        return

    # ======================================================
    # BẢNG CÔNG NỢ
    # ======================================================

    if result_type == "debt_table":

        data = result.get(
            "data",
            []
        )

        if not data:

            st.success(
                "Không có người đang nợ trong khoảng thời gian này."
            )

            return

        # --------------------------------------------------
        # THỐNG KÊ NHANH
        # --------------------------------------------------

        tong_no = 0

        for row in data:

            if not isinstance(row, dict):

                continue

            if "Còn nợ" in row:

                try:

                    tong_no += float(
                        row.get(
                            "Còn nợ",
                            0
                        ) or 0
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            elif "Công nợ" in row:

                try:

                    tong_no += float(
                        row.get(
                            "Công nợ",
                            0
                        ) or 0
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

        st.metric(
            "Tổng công nợ trong bảng",
            _money(tong_no)
        )

        st.dataframe(
            data,
            width="stretch",
            hide_index=True,
            column_config=_tao_column_config(data)
        )

        return

    # ======================================================
    # BẢNG SO SÁNH
    # ======================================================

    if result_type in [
        "comparison_table",
        "compare_table"
    ]:

        data = result.get(
            "data",
            []
        )

        if not data:

            st.info(
                "Không có dữ liệu để so sánh."
            )

            return

        st.markdown(
            "#### 🔎 Đối chiếu dữ liệu"
        )

        _hien_thi_dataframe(
            data,
            result_type
        )

        return

    # ======================================================
    # BẢNG BỘ PHẬN
    # ======================================================

    if result_type == "department_table":

        data = result.get(
            "data",
            []
        )

        if not data:

            st.info(
                "Không có dữ liệu bộ phận trong khoảng thời gian này."
            )

            return

        st.markdown(
            "#### 🏢 Thống kê theo bộ phận"
        )

        _hien_thi_dataframe(
            data,
            result_type
        )

        return

    # ======================================================
    # BẢNG BẤT THƯỜNG
    # ======================================================

    if result_type == "anomaly_table":

        data = result.get(
            "data",
            []
        )

        if not data:

            st.success(
                result.get(
                    "empty_message",
                    "Không phát hiện dữ liệu bất thường."
                )
            )

            return

        st.warning(
            result.get(
                "warning_message",
                "Phát hiện dữ liệu cần kiểm tra."
            )
        )

        _hien_thi_dataframe(
            data,
            result_type
        )

        return

    # ======================================================
    # LỊCH SỬ ĂN
    # ======================================================

    if result_type == "history":

        person_name = result.get(
            "person_name",
            ""
        )

        st.subheader(
            f"📅 Lịch sử ăn — {person_name}"
        )

        data = result.get(
            "data",
            []
        )

        if not data:

            st.info(
                "Người này chưa có dữ liệu ăn trong khoảng thời gian đã chọn."
            )

            return

        _hien_thi_dataframe(
            data,
            result_type
        )

        return

    # ======================================================
    # LỊCH SỬ NỘP TIỀN
    # ======================================================

    if result_type == "payment_history":

        person_name = result.get(
            "person_name",
            ""
        )

        st.subheader(
            f"💳 Lịch sử nộp tiền — {person_name}"
        )

        data = result.get(
            "data",
            []
        )

        if not data:

            st.info(
                "Người này chưa có giao dịch nộp tiền trong khoảng thời gian đã chọn."
            )

            return

        _hien_thi_dataframe(
            data,
            result_type
        )

        return

    # ======================================================
    # BẢNG TIỀN
    # ======================================================

    if result_type == "money_table":

        data = result.get(
            "data",
            []
        )

        if not data:

            st.info(
                "Không có dữ liệu tiền trong khoảng thời gian này."
            )

            return

        _hien_thi_dataframe(
            data,
            result_type
        )

        return

    # ======================================================
    # BẢNG THÔNG THƯỜNG
    # ======================================================

    data = result.get(
        "data",
        []
    )

    if data:

        _hien_thi_dataframe(
            data,
            result_type
        )

    else:

        st.info(
            "Không có dữ liệu phù hợp."
        )


# ==========================================================
# XÓA KẾT QUẢ CŨ KHI ĐỔI CÂU HỎI
# ==========================================================

def _kiem_tra_thay_doi_cau_hoi(
    cau_hoi_id
):

    key = "tra_cuu_cau_hoi_da_chon"

    cau_hoi_cu = st.session_state.get(
        key
    )

    if cau_hoi_cu != cau_hoi_id:

        st.session_state[
            "tra_cuu_result"
        ] = None

        st.session_state[
            "tra_cuu_result_tu_ngay"
        ] = None

        st.session_state[
            "tra_cuu_result_den_ngay"
        ] = None

        st.session_state[
            key
        ] = cau_hoi_id


# ==========================================================
# MÀN HÌNH TRA CỨU
# ==========================================================

def hien_thi_tra_cuu():

    st.title(
        "🆘 Hỗ trợ & Tra cứu dữ liệu"
    )

    st.caption(
        "Tra cứu chấm cơm, người ăn, công nợ, "
        "nộp tiền, bộ phận, lịch sử và các trường hợp "
        "bất thường hoặc cần đối chiếu."
    )

    st.divider()

    # ======================================================
    # NHÓM CÂU HỎI
    # ======================================================

    nhom_cau_hoi = (
        TraCuuController
        .lay_nhom_cau_hoi()
    )

    if not nhom_cau_hoi:

        st.warning(
            "Chưa có câu hỏi tra cứu."
        )

        return

    col1, col2 = st.columns(
        [1, 2]
    )

    # ======================================================
    # CHỌN NHÓM
    # ======================================================

    with col1:

        nhom = st.selectbox(
            "📂 Nhóm tra cứu",
            nhom_cau_hoi,
            key="tra_cuu_nhom"
        )

    # ======================================================
    # LẤY CÂU HỎI
    # ======================================================

    danh_sach_cau_hoi = (
        TraCuuController
        .lay_cau_hoi_theo_nhom(
            nhom
        )
    )

    if not danh_sach_cau_hoi:

        st.warning(
            "Nhóm này chưa có câu hỏi."
        )

        return

    # ======================================================
    # CHỌN CÂU HỎI
    # ======================================================

    with col2:

        cau_hoi_texts = [
            item["text"]
            for item in danh_sach_cau_hoi
        ]

        cau_hoi_text = st.selectbox(
            "❓ Câu hỏi",
            cau_hoi_texts,
            key=f"tra_cuu_question_{nhom}"
        )

    cau_hoi = next(
        (
            item
            for item in danh_sach_cau_hoi
            if item["text"] == cau_hoi_text
        ),
        None
    )

    if not cau_hoi:

        return

    # ======================================================
    # XÓA KẾT QUẢ CŨ
    # ======================================================

    _kiem_tra_thay_doi_cau_hoi(
        cau_hoi["id"]
    )

    st.divider()

    # ======================================================
    # KHOẢNG THỜI GIAN
    # ======================================================

    st.markdown(
        "### 📅 Khoảng thời gian"
    )

    lua_chon_thoi_gian = st.radio(
        "Chọn thời gian",
        [
            "Hôm nay",
            "Hôm qua",
            "7 ngày gần đây",
            "Tháng này",
            "Khoảng thời gian"
        ],
        horizontal=True,
        key="tra_cuu_thoi_gian"
    )

    # ======================================================
    # KHOẢNG TỰ CHỌN
    # ======================================================

    if lua_chon_thoi_gian == "Khoảng thời gian":

        col_date_1, col_date_2 = st.columns(2)

        with col_date_1:

            st.date_input(
                "Từ ngày",
                value=st.session_state.get(
                    "tra_cuu_tu_ngay",
                    date.today()
                ),
                key="tra_cuu_tu_ngay"
            )

        with col_date_2:

            st.date_input(
                "Đến ngày",
                value=st.session_state.get(
                    "tra_cuu_den_ngay",
                    date.today()
                ),
                key="tra_cuu_den_ngay"
            )

    # ======================================================
    # LẤY KHOẢNG
    # ======================================================

    tu_ngay_obj, den_ngay_obj = (
        _lay_khoang_thoi_gian()
    )

    # ======================================================
    # KIỂM TRA NGÀY
    # ======================================================

    if tu_ngay_obj > den_ngay_obj:

        st.error(
            "Ngày bắt đầu không được lớn hơn ngày kết thúc."
        )

        return

    # ======================================================
    # HIỂN THỊ PHẠM VI
    # ======================================================

    st.caption(
        "📌 Đang tra cứu từ "
        f"{tu_ngay_obj.strftime('%d/%m/%Y')}"
        " đến "
        f"{den_ngay_obj.strftime('%d/%m/%Y')}"
    )

    st.divider()

    # ======================================================
    # CHỌN NGƯỜI
    # ======================================================

    danh_sach_nguoi = []

    if cau_hoi.get(
        "need_person",
        False
    ):

        result_people = (
            TraCuuController
            .lay_danh_sach_nguoi()
        )

        if not result_people.get(
            "success",
            False
        ):

            st.error(
                result_people.get(
                    "message",
                    "Không thể lấy danh sách người."
                )
            )

            return

        danh_sach_nguoi = (
            result_people.get(
                "data",
                []
            )
        )

        if not danh_sach_nguoi:

            st.warning(
                "Chưa có người ăn đang hoạt động."
            )

            return

        person_options = []

        for person in danh_sach_nguoi:

            ho_ten = person.get(
                "ho_ten",
                ""
            )

            bo_phan = person.get(
                "bo_phan",
                "Chưa có bộ phận"
            )

            person_id = person.get(
                "id"
            )

            label = (
                f"{ho_ten}"
                f" — "
                f"{bo_phan}"
            )

            person_options.append(
                (
                    label,
                    person_id
                )
            )

        # --------------------------------------------------
        # NHIỀU NGƯỜI
        # --------------------------------------------------

        if cau_hoi.get(
            "multi_person",
            False
        ):

            selected_people = st.multiselect(
                "👥 Chọn người",
                person_options,
                format_func=lambda item: item[0],
                key=f"tra_cuu_people_{cau_hoi['id']}"
            )

        # --------------------------------------------------
        # MỘT NGƯỜI
        # --------------------------------------------------

        else:

            selected_people = []

            selected_person = st.selectbox(
                "👤 Chọn người",
                person_options,
                format_func=lambda item: item[0],
                key=f"tra_cuu_person_{cau_hoi['id']}"
            )

            if selected_person:

                selected_people = [
                    selected_person
                ]

    else:

        selected_people = []

    # ======================================================
    # CHỌN BỘ PHẬN
    # ======================================================

    bo_phan_id = None

    if cau_hoi.get(
        "need_department",
        False
    ):

        result_department = (
            TraCuuController
            .lay_danh_sach_bo_phan()
        )

        if not result_department.get(
            "success",
            False
        ):

            st.error(
                result_department.get(
                    "message",
                    "Không thể lấy danh sách bộ phận."
                )
            )

            return

        danh_sach_bo_phan = (
            result_department.get(
                "data",
                []
            )
        )

        if not danh_sach_bo_phan:

            st.warning(
                "Chưa có bộ phận."
            )

            return

        department_options = [
            (
                item["ten"],
                item["id"]
            )
            for item in danh_sach_bo_phan
        ]

        selected_department = st.selectbox(
            "🏢 Chọn bộ phận",
            department_options,
            format_func=lambda item: item[0],
            key=f"tra_cuu_department_{cau_hoi['id']}"
        )

        if selected_department:

            bo_phan_id = selected_department[1]

    # ======================================================
    # GỢI Ý
    # ======================================================

    if cau_hoi.get(
        "need_person",
        False
    ):

        if cau_hoi.get(
            "multi_person",
            False
        ):

            st.caption(
                "💡 Có thể chọn một hoặc nhiều người. "
                "Gõ tên để tìm nhanh."
            )

        else:

            st.caption(
                "💡 Chọn người cần tra cứu."
            )

    if cau_hoi.get(
        "need_department",
        False
    ):

        st.caption(
            "💡 Chọn bộ phận cần kiểm tra."
        )

    # ======================================================
    # ĐIỀU KIỆN TRA CỨU
    # ======================================================

    co_the_tra_cuu = True

    # ------------------------------------------------------
    # NGƯỜI
    # ------------------------------------------------------

    if cau_hoi.get(
        "need_person",
        False
    ):

        if not selected_people:

            co_the_tra_cuu = False

    # ------------------------------------------------------
    # BỘ PHẬN
    # ------------------------------------------------------

    if cau_hoi.get(
        "need_department",
        False
    ):

        if bo_phan_id is None:

            co_the_tra_cuu = False

    # ------------------------------------------------------
    # NGÀY
    # ------------------------------------------------------

    if tu_ngay_obj > den_ngay_obj:

        co_the_tra_cuu = False

    # ======================================================
    # NÚT TRA CỨU
    # ======================================================

    st.write("")

    if not co_the_tra_cuu:

        st.info(
            "💡 Vui lòng chọn đầy đủ thông tin "
            "trước khi tra cứu."
        )

    if st.button(
        "🔍 Tra cứu",
        type="primary",
        width="stretch",
        disabled=not co_the_tra_cuu,
        key=f"tra_cuu_button_{cau_hoi['id']}"
    ):

        danh_sach_ids = [
            item[1]
            for item in selected_people
        ]

        result = (
            TraCuuController
            .tra_cuu(
                cau_hoi_id=cau_hoi["id"],
                danh_sach_nguoi_ids=danh_sach_ids,
                tu_ngay=(
                    tu_ngay_obj.isoformat()
                    if tu_ngay_obj
                    else None
                ),
                den_ngay=(
                    den_ngay_obj.isoformat()
                    if den_ngay_obj
                    else None
                ),
                bo_phan_id=bo_phan_id
            )
        )

        # --------------------------------------------------
        # LƯU KẾT QUẢ
        # --------------------------------------------------

        st.session_state[
            "tra_cuu_result"
        ] = result

        st.session_state[
            "tra_cuu_result_tu_ngay"
        ] = tu_ngay_obj

        st.session_state[
            "tra_cuu_result_den_ngay"
        ] = den_ngay_obj

        st.session_state[
            "tra_cuu_result_question_id"
        ] = cau_hoi["id"]

    # ======================================================
    # KẾT QUẢ
    # ======================================================

    result = st.session_state.get(
        "tra_cuu_result"
    )

    result_question_id = (
        st.session_state.get(
            "tra_cuu_result_question_id"
        )
    )

    # ------------------------------------------------------
    # CHỈ HIỂN THỊ KẾT QUẢ CỦA CÂU HỎI HIỆN TẠI
    # ------------------------------------------------------

    if (
        result
        and result_question_id == cau_hoi["id"]
    ):

        st.divider()

        st.subheader(
            "📊 Kết quả tra cứu"
        )

        # --------------------------------------------------
        # KHOẢNG THỜI GIAN CỦA KẾT QUẢ
        # --------------------------------------------------

        result_tu_ngay = (
            st.session_state.get(
                "tra_cuu_result_tu_ngay"
            )
        )

        result_den_ngay = (
            st.session_state.get(
                "tra_cuu_result_den_ngay"
            )
        )

        if (
            result_tu_ngay
            and result_den_ngay
        ):

            st.caption(
                "📅 Phạm vi dữ liệu của kết quả: "
                f"{result_tu_ngay.strftime('%d/%m/%Y')}"
                " → "
                f"{result_den_ngay.strftime('%d/%m/%Y')}"
            )

        # --------------------------------------------------
        # HIỂN THỊ
        # --------------------------------------------------

        _hien_thi_ket_qua(
            result
        )