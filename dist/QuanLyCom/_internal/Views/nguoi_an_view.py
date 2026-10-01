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


def _lay_danh_sach_bo_phan():
    try:
        return BoPhanController.lay_dang_hoat_dong() or []
    except Exception:
        return []


def _lay_nguoi_theo_id(danh_sach, nguoi_id):
    for nguoi in danh_sach:
        if nguoi[0] == nguoi_id:
            return nguoi
    return None


def _trang_thai_hien_thi(dang_hoat_dong, text):
    if dang_hoat_dong == 1:
        return text["status_active"]
    return text["status_inactive"]


def _tao_dataframe_chinh_sua(danh_sach, danh_sach_bo_phan, text):
    bo_phan_map = {
        bo_phan[1]: bo_phan[0]
        for bo_phan in danh_sach_bo_phan
    }

    rows = []

    for nguoi in danh_sach:
        nguoi_id = nguoi[0]
        ho_ten = nguoi[1]
        sdt = nguoi[2] or ""
        bo_phan = nguoi[4] or text["no_department"]
        dang_hoat_dong = nguoi[5]
        ngay_tao = nguoi[6] or ""

        rows.append(
            {
                text["col_id"]: nguoi_id,
                text["col_name"]: ho_ten,
                text["col_phone"]: sdt,
                text["col_department"]: bo_phan,
                text["col_status"]: _trang_thai_hien_thi(
                    dang_hoat_dong,
                    text,
                ),
                text["col_created"]: ngay_tao,
            }
        )

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df[text["col_id"]] = df[text["col_id"]].astype(int)

    return df


def _tao_dataframe_them_moi(text):
    return pd.DataFrame(
        columns=[
            text["col_name"],
            text["col_phone"],
            text["col_department"],
        ]
    )


def hien_thi_nguoi_an():

    hien_thi_thong_bao_da_luu()

    language = st.session_state.get(
        "language",
        "vi",
    )

    texts = {
        "vi": {
            "header": "👩‍🍳 Quản lý người ăn",
            "header_desc": (
                "Quản lý danh sách nhân viên, bộ phận "
                "và trạng thái sử dụng suất ăn."
            ),

            "overview": "Tổng quan",
            "total": "Tổng số",
            "active": "Đang hoạt động",
            "inactive": "Đã ngừng",
            "department_count": "Số bộ phận",

            "add": "Thêm người ăn",
            "new_person": "👤 Thông tin người ăn mới",
            "basic_info": (
                "Họ và tên là bắt buộc. Số điện thoại và bộ phận "
                "có thể bổ sung sau."
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
            "search_placeholder": "Nhập tên hoặc số điện thoại...",

            "status": "Trạng thái",
            "all": "Tất cả",
            "active_status": "Đang hoạt động",
            "inactive_status": "Đã ngừng",

            "department_filter": "Bộ phận",
            "all_department": "Tất cả",

            "page_size": "Số dòng / trang",
            "page": "Trang",
            "of_page": "/",
            "showing": "Đang hiển thị",
            "of": "/",
            "people": "người",

            "not_found": "🌷 Không tìm thấy người ăn phù hợp.",

            "col_id": "ID",
            "col_name": "Họ tên",
            "col_department": "Bộ phận",
            "col_phone": "Số điện thoại",
            "col_status": "Trạng thái",
            "col_created": "Ngày tạo",

            "not_updated": "Chưa cập nhật",

            "edit_table": "✏️ Chỉnh sửa trực tiếp",
            "edit_table_desc": (
                "Bạn có thể sửa họ tên, số điện thoại, bộ phận "
                "và trạng thái trực tiếp trong bảng."
            ),

            "save_changes": "💾 Lưu thay đổi",
            "cancel_changes": "↩️ Hủy thay đổi",
            "refresh": "🔄 Làm mới",

            "changed_rows": "Có thay đổi chưa lưu",
            "no_changes": "Không có thay đổi nào cần lưu.",
            "save_success": "Đã lưu thay đổi thành công.",
            "save_partial": "Đã lưu thay đổi, nhưng có một số dòng không cập nhật được.",

            "empty_name": "Họ và tên không được để trống.",
            "duplicate_name": "Phát hiện người ăn bị trùng thông tin.",

            "operation_error": "Không thể thực hiện thao tác.",
            "load_error": "Không thể tải danh sách người ăn.",
            "department_load_error": "Không thể tải danh sách bộ phận.",

            "no_department_available": (
                "Chưa có bộ phận hoạt động. "
                "Bạn vẫn có thể thêm người ăn trước."
            ),

            "confirm_stop": (
                "Bạn đang chuyển một hoặc nhiều người sang trạng thái "
                "Đã ngừng. Hãy kiểm tra lại trước khi lưu."
            ),

            "confirm_activate": (
                "Bạn đang kích hoạt lại một hoặc nhiều người."
            ),

            "add_person_success": "Đã thêm người ăn thành công.",

            "status_active": "🟢 Đang hoạt động",
            "status_inactive": "⚪ Đã ngừng",

            "new_department": "Chưa phân bộ phận",
        },

        "en": {
            "header": "👩‍🍳 Meal Participants",
            "header_desc": (
                "Manage employees, departments "
                "and meal participation status."
            ),

            "overview": "Overview",
            "total": "Total",
            "active": "Active",
            "inactive": "Inactive",
            "department_count": "Departments",

            "add": "Add participant",
            "new_person": "👤 New participant information",
            "basic_info": (
                "Name is required. Phone number and department "
                "can be added later."
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
            "search_placeholder": "Enter name or phone number...",

            "status": "Status",
            "all": "All",
            "active_status": "Active",
            "inactive_status": "Inactive",

            "department_filter": "Department",
            "all_department": "All",

            "page_size": "Rows / page",
            "page": "Page",
            "of_page": "/",
            "showing": "Showing",
            "of": "/",
            "people": "people",

            "not_found": "🌷 No matching participant found.",

            "col_id": "ID",
            "col_name": "Name",
            "col_department": "Department",
            "col_phone": "Phone",
            "col_status": "Status",
            "col_created": "Created",

            "not_updated": "Not updated",

            "edit_table": "✏️ Edit directly",
            "edit_table_desc": (
                "Edit name, phone, department and status "
                "directly in the table."
            ),

            "save_changes": "💾 Save changes",
            "cancel_changes": "↩️ Cancel changes",
            "refresh": "🔄 Refresh",

            "changed_rows": "Unsaved changes",
            "no_changes": "There are no changes to save.",
            "save_success": "Changes saved successfully.",
            "save_partial": (
                "Changes were saved, but some rows could not be updated."
            ),

            "empty_name": "Name cannot be empty.",
            "duplicate_name": "Duplicate participant information detected.",

            "operation_error": "Unable to complete the operation.",
            "load_error": "Unable to load participants.",
            "department_load_error": "Unable to load departments.",

            "no_department_available": (
                "No active departments are available. "
                "You can still add participants first."
            ),

            "confirm_stop": (
                "One or more participants will be changed "
                "to inactive. Please review before saving."
            ),

            "confirm_activate": (
                "One or more participants will be activated."
            ),

            "add_person_success": "Participant added successfully.",

            "status_active": "🟢 Active",
            "status_inactive": "⚪ Inactive",

            "new_department": "No department",
        },

        "zh": {
            "header": "👩‍🍳 用餐人员管理",
            "header_desc": "管理员工、部门和用餐状态。",

            "overview": "概览",
            "total": "总人数",
            "active": "正在使用",
            "inactive": "已停用",
            "department_count": "部门数量",

            "add": "添加用餐人员",
            "new_person": "👤 新用餐人员信息",
            "basic_info": "姓名为必填项，电话和部门可以之后补充。",

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
            "search_placeholder": "输入姓名或电话号码...",

            "status": "状态",
            "all": "全部",
            "active_status": "正在使用",
            "inactive_status": "已停用",

            "department_filter": "部门",
            "all_department": "全部",

            "page_size": "每页行数",
            "page": "页",
            "of_page": "/",
            "showing": "显示",
            "of": "/",
            "people": "人",

            "not_found": "🌷 没有找到符合条件的人员。",

            "col_id": "ID",
            "col_name": "姓名",
            "col_department": "部门",
            "col_phone": "电话",
            "col_status": "状态",
            "col_created": "创建时间",

            "not_updated": "未更新",

            "edit_table": "✏️ 直接编辑",
            "edit_table_desc": (
                "可以直接在表格中修改姓名、电话、部门和状态。"
            ),

            "save_changes": "💾 保存修改",
            "cancel_changes": "↩️ 取消修改",
            "refresh": "🔄 刷新",

            "changed_rows": "有未保存的修改",
            "no_changes": "没有需要保存的修改。",
            "save_success": "修改已成功保存。",
            "save_partial": "修改已保存，但部分数据无法更新。",

            "empty_name": "姓名不能为空。",
            "duplicate_name": "检测到重复的人员信息。",

            "operation_error": "无法完成操作。",
            "load_error": "无法加载用餐人员名单。",
            "department_load_error": "无法加载部门列表。",

            "no_department_available": (
                "暂无可用部门。仍然可以先添加人员。"
            ),

            "confirm_stop": (
                "一个或多个人员将被设置为停用，请保存前确认。"
            ),

            "confirm_activate": "一个或多个人员将重新启用。",

            "add_person_success": "人员添加成功。",

            "status_active": "🟢 正在使用",
            "status_inactive": "⚪ 已停用",

            "new_department": "未分配部门",
        },
    }

    text = texts.get(
        language,
        texts["vi"],
    )

    hien_thi_header(
        text["header"],
        text["header_desc"],
    )

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

    danh_sach_bo_phan = _lay_danh_sach_bo_phan()

    if not danh_sach_bo_phan:
        try:
            BoPhanController.lay_dang_hoat_dong()
        except Exception:
            pass

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

            if danh_sach_bo_phan:

                bo_phan_options = {
                    text["no_department"]: None
                }

                for bo_phan in danh_sach_bo_phan:
                    bo_phan_options[
                        bo_phan[1]
                    ] = bo_phan[0]

                bo_phan_label = st.selectbox(
                    text["department"],
                    list(
                        bo_phan_options.keys()
                    ),
                    key="nguoi_an_add_department",
                )

                bo_phan_id_moi = bo_phan_options[
                    bo_phan_label
                ]

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

    hien_thi_tieu_de_section(
        text["list"],
        "👥",
    )

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

        bo_phan_filter_id = bo_phan_filter_options[
            bo_phan_filter_label
        ]

    with col4:

        so_dong_trang = st.selectbox(
            text["page_size"],
            [10, 20, 50, 100],
            index=1,
            key="nguoi_an_page_size",
        )

    danh_sach_hien_thi = danh_sach.copy()

    tu_khoa_lower = tu_khoa.strip().lower()

    if tu_khoa_lower:

        danh_sach_hien_thi = [
            nguoi
            for nguoi in danh_sach_hien_thi
            if (
                tu_khoa_lower in str(
                    nguoi[1] or ""
                ).lower()
                or tu_khoa_lower in str(
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
        or st.session_state["nguoi_an_page"] > tong_so_trang
    ):

        st.session_state[
            "nguoi_an_page"
        ] = 1

    trang_hien_tai = st.session_state[
        "nguoi_an_page"
    ]

    bat_dau = (
        trang_hien_tai - 1
    ) * so_dong_trang

    ket_thuc = min(
        bat_dau + so_dong_trang,
        tong_so,
    )

    danh_sach_trang = danh_sach_hien_thi[
        bat_dau:ket_thuc
    ]

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

    st.caption(
        text["edit_table_desc"]
    )

    df_ban_dau = _tao_dataframe_chinh_sua(
        danh_sach_trang,
        danh_sach_bo_phan,
        text,
    )

    ten_cot_id = text["col_id"]
    ten_cot_ten = text["col_name"]
    ten_cot_sdt = text["col_phone"]
    ten_cot_bo_phan = text["col_department"]
    ten_cot_trang_thai = text["col_status"]
    ten_cot_ngay_tao = text["col_created"]

    danh_sach_ten_bo_phan = [
        text["no_department"]
    ] + [
        bo_phan[1]
        for bo_phan in danh_sach_bo_phan
    ]

    danh_sach_trang_thai = [
        text["status_active"],
        text["status_inactive"],
    ]

    edited_df = st.data_editor(
        df_ban_dau,
        width="stretch",
        hide_index=True,
        num_rows="fixed",
        key="nguoi_an_editor",
        column_config={

            ten_cot_id:
                st.column_config.NumberColumn(
                    ten_cot_id,
                    disabled=True,
                    width="small",
                ),

            ten_cot_ten:
                st.column_config.TextColumn(
                    ten_cot_ten,
                    required=True,
                    width="medium",
                ),

            ten_cot_sdt:
                st.column_config.TextColumn(
                    ten_cot_sdt,
                    width="medium",
                ),

            ten_cot_bo_phan:
                st.column_config.SelectboxColumn(
                    ten_cot_bo_phan,
                    options=danh_sach_ten_bo_phan,
                    width="medium",
                ),

            ten_cot_trang_thai:
                st.column_config.SelectboxColumn(
                    ten_cot_trang_thai,
                    options=danh_sach_trang_thai,
                    width="medium",
                ),

            ten_cot_ngay_tao:
                st.column_config.TextColumn(
                    ten_cot_ngay_tao,
                    disabled=True,
                    width="medium",
                ),
        },
    )

    co_thay_doi = not edited_df.equals(
        df_ban_dau
    )

    if co_thay_doi:

        st.warning(
            f"⚠️ {text['changed_rows']}"
        )

    col1, col2, col3 = st.columns(
        [1.4, 1, 1.4],
    )

    with col1:

        luu_thay_doi = st.button(
            text["save_changes"],
            type="primary",
            width="stretch",
            key="nguoi_an_save_changes",
        )

    with col2:

        huy_thay_doi = st.button(
            text["cancel_changes"],
            width="stretch",
            key="nguoi_an_cancel_changes",
        )

    with col3:

        lam_moi = st.button(
            text["refresh"],
            width="stretch",
            key="nguoi_an_refresh",
        )

    if huy_thay_doi:

        st.rerun()

    if lam_moi:

        st.rerun()

    if luu_thay_doi:

        if not co_thay_doi:

            st.info(
                text["no_changes"]
            )

        else:

            thay_doi = 0
            loi = 0
            thong_bao_loi = []

            df_goc = df_ban_dau.reset_index(
                drop=True
            )

            df_moi = edited_df.reset_index(
                drop=True
            )

            for index in range(
                    len(df_moi)
            ):

                row_goc = df_goc.iloc[index]
                row_moi = df_moi.iloc[index]

                try:

                    nguoi_id = int(
                        row_goc[ten_cot_id]
                    )

                    ho_ten_moi = str(
                        row_moi[ten_cot_ten]
                    ).strip()

                    if pd.isna(
                            row_moi[ten_cot_sdt]
                    ):
                        sdt_moi = ""
                    else:
                        sdt_moi = str(
                            row_moi[ten_cot_sdt]
                        ).strip()

                    bo_phan_moi_label = str(
                        row_moi[ten_cot_bo_phan]
                    ).strip()

                    trang_thai_moi = str(
                        row_moi[ten_cot_trang_thai]
                    ).strip()

                    if not ho_ten_moi:
                        loi += 1

                        thong_bao_loi.append(
                            f"ID {nguoi_id}: "
                            f"{text['empty_name']}"
                        )

                        continue

                    bo_phan_moi_id = None

                    for bo_phan in danh_sach_bo_phan:

                        if (
                                bo_phan[1]
                                == bo_phan_moi_label
                        ):
                            bo_phan_moi_id = (
                                bo_phan[0]
                            )

                            break

                    dang_hoat_dong_moi = (
                        1
                        if trang_thai_moi
                           == text["status_active"]
                        else 0
                    )

                    ten_goc = str(
                        row_goc[ten_cot_ten]
                    ).strip()

                    if pd.isna(
                            row_goc[ten_cot_sdt]
                    ):
                        sdt_goc = ""
                    else:
                        sdt_goc = str(
                            row_goc[ten_cot_sdt]
                        ).strip()

                    bo_phan_goc = str(
                        row_goc[ten_cot_bo_phan]
                    ).strip()

                    trang_thai_goc_text = str(
                        row_goc[ten_cot_trang_thai]
                    ).strip()

                    co_thay_doi_dong = (
                            ten_goc != ho_ten_moi
                            or sdt_goc != sdt_moi
                            or bo_phan_goc != bo_phan_moi_label
                            or trang_thai_goc_text != trang_thai_moi
                    )

                    if not co_thay_doi_dong:
                        continue

                    nguoi_goc = _lay_nguoi_theo_id(
                        danh_sach,
                        nguoi_id,
                    )

                    if nguoi_goc is None:
                        loi += 1

                        thong_bao_loi.append(
                            f"ID {nguoi_id}: "
                            f"{text['operation_error']}"
                        )

                        continue

                    trang_thai_goc = nguoi_goc[5]

                    result_update = (
                        NguoiAnController.cap_nhat(
                            nguoi_an_id=nguoi_id,
                            ho_ten=ho_ten_moi,
                            sdt=sdt_moi or None,
                            bo_phan_id=bo_phan_moi_id,
                        )
                    )

                    if not result_update["success"]:
                        loi += 1

                        thong_bao_loi.append(
                            f"ID {nguoi_id}: "
                            f"{result_update.get('message', text['operation_error'])}"
                        )

                        continue

                    if (
                            trang_thai_goc == 1
                            and dang_hoat_dong_moi == 0
                    ):

                        result_status = (
                            NguoiAnController
                            .ngung_hoat_dong(
                                nguoi_id
                            )
                        )

                    elif (
                            trang_thai_goc == 0
                            and dang_hoat_dong_moi == 1
                    ):

                        result_status = (
                            NguoiAnController
                            .kich_hoat_lai(
                                nguoi_id
                            )
                        )

                    else:

                        result_status = {
                            "success": True
                        }

                    if not result_status["success"]:
                        loi += 1

                        thong_bao_loi.append(
                            f"ID {nguoi_id}: "
                            f"{result_status.get('message', text['operation_error'])}"
                        )

                        continue

                    thay_doi += 1

                except Exception as error:

                    loi += 1

                    thong_bao_loi.append(
                        f"ID {row_goc[ten_cot_id]}: "
                        f"{error}"
                    )

            if thay_doi > 0 and loi == 0:

                st.session_state[
                    "_qlc_pending_notification"
                ] = {
                    "message": (
                        f"{text['save_success']} "
                        f"({thay_doi})"
                    ),
                    "loai": "success",
                }

                st.rerun()

            elif thay_doi > 0 and loi > 0:

                st.session_state[
                    "_qlc_pending_notification"
                ] = {
                    "message": (
                        f"{text['save_partial']} "
                        f"✓ {thay_doi} "
                        f"• ⚠️ {loi}"
                    ),
                    "loai": "warning",
                }

                for message in thong_bao_loi[:5]:
                    st.warning(
                        message
                    )

                st.rerun()

            else:

                for message in thong_bao_loi[:5]:
                    st.error(
                        message
                    )

            if thay_doi > 0 and loi == 0:

                st.session_state[
                    "_qlc_pending_notification"
                ] = {
                    "message": (
                        f"{text['save_success']} "
                        f"({thay_doi})"
                    ),
                    "loai": "success",
                }

                st.rerun()

            elif thay_doi > 0 and loi > 0:

                st.session_state[
                    "_qlc_pending_notification"
                ] = {
                    "message": (
                        f"{text['save_partial']} "
                        f"✓ {thay_doi} "
                        f"• ⚠️ {loi}"
                    ),
                    "loai": "warning",
                }

                for message in thong_bao_loi[:5]:

                    st.warning(
                        message
                    )

                st.rerun()

            else:

                for message in thong_bao_loi[:5]:

                    st.error(
                        message
                    )

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