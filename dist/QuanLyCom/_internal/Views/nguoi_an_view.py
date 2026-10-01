# -*- coding: utf-8 -*-

import math

import pandas as pd
import streamlit as st

from Controllers.nguoi_an_controller import NguoiAnController
from Controllers.bo_phan_controller import BoPhanController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section,
)

from Utils.notification import (
    hien_thi_thong_bao_da_luu,
)


# ==========================================================
# HỖ TRỢ
# ==========================================================

def _tao_dataframe(danh_sach, text):

    rows = []

    for nguoi in danh_sach:

        nguoi_id = nguoi[0]
        ho_ten = nguoi[1]

        sdt = nguoi[2] or text["not_updated"]

        bo_phan = nguoi[4] or text["no_department"]

        dang_hoat_dong = nguoi[5]

        ngay_tao = nguoi[6] or ""

        if dang_hoat_dong == 1:
            trang_thai = text["status_active"]
        else:
            trang_thai = text["status_inactive"]

        rows.append(
            {
                text["col_id"]: nguoi_id,
                text["col_name"]: ho_ten,
                text["col_department"]: bo_phan,
                text["col_phone"]: sdt,
                text["col_status"]: trang_thai,
                text["col_created"]: ngay_tao,
            }
        )

    return pd.DataFrame(rows)


def _lay_nguoi_theo_id(danh_sach, nguoi_id):

    for nguoi in danh_sach:

        if nguoi[0] == nguoi_id:
            return nguoi

    return None


def _lay_danh_sach_bo_phan():

    try:

        danh_sach = BoPhanController.lay_dang_hoat_dong()

        return danh_sach or []

    except Exception:

        return []


# ==========================================================
# GIAO DIỆN CHÍNH
# ==========================================================

def hien_thi_nguoi_an():

    hien_thi_thong_bao_da_luu()

    # ======================================================
    # NGÔN NGỮ
    # ======================================================

    language = st.session_state.get(
        "language",
        "vi",
    )

    # ======================================================
    # NỘI DUNG
    # ======================================================

    texts = {

        "vi": {

            "header": "👩‍🍳 Quản lý người ăn",

            "header_desc": (
                "Quản lý nhân viên, bộ phận, trạng thái hoạt động "
                "và thông tin người ăn."
            ),

            "overview": "Tổng quan",

            "total": "Tổng số",

            "active": "Đang hoạt động",

            "inactive": "Đã ngừng",

            "department_count": "Số bộ phận",

            "add": "Thêm người ăn",

            "new_person": "👤 Thông tin người ăn mới",

            "basic_info": (
                "Nhập thông tin cơ bản. Họ và tên là bắt buộc."
            ),

            "name": "Họ và tên",

            "name_required": "Họ và tên *",

            "name_placeholder": "Ví dụ: Nguyễn Văn A",

            "phone": "Số điện thoại",

            "phone_placeholder": "Không bắt buộc",

            "department": "Bộ phận",

            "department_placeholder": "Chọn bộ phận...",

            "no_department": "Chưa phân bộ phận",

            "all_departments": "🏢 Tất cả bộ phận",

            "add_button": "✨ Thêm người ăn",

            "enter_name": "Vui lòng nhập họ và tên.",

            "list": "Danh sách người ăn",

            "search": "🔎 Tìm kiếm",

            "search_placeholder": (
                "Nhập tên hoặc số điện thoại..."
            ),

            "status": "Trạng thái",

            "all": "Tất cả",

            "active_status": "Đang hoạt động",

            "inactive_status": "Đã ngừng",

            "page_size": "Số dòng / trang",

            "page": "Trang",

            "of_page": "/",

            "showing": "Đang hiển thị",

            "of": "/",

            "people": "người",

            "not_found": (
                "🌷 Không tìm thấy người ăn phù hợp."
            ),

            "col_id": "ID",

            "col_name": "Họ tên",

            "col_department": "Bộ phận",

            "col_phone": "Số điện thoại",

            "col_status": "Trạng thái",

            "col_created": "Ngày tạo",

            "not_updated": "Chưa cập nhật",

            "selected": "Người đang chọn",

            "select_person": "Chọn người ăn",

            "select_placeholder": "Chọn một người...",

            "person_id": "ID người ăn",

            "current_status": "Trạng thái hiện tại",

            "current_department": "Bộ phận hiện tại",

            "actions": "Thao tác",

            "edit": "✏️ Chỉnh sửa",

            "stop": "⏸️ Ngừng hoạt động",

            "activate": "🔄 Kích hoạt lại",

            "edit_info": "✏️ Chỉnh sửa thông tin",

            "save": "💾 Lưu thay đổi",

            "cancel": "Hủy",

            "confirm_stop": (
                "Bạn có chắc muốn ngừng người ăn này?"
            ),

            "confirm_activate": (
                "Bạn có muốn kích hoạt lại người ăn này?"
            ),

            "load_error": (
                "Không thể tải danh sách người ăn."
            ),

            "operation_error": (
                "Không thể thực hiện thao tác."
            ),

            "empty_name": (
                "Họ và tên không được để trống."
            ),

            "status_active": "🟢 Đang hoạt động",

            "status_inactive": "⚪ Đã ngừng",

            "no_selection": (
                "Vui lòng chọn một người ăn trước."
            ),

            "department_load_error": (
                "Không thể tải danh sách bộ phận."
            ),

            "no_department_available": (
                "Chưa có bộ phận. Bạn có thể thêm người ăn "
                "trước và phân bộ phận sau."
            ),

            "department_filter": "Lọc theo bộ phận",

            "all_department": "Tất cả",

        },

        "en": {

            "header": "👩‍🍳 Meal Participants",

            "header_desc": (
                "Manage employees, departments, activity status "
                "and meal information."
            ),

            "overview": "Overview",

            "total": "Total",

            "active": "Active",

            "inactive": "Inactive",

            "department_count": "Departments",

            "add": "Add participant",

            "new_person": "👤 New participant information",

            "basic_info": (
                "Enter basic information. Name is required."
            ),

            "name": "Name",

            "name_required": "Name *",

            "name_placeholder": "Example: John Smith",

            "phone": "Phone number",

            "phone_placeholder": "Optional",

            "department": "Department",

            "department_placeholder": "Select department...",

            "no_department": "No department",

            "all_departments": "🏢 All departments",

            "add_button": "✨ Add participant",

            "enter_name": "Please enter a name.",

            "list": "Participant list",

            "search": "🔎 Search",

            "search_placeholder": (
                "Enter name or phone number..."
            ),

            "status": "Status",

            "all": "All",

            "active_status": "Active",

            "inactive_status": "Inactive",

            "page_size": "Rows / page",

            "page": "Page",

            "of_page": "/",

            "showing": "Showing",

            "of": "/",

            "people": "people",

            "not_found": (
                "🌷 No matching participant found."
            ),

            "col_id": "ID",

            "col_name": "Name",

            "col_department": "Department",

            "col_phone": "Phone",

            "col_status": "Status",

            "col_created": "Created",

            "not_updated": "Not updated",

            "selected": "Selected participant",

            "select_person": "Select participant",

            "select_placeholder": (
                "Select a participant..."
            ),

            "person_id": "Participant ID",

            "current_status": "Current status",

            "current_department": "Current department",

            "actions": "Actions",

            "edit": "✏️ Edit",

            "stop": "⏸️ Disable",

            "activate": "🔄 Activate",

            "edit_info": "✏️ Edit information",

            "save": "💾 Save changes",

            "cancel": "Cancel",

            "confirm_stop": (
                "Are you sure you want to disable this participant?"
            ),

            "confirm_activate": (
                "Do you want to activate this participant?"
            ),

            "load_error": (
                "Unable to load participants."
            ),

            "operation_error": (
                "Unable to complete the operation."
            ),

            "empty_name": (
                "Name cannot be empty."
            ),

            "status_active": "🟢 Active",

            "status_inactive": "⚪ Inactive",

            "no_selection": (
                "Please select a participant first."
            ),

            "department_load_error": (
                "Unable to load departments."
            ),

            "no_department_available": (
                "No departments available yet. "
                "You can add the participant first "
                "and assign a department later."
            ),

            "department_filter": "Filter by department",

            "all_department": "All",

        },

        "zh": {

            "header": "👩‍🍳 用餐人员管理",

            "header_desc": (
                "管理员工、部门、活动状态和用餐信息。"
            ),

            "overview": "概览",

            "total": "总人数",

            "active": "正在使用",

            "inactive": "已停用",

            "department_count": "部门数量",

            "add": "添加用餐人员",

            "new_person": "👤 新用餐人员信息",

            "basic_info": (
                "请输入基本信息。姓名为必填项。"
            ),

            "name": "姓名",

            "name_required": "姓名 *",

            "name_placeholder": "例如：张三",

            "phone": "电话号码",

            "phone_placeholder": "可选",

            "department": "部门",

            "department_placeholder": "请选择部门...",

            "no_department": "未分配部门",

            "all_departments": "🏢 全部部门",

            "add_button": "✨ 添加人员",

            "enter_name": "请输入姓名。",

            "list": "用餐人员名单",

            "search": "🔎 搜索",

            "search_placeholder": (
                "输入姓名或电话号码..."
            ),

            "status": "状态",

            "all": "全部",

            "active_status": "正在使用",

            "inactive_status": "已停用",

            "page_size": "每页行数",

            "page": "页",

            "of_page": "/",

            "showing": "显示",

            "of": "/",

            "people": "人",

            "not_found": (
                "🌷 没有找到符合条件的人员。"
            ),

            "col_id": "ID",

            "col_name": "姓名",

            "col_department": "部门",

            "col_phone": "电话",

            "col_status": "状态",

            "col_created": "创建时间",

            "not_updated": "未更新",

            "selected": "当前人员",

            "select_person": "选择人员",

            "select_placeholder": "请选择人员...",

            "person_id": "人员ID",

            "current_status": "当前状态",

            "current_department": "当前部门",

            "actions": "操作",

            "edit": "✏️ 编辑",

            "stop": "⏸️ 停用",

            "activate": "🔄 启用",

            "edit_info": "✏️ 编辑信息",

            "save": "💾 保存修改",

            "cancel": "取消",

            "confirm_stop": (
                "确定要停用该人员吗？"
            ),

            "confirm_activate": (
                "要重新启用该人员吗？"
            ),

            "load_error": (
                "无法加载用餐人员名单。"
            ),

            "operation_error": (
                "无法完成操作。"
            ),

            "empty_name": (
                "姓名不能为空。"
            ),

            "status_active": "🟢 正在使用",

            "status_inactive": "⚪ 已停用",

            "no_selection": (
                "请先选择一名用餐人员。"
            ),

            "department_load_error": (
                "无法加载部门列表。"
            ),

            "no_department_available": (
                "暂无部门。可以先添加人员，"
                "之后再分配部门。"
            ),

            "department_filter": "按部门筛选",

            "all_department": "全部",

        },
    }

    text = texts.get(
        language,
        texts["vi"],
    )

    # ======================================================
    # 1. HEADER
    # ======================================================

    hien_thi_header(
        text["header"],
        text["header_desc"],
    )

    # ======================================================
    # 2. LẤY DANH SÁCH NGƯỜI
    # ======================================================

    result = NguoiAnController.lay_danh_sach()

    if not result["success"]:

        st.error(
            result.get(
                "message",
                text["load_error"],
            )
        )

        return

    danh_sach = result.get(
        "data",
        [],
    )

    # ======================================================
    # 3. LẤY DANH SÁCH BỘ PHẬN
    # ======================================================

    try:

        danh_sach_bo_phan = (
            BoPhanController.lay_dang_hoat_dong()
            or []
        )

    except Exception as error:

        danh_sach_bo_phan = []

        st.warning(
            f"{text['department_load_error']} {error}"
        )

    # ======================================================
    # 4. TỔNG QUAN
    # ======================================================

    dang_hoat_dong = [
        nguoi
        for nguoi in danh_sach
        if nguoi[5] == 1
    ]

    da_ngung = [
        nguoi
        for nguoi in danh_sach
        if nguoi[5] == 0
    ]

    hien_thi_tieu_de_section(
        text["overview"],
        "📊",
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        hien_thi_the(
            text["total"],
            len(danh_sach),
            "👥",
        )

    with col2:

        hien_thi_the(
            text["active"],
            len(dang_hoat_dong),
            "🟢",
        )

    with col3:

        hien_thi_the(
            text["inactive"],
            len(da_ngung),
            "⚪",
        )

    with col4:

        hien_thi_the(
            text["department_count"],
            len(danh_sach_bo_phan),
            "🏢",
        )

    # ======================================================
    # 5. THÊM NGƯỜI ĂN
    # ======================================================

    hien_thi_tieu_de_section(
        text["add"],
        "➕",
    )

    with st.expander(
        text["new_person"],
        expanded=False,
    ):

        st.caption(
            text["basic_info"]
        )

        with st.form(
            key="form_them_nguoi_an",
            clear_on_submit=True,
        ):

            col1, col2 = st.columns(2)

            with col1:

                ho_ten = st.text_input(
                    text["name_required"],
                    placeholder=text["name_placeholder"],
                )

            with col2:

                sdt = st.text_input(
                    text["phone"],
                    placeholder=text["phone_placeholder"],
                )

            # ----------------------------------------------
            # BỘ PHẬN
            # ----------------------------------------------

            if danh_sach_bo_phan:

                bo_phan_options = {
                    text["no_department"]: None
                }

                for bo_phan in danh_sach_bo_phan:

                    bo_phan_id = bo_phan[0]
                    ten_bo_phan = bo_phan[1]

                    bo_phan_options[
                        ten_bo_phan
                    ] = bo_phan_id

                bo_phan_label = st.selectbox(
                    text["department"],
                    list(
                        bo_phan_options.keys()
                    ),
                    key="nguoi_an_add_department",
                )

                bo_phan_id_moi = (
                    bo_phan_options[
                        bo_phan_label
                    ]
                )

            else:

                st.info(
                    text["no_department_available"]
                )

                bo_phan_id_moi = None

            them_submit = st.form_submit_button(
                text["add_button"],
                type="primary",
                width="stretch",
            )

        if them_submit:

            if not ho_ten.strip():

                st.warning(
                    text["enter_name"]
                )

            else:

                result = (
                    NguoiAnController
                    .them_nguoi_an(
                        ho_ten=ho_ten.strip(),
                        sdt=sdt.strip() or None,
                        bo_phan_id=bo_phan_id_moi,
                    )
                )

                if result["success"]:

                    st.session_state[
                        "_qlc_pending_notification"
                    ] = {
                        "message": result["message"],
                        "loai": "success",
                    }

                    st.rerun()

                else:

                    st.error(
                        result.get(
                            "message",
                            text["operation_error"],
                        )
                    )

    # ======================================================
    # 6. DANH SÁCH
    # ======================================================

    hien_thi_tieu_de_section(
        text["list"],
        "👥",
    )

    # ======================================================
    # 7. BỘ LỌC
    # ======================================================

    col1, col2, col3, col4 = st.columns(
        [2.2, 1.3, 1.3, 1],
    )

    with col1:

        tu_khoa = st.text_input(
            text["search"],
            placeholder=text["search_placeholder"],
            key="nguoi_an_search",
        )

    with col2:

        trang_thai = st.selectbox(
            text["status"],
            [
                text["all"],
                text["active_status"],
                text["inactive_status"],
            ],
            key="nguoi_an_status_filter",
        )

    with col3:

        bo_phan_filter_options = {
            text["all_department"]: None
        }

        for bo_phan in danh_sach_bo_phan:

            bo_phan_filter_options[
                bo_phan[1]
            ] = bo_phan[0]

        bo_phan_filter_label = st.selectbox(
            text["department_filter"],
            list(
                bo_phan_filter_options.keys()
            ),
            key="nguoi_an_department_filter",
        )

        bo_phan_filter_id = (
            bo_phan_filter_options[
                bo_phan_filter_label
            ]
        )

    with col4:

        so_dong_trang = st.selectbox(
            text["page_size"],
            [10, 20, 50, 100],
            index=1,
            key="nguoi_an_page_size",
        )

    # ======================================================
    # 8. LỌC
    # ======================================================

    danh_sach_hien_thi = danh_sach.copy()

    tu_khoa = tu_khoa.strip().lower()

    if tu_khoa:

        danh_sach_hien_thi = [
            nguoi
            for nguoi in danh_sach_hien_thi
            if (
                tu_khoa in str(
                    nguoi[1]
                ).lower()
                or tu_khoa in str(
                    nguoi[2] or ""
                ).lower()
            )
        ]

    if trang_thai == text["active_status"]:

        danh_sach_hien_thi = [
            nguoi
            for nguoi in danh_sach_hien_thi
            if nguoi[5] == 1
        ]

    elif trang_thai == text["inactive_status"]:

        danh_sach_hien_thi = [
            nguoi
            for nguoi in danh_sach_hien_thi
            if nguoi[5] == 0
        ]

    if bo_phan_filter_id is not None:

        danh_sach_hien_thi = [
            nguoi
            for nguoi in danh_sach_hien_thi
            if nguoi[3] == bo_phan_filter_id
        ]

    # ======================================================
    # 9. PHÂN TRANG
    # ======================================================

    tong_so = len(
        danh_sach_hien_thi
    )

    if tong_so == 0:

        st.info(
            text["not_found"]
        )

        return

    tong_so_trang = max(
        1,
        math.ceil(
            tong_so / so_dong_trang
        ),
    )

    if (
        "nguoi_an_page" not in st.session_state
        or st.session_state[
            "nguoi_an_page"
        ] > tong_so_trang
    ):

        st.session_state[
            "nguoi_an_page"
        ] = 1

    trang_hien_tai = st.session_state[
        "nguoi_an_page"
    ]

    if trang_hien_tai > tong_so_trang:

        trang_hien_tai = tong_so_trang

        st.session_state[
            "nguoi_an_page"
        ] = trang_hien_tai

    bat_dau = (
        trang_hien_tai - 1
    ) * so_dong_trang

    ket_thuc = min(
        bat_dau + so_dong_trang,
        tong_so,
    )

    danh_sach_trang = (
        danh_sach_hien_thi[
            bat_dau:ket_thuc
        ]
    )

    # ======================================================
    # 10. THÔNG TIN KẾT QUẢ
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        st.caption(
            f"{text['showing']} "
            f"{bat_dau + 1}–{ket_thuc} "
            f"{text['of']} "
            f"{tong_so} "
            f"{text['people']}"
        )

    with col2:

        st.caption(
            f"{text['page']} "
            f"{trang_hien_tai} "
            f"{text['of_page']} "
            f"{tong_so_trang}"
        )

    # ======================================================
    # 11. BẢNG
    # ======================================================

    df = _tao_dataframe(
        danh_sach_trang,
        text,
    )

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config={

            text["col_id"]:
                st.column_config.NumberColumn(
                    text["col_id"],
                    width="small",
                ),

            text["col_name"]:
                st.column_config.TextColumn(
                    text["col_name"],
                    width="medium",
                ),

            text["col_department"]:
                st.column_config.TextColumn(
                    text["col_department"],
                    width="medium",
                ),

            text["col_phone"]:
                st.column_config.TextColumn(
                    text["col_phone"],
                    width="medium",
                ),

            text["col_status"]:
                st.column_config.TextColumn(
                    text["col_status"],
                    width="medium",
                ),

            text["col_created"]:
                st.column_config.TextColumn(
                    text["col_created"],
                    width="medium",
                ),
        },
    )

    # ======================================================
    # 12. PHÂN TRANG
    # ======================================================

    if tong_so_trang > 1:

        col1, col2, col3 = st.columns(
            [1, 2, 1],
        )

        with col1:

            if st.button(
                "◀",
                key="nguoi_an_prev_page",
                disabled=(
                    trang_hien_tai <= 1
                ),
                width="stretch",
            ):

                st.session_state[
                    "nguoi_an_page"
                ] = max(
                    1,
                    trang_hien_tai - 1,
                )

                st.rerun()

        with col2:

            st.markdown(
                f"<p style='text-align:center;'>"
                f"{text['page']} {trang_hien_tai} "
                f"{text['of_page']} {tong_so_trang}"
                f"</p>",
                unsafe_allow_html=True,
            )

        with col3:

            if st.button(
                "▶",
                key="nguoi_an_next_page",
                disabled=(
                    trang_hien_tai >= tong_so_trang
                ),
                width="stretch",
            ):

                st.session_state[
                    "nguoi_an_page"
                ] = min(
                    tong_so_trang,
                    trang_hien_tai + 1,
                )

                st.rerun()

    # ======================================================
    # 13. CHỌN NGƯỜI ĐỂ THAO TÁC
    # ======================================================

    hien_thi_tieu_de_section(
        text["actions"],
        "⚙️",
    )

    danh_sach_lua_chon = {}

    for nguoi in danh_sach_hien_thi:

        nguoi_id = nguoi[0]
        ho_ten = nguoi[1]

        trang_thai_icon = (
            "🟢"
            if nguoi[5] == 1
            else "⚪"
        )

        bo_phan = (
            nguoi[4]
            or text["no_department"]
        )

        nhan = (
            f"{trang_thai_icon} "
            f"{ho_ten} "
            f"— {bo_phan} "
            f"(ID: {nguoi_id})"
        )

        danh_sach_lua_chon[
            nhan
        ] = nguoi_id

    lua_chon = st.selectbox(
        text["select_person"],
        list(
            danh_sach_lua_chon.keys()
        ),
        index=None,
        placeholder=text["select_placeholder"],
        key="nguoi_an_selected",
    )

    if lua_chon is None:

        st.caption(
            text["no_selection"]
        )

        return

    nguoi_id_duoc_chon = (
        danh_sach_lua_chon[
            lua_chon
        ]
    )

    nguoi_duoc_chon = (
        _lay_nguoi_theo_id(
            danh_sach,
            nguoi_id_duoc_chon,
        )
    )

    if nguoi_duoc_chon is None:

        st.warning(
            text["no_selection"]
        )

        return

    # ======================================================
    # 14. THÔNG TIN NGƯỜI ĐƯỢC CHỌN
    # ======================================================

    nguoi_id = nguoi_duoc_chon[0]

    ho_ten = nguoi_duoc_chon[1]

    sdt = nguoi_duoc_chon[2] or ""

    bo_phan_id = nguoi_duoc_chon[3]

    ten_bo_phan = (
        nguoi_duoc_chon[4]
        or text["no_department"]
    )

    dang_hoat_dong = nguoi_duoc_chon[5]

    ngay_tao = nguoi_duoc_chon[6] or ""

    with st.container(
        border=True
    ):

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                f"#### 👤 {ho_ten}"
            )

            st.caption(
                f"{text['person_id']}: "
                f"{nguoi_id}"
            )

        with col2:

            st.caption(
                text["phone"]
            )

            st.write(
                sdt
                or text["not_updated"]
            )

        with col3:

            st.caption(
                text["current_department"]
            )

            st.write(
                ten_bo_phan
            )

        st.caption(
            text["current_status"]
        )

        if dang_hoat_dong:

            st.write(
                text["status_active"]
            )

        else:

            st.write(
                text["status_inactive"]
            )

    # ======================================================
    # 15. CÁC NÚT THAO TÁC
    # ======================================================

    if dang_hoat_dong:

        col1, col2 = st.columns(2)

        with col1:

            sua = st.button(
                text["edit"],
                key="nguoi_an_action_edit",
                width="stretch",
            )

        with col2:

            ngung = st.button(
                text["stop"],
                key="nguoi_an_action_stop",
                width="stretch",
            )

        if ngung:

            st.session_state[
                "nguoi_an_confirm_stop"
            ] = True

        if st.session_state.get(
            "nguoi_an_confirm_stop",
            False,
        ):

            st.warning(
                text["confirm_stop"]
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✓ " + text["stop"],
                    key="nguoi_an_confirm_stop_yes",
                    type="primary",
                    width="stretch",
                ):

                    result = (
                        NguoiAnController
                        .ngung_hoat_dong(
                            nguoi_id
                        )
                    )

                    if result["success"]:

                        st.session_state[
                            "nguoi_an_confirm_stop"
                        ] = False

                        st.session_state[
                            "_qlc_pending_notification"
                        ] = {
                            "message": result[
                                "message"
                            ],
                            "loai": "success",
                        }

                        st.rerun()

                    else:

                        st.error(
                            result.get(
                                "message",
                                text["operation_error"],
                            )
                        )

            with col2:

                if st.button(
                    text["cancel"],
                    key="nguoi_an_confirm_stop_no",
                    width="stretch",
                ):

                    st.session_state[
                        "nguoi_an_confirm_stop"
                    ] = False

                    st.rerun()

        # ==================================================
        # FORM SỬA
        # ==================================================

        if st.session_state.get(
            "nguoi_an_edit_mode",
            False,
        ):

            with st.expander(
                text["edit_info"],
                expanded=True,
            ):

                with st.form(
                    key="form_sua_nguoi_an",
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        ten_moi = st.text_input(
                            text["name"],
                            value=ho_ten,
                        )

                    with col2:

                        sdt_moi = st.text_input(
                            text["phone"],
                            value=sdt,
                        )

                    # --------------------------------------
                    # BỘ PHẬN KHI SỬA
                    # --------------------------------------

                    bo_phan_edit_options = {}

                    for bo_phan in danh_sach_bo_phan:

                        bo_phan_edit_options[
                            bo_phan[1]
                        ] = bo_phan[0]

                    ten_bo_phan_hien_tai = (
                        ten_bo_phan
                        if bo_phan_id is not None
                        else text["no_department"]
                    )

                    danh_sach_ten_bo_phan = [
                        text["no_department"]
                    ] + list(
                        bo_phan_edit_options.keys()
                    )

                    if (
                        ten_bo_phan_hien_tai
                        not in danh_sach_ten_bo_phan
                    ):

                        danh_sach_ten_bo_phan.insert(
                            1,
                            ten_bo_phan_hien_tai,
                        )

                    index_bo_phan = (
                        danh_sach_ten_bo_phan.index(
                            ten_bo_phan_hien_tai
                        )
                    )

                    bo_phan_moi_label = st.selectbox(
                        text["department"],
                        danh_sach_ten_bo_phan,
                        index=index_bo_phan,
                        key="nguoi_an_edit_department",
                    )

                    if (
                        bo_phan_moi_label
                        == text["no_department"]
                    ):

                        bo_phan_moi_id = None

                    else:

                        bo_phan_moi_id = (
                            bo_phan_edit_options.get(
                                bo_phan_moi_label
                            )
                        )

                    col_a, col_b = st.columns(2)

                    with col_a:

                        luu = st.form_submit_button(
                            text["save"],
                            type="primary",
                            width="stretch",
                        )

                    with col_b:

                        huy = st.form_submit_button(
                            text["cancel"],
                            width="stretch",
                        )

                if luu:

                    if not ten_moi.strip():

                        st.warning(
                            text["empty_name"]
                        )

                    else:

                        result = (
                            NguoiAnController
                            .cap_nhat(
                                nguoi_an_id=nguoi_id,
                                ho_ten=ten_moi.strip(),
                                sdt=sdt_moi.strip()
                                or None,
                                bo_phan_id=bo_phan_moi_id,
                            )
                        )

                        if result["success"]:

                            st.session_state[
                                "nguoi_an_edit_mode"
                            ] = False

                            st.session_state[
                                "_qlc_pending_notification"
                            ] = {
                                "message": result[
                                    "message"
                                ],
                                "loai": "success",
                            }

                            st.rerun()

                        else:

                            st.error(
                                result.get(
                                    "message",
                                    text["operation_error"],
                                )
                            )

                if huy:

                    st.session_state[
                        "nguoi_an_edit_mode"
                    ] = False

                    st.rerun()

        if sua:

            st.session_state[
                "nguoi_an_edit_mode"
            ] = True

            st.rerun()

    else:

        if st.button(
            text["activate"],
            key="nguoi_an_action_activate",
            type="primary",
            width="stretch",
        ):

            st.session_state[
                "nguoi_an_confirm_activate"
            ] = True

        if st.session_state.get(
            "nguoi_an_confirm_activate",
            False,
        ):

            st.info(
                text["confirm_activate"]
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✓ " + text["activate"],
                    key="nguoi_an_confirm_activate_yes",
                    type="primary",
                    width="stretch",
                ):

                    result = (
                        NguoiAnController
                        .kich_hoat_lai(
                            nguoi_id
                        )
                    )

                    if result["success"]:

                        st.session_state[
                            "nguoi_an_confirm_activate"
                        ] = False

                        st.session_state[
                            "_qlc_pending_notification"
                        ] = {
                            "message": result[
                                "message"
                            ],
                            "loai": "success",
                        }

                        st.rerun()

                    else:

                        st.error(
                            result.get(
                                "message",
                                text["operation_error"],
                            )
                        )

            with col2:

                if st.button(
                    text["cancel"],
                    key="nguoi_an_confirm_activate_no",
                    width="stretch",
                ):

                    st.session_state[
                        "nguoi_an_confirm_activate"
                    ] = False

                    st.rerun()

    # ======================================================
    # 16. THÔNG TIN PHỤ
    # ======================================================

    st.caption(
        f"{text['person_id']}: {nguoi_id}  •  "
        f"{text['col_department']}: "
        f"{ten_bo_phan}  •  "
        f"{text['col_created']}: "
        f"{ngay_tao or text['not_updated']}"
    )