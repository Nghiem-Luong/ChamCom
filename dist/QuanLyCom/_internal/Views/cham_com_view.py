# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from datetime import date

from Controllers.nguoi_an_controller import NguoiAnController
from Controllers.ngay_an_controller import NgayAnController
from Controllers.chi_tiet_an_controller import ChiTietAnController
from Controllers.chot_suat_an_controller import ChotSuatAnController
from Controllers.suat_an_phat_sinh_controller import (
    SuatAnPhatSinhController
)

from Views.layout import (
    hien_thi_header,
    hien_thi_the,
    hien_thi_tieu_de_section,
)


def hien_thi_cham_com():

    language = st.session_state.get("language", "vi")

    texts = {
        "vi": {
            "header": "🍚 Chấm cơm hôm nay",
            "header_desc": "Quản lý trạng thái ăn của nhân viên theo từng ngày.",

            "date": "Ngày ăn",
            "meal_info": "Thông tin ngày ăn",
            "price": "Đơn giá",
            "note": "Ghi chú",
            "create": "Tạo ngày ăn",

            "not_created": "Ngày này chưa được tạo.",
            "create_success": "Đã tạo ngày ăn.",
            "create_failed": "Không thể tạo ngày ăn.",

            "suggested": "Đơn giá ngày trước",
            "note_placeholder": "Ghi chú ngày ăn...",

            "workspace": "Quản lý suất ăn",
            "registration": "📝 Đăng ký suất ăn",
            "confirmed": "📋 Danh sách chốt",

            "filter": "Lọc danh sách",
            "all_department": "Tất cả bộ phận",
            "search": "Tìm tên / SĐT",
            "search_placeholder": "Nhập tên hoặc số điện thoại...",

            "people": "Danh sách chấm cơm",
            "status": "Trạng thái",
            "amount": "Tiền cơm",
            "department": "Bộ phận",
            "person": "Nhân viên",
            "stt": "STT",
            "remark": "Ghi chú",
            "phone": "SĐT",

            "register": "🟢 Ăn",
            "not_eat": "⚪ Không ăn",
            "business": "🟠 Đi công tác",
            "unmarked": "🟡 Chưa chấm",

            "status_all": "Tất cả trạng thái",
            "status_unmarked": "Chưa chấm",
            "status_eating": "Ăn",
            "status_not_eating": "Không ăn",
            "status_business": "Đi công tác",

            "select_all": "🟢 Cho danh sách đang lọc ăn",
            "unselect_all": "⚪ Cho danh sách đang lọc không ăn",
            "business_all": "🟠 Cho danh sách đang lọc đi công tác",

            "saved": "Đã lưu.",
            "save_failed": "Lưu dữ liệu thất bại.",

            "edit_help": (
                "Chọn trạng thái sẽ tự động lưu. "
                "Tiền cơm và ghi chú cũng được lưu ngay khi thay đổi."
            ),

            "total": "Tổng số",
            "registered": "Ăn",
            "not_eating": "Không ăn",
            "business_trip": "Công tác",
            "unmarked_count": "Chưa chấm",
            "money": "Tổng tiền",

            "no_people": "Chưa có người ăn đang hoạt động.",
            "no_result": "Không tìm thấy người phù hợp.",

            "load_day_error": "Không thể tải thông tin ngày ăn.",
            "load_people_error": "Không thể tải danh sách người ăn.",
            "load_register_error": "Không thể tải dữ liệu đăng ký.",

            "not_enough_data": "Chưa có dữ liệu đăng ký để chốt.",

            "confirm_title": "Chốt suất ăn",
            "confirm_desc": (
                "Sau khi chốt, danh sách sẽ được lưu thành "
                "một bản riêng và dùng làm danh sách chính thức."
            ),

            "confirm_button": "🔒 CHỐT SUẤT ĂN",

            "confirmed_success": "Đã chốt suất ăn thành công.",
            "confirmed_failed": "Không thể chốt suất ăn.",

            "confirmed_list": "Danh sách chốt chính thức",
            "confirmed_at": "Thời gian chốt",
            "confirmed_by": "Người chốt",

            "open_confirm": "🔓 MỞ CHỐT",

            "open_confirm_desc": (
                "Mở chốt sẽ xóa bản snapshot hiện tại và "
                "cho phép chỉnh sửa đăng ký lại."
            ),

            "open_confirm_success": (
                "Đã mở chốt. Bạn có thể chỉnh sửa danh sách."
            ),

            "open_confirm_failed": "Không thể mở chốt.",

            "status_not_confirmed": "🟡 Chưa chốt",
            "status_confirmed": "🟢 Đã chốt",

            "no_confirmed": "Ngày này chưa có danh sách chốt.",
            "confirm_warning": "Danh sách chốt lấy dữ liệu đã lưu trong hệ thống.",

            "confirm_note": "Ghi chú chốt",

            "extra_meal": "➕ Suất ăn phát sinh",
            "extra_meal_desc": (
                "Dùng cho khách, đoàn kỹ thuật hoặc người tạm thời "
                "không cần tạo hồ sơ trong danh sách người ăn."
            ),
            "extra_name": "Tên người / nhóm",
            "extra_name_placeholder": "VD: Khách Samsung, Đoàn kỹ thuật...",
            "extra_unit": "Đơn vị",
            "extra_unit_placeholder": "VD: Samsung, Nhà thầu...",
            "extra_quantity": "Số lượng",
            "extra_price": "Đơn giá",
            "extra_note": "Ghi chú phát sinh",
            "extra_add": "➕ THÊM SUẤT PHÁT SINH",
            "extra_added": "Đã thêm suất ăn phát sinh.",
            "extra_updated": "Đã cập nhật suất ăn phát sinh.",
            "extra_deleted": "Đã xóa suất ăn phát sinh.",
            "extra_empty": "Chưa có suất ăn phát sinh.",
            "extra_list": "Danh sách suất ăn phát sinh",
            "extra_type": "Loại",
            "extra_total": "Tổng suất phát sinh",
            "extra_money": "Tiền phát sinh",
            "extra_edit": "Sửa",
            "extra_delete": "Xóa",
            "extra_save": "💾 LƯU",
            "extra_cancel": "Hủy",
            "extra_editing": "Đang sửa",
            "extra_people": "Phát sinh",
            "employee": "Nhân viên",
            "generated": "Phát sinh",
            "extra_confirm_warning": (
                "Các suất phát sinh đã thêm sẽ được đưa vào danh sách chốt."
            ),
            "extra_load_error": "Không thể tải suất ăn phát sinh.",
            "extra_save_error": "Không thể lưu suất ăn phát sinh.",

            "quantity": "Số lượng",
            "unit_price": "Đơn giá",
            "total_amount": "Thành tiền",
        },

        "en": {
            "header": "🍚 Meal Attendance",
            "header_desc": "Manage daily meal status of employees.",

            "date": "Meal date",
            "meal_info": "Meal information",
            "price": "Meal price",
            "note": "Note",
            "create": "Create meal day",

            "not_created": "This date has not been created.",
            "create_success": "Meal day created.",
            "create_failed": "Unable to create meal day.",

            "suggested": "Previous day price",
            "note_placeholder": "Meal day note...",

            "workspace": "Meal management",
            "registration": "📝 Meal registration",
            "confirmed": "📋 Confirmed list",

            "filter": "Filter list",
            "all_department": "All departments",
            "search": "Search name / phone",
            "search_placeholder": "Enter name or phone...",

            "people": "Meal attendance list",
            "status": "Status",
            "amount": "Meal amount",
            "department": "Department",
            "person": "Employee",
            "stt": "No.",
            "remark": "Note",
            "phone": "Phone",

            "register": "🟢 Eating",
            "not_eat": "⚪ Not eating",
            "business": "🟠 Business trip",
            "unmarked": "🟡 Unmarked",

            "status_all": "All statuses",
            "status_unmarked": "Unmarked",
            "status_eating": "Eating",
            "status_not_eating": "Not eating",
            "status_business": "Business trip",

            "select_all": "🟢 Mark filtered list eating",
            "unselect_all": "⚪ Mark filtered list not eating",
            "business_all": "🟠 Mark filtered list business trip",

            "saved": "Saved.",
            "save_failed": "Unable to save data.",

            "edit_help": (
                "Changing status saves immediately. "
                "Amount and note are also saved immediately."
            ),

            "total": "Total",
            "registered": "Eating",
            "not_eating": "Not eating",
            "business_trip": "Business trip",
            "unmarked_count": "Unmarked",
            "money": "Total amount",

            "no_people": "No active meal participants.",
            "no_result": "No matching person found.",

            "load_day_error": "Unable to load meal date.",
            "load_people_error": "Unable to load meal participants.",
            "load_register_error": "Unable to load registration data.",

            "not_enough_data": "There is no registration data to confirm.",

            "confirm_title": "Confirm meals",
            "confirm_desc": (
                "After confirmation, the list is saved "
                "as an independent official snapshot."
            ),

            "confirm_button": "🔒 CONFIRM MEALS",

            "confirmed_success": "Meal list confirmed successfully.",
            "confirmed_failed": "Unable to confirm meal list.",

            "confirmed_list": "Official confirmed list",
            "confirmed_at": "Confirmed at",
            "confirmed_by": "Confirmed by",

            "open_confirm": "🔓 OPEN CONFIRMATION",

            "open_confirm_desc": (
                "Opening confirmation removes the current snapshot "
                "and allows registration editing again."
            ),

            "open_confirm_success": (
                "Confirmation opened. You can edit the list again."
            ),

            "open_confirm_failed": "Unable to open confirmation.",

            "status_not_confirmed": "🟡 Not confirmed",
            "status_confirmed": "🟢 Confirmed",

            "no_confirmed": "This date has no confirmed list.",
            "confirm_warning": "The confirmed list uses saved database data.",

            "confirm_note": "Confirmation note",

            "extra_meal": "➕ Extra meals",
            "extra_meal_desc": (
                "For visitors, technical teams or temporary "
                "people without creating a permanent employee record."
            ),
            "extra_name": "Person / group name",
            "extra_name_placeholder": "E.g. Samsung visitors, Technical team...",
            "extra_unit": "Organization",
            "extra_unit_placeholder": "E.g. Samsung, Contractor...",
            "extra_quantity": "Quantity",
            "extra_price": "Unit price",
            "extra_note": "Extra meal note",
            "extra_add": "➕ ADD EXTRA MEAL",
            "extra_added": "Extra meal added.",
            "extra_updated": "Extra meal updated.",
            "extra_deleted": "Extra meal deleted.",
            "extra_empty": "No extra meals.",
            "extra_list": "Extra meal list",
            "extra_type": "Type",
            "extra_total": "Extra meals",
            "extra_money": "Extra amount",
            "extra_edit": "Edit",
            "extra_delete": "Delete",
            "extra_save": "💾 SAVE",
            "extra_cancel": "Cancel",
            "extra_editing": "Editing",
            "extra_people": "Extra",
            "employee": "Employee",
            "generated": "Extra",
            "extra_confirm_warning": (
                "Added extra meals will be included in the confirmed list."
            ),
            "extra_load_error": "Unable to load extra meals.",
            "extra_save_error": "Unable to save extra meal.",

            "quantity": "Quantity",
            "unit_price": "Unit price",
            "total_amount": "Total amount",
        },

        "zh": {
            "header": "🍚 用餐登记",
            "header_desc": "管理每日员工用餐状态。",

            "date": "用餐日期",
            "meal_info": "用餐信息",
            "price": "餐费",
            "note": "备注",
            "create": "创建用餐日期",

            "not_created": "此日期尚未创建。",
            "create_success": "用餐日期已创建。",
            "create_failed": "无法创建用餐日期。",

            "suggested": "上一天餐费",
            "note_placeholder": "用餐日期备注...",

            "workspace": "用餐管理",
            "registration": "📝 用餐登记",
            "confirmed": "📋 已确认名单",

            "filter": "筛选名单",
            "all_department": "所有部门",
            "search": "姓名 / 电话",
            "search_placeholder": "输入姓名或电话...",

            "people": "用餐名单",
            "status": "状态",
            "amount": "餐费",
            "department": "部门",
            "person": "员工",
            "stt": "序号",
            "remark": "备注",
            "phone": "电话",

            "register": "🟢 用餐",
            "not_eat": "⚪ 不用餐",
            "business": "🟠 出差",
            "unmarked": "🟡 未登记",

            "status_all": "所有状态",
            "status_unmarked": "未登记",
            "status_eating": "用餐",
            "status_not_eating": "不用餐",
            "status_business": "出差",

            "select_all": "🟢 当前列表设为用餐",
            "unselect_all": "⚪ 当前列表设为不用餐",
            "business_all": "🟠 当前列表设为出差",

            "saved": "已保存。",
            "save_failed": "保存失败。",

            "edit_help": (
                "修改状态会立即保存。金额和备注也会立即保存。"
            ),

            "total": "总人数",
            "registered": "用餐",
            "not_eating": "不用餐",
            "business_trip": "出差",
            "unmarked_count": "未登记",
            "money": "总金额",

            "no_people": "暂无正在使用的用餐人员。",
            "no_result": "没有找到符合条件的人员。",

            "load_day_error": "无法加载用餐日期。",
            "load_people_error": "无法获取用餐人员。",
            "load_register_error": "无法获取登记数据。",

            "not_enough_data": "暂无可确认的登记数据。",

            "confirm_title": "确认用餐名单",
            "confirm_desc": (
                "确认后，名单会保存为独立的正式快照。"
            ),

            "confirm_button": "🔒 确认用餐",

            "confirmed_success": "用餐名单确认成功。",
            "confirmed_failed": "无法确认用餐名单。",

            "confirmed_list": "正式确认名单",
            "confirmed_at": "确认时间",
            "confirmed_by": "确认人",

            "open_confirm": "🔓 解除确认",

            "open_confirm_desc": (
                "解除确认后将删除当前快照，并允许重新编辑登记。"
            ),

            "open_confirm_success": "已解除确认，可以重新编辑名单。",
            "open_confirm_failed": "无法解除确认。",

            "status_not_confirmed": "🟡 未确认",
            "status_confirmed": "🟢 已确认",

            "no_confirmed": "此日期还没有确认名单。",
            "confirm_warning": "确认名单使用数据库中已保存的数据。",

            "confirm_note": "确认备注",

            "extra_meal": "➕ 临时餐食",
            "extra_meal_desc": (
                "用于访客、技术团队或临时人员，"
                "无需创建正式人员档案。"
            ),
            "extra_name": "人员 / 团队名称",
            "extra_name_placeholder": "例如：三星访客、技术团队...",
            "extra_unit": "单位",
            "extra_unit_placeholder": "例如：三星、承包商...",
            "extra_quantity": "数量",
            "extra_price": "单价",
            "extra_note": "临时餐备注",
            "extra_add": "➕ 添加临时餐",
            "extra_added": "临时餐已添加。",
            "extra_updated": "临时餐已更新。",
            "extra_deleted": "临时餐已删除。",
            "extra_empty": "暂无临时餐。",
            "extra_list": "临时餐名单",
            "extra_type": "类型",
            "extra_total": "临时餐数量",
            "extra_money": "临时餐金额",
            "extra_edit": "编辑",
            "extra_delete": "删除",
            "extra_save": "💾 保存",
            "extra_cancel": "取消",
            "extra_editing": "编辑中",
            "extra_people": "临时",
            "employee": "员工",
            "generated": "临时",
            "extra_confirm_warning": "已添加的临时餐会进入正式确认名单。",
            "extra_load_error": "无法获取临时餐数据。",
            "extra_save_error": "无法保存临时餐。",

            "quantity": "数量",
            "unit_price": "单价",
            "total_amount": "总金额",
        },
    }

    text = texts.get(language, texts["vi"])

    hien_thi_header(
        text["header"],
        text["header_desc"]
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        ngay_chon = st.date_input(
            text["date"],
            value=date.today(),
            format="DD/MM/YYYY"
        )

    ngay_str = ngay_chon.strftime("%Y-%m-%d")

    result_ngay = NgayAnController.tim_theo_ngay(
        ngay_str
    )

    if not result_ngay.get("success", False):
        st.error(
            result_ngay.get(
                "message",
                text["load_day_error"]
            )
        )
        return

    ngay_an = result_ngay.get("data")

    if not ngay_an:

        st.info(text["not_created"])

        don_gia_mac_dinh = 30000

        try:
            result_truoc = NgayAnController.lay_ngay_truoc_do(
                ngay_str
            )

            if result_truoc.get("success", False):

                ngay_truoc = result_truoc.get("data")

                if (
                    ngay_truoc
                    and ngay_truoc[2] is not None
                ):
                    don_gia_mac_dinh = int(
                        ngay_truoc[2]
                    )

        except Exception:
            don_gia_mac_dinh = 30000

        hien_thi_tieu_de_section(
            text["meal_info"],
            "⚙️"
        )

        col1, col2 = st.columns(2)

        with col1:

            don_gia = st.number_input(
                text["price"],
                min_value=0,
                step=1000,
                value=don_gia_mac_dinh,
                format="%d"
            )

            st.caption(
                f"{text['suggested']}: "
                f"{don_gia_mac_dinh:,.0f} đ"
            )

        with col2:

            ghi_chu = st.text_input(
                text["note"],
                placeholder=text["note_placeholder"]
            )

        if st.button(
            text["create"],
            type="primary",
            width="stretch"
        ):

            result = NgayAnController.tao_ngay_an(
                ngay=ngay_str,
                don_gia_mac_dinh=don_gia,
                ghi_chu=ghi_chu
            )

            if result.get("success", False):

                st.success(
                    result.get(
                        "message",
                        text["create_success"]
                    )
                )

                st.rerun()

            else:

                st.error(
                    result.get(
                        "message",
                        text["create_failed"]
                    )
                )

        return

    ngay_an_id = ngay_an[0]

    don_gia = ngay_an[2]

    if don_gia is None:
        don_gia = 0

    don_gia = int(don_gia)

    trang_thai_chot = ChotSuatAnController.lay_trang_thai(
        ngay_an_id
    )

    da_chot = bool(
        trang_thai_chot.get(
            "da_chot",
            False
        )
    )

    result_nguoi = (
        NguoiAnController.lay_danh_sach_dang_hoat_dong()
    )

    if not result_nguoi.get("success", False):

        st.error(
            result_nguoi.get(
                "message",
                text["load_people_error"]
            )
        )

        return

    danh_sach = result_nguoi.get(
        "data",
        []
    )

    if not danh_sach:

        st.info(text["no_people"])

    result_cham = ChiTietAnController.lay_theo_ngay(
        ngay_an_id
    )

    if not result_cham.get("success", False):

        st.error(
            result_cham.get(
                "message",
                text["load_register_error"]
            )
        )

        return

    du_lieu_da_luu = result_cham.get(
        "data",
        []
    )

    du_lieu_theo_nguoi = {}

    for item in du_lieu_da_luu:

        try:

            nguoi_an_id = int(item[1])

            trang_thai = (
                item[8]
                if len(item) > 8 and item[8]
                else (
                    "Đăng ký"
                    if bool(item[5])
                    else "Không ăn"
                )
            )

            so_tien = item[6] or 0
            ghi_chu = item[7] or ""

            du_lieu_theo_nguoi[nguoi_an_id] = {
                "chi_tiet_id": item[0],
                "trang_thai": trang_thai,
                "so_tien": int(float(so_tien)),
                "ghi_chu": ghi_chu,
            }

        except (
            IndexError,
            TypeError,
            ValueError
        ):
            continue

    try:

        danh_sach_phat_sinh = (
            SuatAnPhatSinhController.lay_theo_ngay(
                ngay_an_id
            )
        )

    except Exception as exc:

        st.error(
            f"{text['extra_load_error']} {exc}"
        )

        return

    tong_dang_ky = 0
    tong_khong_an = 0
    tong_cong_tac = 0
    tong_chua_cham = 0
    tong_tien = 0

    for nguoi in danh_sach:

        try:
            nguoi_an_id = int(nguoi[0])
        except (
            TypeError,
            ValueError,
            IndexError
        ):
            continue

        du_lieu = du_lieu_theo_nguoi.get(
            nguoi_an_id
        )

        if du_lieu is None:

            tong_chua_cham += 1
            continue

        trang_thai = du_lieu["trang_thai"]
        so_tien = du_lieu["so_tien"]

        if trang_thai == "Đăng ký":

            tong_dang_ky += 1
            tong_tien += so_tien

        elif trang_thai == "Đi công tác":

            tong_cong_tac += 1

        elif trang_thai == "Không ăn":

            tong_khong_an += 1

        else:

            tong_chua_cham += 1

    tong_phat_sinh_suat = 0
    tong_phat_sinh_tien = 0

    for item in danh_sach_phat_sinh:

        try:
            so_luong = int(item[4] or 0)
        except (
            TypeError,
            ValueError,
            IndexError
        ):
            so_luong = 0

        try:
            don_gia_phat_sinh = float(item[5] or 0)
        except (
            TypeError,
            ValueError,
            IndexError
        ):
            don_gia_phat_sinh = 0

        tong_phat_sinh_suat += so_luong
        tong_phat_sinh_tien += (
            so_luong * don_gia_phat_sinh
        )

    tong_so_nguoi = len(danh_sach)

    hien_thi_tieu_de_section(
        text["meal_info"],
        "📅"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        hien_thi_the(
            text["date"],
            ngay_chon.strftime("%d/%m/%Y"),
            "📅"
        )

    with col2:
        hien_thi_the(
            text["price"],
            f"{don_gia:,.0f} đ",
            "💰"
        )

    with col3:
        hien_thi_the(
            text["total"],
            tong_so_nguoi,
            "👥"
        )

    with col4:

        if da_chot:

            hien_thi_the(
                text["status_confirmed"],
                "✓",
                "🔒"
            )

        else:

            hien_thi_the(
                text["status_not_confirmed"],
                "—",
                "🔓"
            )

    st.markdown("")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        hien_thi_the(
            text["total"],
            tong_so_nguoi,
            "👥"
        )

    with col2:
        hien_thi_the(
            text["registered"],
            tong_dang_ky,
            "🟢"
        )

    with col3:
        hien_thi_the(
            text["not_eating"],
            tong_khong_an,
            "⚪"
        )

    with col4:
        hien_thi_the(
            text["business_trip"],
            tong_cong_tac,
            "🟠"
        )

    with col5:
        hien_thi_the(
            text["unmarked_count"],
            tong_chua_cham,
            "🟡"
        )

    with col6:
        hien_thi_the(
            text["money"],
            f"{tong_tien:,.0f} đ",
            "💰"
        )

    st.markdown("")

    che_do_key = f"meal_workspace_{ngay_str}"

    if da_chot:

        che_do_options = [
            text["confirmed"]
        ]

    else:

        che_do_options = [
            text["registration"],
            text["confirmed"]
        ]

    che_do = st.radio(
        text["workspace"],
        che_do_options,
        horizontal=True,
        key=che_do_key
    )

    if che_do == text["registration"]:

        if da_chot:

            st.success(
                f"{text['status_confirmed']} • "
                f"{trang_thai_chot.get('ngay_chot') or ''}"
            )

            st.info(
                text["open_confirm_desc"]
            )

            if st.button(
                text["open_confirm"],
                type="secondary",
                width="stretch",
                key=f"open_confirm_{ngay_str}"
            ):

                try:

                    ChotSuatAnController.mo_chot(
                        ngay_an_id
                    )

                    st.success(
                        text["open_confirm_success"]
                    )

                    st.rerun()

                except Exception as exc:

                    st.error(
                        f"{text['open_confirm_failed']} "
                        f"{exc}"
                    )

            return

        hien_thi_tieu_de_section(
            text["people"],
            "👥"
        )

        st.caption(
            f"💡 {text['edit_help']}"
        )

        bo_phan_map = {}

        for nguoi in danh_sach:

            try:

                ten_bo_phan = (
                    nguoi[4]
                    if nguoi[4]
                    else "Chưa phân bộ phận"
                )

                bo_phan_map[str(ten_bo_phan)] = str(
                    ten_bo_phan
                )

            except (
                IndexError,
                TypeError
            ):
                continue

        danh_sach_bo_phan = [
            text["all_department"]
        ]

        danh_sach_bo_phan.extend(
            sorted(
                bo_phan_map.values(),
                key=lambda x: x.lower()
            )
        )

        col1, col2, col3 = st.columns(
            [1.2, 1.2, 2]
        )

        with col1:

            bo_phan_chon = st.selectbox(
                text["department"],
                danh_sach_bo_phan,
                key=f"filter_department_{ngay_str}"
            )

        with col2:

            trang_thai_loc = st.selectbox(
                text["status"],
                [
                    text["status_all"],
                    text["status_unmarked"],
                    text["status_eating"],
                    text["status_not_eating"],
                    text["status_business"],
                ],
                key=f"filter_status_{ngay_str}"
            )

        with col3:

            tu_khoa = st.text_input(
                text["search"],
                placeholder=text["search_placeholder"],
                key=f"filter_search_{ngay_str}"
            )

        danh_sach_hien_thi = []

        for nguoi in danh_sach:

            try:

                nguoi_an_id = int(nguoi[0])
                ho_ten = str(nguoi[1] or "")
                sdt = str(nguoi[2] or "")
                ten_bo_phan = (
                    nguoi[4]
                    if nguoi[4]
                    else "Chưa phân bộ phận"
                )

            except (
                IndexError,
                TypeError,
                ValueError
            ):
                continue

            du_lieu = du_lieu_theo_nguoi.get(
                nguoi_an_id
            )

            if du_lieu is None:

                trang_thai_db = "Chưa chấm"

            else:

                trang_thai_db = du_lieu["trang_thai"]

            if (
                bo_phan_chon
                != text["all_department"]
            ):

                if str(ten_bo_phan) != str(
                    bo_phan_chon
                ):
                    continue

            if tu_khoa.strip():

                keyword = tu_khoa.strip().lower()

                if (
                    keyword not in ho_ten.lower()
                    and keyword not in sdt.lower()
                ):
                    continue

            if (
                trang_thai_loc
                != text["status_all"]
            ):

                if (
                    trang_thai_loc
                    == text["status_unmarked"]
                ):

                    if trang_thai_db != "Chưa chấm":
                        continue

                elif (
                    trang_thai_loc
                    == text["status_eating"]
                ):

                    if trang_thai_db != "Đăng ký":
                        continue

                elif (
                    trang_thai_loc
                    == text["status_not_eating"]
                ):

                    if trang_thai_db != "Không ăn":
                        continue

                elif (
                    trang_thai_loc
                    == text["status_business"]
                ):

                    if trang_thai_db != "Đi công tác":
                        continue

            danh_sach_hien_thi.append(
                nguoi
            )

        col1, col2, col3 = st.columns(3)

        def _luu_nguoi(
            nguoi_an_id,
            trang_thai_db,
            so_tien,
            ghi_chu
        ):

            try:

                nguoi_an_id = int(
                    nguoi_an_id
                )

                if trang_thai_db == "Đăng ký":

                    da_an = 1

                    if so_tien <= 0:
                        so_tien = don_gia

                elif trang_thai_db == "Đi công tác":

                    da_an = 0
                    so_tien = 0

                elif trang_thai_db == "Không ăn":

                    da_an = 0
                    so_tien = 0

                else:

                    return {
                        "success": True,
                        "message": "Chưa chấm"
                    }

                du_lieu_cu = (
                    du_lieu_theo_nguoi.get(
                        nguoi_an_id
                    )
                )

                if du_lieu_cu:

                    result = (
                        ChiTietAnController.cap_nhat(
                            chi_tiet_id=du_lieu_cu[
                                "chi_tiet_id"
                            ],
                            da_an=da_an,
                            so_tien_phai_tra=so_tien,
                            ghi_chu=(
                                ghi_chu
                                or None
                            ),
                            trang_thai=trang_thai_db
                        )
                    )

                else:

                    result = (
                        ChiTietAnController.them_chi_tiet(
                            nguoi_an_id=nguoi_an_id,
                            ngay_an_id=ngay_an_id,
                            da_an=da_an,
                            so_tien_phai_tra=so_tien,
                            ghi_chu=(
                                ghi_chu
                                or None
                            ),
                            trang_thai=trang_thai_db
                        )
                    )

                return result

            except Exception as exc:

                return {
                    "success": False,
                    "message": str(exc)
                }

        def _luu_status_callback(
            nguoi_an_id,
            widget_key
        ):

            value = st.session_state.get(
                widget_key
            )

            if value is None:
                return

            if value == text["unmarked"]:
                return

            if value == text["register"]:

                trang_thai_db = "Đăng ký"

            elif value == text["business"]:

                trang_thai_db = "Đi công tác"

            else:

                trang_thai_db = "Không ăn"

            du_lieu_cu = (
                du_lieu_theo_nguoi.get(
                    nguoi_an_id
                )
            )

            if du_lieu_cu:

                so_tien = du_lieu_cu["so_tien"]
                ghi_chu = du_lieu_cu["ghi_chu"]

            else:

                so_tien = don_gia
                ghi_chu = ""

            result = _luu_nguoi(
                nguoi_an_id,
                trang_thai_db,
                so_tien,
                ghi_chu
            )

            if not result.get(
                "success",
                False
            ):

                st.session_state[
                    f"meal_error_{ngay_str}"
                ] = result.get(
                    "message",
                    text["save_failed"]
                )

        def _luu_amount_callback(
            nguoi_an_id,
            widget_key
        ):

            value = st.session_state.get(
                widget_key,
                0
            )

            try:

                so_tien = int(
                    float(value or 0)
                )

            except (
                TypeError,
                ValueError
            ):

                so_tien = 0

            du_lieu_cu = (
                du_lieu_theo_nguoi.get(
                    nguoi_an_id
                )
            )

            if du_lieu_cu:

                trang_thai_db = (
                    du_lieu_cu["trang_thai"]
                )

                ghi_chu = (
                    du_lieu_cu["ghi_chu"]
                )

            else:

                return

            if trang_thai_db != "Đăng ký":
                return

            result = _luu_nguoi(
                nguoi_an_id,
                trang_thai_db,
                so_tien,
                ghi_chu
            )

            if not result.get(
                "success",
                False
            ):

                st.session_state[
                    f"meal_error_{ngay_str}"
                ] = result.get(
                    "message",
                    text["save_failed"]
                )

        def _luu_note_callback(
            nguoi_an_id,
            widget_key
        ):

            ghi_chu = st.session_state.get(
                widget_key,
                ""
            )

            du_lieu_cu = (
                du_lieu_theo_nguoi.get(
                    nguoi_an_id
                )
            )

            if not du_lieu_cu:
                return

            trang_thai_db = (
                du_lieu_cu["trang_thai"]
            )

            so_tien = (
                du_lieu_cu["so_tien"]
            )

            result = _luu_nguoi(
                nguoi_an_id,
                trang_thai_db,
                so_tien,
                str(ghi_chu).strip()
            )

            if not result.get(
                "success",
                False
            ):

                st.session_state[
                    f"meal_error_{ngay_str}"
                ] = result.get(
                    "message",
                    text["save_failed"]
                )

        # ==========================================================
        # CÁC NÚT CHẤM NHANH
        # ==========================================================
        #
        # Không pop status_key nữa.
        #
        # Sau khi lưu DB, ghi trực tiếp giá trị mới vào
        # st.session_state của selectbox.
        #
        # Đồng thời cập nhật tiền cơm tương ứng.
        #
        # Khi st.rerun(), selectbox sẽ hiển thị đúng trạng thái
        # vừa chấm nhanh.
        # ==========================================================

        with col1:

            if st.button(
                text["select_all"],
                width="stretch",
                key=f"quick_all_{ngay_str}"
            ):

                success = True

                for nguoi in danh_sach_hien_thi:

                    try:

                        nguoi_an_id = int(
                            nguoi[0]
                        )

                        du_lieu_cu = (
                            du_lieu_theo_nguoi.get(
                                nguoi_an_id
                            )
                        )

                        ghi_chu = (
                            du_lieu_cu["ghi_chu"]
                            if du_lieu_cu
                            else ""
                        )

                        result = _luu_nguoi(
                            nguoi_an_id,
                            "Đăng ký",
                            don_gia,
                            ghi_chu
                        )

                        if not result.get(
                            "success",
                            False
                        ):

                            success = False

                            st.error(
                                result.get(
                                    "message",
                                    text["save_failed"]
                                )
                            )

                            break

                        status_key = (
                            f"meal_status_"
                            f"{ngay_str}_"
                            f"{nguoi_an_id}"
                        )

                        amount_key = (
                            f"meal_amount_"
                            f"{ngay_str}_"
                            f"{nguoi_an_id}"
                        )

                        st.session_state[
                            status_key
                        ] = text["register"]

                        st.session_state[
                            amount_key
                        ] = int(don_gia)

                    except Exception as exc:

                        success = False

                        st.error(
                            f"{text['save_failed']} "
                            f"{exc}"
                        )

                        break

                if success:

                    st.success(
                        text["saved"]
                    )

                    st.rerun()

        with col2:

            if st.button(
                text["unselect_all"],
                width="stretch",
                key=f"quick_none_{ngay_str}"
            ):

                success = True

                for nguoi in danh_sach_hien_thi:

                    try:

                        nguoi_an_id = int(
                            nguoi[0]
                        )

                        du_lieu_cu = (
                            du_lieu_theo_nguoi.get(
                                nguoi_an_id
                            )
                        )

                        ghi_chu = (
                            du_lieu_cu["ghi_chu"]
                            if du_lieu_cu
                            else ""
                        )

                        result = _luu_nguoi(
                            nguoi_an_id,
                            "Không ăn",
                            0,
                            ghi_chu
                        )

                        if not result.get(
                            "success",
                            False
                        ):

                            success = False

                            st.error(
                                result.get(
                                    "message",
                                    text["save_failed"]
                                )
                            )

                            break

                        status_key = (
                            f"meal_status_"
                            f"{ngay_str}_"
                            f"{nguoi_an_id}"
                        )

                        amount_key = (
                            f"meal_amount_"
                            f"{ngay_str}_"
                            f"{nguoi_an_id}"
                        )

                        st.session_state[
                            status_key
                        ] = text["not_eat"]

                        st.session_state[
                            amount_key
                        ] = 0

                    except Exception as exc:

                        success = False

                        st.error(
                            f"{text['save_failed']} "
                            f"{exc}"
                        )

                        break

                if success:

                    st.success(
                        text["saved"]
                    )

                    st.rerun()

        with col3:

            if st.button(
                text["business_all"],
                width="stretch",
                key=f"quick_business_{ngay_str}"
            ):

                success = True

                for nguoi in danh_sach_hien_thi:

                    try:

                        nguoi_an_id = int(
                            nguoi[0]
                        )

                        du_lieu_cu = (
                            du_lieu_theo_nguoi.get(
                                nguoi_an_id
                            )
                        )

                        ghi_chu = (
                            du_lieu_cu["ghi_chu"]
                            if du_lieu_cu
                            else ""
                        )

                        result = _luu_nguoi(
                            nguoi_an_id,
                            "Đi công tác",
                            0,
                            ghi_chu
                        )

                        if not result.get(
                            "success",
                            False
                        ):

                            success = False

                            st.error(
                                result.get(
                                    "message",
                                    text["save_failed"]
                                )
                            )

                            break

                        status_key = (
                            f"meal_status_"
                            f"{ngay_str}_"
                            f"{nguoi_an_id}"
                        )

                        amount_key = (
                            f"meal_amount_"
                            f"{ngay_str}_"
                            f"{nguoi_an_id}"
                        )

                        st.session_state[
                            status_key
                        ] = text["business"]

                        st.session_state[
                            amount_key
                        ] = 0

                    except Exception as exc:

                        success = False

                        st.error(
                            f"{text['save_failed']} "
                            f"{exc}"
                        )

                        break

                if success:

                    st.success(
                        text["saved"]
                    )

                    st.rerun()

        st.markdown("")

        if not danh_sach_hien_thi:

            st.info(text["no_result"])

        else:

            st.caption(
                f"{len(danh_sach_hien_thi)} / "
                f"{len(danh_sach)}"
            )

            header_col1, header_col2, header_col3, header_col4 = st.columns(
                [0.35, 2.4, 1.7, 2.4]
            )

            with header_col1:
                st.caption(text["stt"])

            with header_col2:
                st.caption(text["person"])

            with header_col3:
                st.caption(text["status"])

            with header_col4:
                st.caption(
                    f"{text['amount']} / {text['remark']}"
                )

            for index, nguoi in enumerate(
                danh_sach_hien_thi,
                start=1
            ):

                nguoi_an_id = int(
                    nguoi[0]
                )

                ho_ten = str(
                    nguoi[1] or ""
                )

                sdt = str(
                    nguoi[2] or ""
                )

                ten_bo_phan = (
                    nguoi[4]
                    if nguoi[4]
                    else "Chưa phân bộ phận"
                )

                du_lieu = (
                    du_lieu_theo_nguoi.get(
                        nguoi_an_id
                    )
                )

                if du_lieu:

                    trang_thai_db = (
                        du_lieu["trang_thai"]
                    )

                    so_tien_hien_tai = (
                        du_lieu["so_tien"]
                    )

                    ghi_chu_hien_tai = (
                        du_lieu["ghi_chu"]
                    )

                else:

                    trang_thai_db = "Chưa chấm"
                    so_tien_hien_tai = 0
                    ghi_chu_hien_tai = ""

                if trang_thai_db == "Đăng ký":

                    status_hien_thi = text["register"]

                elif trang_thai_db == "Không ăn":

                    status_hien_thi = text["not_eat"]

                elif trang_thai_db == "Đi công tác":

                    status_hien_thi = text["business"]

                else:

                    status_hien_thi = text["unmarked"]

                status_key = (
                    f"meal_status_"
                    f"{ngay_str}_"
                    f"{nguoi_an_id}"
                )

                amount_key = (
                    f"meal_amount_"
                    f"{ngay_str}_"
                    f"{nguoi_an_id}"
                )

                note_key = (
                    f"meal_note_"
                    f"{ngay_str}_"
                    f"{nguoi_an_id}"
                )

                status_options = [
                    text["unmarked"],
                    text["register"],
                    text["not_eat"],
                    text["business"],
                ]

                # ==================================================
                # ĐỒNG BỘ STATE TỪ DATABASE
                # ==================================================
                #
                # Không truyền index= vào selectbox.
                # Giá trị của selectbox được quản lý duy nhất
                # thông qua st.session_state.
                # ==================================================

                current_status_state = (
                    st.session_state.get(
                        status_key
                    )
                )

                if current_status_state is None:

                    st.session_state[
                        status_key
                    ] = status_hien_thi

                elif current_status_state not in status_options:

                    st.session_state[
                        status_key
                    ] = status_hien_thi

                elif (
                    current_status_state
                    == text["unmarked"]
                    and status_hien_thi
                    != text["unmarked"]
                ):

                    st.session_state[
                        status_key
                    ] = status_hien_thi

                col1, col2, col3, col4 = st.columns(
                    [0.35, 2.4, 1.7, 2.4]
                )

                with col1:

                    st.write(
                        f"**{index}**"
                    )

                with col2:

                    st.write(
                        f"**{ho_ten}**"
                    )

                    thong_tin_phu = []

                    if ten_bo_phan:
                        thong_tin_phu.append(
                            str(ten_bo_phan)
                        )

                    if sdt:
                        thong_tin_phu.append(
                            f"{text['phone']}: {sdt}"
                        )

                    if thong_tin_phu:

                        st.caption(
                            " • ".join(
                                thong_tin_phu
                            )
                        )

                with col3:

                    # ==================================================
                    # FIX STREAMLIT SESSION STATE
                    # ==================================================
                    #
                    # Không dùng index=selected_index ở đây.
                    # status_key đã được khởi tạo trong session_state
                    # ở phía trên.
                    # ==================================================

                    st.selectbox(
                        text["status"],
                        status_options,
                        key=status_key,
                        on_change=_luu_status_callback,
                        args=(
                            nguoi_an_id,
                            status_key,
                        ),
                        label_visibility="collapsed"
                    )

                with col4:

                    if trang_thai_db == "Đăng ký":

                        amount_value = int(
                            so_tien_hien_tai
                            or don_gia
                        )

                    else:

                        amount_value = 0

                    amount_col, note_col = st.columns(
                        [1, 1.25]
                    )

                    with amount_col:

                        # Khởi tạo state tiền nếu chưa có.
                        # Không truyền value= vào number_input.
                        if amount_key not in st.session_state:

                            st.session_state[
                                amount_key
                            ] = amount_value

                        st.number_input(
                            text["amount"],
                            min_value=0,
                            step=1000,
                            format="%d",
                            key=amount_key,
                            disabled=(
                                trang_thai_db
                                != "Đăng ký"
                            ),
                            on_change=_luu_amount_callback,
                            args=(
                                nguoi_an_id,
                                amount_key,
                            ),
                            label_visibility="collapsed"
                        )

                    with note_col:

                        st.text_input(
                            text["remark"],
                            value=ghi_chu_hien_tai,
                            key=note_key,
                            on_change=_luu_note_callback,
                            args=(
                                nguoi_an_id,
                                note_key,
                            ),
                            label_visibility="collapsed",
                            placeholder=text["remark"]
                        )

            if index < len(
                danh_sach_hien_thi
            ):

                st.divider()

        meal_error_key = (
            f"meal_error_{ngay_str}"
        )

        if st.session_state.get(
            meal_error_key
        ):

            st.error(
                st.session_state.pop(
                    meal_error_key
                )
            )

        hien_thi_tieu_de_section(
            text["extra_meal"],
            "➕"
        )

        st.caption(
            text["extra_meal_desc"]
        )

        with st.expander(
            text["extra_meal"],
            expanded=False
        ):

            col1, col2 = st.columns(2)

            with col1:

                extra_name = st.text_input(
                    text["extra_name"],
                    placeholder=text["extra_name_placeholder"],
                    key=f"extra_name_{ngay_str}"
                )

            with col2:

                extra_unit = st.text_input(
                    text["extra_unit"],
                    placeholder=text["extra_unit_placeholder"],
                    key=f"extra_unit_{ngay_str}"
                )

            col1, col2, col3 = st.columns(3)

            with col1:

                extra_quantity = st.number_input(
                    text["extra_quantity"],
                    min_value=1,
                    step=1,
                    value=1,
                    key=f"extra_quantity_{ngay_str}"
                )

            with col2:

                extra_price = st.number_input(
                    text["extra_price"],
                    min_value=0,
                    step=1000,
                    value=don_gia,
                    format="%d",
                    key=f"extra_price_{ngay_str}"
                )

            with col3:

                extra_note = st.text_input(
                    text["extra_note"],
                    key=f"extra_note_{ngay_str}"
                )

            if st.button(
                text["extra_add"],
                type="primary",
                width="stretch",
                key=f"extra_add_{ngay_str}"
            ):

                if not extra_name.strip():

                    st.error(
                        f"{text['extra_name']}: "
                        f"không được để trống."
                    )

                else:

                    try:

                        SuatAnPhatSinhController.them(
                            ngay_an_id=ngay_an_id,
                            ho_ten=extra_name,
                            don_vi=extra_unit,
                            so_luong=extra_quantity,
                            don_gia=extra_price,
                            ghi_chu=extra_note
                        )

                        st.success(
                            text["extra_added"]
                        )

                        st.rerun()

                    except Exception as exc:

                        st.error(
                            f"{text['extra_save_error']} "
                            f"{exc}"
                        )

        if danh_sach_phat_sinh:

            hien_thi_tieu_de_section(
                text["extra_list"],
                "📋"
            )

            for item in danh_sach_phat_sinh:

                suat_id = item[0]
                ho_ten = item[2] or ""
                don_vi = item[3] or ""
                so_luong = item[4] or 1
                don_gia_ps = item[5] or 0
                ghi_chu_ps = item[6] or ""

                edit_key = (
                    f"extra_editing_"
                    f"{ngay_str}_"
                    f"{suat_id}"
                )

                if st.session_state.get(
                    edit_key,
                    False
                ):

                    st.info(
                        f"{text['extra_editing']}: "
                        f"{ho_ten}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        edit_name = st.text_input(
                            text["extra_name"],
                            value=ho_ten,
                            key=f"edit_name_{suat_id}"
                        )

                    with col2:

                        edit_unit = st.text_input(
                            text["extra_unit"],
                            value=don_vi,
                            key=f"edit_unit_{suat_id}"
                        )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        edit_quantity = st.number_input(
                            text["extra_quantity"],
                            min_value=1,
                            step=1,
                            value=int(so_luong),
                            key=f"edit_quantity_{suat_id}"
                        )

                    with col2:

                        edit_price = st.number_input(
                            text["extra_price"],
                            min_value=0,
                            step=1000,
                            value=int(float(don_gia_ps)),
                            format="%d",
                            key=f"edit_price_{suat_id}"
                        )

                    with col3:

                        edit_note = st.text_input(
                            text["extra_note"],
                            value=ghi_chu_ps,
                            key=f"edit_note_{suat_id}"
                        )

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            text["extra_save"],
                            type="primary",
                            width="stretch",
                            key=f"extra_save_{suat_id}"
                        ):

                            try:

                                SuatAnPhatSinhController.cap_nhat(
                                    suat_an_id=suat_id,
                                    ho_ten=edit_name,
                                    don_vi=edit_unit,
                                    so_luong=edit_quantity,
                                    don_gia=edit_price,
                                    ghi_chu=edit_note
                                )

                                st.session_state[
                                    edit_key
                                ] = False

                                st.success(
                                    text["extra_updated"]
                                )

                                st.rerun()

                            except Exception as exc:

                                st.error(
                                    f"{text['extra_save_error']} "
                                    f"{exc}"
                                )

                    with col2:

                        if st.button(
                            text["extra_cancel"],
                            width="stretch",
                            key=f"extra_cancel_{suat_id}"
                        ):

                            st.session_state[
                                edit_key
                            ] = False

                            st.rerun()

                else:

                    col1, col2, col3, col4, col5 = st.columns(
                        [2.3, 1.5, 0.8, 1.2, 1.2]
                    )

                    with col1:

                        st.write(
                            f"**{ho_ten}**"
                        )

                        if don_vi:
                            st.caption(don_vi)

                        if ghi_chu_ps:
                            st.caption(ghi_chu_ps)

                    with col2:

                        st.write(
                            f"{so_luong} "
                            f"{text['quantity'].lower()}"
                        )

                    with col3:

                        st.write(
                            f"{float(don_gia_ps):,.0f}"
                        )

                    with col4:

                        thanh_tien = (
                            int(so_luong)
                            * float(don_gia_ps)
                        )

                        st.write(
                            f"{thanh_tien:,.0f} đ"
                        )

                    with col5:

                        edit_col, delete_col = st.columns(2)

                        with edit_col:

                            if st.button(
                                "✏️",
                                key=f"extra_edit_{suat_id}",
                                help=text["extra_edit"]
                            ):

                                st.session_state[
                                    edit_key
                                ] = True

                                st.rerun()

                        with delete_col:

                            if st.button(
                                "🗑️",
                                key=f"extra_delete_{suat_id}",
                                help=text["extra_delete"]
                            ):

                                try:

                                    SuatAnPhatSinhController.xoa(
                                        suat_id
                                    )

                                    st.success(
                                        text["extra_deleted"]
                                    )

                                    st.rerun()

                                except Exception as exc:

                                    st.error(
                                        f"{text['extra_save_error']} "
                                        f"{exc}"
                                    )

            col1, col2 = st.columns(2)

            with col1:

                hien_thi_the(
                    text["extra_total"],
                    tong_phat_sinh_suat,
                    "➕"
                )

            with col2:

                hien_thi_the(
                    text["extra_money"],
                    f"{tong_phat_sinh_tien:,.0f} đ",
                    "💰"
                )

        else:

            st.caption(
                text["extra_empty"]
            )

        st.markdown("")

        hien_thi_tieu_de_section(
            text["confirm_title"],
            "🔒"
        )

        st.info(
            text["confirm_warning"]
        )

        st.info(
            text["extra_confirm_warning"]
        )

        col1, col2 = st.columns([3, 1])

        with col1:

            ghi_chu_chot = st.text_input(
                text["confirm_note"],
                placeholder=text["note_placeholder"],
                key=f"confirm_note_{ngay_str}"
            )

        with col2:

            if st.button(
                text["confirm_button"],
                type="primary",
                width="stretch",
                key=f"confirm_meal_{ngay_str}"
            ):

                try:

                    result_saved = (
                        ChiTietAnController.lay_theo_ngay(
                            ngay_an_id
                        )
                    )

                    if not result_saved.get(
                        "success",
                        False
                    ):

                        raise ValueError(
                            result_saved.get(
                                "message",
                                text["load_register_error"]
                            )
                        )

                    rows_saved = result_saved.get(
                        "data",
                        []
                    )

                    nguoi_map = {}

                    for nguoi in danh_sach:

                        try:

                            nguoi_map[
                                int(nguoi[0])
                            ] = nguoi

                        except (
                            TypeError,
                            ValueError
                        ):
                            continue

                    danh_sach_chot = []
                    da_co_id = set()

                    for item in rows_saved:

                        try:

                            nguoi_an_id = int(
                                item[1]
                            )

                            nguoi = nguoi_map.get(
                                nguoi_an_id
                            )

                            if nguoi:

                                ho_ten = str(
                                    nguoi[1]
                                )

                                bo_phan = (
                                    nguoi[4]
                                    if nguoi[4]
                                    else "Chưa phân bộ phận"
                                )

                            else:

                                ho_ten = str(
                                    item[2]
                                )

                                bo_phan = (
                                    "Chưa phân bộ phận"
                                )

                            trang_thai = (
                                item[8]
                                if len(item) > 8 and item[8]
                                else (
                                    "Đăng ký"
                                    if bool(item[5])
                                    else "Không ăn"
                                )
                            )

                            so_tien = item[6] or 0
                            ghi_chu = item[7] or ""

                            danh_sach_chot.append(
                                {
                                    "nguoi_an_id":
                                        nguoi_an_id,
                                    "ho_ten":
                                        ho_ten,
                                    "bo_phan":
                                        bo_phan,
                                    "trang_thai":
                                        trang_thai,
                                    "so_tien":
                                        float(so_tien),
                                    "ghi_chu":
                                        ghi_chu,
                                    "loai_nguoi":
                                        "Nhân viên",
                                    "suat_an_phat_sinh_id":
                                        None,
                                    "so_luong":
                                        1,
                                    "don_gia":
                                        float(so_tien),
                                }
                            )

                            da_co_id.add(
                                nguoi_an_id
                            )

                        except (
                            IndexError,
                            TypeError,
                            ValueError
                        ):
                            continue

                    for nguoi in danh_sach:

                        try:

                            nguoi_an_id = int(
                                nguoi[0]
                            )

                        except (
                            TypeError,
                            ValueError
                        ):
                            continue

                        if nguoi_an_id in da_co_id:
                            continue

                        danh_sach_chot.append(
                            {
                                "nguoi_an_id":
                                    nguoi_an_id,
                                "ho_ten":
                                    str(nguoi[1]),
                                "bo_phan":
                                    (
                                        nguoi[4]
                                        if nguoi[4]
                                        else "Chưa phân bộ phận"
                                    ),
                                "trang_thai":
                                    "Chưa chấm",
                                "so_tien":
                                    0.0,
                                "ghi_chu":
                                    "",
                                "loai_nguoi":
                                    "Nhân viên",
                                "suat_an_phat_sinh_id":
                                    None,
                                "so_luong":
                                    1,
                                "don_gia":
                                    0.0,
                            }
                        )

                    for item in danh_sach_phat_sinh:

                        try:

                            suat_id = int(
                                item[0]
                            )

                            ho_ten = str(
                                item[2]
                            )

                            don_vi = str(
                                item[3] or ""
                            ).strip()

                            so_luong = int(
                                item[4] or 1
                            )

                            don_gia_ps = float(
                                item[5] or 0
                            )

                            ghi_chu_ps = (
                                item[6] or ""
                            )

                            bo_phan_ps = (
                                don_vi
                                if don_vi
                                else text["generated"]
                            )

                            so_tien_ps = (
                                so_luong
                                * don_gia_ps
                            )

                            danh_sach_chot.append(
                                {
                                    "nguoi_an_id":
                                        None,
                                    "ho_ten":
                                        ho_ten,
                                    "bo_phan":
                                        bo_phan_ps,
                                    "trang_thai":
                                        "Đăng ký",
                                    "so_tien":
                                        so_tien_ps,
                                    "ghi_chu":
                                        ghi_chu_ps,
                                    "loai_nguoi":
                                        "Phát sinh",
                                    "suat_an_phat_sinh_id":
                                        suat_id,
                                    "so_luong":
                                        so_luong,
                                    "don_gia":
                                        don_gia_ps,
                                }
                            )

                        except (
                            IndexError,
                            TypeError,
                            ValueError
                        ):
                            continue

                    if not danh_sach_chot:

                        raise ValueError(
                            text["not_enough_data"]
                        )

                    ChotSuatAnController.chot_suat_an(
                        ngay_an_id=ngay_an_id,
                        danh_sach=danh_sach_chot,
                        nguoi_chot="Chính tôi",
                        ghi_chu=(
                            ghi_chu_chot
                            or None
                        )
                    )

                    st.success(
                        text["confirmed_success"]
                    )

                    st.rerun()

                except Exception as exc:

                    st.error(
                        f"{text['confirmed_failed']} "
                        f"{exc}"
                    )

        return

    hien_thi_tieu_de_section(
        text["confirmed_list"],
        "📋"
    )

    if not da_chot:

        st.info(
            text["no_confirmed"]
        )

        st.caption(
            text["confirm_warning"]
        )

        return

    col1, col2, col3 = st.columns(3)

    with col1:

        hien_thi_the(
            text["status_confirmed"],
            "✓",
            "🔒"
        )

    with col2:

        hien_thi_the(
            text["confirmed_at"],
            (
                trang_thai_chot.get(
                    "ngay_chot"
                )
                or "—"
            ),
            "🕐"
        )

    with col3:

        hien_thi_the(
            text["confirmed_by"],
            (
                trang_thai_chot.get(
                    "nguoi_chot"
                )
                or "—"
            ),
            "👤"
        )

    danh_sach_chot = (
        ChotSuatAnController.lay_danh_sach_chot(
            ngay_an_id
        )
    )

    if not danh_sach_chot:

        st.warning(
            text["no_confirmed"]
        )

        return

    thong_ke = (
        ChotSuatAnController.thong_ke_chot(
            ngay_an_id
        )
    )

    tong_so_chot = thong_ke.get(
        "tong_so",
        0
    )

    tong_an_chot = thong_ke.get(
        "so_nguoi_an",
        0
    )

    tong_khong_an_chot = thong_ke.get(
        "so_nguoi_khong_an",
        0
    )

    tong_cong_tac_chot = thong_ke.get(
        "so_nguoi_cong_tac",
        0
    )

    tong_tien_chot = thong_ke.get(
        "tong_tien",
        0
    )

    thong_ke_phat_sinh = (
        ChotSuatAnController.thong_ke_phat_sinh(
            ngay_an_id
        )
    )

    tong_phat_sinh_chot = (
        thong_ke_phat_sinh.get(
            "so_suat",
            0
        )
    )

    tong_tien_phat_sinh_chot = (
        thong_ke_phat_sinh.get(
            "tong_tien",
            0
        )
    )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:

        hien_thi_the(
            text["total"],
            tong_so_chot,
            "👥"
        )

    with col2:

        hien_thi_the(
            text["registered"],
            tong_an_chot,
            "🟢"
        )

    with col3:

        hien_thi_the(
            text["not_eating"],
            tong_khong_an_chot,
            "⚪"
        )

    with col4:

        hien_thi_the(
            text["business_trip"],
            tong_cong_tac_chot,
            "🟠"
        )

    with col5:

        hien_thi_the(
            text["extra_people"],
            tong_phat_sinh_chot,
            "➕"
        )

    with col6:

        hien_thi_the(
            text["money"],
            f"{tong_tien_chot:,.0f} đ",
            "💰"
        )

    st.caption(
        f"{text['extra_money']}: "
        f"{tong_tien_phat_sinh_chot:,.0f} đ"
    )

    hien_thi_tieu_de_section(
        text["filter"],
        "🔎"
    )

    col1, col2, col3, col4 = st.columns(
        [1.2, 1.5, 2, 1.2]
    )

    danh_sach_bo_phan_chot = sorted(
        {
            str(
                item.get(
                    "bo_phan"
                )
                or "Chưa phân bộ phận"
            )
            for item in danh_sach_chot
        },
        key=lambda x: x.lower()
    )

    with col1:

        bo_phan_chot = st.selectbox(
            text["department"],
            [
                text["all_department"]
            ]
            + danh_sach_bo_phan_chot,
            key=f"confirmed_department_{ngay_str}"
        )

    with col2:

        trang_thai_chot_loc = st.selectbox(
            text["status"],
            [
                text["status_all"],
                text["status_unmarked"],
                text["status_eating"],
                text["status_not_eating"],
                text["status_business"],
            ],
            key=f"confirmed_status_{ngay_str}"
        )

    with col3:

        tu_khoa_chot = st.text_input(
            text["search"],
            placeholder=text["search_placeholder"],
            key=f"confirmed_search_{ngay_str}"
        )

    with col4:

        all_type = (
            "Tất cả"
            if language == "vi"
            else "All"
            if language == "en"
            else "全部"
        )

        loai_options = [
            all_type,
            text["employee"],
            text["generated"],
        ]

        loai_chot = st.selectbox(
            text["extra_type"],
            loai_options,
            key=f"confirmed_type_{ngay_str}"
        )

    danh_sach_chot_hien_thi = []

    for item in danh_sach_chot:

        ten = str(
            item.get(
                "ho_ten",
                ""
            )
        )

        bo_phan = str(
            item.get(
                "bo_phan",
                ""
            )
        )

        loai_nguoi = item.get(
            "loai_nguoi",
            "Nhân viên"
        )

        trang_thai_db = item.get(
            "trang_thai",
            "Chưa chấm"
        )

        if (
            bo_phan_chot
            != text["all_department"]
        ):

            if bo_phan != str(
                bo_phan_chot
            ):
                continue

        if tu_khoa_chot.strip():

            if (
                tu_khoa_chot.strip().lower()
                not in ten.lower()
            ):
                continue

        if (
            trang_thai_chot_loc
            != text["status_all"]
        ):

            if (
                trang_thai_chot_loc
                == text["status_unmarked"]
            ):

                if trang_thai_db != "Chưa chấm":
                    continue

            elif (
                trang_thai_chot_loc
                == text["status_eating"]
            ):

                if trang_thai_db != "Đăng ký":
                    continue

            elif (
                trang_thai_chot_loc
                == text["status_not_eating"]
            ):

                if trang_thai_db != "Không ăn":
                    continue

            elif (
                trang_thai_chot_loc
                == text["status_business"]
            ):

                if trang_thai_db != "Đi công tác":
                    continue

        if loai_chot == text["employee"]:

            if loai_nguoi != "Nhân viên":
                continue

        elif loai_chot == text["generated"]:

            if loai_nguoi != "Phát sinh":
                continue

        danh_sach_chot_hien_thi.append(
            item
        )

    if not danh_sach_chot_hien_thi:

        st.info(
            text["no_result"]
        )

        return

    rows_chot = []

    for index, item in enumerate(
        danh_sach_chot_hien_thi,
        start=1
    ):

        trang_thai = item.get(
            "trang_thai",
            "Chưa chấm"
        )

        if trang_thai == "Đăng ký":

            trang_thai_hien_thi = (
                text["register"]
            )

        elif trang_thai == "Đi công tác":

            trang_thai_hien_thi = (
                text["business"]
            )

        elif trang_thai == "Không ăn":

            trang_thai_hien_thi = (
                text["not_eat"]
            )

        else:

            trang_thai_hien_thi = (
                text["unmarked"]
            )

        loai_nguoi = item.get(
            "loai_nguoi",
            "Nhân viên"
        )

        if loai_nguoi == "Phát sinh":

            ten_hien_thi = (
                "➕ "
                + str(
                    item.get(
                        "ho_ten",
                        ""
                    )
                )
            )

        else:

            ten_hien_thi = (
                "👤 "
                + str(
                    item.get(
                        "ho_ten",
                        ""
                    )
                )
            )

        rows_chot.append(
            {
                text["stt"]: index,
                text["person"]: ten_hien_thi,
                text["department"]:
                    item.get(
                        "bo_phan",
                        ""
                    ),
                text["status"]:
                    trang_thai_hien_thi,
                text["quantity"]:
                    item.get(
                        "so_luong",
                        1
                    ),
                text["amount"]:
                    item.get(
                        "so_tien",
                        0
                    ),
                text["remark"]:
                    item.get(
                        "ghi_chu",
                        ""
                    ),
            }
        )

    df_chot = pd.DataFrame(
        rows_chot
    )

    st.dataframe(
        df_chot,
        width="stretch",
        hide_index=True,
        column_config={
            text["stt"]:
                st.column_config.NumberColumn(
                    text["stt"],
                    width="small"
                ),

            text["person"]:
                st.column_config.TextColumn(
                    text["person"],
                    width="medium"
                ),

            text["department"]:
                st.column_config.TextColumn(
                    text["department"],
                    width="medium"
                ),

            text["status"]:
                st.column_config.TextColumn(
                    text["status"],
                    width="medium"
                ),

            text["quantity"]:
                st.column_config.NumberColumn(
                    text["quantity"],
                    width="small"
                ),

            text["amount"]:
                st.column_config.NumberColumn(
                    text["amount"],
                    format="%.0f đ",
                    width="small"
                ),

            text["remark"]:
                st.column_config.TextColumn(
                    text["remark"],
                    width="medium"
                ),
        }
    )

    st.markdown("")

    st.warning(
        text["open_confirm_desc"]
    )

    if st.button(
        text["open_confirm"],
        type="secondary",
        width="stretch",
        key=f"open_confirm_bottom_{ngay_str}"
    ):

        try:

            ChotSuatAnController.mo_chot(
                ngay_an_id
            )

            st.success(
                text["open_confirm_success"]
            )

            st.rerun()

        except Exception as exc:

            st.error(
                f"{text['open_confirm_failed']} "
                f"{exc}"
            )


hien_thi_cham_com()