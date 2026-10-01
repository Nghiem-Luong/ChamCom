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

            "save": "💾 Lưu thay đổi",
            "cancel_changes": "↩️ Hủy thay đổi",
            "no_changes": "Không có thay đổi nào cần lưu.",

            "empty_name": "Tên bộ phận không được để trống.",
            "not_found": "🌷 Không tìm thấy bộ phận phù hợp.",

            "status_active": "🟢 Đang hoạt động",
            "status_inactive": "⚪ Đã ngừng",

            "col_id": "ID",
            "col_name": "Tên bộ phận",
            "col_people": "Số người",
            "col_status": "Trạng thái",
            "col_created": "Ngày tạo",

            "people_count": "người",

            "save_success": "Đã lưu thay đổi",
            "save_partial": "Đã lưu một phần thay đổi",
            "operation_error": "Không thể cập nhật bộ phận.",

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

            "save": "💾 Save changes",
            "cancel_changes": "↩️ Cancel changes",
            "no_changes": "There are no changes to save.",

            "empty_name": "Department name cannot be empty.",
            "not_found": "🌷 No matching department found.",

            "status_active": "🟢 Active",
            "status_inactive": "⚪ Inactive",

            "col_id": "ID",
            "col_name": "Department",
            "col_people": "People",
            "col_status": "Status",
            "col_created": "Created",

            "people_count": "people",

            "save_success": "Changes saved",
            "save_partial": "Changes partially saved",
            "operation_error": "Unable to update department.",

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

            "save": "💾 保存修改",
            "cancel_changes": "↩️ 取消修改",
            "no_changes": "没有需要保存的修改。",

            "empty_name": "部门名称不能为空。",
            "not_found": "🌷 没有找到符合条件的部门。",

            "status_active": "🟢 正在使用",
            "status_inactive": "⚪ 已停用",

            "col_id": "ID",
            "col_name": "部门名称",
            "col_people": "人数",
            "col_status": "状态",
            "col_created": "创建时间",

            "people_count": "人",

            "save_success": "修改已保存",
            "save_partial": "部分修改已保存",
            "operation_error": "无法更新部门。",

            "error": "发生错误。",
        },
    }

    text = texts.get(
        language,
        texts["vi"],
    )

    hien_thi_header(
        text["header"],
        text["desc"],
    )

    try:
        danh_sach = BoPhanController.lay_tat_ca()
    except Exception as error:
        st.error(
            f"{text['error']} {error}"
        )
        return

    if danh_sach is None:
        danh_sach = []

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

            ten_bo_phan = ten_bo_phan.strip()

            if not ten_bo_phan:

                st.warning(
                    text["empty_name"]
                )

            else:

                try:

                    BoPhanController.them_bo_phan(
                        ten_bo_phan
                    )

                    st.session_state[
                        "_qlc_pending_notification"
                    ] = {
                        "message": (
                            f"{text['add_button']} "
                            f"• {ten_bo_phan}"
                        ),
                        "loai": "success",
                    }

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"{text['error']} {error}"
                    )

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

    def dem_nguoi(bo_phan_id):

        return sum(
            1
            for nguoi in danh_sach_nguoi
            if len(nguoi) > 3
            and nguoi[3] == bo_phan_id
        )

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

    df_ban_dau = pd.DataFrame(rows)

    if "bo_phan_editor_version" not in st.session_state:

        st.session_state[
            "bo_phan_editor_version"
        ] = 0

    editor_version = st.session_state[
        "bo_phan_editor_version"
    ]

    edited_df = st.data_editor(
        df_ban_dau,
        width="stretch",
        hide_index=True,
        key=f"bo_phan_editor_{editor_version}",
        num_rows="fixed",
        column_config={
            text["col_id"]: st.column_config.NumberColumn(
                text["col_id"],
                disabled=True,
                width="small",
            ),

            text["col_name"]: st.column_config.TextColumn(
                text["col_name"],
                required=True,
                width="large",
            ),

            text["col_people"]: st.column_config.NumberColumn(
                text["col_people"],
                disabled=True,
                width="small",
            ),

            text["col_status"]: st.column_config.SelectboxColumn(
                text["col_status"],
                options=[
                    text["status_active"],
                    text["status_inactive"],
                ],
                required=True,
                width="medium",
            ),

            text["col_created"]: st.column_config.TextColumn(
                text["col_created"],
                disabled=True,
                width="medium",
            ),
        },
        disabled=[
            text["col_id"],
            text["col_people"],
            text["col_created"],
        ],
    )

    df_goc = df_ban_dau.reset_index(drop=True)
    df_moi = edited_df.reset_index(drop=True)

    co_thay_doi = not df_goc.equals(df_moi)

    col1, col2, col3 = st.columns(
        [2, 2, 6]
    )

    with col1:

        luu_thay_doi = st.button(
            text["save"],
            type="primary",
            width="stretch",
            key="bo_phan_save_changes",
        )

    with col2:

        huy_thay_doi = st.button(
            text["cancel_changes"],
            width="stretch",
            key="bo_phan_cancel_changes",
        )

    if huy_thay_doi:

        st.session_state[
            "bo_phan_editor_version"
        ] += 1

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

            for index in range(
                len(df_moi)
            ):

                row_goc = df_goc.iloc[index]
                row_moi = df_moi.iloc[index]

                try:

                    bo_phan_id = int(
                        row_goc[
                            text["col_id"]
                        ]
                    )

                    ten_goc = str(
                        row_goc[
                            text["col_name"]
                        ]
                    ).strip()

                    ten_moi = str(
                        row_moi[
                            text["col_name"]
                        ]
                    ).strip()

                    trang_thai_goc = str(
                        row_goc[
                            text["col_status"]
                        ]
                    ).strip()

                    trang_thai_moi = str(
                        row_moi[
                            text["col_status"]
                        ]
                    ).strip()

                    if not ten_moi:

                        loi += 1

                        thong_bao_loi.append(
                            f"ID {bo_phan_id}: "
                            f"{text['empty_name']}"
                        )

                        continue

                    ten_da_thay_doi = (
                        ten_goc
                        != ten_moi
                    )

                    trang_thai_da_thay_doi = (
                        trang_thai_goc
                        != trang_thai_moi
                    )

                    if not ten_da_thay_doi and not trang_thai_da_thay_doi:

                        continue

                    if ten_da_thay_doi:

                        try:

                            BoPhanController.cap_nhat(
                                bo_phan_id,
                                ten_moi,
                            )

                        except Exception as error:

                            loi += 1

                            thong_bao_loi.append(
                                f"ID {bo_phan_id}: "
                                f"{error}"
                            )

                            continue

                    if trang_thai_da_thay_doi:

                        if (
                            trang_thai_moi
                            == text["status_active"]
                        ):

                            if (
                                trang_thai_goc
                                == text["status_inactive"]
                            ):

                                BoPhanController.kich_hoat_lai(
                                    bo_phan_id
                                )

                        elif (
                            trang_thai_moi
                            == text["status_inactive"]
                        ):

                            if (
                                trang_thai_goc
                                == text["status_active"]
                            ):

                                BoPhanController.ngung_hoat_dong(
                                    bo_phan_id
                                )

                    thay_doi += 1

                except Exception as error:

                    loi += 1

                    thong_bao_loi.append(
                        f"ID {row_goc[text['col_id']]}: "
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

                st.session_state[
                    "bo_phan_editor_version"
                ] += 1

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

                st.session_state[
                    "bo_phan_editor_version"
                ] += 1

                st.rerun()

            else:

                for message in thong_bao_loi[:5]:

                    st.error(
                        message
                    )

    st.caption(
        "💡 "
        + (
            "Chỉnh sửa tên hoặc trạng thái trực tiếp trong bảng, "
            "sau đó bấm Lưu thay đổi."
            if language == "vi"
            else
            "Edit the department name or status directly in the table, "
            "then click Save changes."
            if language == "en"
            else
            "直接在表格中修改部门名称或状态，然后点击保存修改。"
        )
    )