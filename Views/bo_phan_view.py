# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st

from Controllers.bo_phan_controller import BoPhanController
from Controllers.nguoi_an_controller import NguoiAnController

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section,
)

from Utils.notification import (
    hien_thi_thong_bao_da_luu,
)


def hien_thi_bo_phan():

    hien_thi_thong_bao_da_luu()

    language = st.session_state.get(
        "language",
        "vi",
    )

    texts = {
        "vi": {
            "header": "🏢 Quản lý bộ phận",
            "desc": "Quản lý phòng ban và phân bổ người ăn theo bộ phận.",

            "overview": "Tổng quan",
            "total": "Tổng bộ phận",
            "active": "Đang hoạt động",
            "inactive": "Đã ngừng",
            "people": "Tổng người",

            "add": "Thêm bộ phận",
            "new": "🏢 Thông tin bộ phận mới",
            "name": "Tên bộ phận",
            "name_required": "Tên bộ phận *",
            "placeholder": "Ví dụ: Kho",
            "add_button": "✨ Thêm bộ phận",

            "list": "Danh sách bộ phận",
            "status": "Trạng thái",
            "all": "Tất cả",
            "active_status": "Đang hoạt động",
            "inactive_status": "Đã ngừng",

            "search": "🔎 Tìm kiếm",
            "search_placeholder": "Nhập tên bộ phận...",

            "select": "Chọn bộ phận",
            "select_placeholder": "Chọn một bộ phận...",

            "actions": "Thao tác",
            "edit": "✏️ Chỉnh sửa",
            "stop": "⏸️ Ngừng hoạt động",
            "activate": "🔄 Kích hoạt lại",

            "edit_info": "✏️ Chỉnh sửa bộ phận",
            "save": "💾 Lưu thay đổi",
            "cancel": "Hủy",

            "confirm_stop": "Bạn có chắc muốn ngừng bộ phận này?",
            "confirm_activate": "Bạn có muốn kích hoạt lại bộ phận này?",

            "empty_name": "Tên bộ phận không được để trống.",
            "not_found": "🌷 Không tìm thấy bộ phận phù hợp.",
            "no_selection": "Vui lòng chọn một bộ phận trước.",

            "status_active": "🟢 Đang hoạt động",
            "status_inactive": "⚪ Đã ngừng",

            "col_id": "ID",
            "col_name": "Tên bộ phận",
            "col_people": "Số người",
            "col_status": "Trạng thái",
            "col_created": "Ngày tạo",

            "people_count": "người",
            "error": "Có lỗi xảy ra.",
        },

        "en": {
            "header": "🏢 Department Management",
            "desc": "Manage departments and assign meal participants.",

            "overview": "Overview",
            "total": "Total departments",
            "active": "Active",
            "inactive": "Inactive",
            "people": "Total people",

            "add": "Add department",
            "new": "🏢 New department information",
            "name": "Department name",
            "name_required": "Department name *",
            "placeholder": "Example: Warehouse",
            "add_button": "✨ Add department",

            "list": "Department list",
            "status": "Status",
            "all": "All",
            "active_status": "Active",
            "inactive_status": "Inactive",

            "search": "🔎 Search",
            "search_placeholder": "Enter department name...",

            "select": "Select department",
            "select_placeholder": "Select a department...",

            "actions": "Actions",
            "edit": "✏️ Edit",
            "stop": "⏸️ Disable",
            "activate": "🔄 Activate",

            "edit_info": "✏️ Edit department",
            "save": "💾 Save changes",
            "cancel": "Cancel",

            "confirm_stop": "Are you sure you want to disable this department?",
            "confirm_activate": "Do you want to activate this department?",

            "empty_name": "Department name cannot be empty.",
            "not_found": "🌷 No matching department found.",
            "no_selection": "Please select a department first.",

            "status_active": "🟢 Active",
            "status_inactive": "⚪ Inactive",

            "col_id": "ID",
            "col_name": "Department",
            "col_people": "People",
            "col_status": "Status",
            "col_created": "Created",

            "people_count": "people",
            "error": "An error occurred.",
        },

        "zh": {
            "header": "🏢 部门管理",
            "desc": "管理部门以及用餐人员的部门分配。",

            "overview": "概览",
            "total": "部门总数",
            "active": "正在使用",
            "inactive": "已停用",
            "people": "总人数",

            "add": "添加部门",
            "new": "🏢 新部门信息",
            "name": "部门名称",
            "name_required": "部门名称 *",
            "placeholder": "例如：仓库",
            "add_button": "✨ 添加部门",

            "list": "部门列表",
            "status": "状态",
            "all": "全部",
            "active_status": "正在使用",
            "inactive_status": "已停用",

            "search": "🔎 搜索",
            "search_placeholder": "输入部门名称...",

            "select": "选择部门",
            "select_placeholder": "请选择部门...",

            "actions": "操作",
            "edit": "✏️ 编辑",
            "stop": "⏸️ 停用",
            "activate": "🔄 启用",

            "edit_info": "✏️ 编辑部门",
            "save": "💾 保存修改",
            "cancel": "取消",

            "confirm_stop": "确定要停用该部门吗？",
            "confirm_activate": "要重新启用该部门吗？",

            "empty_name": "部门名称不能为空。",
            "not_found": "🌷 没有找到符合条件的部门。",
            "no_selection": "请先选择一个部门。",

            "status_active": "🟢 正在使用",
            "status_inactive": "⚪ 已停用",

            "col_id": "ID",
            "col_name": "部门名称",
            "col_people": "人数",
            "col_status": "状态",
            "col_created": "创建时间",

            "people_count": "人",
            "error": "发生错误。",
        },
    }

    text = texts.get(
        language,
        texts["vi"],
    )

    # ==========================================================
    # HEADER
    # ==========================================================

    hien_thi_header(
        text["header"],
        text["desc"],
    )

    # ==========================================================
    # LẤY DỮ LIỆU BỘ PHẬN
    # ==========================================================

    try:
        danh_sach = BoPhanController.lay_tat_ca()
    except Exception as error:
        st.error(
            f"{text['error']} {error}"
        )
        return

    if danh_sach is None:
        danh_sach = []

    # ==========================================================
    # LẤY DỮ LIỆU NGƯỜI ĂN
    # ==========================================================

    try:
        nguoi_result = (
            NguoiAnController
            .lay_danh_sach()
        )

        if nguoi_result.get("success"):
            danh_sach_nguoi = nguoi_result.get(
                "data",
                [],
            )
        else:
            danh_sach_nguoi = []

    except Exception:
        danh_sach_nguoi = []

    # ==========================================================
    # THỐNG KÊ
    # ==========================================================

    dang_hoat_dong = [
        bo_phan
        for bo_phan in danh_sach
        if bo_phan[2] == 1
    ]

    da_ngung = [
        bo_phan
        for bo_phan in danh_sach
        if bo_phan[2] == 0
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
            "🏢",
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
            text["people"],
            len(danh_sach_nguoi),
            "👥",
        )

    # ==========================================================
    # THÊM BỘ PHẬN
    # ==========================================================

    hien_thi_tieu_de_section(
        text["add"],
        "➕",
    )

    with st.expander(
        text["new"],
        expanded=False,
    ):

        with st.form(
            key="form_them_bo_phan",
            clear_on_submit=True,
        ):

            ten_bo_phan = st.text_input(
                text["name_required"],
                placeholder=text["placeholder"],
            )

            them_submit = st.form_submit_button(
                text["add_button"],
                type="primary",
                width="stretch",
            )

        if them_submit:

            if not ten_bo_phan.strip():

                st.warning(
                    text["empty_name"]
                )

            else:

                try:

                    BoPhanController.them_bo_phan(
                        ten_bo_phan.strip()
                    )

                    st.session_state[
                        "_qlc_pending_notification"
                    ] = {
                        "message": (
                            f"{text['add_button']} "
                            f"• {ten_bo_phan.strip()}"
                        ),
                        "loai": "success",
                    }

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"{text['error']} {error}"
                    )

    # ==========================================================
    # DANH SÁCH
    # ==========================================================

    hien_thi_tieu_de_section(
        text["list"],
        "🏢",
    )

    col1, col2 = st.columns(2)

    with col1:

        tu_khoa = st.text_input(
            text["search"],
            placeholder=text["search_placeholder"],
            key="bo_phan_search",
        )

    with col2:

        trang_thai = st.selectbox(
            text["status"],
            [
                text["all"],
                text["active_status"],
                text["inactive_status"],
            ],
            key="bo_phan_status_filter",
        )

    # ==========================================================
    # LỌC
    # ==========================================================

    danh_sach_hien_thi = danh_sach.copy()

    tu_khoa = tu_khoa.strip().lower()

    if tu_khoa:

        danh_sach_hien_thi = [
            bo_phan
            for bo_phan in danh_sach_hien_thi
            if tu_khoa in str(
                bo_phan[1]
            ).lower()
        ]

    if trang_thai == text["active_status"]:

        danh_sach_hien_thi = [
            bo_phan
            for bo_phan in danh_sach_hien_thi
            if bo_phan[2] == 1
        ]

    elif trang_thai == text["inactive_status"]:

        danh_sach_hien_thi = [
            bo_phan
            for bo_phan in danh_sach_hien_thi
            if bo_phan[2] == 0
        ]

    if not danh_sach_hien_thi:

        st.info(
            text["not_found"]
        )

        return

    # ==========================================================
    # ĐẾM NGƯỜI THEO BỘ PHẬN
    # ==========================================================

    def dem_nguoi(bo_phan_id):

        return sum(
            1
            for nguoi in danh_sach_nguoi
            if len(nguoi) > 3
            and nguoi[3] == bo_phan_id
        )

    # ==========================================================
    # DATAFRAME
    # ==========================================================

    rows = []

    for bo_phan in danh_sach_hien_thi:

        bo_phan_id = bo_phan[0]
        ten_bo_phan = bo_phan[1]
        trang_thai_db = bo_phan[2]
        ngay_tao = bo_phan[3] or ""

        so_nguoi = dem_nguoi(
            bo_phan_id
        )

        if trang_thai_db == 1:
            trang_thai_text = (
                text["status_active"]
            )
        else:
            trang_thai_text = (
                text["status_inactive"]
            )

        rows.append(
            {
                text["col_id"]: bo_phan_id,
                text["col_name"]: ten_bo_phan,
                text["col_people"]: so_nguoi,
                text["col_status"]: trang_thai_text,
                text["col_created"]: ngay_tao,
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )

    # ==========================================================
    # CHỌN BỘ PHẬN
    # ==========================================================

    hien_thi_tieu_de_section(
        text["actions"],
        "⚙️",
    )

    danh_sach_lua_chon = {}

    for bo_phan in danh_sach_hien_thi:

        bo_phan_id = bo_phan[0]
        ten_bo_phan = bo_phan[1]

        icon = (
            "🟢"
            if bo_phan[2] == 1
            else "⚪"
        )

        nhan = (
            f"{icon} "
            f"{ten_bo_phan} "
            f"(ID: {bo_phan_id})"
        )

        danh_sach_lua_chon[
            nhan
        ] = bo_phan_id

    lua_chon = st.selectbox(
        text["select"],
        list(
            danh_sach_lua_chon.keys()
        ),
        index=None,
        placeholder=text["select_placeholder"],
        key="bo_phan_selected",
    )

    if lua_chon is None:

        st.caption(
            text["no_selection"]
        )

        return

    bo_phan_id_duoc_chon = (
        danh_sach_lua_chon[
            lua_chon
        ]
    )

    bo_phan_duoc_chon = None

    for bo_phan in danh_sach:

        if (
            bo_phan[0]
            == bo_phan_id_duoc_chon
        ):

            bo_phan_duoc_chon = bo_phan
            break

    if bo_phan_duoc_chon is None:

        st.warning(
            text["no_selection"]
        )

        return

    # ==========================================================
    # THÔNG TIN BỘ PHẬN
    # ==========================================================

    bo_phan_id = bo_phan_duoc_chon[0]
    ten_bo_phan = bo_phan_duoc_chon[1]
    dang_hoat_dong = bo_phan_duoc_chon[2]
    ngay_tao = bo_phan_duoc_chon[3] or ""

    so_nguoi = dem_nguoi(
        bo_phan_id
    )

    with st.container(border=True):

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                f"#### 🏢 {ten_bo_phan}"
            )

            st.caption(
                f"{text['col_id']}: "
                f"{bo_phan_id}"
            )

        with col2:

            st.caption(
                text["people"]
            )

            st.write(
                f"{so_nguoi} "
                f"{text['people_count']}"
            )

        with col3:

            st.caption(
                text["status"]
            )

            if dang_hoat_dong:

                st.write(
                    text["status_active"]
                )

            else:

                st.write(
                    text["status_inactive"]
                )

    # ==========================================================
    # CHỈNH SỬA / NGỪNG HOẠT ĐỘNG
    # ==========================================================

    if dang_hoat_dong:

        col1, col2 = st.columns(2)

        with col1:

            sua = st.button(
                text["edit"],
                key="bo_phan_action_edit",
                width="stretch",
            )

        with col2:

            ngung = st.button(
                text["stop"],
                key="bo_phan_action_stop",
                width="stretch",
            )

        if ngung:

            st.session_state[
                "bo_phan_confirm_stop"
            ] = True

        if st.session_state.get(
            "bo_phan_confirm_stop",
            False,
        ):

            st.warning(
                text["confirm_stop"]
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✓ " + text["stop"],
                    key="bo_phan_confirm_stop_yes",
                    type="primary",
                    width="stretch",
                ):

                    try:

                        BoPhanController.ngung_hoat_dong(
                            bo_phan_id
                        )

                        st.session_state[
                            "bo_phan_confirm_stop"
                        ] = False

                        st.session_state[
                            "_qlc_pending_notification"
                        ] = {
                            "message": text["stop"],
                            "loai": "success",
                        }

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"{text['error']} {error}"
                        )

            with col2:

                if st.button(
                    text["cancel"],
                    key="bo_phan_confirm_stop_no",
                    width="stretch",
                ):

                    st.session_state[
                        "bo_phan_confirm_stop"
                    ] = False

                    st.rerun()

        # ======================================================
        # CHỈNH SỬA
        # ======================================================

        if sua:

            st.session_state[
                "bo_phan_edit_mode"
            ] = True

        if st.session_state.get(
            "bo_phan_edit_mode",
            False,
        ):

            with st.expander(
                text["edit_info"],
                expanded=True,
            ):

                with st.form(
                    key="form_sua_bo_phan",
                ):

                    ten_moi = st.text_input(
                        text["name"],
                        value=ten_bo_phan,
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        luu = st.form_submit_button(
                            text["save"],
                            type="primary",
                            width="stretch",
                        )

                    with col2:

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

                        try:

                            BoPhanController.cap_nhat(
                                bo_phan_id,
                                ten_moi.strip(),
                            )

                            st.session_state[
                                "bo_phan_edit_mode"
                            ] = False

                            st.session_state[
                                "_qlc_pending_notification"
                            ] = {
                                "message": text["save"],
                                "loai": "success",
                            }

                            st.rerun()

                        except Exception as error:

                            st.error(
                                f"{text['error']} {error}"
                            )

                if huy:

                    st.session_state[
                        "bo_phan_edit_mode"
                    ] = False

                    st.rerun()

    # ==========================================================
    # KÍCH HOẠT LẠI
    # ==========================================================

    else:

        if st.button(
            text["activate"],
            key="bo_phan_action_activate",
            type="primary",
            width="stretch",
        ):

            st.session_state[
                "bo_phan_confirm_activate"
            ] = True

        if st.session_state.get(
            "bo_phan_confirm_activate",
            False,
        ):

            st.info(
                text["confirm_activate"]
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✓ " + text["activate"],
                    key="bo_phan_confirm_activate_yes",
                    type="primary",
                    width="stretch",
                ):

                    try:

                        BoPhanController.kich_hoat_lai(
                            bo_phan_id
                        )

                        st.session_state[
                            "bo_phan_confirm_activate"
                        ] = False

                        st.session_state[
                            "_qlc_pending_notification"
                        ] = {
                            "message": text["activate"],
                            "loai": "success",
                        }

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"{text['error']} {error}"
                        )

            with col2:

                if st.button(
                    text["cancel"],
                    key="bo_phan_confirm_activate_no",
                    width="stretch",
                ):

                    st.session_state[
                        "bo_phan_confirm_activate"
                    ] = False

                    st.rerun()

    # ==========================================================
    # THÔNG TIN CUỐI
    # ==========================================================

    st.caption(
        f"{text['col_id']}: {bo_phan_id}  •  "
        f"{text['col_created']}: "
        f"{ngay_tao}"
    )