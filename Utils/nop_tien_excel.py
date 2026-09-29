# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime

import pandas as pd

from openpyxl import load_workbook
from openpyxl.styles import (
    Font,
    PatternFill,
    Border,
    Side,
    Alignment
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins


# ==========================================================
# CẤU HÌNH MÀU
# ==========================================================

MAU_XANH_DAM = "1F4E78"
MAU_XANH = "5B9BD5"
MAU_XANH_NHAT = "D9EAF7"

MAU_XANH_LA = "E2F0D9"
MAU_VANG = "FFF2CC"
MAU_DO_NHAT = "FCE4D6"
MAU_XAM = "F2F2F2"

MAU_TRANG = "FFFFFF"
MAU_DEN = "000000"
MAU_XAM_CHU = "666666"

MAU_VIEN = "B7C9D6"


# ==========================================================
# FONT
# ==========================================================

FONT_TIEU_DE = Font(
    name="Arial",
    size=18,
    bold=True,
    color=MAU_TRANG
)

FONT_PHU = Font(
    name="Arial",
    size=10,
    color=MAU_XAM_CHU
)

FONT_HEADER = Font(
    name="Arial",
    size=10,
    bold=True,
    color=MAU_TRANG
)

FONT_BODY = Font(
    name="Arial",
    size=10,
    color=MAU_DEN
)

FONT_TONG = Font(
    name="Arial",
    size=10,
    bold=True,
    color=MAU_DEN
)


# ==========================================================
# BORDER
# ==========================================================

VIEN_MONG = Side(
    style="thin",
    color=MAU_VIEN
)

BORDER_ALL = Border(
    left=VIEN_MONG,
    right=VIEN_MONG,
    top=VIEN_MONG,
    bottom=VIEN_MONG
)


# ==========================================================
# THƯ MỤC
# ==========================================================

def _tao_thu_muc_xuat():
    """
    Tạo thư mục BaoCao.
    """

    thu_muc = Path("BaoCao")

    thu_muc.mkdir(
        parents=True,
        exist_ok=True
    )

    return thu_muc


# ==========================================================
# CHUYỂN DATAFRAME
# ==========================================================

def _to_dataframe(data):
    """
    Đảm bảo dữ liệu luôn là DataFrame.
    """

    if data is None:
        return pd.DataFrame()

    if isinstance(data, pd.DataFrame):
        return data.copy()

    try:
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()


# ==========================================================
# FORMAT TIỀN
# ==========================================================

def _dinh_dang_tien(
    worksheet,
    ten_cot,
    dong_bat_dau,
    dong_ket_thuc
):
    """
    Định dạng cột tiền.
    """

    headers = {}

    for cell in worksheet[5]:
        headers[str(cell.value)] = cell.column

    if ten_cot not in headers:
        return

    col_index = headers[ten_cot]

    for row in range(
        dong_bat_dau,
        dong_ket_thuc + 1
    ):

        worksheet.cell(
            row=row,
            column=col_index
        ).number_format = '#,##0" đ"'


# ==========================================================
# FORMAT NGÀY
# ==========================================================

def _dinh_dang_ngay(
    worksheet,
    dong_bat_dau,
    dong_ket_thuc
):
    """
    Tự nhận diện các cột ngày.
    """

    cot_ngay = {
        "Ngày",
        "Ngày nộp",
        "Từ ngày",
        "Đến ngày",
        "Ngày ăn",
        "Thời gian"
    }

    for cell in worksheet[5]:

        ten_cot = str(
            cell.value or ""
        ).strip()

        if ten_cot not in cot_ngay:
            continue

        col_index = cell.column

        for row in range(
            dong_bat_dau,
            dong_ket_thuc + 1
        ):

            worksheet.cell(
                row=row,
                column=col_index
            ).number_format = "dd/mm/yyyy"


# ==========================================================
# TIÊU ĐỀ
# ==========================================================

def _tao_tieu_de(
    worksheet,
    tieu_de,
    mo_ta=None,
    ky_bao_cao=None
):
    """
    Tạo phần đầu báo cáo.
    """

    max_col = max(
        worksheet.max_column,
        6
    )

    worksheet.merge_cells(
        start_row=1,
        start_column=1,
        end_row=1,
        end_column=max_col
    )

    cell = worksheet.cell(
        row=1,
        column=1
    )

    cell.value = tieu_de
    cell.font = FONT_TIEU_DE
    cell.fill = PatternFill(
        "solid",
        fgColor=MAU_XANH_DAM
    )

    cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    worksheet.row_dimensions[1].height = 32

    # Tô toàn bộ dòng tiêu đề
    for col in range(1, max_col + 1):

        worksheet.cell(
            row=1,
            column=col
        ).fill = PatternFill(
            "solid",
            fgColor=MAU_XANH_DAM
        )

    # Mô tả
    worksheet.merge_cells(
        start_row=2,
        start_column=1,
        end_row=2,
        end_column=max_col
    )

    mo_ta_cell = worksheet.cell(
        row=2,
        column=1
    )

    mo_ta_cell.value = (
        mo_ta
        or "Báo cáo quản lý tiền cơm và công nợ"
    )

    mo_ta_cell.font = FONT_PHU

    mo_ta_cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    worksheet.row_dimensions[2].height = 20

    # Kỳ báo cáo
    worksheet.merge_cells(
        start_row=3,
        start_column=1,
        end_row=3,
        end_column=max_col
    )

    ky_cell = worksheet.cell(
        row=3,
        column=1
    )

    if ky_bao_cao:

        ky_cell.value = (
            f"Kỳ báo cáo: {ky_bao_cao}"
        )

    else:

        ky_cell.value = (
            "Ngày xuất: "
            + datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )

    ky_cell.font = FONT_PHU

    ky_cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    worksheet.row_dimensions[3].height = 20


# ==========================================================
# THÔNG TIN BÁO CÁO
# ==========================================================

def _tao_thong_tin(
    worksheet,
    dataframe
):
    """
    Tạo dòng thống kê nhanh.
    """

    max_col = max(
        worksheet.max_column,
        6
    )

    so_dong = len(dataframe)

    tong_phai_tra = 0
    tong_da_nop = 0
    tong_no = 0
    tong_du = 0

    if not dataframe.empty:

        if "Phải trả" in dataframe.columns:
            tong_phai_tra = pd.to_numeric(
                dataframe["Phải trả"],
                errors="coerce"
            ).fillna(0).sum()

        if "Đã nộp" in dataframe.columns:
            tong_da_nop = pd.to_numeric(
                dataframe["Đã nộp"],
                errors="coerce"
            ).fillna(0).sum()

        if "Còn nợ" in dataframe.columns:
            tong_no = pd.to_numeric(
                dataframe["Còn nợ"],
                errors="coerce"
            ).fillna(0).sum()

        if "Nộp thừa" in dataframe.columns:
            tong_du = pd.to_numeric(
                dataframe["Nộp thừa"],
                errors="coerce"
            ).fillna(0).sum()

    # Không phải sheet nào cũng cần đủ 4 ô.
    thong_tin = [
        ("Số dòng", so_dong),
        ("Phải trả", tong_phai_tra),
        ("Đã nộp", tong_da_nop),
        (
            "Chênh lệch",
            tong_da_nop - tong_phai_tra
        )
    ]

    so_o = min(
        len(thong_tin),
        max_col
    )

    for index in range(so_o):

        cot = index + 1

        label, value = thong_tin[index]

        cell_label = worksheet.cell(
            row=4,
            column=cot
        )

        cell_value = worksheet.cell(
            row=4,
            column=cot
        )

        # Không thể tạo 2 dòng trong cùng ô
        # nên dùng ghi chú ngắn.
        cell_value.value = (
            f"{label}: "
            f"{value:,.0f}"
            if isinstance(value, (int, float))
            else f"{label}: {value}"
        )

        cell_value.font = Font(
            name="Arial",
            size=9,
            bold=True,
            color=MAU_XANH_DAM
        )

        cell_value.fill = PatternFill(
            "solid",
            fgColor=MAU_XANH_NHAT
        )

        cell_value.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        cell_value.border = BORDER_ALL

    worksheet.row_dimensions[4].height = 22


# ==========================================================
# HEADER BẢNG
# ==========================================================

def _dinh_dang_header(
    worksheet,
    dong_header=5
):
    """
    Định dạng header của bảng.
    """

    for cell in worksheet[dong_header]:

        if cell.value is None:
            continue

        cell.font = FONT_HEADER

        cell.fill = PatternFill(
            "solid",
            fgColor=MAU_XANH
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

        cell.border = BORDER_ALL

    worksheet.row_dimensions[
        dong_header
    ].height = 30


# ==========================================================
# BODY
# ==========================================================

def _dinh_dang_body(
    worksheet,
    dong_bat_dau,
    dong_ket_thuc
):
    """
    Định dạng dữ liệu.
    """

    for row in range(
        dong_bat_dau,
        dong_ket_thuc + 1
    ):

        mau_nen = (
            MAU_TRANG
            if row % 2
            else "F7FBFD"
        )

        for col in range(
            1,
            worksheet.max_column + 1
        ):

            cell = worksheet.cell(
                row=row,
                column=col
            )

            cell.font = FONT_BODY

            cell.fill = PatternFill(
                "solid",
                fgColor=mau_nen
            )

            cell.border = BORDER_ALL

            cell.alignment = Alignment(
                vertical="center",
                wrap_text=True
            )


# ==========================================================
# DÒNG TỔNG
# ==========================================================

def _tao_dong_tong(
    worksheet,
    dataframe,
    dong_tong
):
    """
    Tạo dòng tổng cuối bảng.
    """

    if dataframe.empty:
        return

    worksheet.cell(
        row=dong_tong,
        column=1
    ).value = "TỔNG CỘNG"

    worksheet.cell(
        row=dong_tong,
        column=1
    ).font = FONT_TONG

    worksheet.cell(
        row=dong_tong,
        column=1
    ).fill = PatternFill(
        "solid",
        fgColor=MAU_XANH_NHAT
    )

    worksheet.cell(
        row=dong_tong,
        column=1
    ).border = BORDER_ALL

    for index, ten_cot in enumerate(
        dataframe.columns,
        start=1
    ):

        if ten_cot in {
            "Phải trả",
            "Đã nộp",
            "Còn nợ",
            "Nộp thừa",
            "Số tiền",
            "Tổng tiền",
            "Đơn giá"
        }:

            try:

                value = pd.to_numeric(
                    dataframe[ten_cot],
                    errors="coerce"
                ).fillna(0).sum()

                cell = worksheet.cell(
                    row=dong_tong,
                    column=index
                )

                cell.value = float(value)

                cell.number_format = (
                    '#,##0" đ"'
                )

            except Exception:
                pass

        cell = worksheet.cell(
            row=dong_tong,
            column=index
        )

        cell.font = FONT_TONG

        cell.fill = PatternFill(
            "solid",
            fgColor=MAU_XANH_NHAT
        )

        cell.border = BORDER_ALL

        cell.alignment = Alignment(
            vertical="center",
            horizontal=(
                "right"
                if ten_cot in {
                    "Phải trả",
                    "Đã nộp",
                    "Còn nợ",
                    "Nộp thừa",
                    "Số tiền",
                    "Tổng tiền",
                    "Đơn giá"
                }
                else "left"
            )
        )


# ==========================================================
# TỰ ĐỘNG ĐỘ RỘNG
# ==========================================================

def _tu_dong_do_rong(
    worksheet
):
    """
    Tự động điều chỉnh độ rộng cột.
    """

    for column_cells in worksheet.columns:

        max_length = 0

        for cell in column_cells:

            try:

                value = str(
                    cell.value
                    if cell.value is not None
                    else ""
                )

                max_length = max(
                    max_length,
                    len(value)
                )

            except Exception:
                pass

        width = min(
            max(
                max_length + 3,
                12
            ),
            35
        )

        column_letter = get_column_letter(
            column_cells[0].column
        )

        worksheet.column_dimensions[
            column_letter
        ].width = width


# ==========================================================
# ĐỊNH DẠNG TRẠNG THÁI
# ==========================================================

def _dinh_dang_trang_thai(
    worksheet
):
    """
    Tô màu trạng thái:
    - Còn nợ
    - Đã đủ
    - Nộp thừa
    """

    for row in range(
        1,
        worksheet.max_row + 1
    ):

        for col in range(
            1,
            worksheet.max_column + 1
        ):

            cell = worksheet.cell(
                row=row,
                column=col
            )

            value = str(
                cell.value or ""
            ).strip()

            if value == "Còn nợ":

                cell.font = Font(
                    name="Arial",
                    size=10,
                    bold=True,
                    color="C00000"
                )

                cell.fill = PatternFill(
                    "solid",
                    fgColor=MAU_DO_NHAT
                )

            elif value == "Đã đủ":

                cell.font = Font(
                    name="Arial",
                    size=10,
                    bold=True,
                    color="006100"
                )

                cell.fill = PatternFill(
                    "solid",
                    fgColor=MAU_XANH_LA
                )

            elif value == "Nộp thừa":

                cell.font = Font(
                    name="Arial",
                    size=10,
                    bold=True,
                    color="9C6500"
                )

                cell.fill = PatternFill(
                    "solid",
                    fgColor=MAU_VANG
                )


# ==========================================================
# THIẾT LẬP IN
# ==========================================================

def _cau_hinh_in(
    worksheet,
    dong_header=5
):
    """
    Cấu hình trang in A4.
    """

    worksheet.freeze_panes = (
        f"A{dong_header + 1}"
    )

    worksheet.auto_filter.ref = (
        f"A{dong_header}:"
        f"{get_column_letter(worksheet.max_column)}"
        f"{worksheet.max_row}"
    )

    worksheet.sheet_view.showGridLines = False

    worksheet.page_setup.orientation = (
        "landscape"
    )

    worksheet.page_setup.paperSize = (
        worksheet.PAPERSIZE_A4
    )

    worksheet.page_setup.fitToWidth = 1
    worksheet.page_setup.fitToHeight = 0

    worksheet.sheet_properties.pageSetUpPr.fitToPage = True

    worksheet.page_margins = PageMargins(
        left=0.25,
        right=0.25,
        top=0.5,
        bottom=0.5,
        header=0.2,
        footer=0.2
    )

    worksheet.print_title_rows = (
        f"1:{dong_header}"
    )

    worksheet.oddFooter.center.text = (
        "Trang &P / &N"
    )

    worksheet.oddFooter.right.text = (
        "Xuất ngày: "
        + datetime.now().strftime(
            "%d/%m/%Y"
        )
    )


# ==========================================================
# GHI DATAFRAME
# ==========================================================

def _ghi_dataframe_excel(
    dataframe,
    writer,
    ten_sheet,
    tieu_de,
    mo_ta=None,
    ky_bao_cao=None
):
    """
    Ghi một DataFrame thành báo cáo Excel hoàn chỉnh.
    """

    dataframe = _to_dataframe(
        dataframe
    )

    if dataframe.empty:

        dataframe = pd.DataFrame(
            {
                "Thông báo": [
                    "Không có dữ liệu trong kỳ báo cáo."
                ]
            }
        )

    # Ghi bắt đầu từ dòng 5
    dataframe.to_excel(
        writer,
        sheet_name=ten_sheet,
        index=False,
        startrow=4
    )

    worksheet = writer.sheets[
        ten_sheet
    ]

    # Tiêu đề
    _tao_tieu_de(
        worksheet=worksheet,
        tieu_de=tieu_de,
        mo_ta=mo_ta,
        ky_bao_cao=ky_bao_cao
    )

    # Header
    _dinh_dang_header(
        worksheet,
        dong_header=5
    )

    dong_data_dau = 6

    dong_data_cuoi = (
        5 + len(dataframe)
    )

    # Body
    _dinh_dang_body(
        worksheet,
        dong_data_dau,
        dong_data_cuoi
    )

    # Tổng
    dong_tong = (
        dong_data_cuoi + 1
    )

    _tao_dong_tong(
        worksheet,
        dataframe,
        dong_tong
    )

    # Tiền
    cac_cot_tien = {
        "Phải trả",
        "Đã nộp",
        "Còn nợ",
        "Nộp thừa",
        "Số tiền",
        "Tổng tiền",
        "Đơn giá"
    }

    for ten_cot in cac_cot_tien:

        _dinh_dang_tien(
            worksheet,
            ten_cot,
            dong_data_dau,
            dong_tong
        )

    # Ngày
    _dinh_dang_ngay(
        worksheet,
        dong_data_dau,
        dong_data_cuoi
    )

    # Trạng thái
    _dinh_dang_trang_thai(
        worksheet
    )

    # Thông tin
    _tao_thong_tin(
        worksheet,
        dataframe
    )

    # Độ rộng
    _tu_dong_do_rong(
        worksheet
    )

    # In
    _cau_hinh_in(
        worksheet,
        dong_header=5
    )

    worksheet.row_dimensions[
        dong_tong
    ].height = 24


# ==========================================================
# XUẤT BÁO CÁO
# ==========================================================

def xuat_bao_cao_cong_no_excel(
    tong_hop_thang=None,
    tong_hop_tuan=None,
    chi_tiet_ca_nhan=None,
    chi_tiet_tien_com=None,
    lich_su_nop_tien=None,
    van_de_phat_sinh=None,
    ten_bao_cao=None,
    ky_bao_cao=None
):
    """
    Xuất báo cáo công nợ Excel chuyên nghiệp.

    Các sheet:

    1. Tong_Hop_Thang
    2. Tong_Hop_Tuan
    3. Chi_Tiet_Ca_Nhan
    4. Chi_Tiet_Tien_Com
    5. Lich_Su_Nop_Tien
    6. Van_De_Phat_Sinh
    """

    try:

        thu_muc = _tao_thu_muc_xuat()

        if not ten_bao_cao:

            ten_bao_cao = (
                "BaoCao_CongNo_"
                + datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )
                + ".xlsx"
            )

        # Đảm bảo có .xlsx
        if not ten_bao_cao.lower().endswith(
            ".xlsx"
        ):

            ten_bao_cao += ".xlsx"

        duong_dan = (
            thu_muc
            / ten_bao_cao
        )

        with pd.ExcelWriter(
            duong_dan,
            engine="openpyxl"
        ) as writer:

            da_co_sheet = False

            # ==================================================
            # 1. TỔNG HỢP THÁNG
            # ==================================================

            if tong_hop_thang is not None:

                _ghi_dataframe_excel(
                    dataframe=tong_hop_thang,
                    writer=writer,
                    ten_sheet="Tong_Hop_Thang",
                    tieu_de=(
                        "BÁO CÁO TỔNG HỢP CÔNG NỢ TIỀN CƠM"
                    ),
                    mo_ta=(
                        "Tổng hợp tình trạng phải trả, "
                        "đã nộp và số dư của từng người"
                    ),
                    ky_bao_cao=ky_bao_cao
                )

                da_co_sheet = True

            # ==================================================
            # 2. TỔNG HỢP TUẦN
            # ==================================================

            if tong_hop_tuan is not None:

                _ghi_dataframe_excel(
                    dataframe=tong_hop_tuan,
                    writer=writer,
                    ten_sheet="Tong_Hop_Tuan",
                    tieu_de=(
                        "BÁO CÁO CÔNG NỢ THEO TUẦN"
                    ),
                    mo_ta=(
                        "Theo dõi công nợ lũy kế "
                        "qua từng tuần"
                    ),
                    ky_bao_cao=ky_bao_cao
                )

                da_co_sheet = True

            # ==================================================
            # 3. CHI TIẾT CÁ NHÂN
            # ==================================================

            if chi_tiet_ca_nhan is not None:

                _ghi_dataframe_excel(
                    dataframe=chi_tiet_ca_nhan,
                    writer=writer,
                    ten_sheet="Chi_Tiet_Ca_Nhan",
                    tieu_de=(
                        "CHI TIẾT CÔNG NỢ TỪNG NGƯỜI"
                    ),
                    mo_ta=(
                        "Thông tin chi tiết về tiền cơm "
                        "và tình trạng thanh toán"
                    ),
                    ky_bao_cao=ky_bao_cao
                )

                da_co_sheet = True

            # ==================================================
            # 4. CHI TIẾT TIỀN CƠM
            # ==================================================

            if chi_tiet_tien_com is not None:

                _ghi_dataframe_excel(
                    dataframe=chi_tiet_tien_com,
                    writer=writer,
                    ten_sheet="Chi_Tiet_Tien_Com",
                    tieu_de=(
                        "CHI TIẾT TIỀN CƠM"
                    ),
                    mo_ta=(
                        "Danh sách suất ăn và "
                        "số tiền phải trả"
                    ),
                    ky_bao_cao=ky_bao_cao
                )

                da_co_sheet = True

            # ==================================================
            # 5. LỊCH SỬ NỘP TIỀN
            # ==================================================

            if lich_su_nop_tien is not None:

                _ghi_dataframe_excel(
                    dataframe=lich_su_nop_tien,
                    writer=writer,
                    ten_sheet="Lich_Su_Nop_Tien",
                    tieu_de=(
                        "LỊCH SỬ GIAO DỊCH NỘP TIỀN"
                    ),
                    mo_ta=(
                        "Theo dõi toàn bộ các giao dịch "
                        "tiền mặt và chuyển khoản"
                    ),
                    ky_bao_cao=ky_bao_cao
                )

                da_co_sheet = True

            # ==================================================
            # 6. VẤN ĐỀ PHÁT SINH
            # ==================================================

            if van_de_phat_sinh is not None:

                _ghi_dataframe_excel(
                    dataframe=van_de_phat_sinh,
                    writer=writer,
                    ten_sheet="Van_De_Phat_Sinh",
                    tieu_de=(
                        "DANH SÁCH VẤN ĐỀ PHÁT SINH"
                    ),
                    mo_ta=(
                        "Các trường hợp cần kiểm tra "
                        "hoặc đối chiếu"
                    ),
                    ky_bao_cao=ky_bao_cao
                )

                da_co_sheet = True

            # ==================================================
            # KHÔNG CÓ SHEET
            # ==================================================

            if not da_co_sheet:

                _ghi_dataframe_excel(
                    dataframe=pd.DataFrame(
                        {
                            "Thông báo": [
                                "Chưa có dữ liệu để xuất báo cáo."
                            ]
                        }
                    ),
                    writer=writer,
                    ten_sheet="Bao_Cao",
                    tieu_de=(
                        "BÁO CÁO CÔNG NỢ TIỀN CƠM"
                    ),
                    mo_ta=(
                        "Không có dữ liệu để xuất"
                    ),
                    ky_bao_cao=ky_bao_cao
                )

        return {
            "success": True,
            "message": (
                "Xuất báo cáo Excel thành công."
            ),
            "file_path": str(
                duong_dan.resolve()
            )
        }

    except Exception as error:

        return {
            "success": False,
            "message": (
                "Không thể xuất báo cáo Excel: "
                f"{error}"
            ),
            "file_path": None
        }