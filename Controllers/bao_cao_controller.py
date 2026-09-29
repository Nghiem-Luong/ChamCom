from Database.database import get_connection
from pathlib import Path
import csv

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter


class BaoCaoController:

    # ==========================================================
    # 1. LẤY DỮ LIỆU BÁO CÁO
    # ==========================================================

    @staticmethod
    def lay_du_lieu_bao_cao(
        tu_ngay,
        den_ngay,
        ten_nguoi=""
    ):

        if not tu_ngay or not den_ngay:

            return {
                "success": False,
                "message": "Vui lòng chọn đầy đủ ngày.",
                "data": []
            }

        if tu_ngay > den_ngay:

            return {
                "success": False,
                "message": "Ngày bắt đầu không được lớn hơn ngày kết thúc.",
                "data": []
            }

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    a.Ngay,
                    n.HoTen,
                    n.SDT,
                    c.DaAn,
                    c.SoTienPhaiTra,
                    c.GhiChu
                FROM ChiTietAn c

                INNER JOIN NguoiAn n
                    ON c.NguoiAnId = n.Id

                INNER JOIN NgayAn a
                    ON c.NgayAnId = a.Id

                WHERE a.Ngay BETWEEN ?
                    AND ?
                    AND n.HoTen LIKE ?

                ORDER BY
                    a.Ngay,
                    n.HoTen
                """,
                (
                    tu_ngay,
                    den_ngay,
                    f"%{ten_nguoi.strip()}%"
                )
            )

            data = cursor.fetchall()

            return {
                "success": True,
                "data": data
            }

        except Exception as error:

            return {
                "success": False,
                "message": f"Không thể lấy dữ liệu báo cáo: {error}",
                "data": []
            }

        finally:

            connection.close()

    # ==========================================================
    # 2. XUẤT EXCEL
    # ==========================================================

    @staticmethod
    def xuat_excel(
        tu_ngay,
        den_ngay,
        file_path,
        ten_nguoi=""
    ):

        result = BaoCaoController.lay_du_lieu_bao_cao(
            tu_ngay,
            den_ngay,
            ten_nguoi
        )

        if not result["success"]:
            return result

        try:

            file_path = Path(file_path)

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            workbook = Workbook()

            # ==================================================
            # STYLE CHUNG
            # ==================================================

            thin_border = Border(
                left=Side(style="thin"),
                right=Side(style="thin"),
                top=Side(style="thin"),
                bottom=Side(style="thin")
            )

            title_font = Font(
                bold=True,
                size=16
            )

            header_font = Font(
                bold=True,
                size=11
            )

            normal_font = Font(
                size=11
            )

            center_alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

            left_alignment = Alignment(
                horizontal="left",
                vertical="center"
            )

            # ==================================================
            # SHEET 1: BÁO CÁO
            # ==================================================

            sheet_bao_cao = workbook.active

            sheet_bao_cao.title = "Báo cáo"

            # Chiều rộng cột

            widths = {
                "A": 8,
                "B": 16,
                "C": 28,
                "D": 16,
                "E": 14,
                "F": 20,
                "G": 30
            }

            for column, width in widths.items():

                sheet_bao_cao.column_dimensions[
                    column
                ].width = width

            current_row = 1

            # --------------------------------------------------
            # Gom dữ liệu theo ngày
            # --------------------------------------------------

            du_lieu_theo_ngay = {}

            for row in result["data"]:

                ngay = row[0]

                if ngay not in du_lieu_theo_ngay:

                    du_lieu_theo_ngay[ngay] = []

                du_lieu_theo_ngay[ngay].append(row)

            # --------------------------------------------------
            # Ghi từng ngày
            # --------------------------------------------------

            for ngay in sorted(du_lieu_theo_ngay):

                # ==============================================
                # TIÊU ĐỀ NGÀY
                # ==============================================

                sheet_bao_cao.merge_cells(
                    start_row=current_row,
                    start_column=1,
                    end_row=current_row,
                    end_column=7
                )

                cell_title = sheet_bao_cao.cell(
                    row=current_row,
                    column=1
                )

                # Chuyển YYYY-MM-DD thành DD/MM/YYYY

                try:

                    ngay_hien_thi = (
                        f"{ngay[8:10]}/"
                        f"{ngay[5:7]}/"
                        f"{ngay[0:4]}"
                    )

                except Exception:

                    ngay_hien_thi = str(ngay)

                cell_title.value = (
                    f"CHẤM CƠM NGÀY {ngay_hien_thi}"
                )

                cell_title.font = title_font

                cell_title.alignment = center_alignment

                current_row += 1

                # ==============================================
                # TIÊU ĐỀ CỘT
                # ==============================================

                headers = [
                    "STT",
                    "Ngày",
                    "Họ tên",
                    "SĐT",
                    "Đã ăn",
                    "Số tiền phải trả",
                    "Ghi chú"
                ]

                for column_index, header in enumerate(
                    headers,
                    start=1
                ):

                    cell = sheet_bao_cao.cell(
                        row=current_row,
                        column=column_index
                    )

                    cell.value = header

                    cell.font = header_font

                    cell.alignment = center_alignment

                    cell.border = thin_border

                current_row += 1

                # ==============================================
                # DỮ LIỆU
                # ==============================================

                danh_sach = du_lieu_theo_ngay[ngay]

                for stt, row in enumerate(
                    danh_sach,
                    start=1
                ):

                    (
                        ngay_db,
                        ho_ten,
                        sdt,
                        da_an,
                        so_tien,
                        ghi_chu
                    ) = row

                    try:

                        ngay_hien_thi = (
                            f"{ngay_db[8:10]}/"
                            f"{ngay_db[5:7]}/"
                            f"{ngay_db[0:4]}"
                        )

                    except Exception:

                        ngay_hien_thi = str(ngay_db)

                    du_lieu_excel = [
                        stt,
                        ngay_hien_thi,
                        ho_ten,
                        sdt or "",
                        "Có" if da_an == 1 else "Không",
                        so_tien or 0,
                        ghi_chu or ""
                    ]

                    for column_index, value in enumerate(
                        du_lieu_excel,
                        start=1
                    ):

                        cell = sheet_bao_cao.cell(
                            row=current_row,
                            column=column_index
                        )

                        cell.value = value

                        cell.font = normal_font

                        cell.border = thin_border

                        if column_index in [1, 2, 4, 5]:

                            cell.alignment = center_alignment

                        else:

                            cell.alignment = left_alignment

                        # Định dạng tiền

                        if column_index == 6:

                            cell.number_format = (
                                '#,##0 "đ"'
                            )

                            cell.alignment = Alignment(
                                horizontal="right",
                                vertical="center"
                            )

                    current_row += 1

                # ==============================================
                # DÒNG TỔNG TIỀN TRONG NGÀY
                # ==============================================

                tong_tien_ngay = sum(
                    (row[4] or 0)
                    for row in danh_sach
                    if row[3] == 1
                )

                so_luot_an_ngay = sum(
                    1
                    for row in danh_sach
                    if row[3] == 1
                )

                sheet_bao_cao.merge_cells(
                    start_row=current_row,
                    start_column=1,
                    end_row=current_row,
                    end_column=5
                )

                cell_tong = sheet_bao_cao.cell(
                    row=current_row,
                    column=1
                )

                cell_tong.value = (
                    f"Tổng lượt ăn: {so_luot_an_ngay}"
                )

                cell_tong.font = Font(
                    bold=True,
                    size=11
                )

                cell_tong.alignment = Alignment(
                    horizontal="right",
                    vertical="center"
                )

                cell_tong.border = thin_border

                cell_tien = sheet_bao_cao.cell(
                    row=current_row,
                    column=6
                )

                cell_tien.value = tong_tien_ngay

                cell_tien.font = Font(
                    bold=True,
                    size=11
                )

                cell_tien.number_format = (
                    '#,##0 "đ"'
                )

                cell_tien.alignment = Alignment(
                    horizontal="right",
                    vertical="center"
                )

                cell_tien.border = thin_border

                cell_ghi_chu = sheet_bao_cao.cell(
                    row=current_row,
                    column=7
                )

                cell_ghi_chu.border = thin_border

                current_row += 2

            # ==================================================
            # SHEET 2: THEO NGÀY
            # ==================================================

            sheet_ngay = workbook.create_sheet(
                "Theo ngày"
            )

            sheet_ngay.append([
                "Ngày",
                "Số người ăn",
                "Tổng tiền"
            ])

            thong_ke_ngay = {}

            for row in result["data"]:

                ngay = row[0]
                da_an = row[3]
                so_tien = row[4] or 0

                if ngay not in thong_ke_ngay:

                    thong_ke_ngay[ngay] = {
                        "so_nguoi": 0,
                        "tong_tien": 0
                    }

                if da_an == 1:

                    thong_ke_ngay[ngay]["so_nguoi"] += 1

                    thong_ke_ngay[ngay]["tong_tien"] += (
                        so_tien
                    )

            for ngay in sorted(thong_ke_ngay):

                sheet_ngay.append([
                    BaoCaoController._format_ngay(
                        ngay
                    ),
                    thong_ke_ngay[ngay]["so_nguoi"],
                    thong_ke_ngay[ngay]["tong_tien"]
                ])

            # ==================================================
            # SHEET 3: THEO NGƯỜI
            # ==================================================

            sheet_nguoi = workbook.create_sheet(
                "Theo người"
            )

            sheet_nguoi.append([
                "Họ tên",
                "Số lần ăn",
                "Tổng tiền"
            ])

            thong_ke_nguoi = {}

            for row in result["data"]:

                ho_ten = row[1]
                da_an = row[3]
                so_tien = row[4] or 0

                if ho_ten not in thong_ke_nguoi:

                    thong_ke_nguoi[ho_ten] = {
                        "so_lan": 0,
                        "tong_tien": 0
                    }

                if da_an == 1:

                    thong_ke_nguoi[ho_ten]["so_lan"] += 1

                    thong_ke_nguoi[ho_ten]["tong_tien"] += (
                        so_tien
                    )

            for ho_ten in sorted(thong_ke_nguoi):

                sheet_nguoi.append([
                    ho_ten,
                    thong_ke_nguoi[ho_ten]["so_lan"],
                    thong_ke_nguoi[ho_ten]["tong_tien"]
                ])

            # ==================================================
            # SHEET 4: TỔNG QUAN
            # ==================================================

            sheet_tong_quan = workbook.create_sheet(
                "Tổng quan"
            )

            tong_luot_an = sum(
                1
                for row in result["data"]
                if row[3] == 1
            )

            tong_tien = sum(
                (row[4] or 0)
                for row in result["data"]
                if row[3] == 1
            )

            so_ngay = len(
                du_lieu_theo_ngay
            )

            trung_binh = (
                tong_tien / tong_luot_an
                if tong_luot_an > 0
                else 0
            )

            sheet_tong_quan.append([
                "BÁO CÁO QUẢN LÝ CHẤM CƠM"
            ])

            sheet_tong_quan.append([])

            sheet_tong_quan.append([
                "Từ ngày",
                BaoCaoController._format_ngay(
                    tu_ngay
                )
            ])

            sheet_tong_quan.append([
                "Đến ngày",
                BaoCaoController._format_ngay(
                    den_ngay
                )
            ])

            if ten_nguoi.strip():

                sheet_tong_quan.append([
                    "Người tìm kiếm",
                    ten_nguoi.strip()
                ])

            sheet_tong_quan.append([])

            sheet_tong_quan.append([
                "Số ngày",
                so_ngay
            ])

            sheet_tong_quan.append([
                "Tổng lượt ăn",
                tong_luot_an
            ])

            sheet_tong_quan.append([
                "Tổng tiền",
                tong_tien
            ])

            sheet_tong_quan.append([
                "Trung bình/lượt",
                trung_binh
            ])

            # ==================================================
            # ĐỊNH DẠNG SHEET
            # ==================================================

            for sheet in workbook.worksheets:

                for row in sheet.iter_rows():

                    for cell in row:

                        if cell.value is not None:

                            cell.alignment = Alignment(
                                vertical="center",
                                wrap_text=True
                            )

                # Tự động điều chỉnh độ rộng
                # nhưng không làm quá rộng

                for column_cells in sheet.columns:

                    max_length = 0

                    column_index = (
                        column_cells[0].column
                    )

                    column_letter = get_column_letter(
                        column_index
                    )

                    for cell in column_cells:

                        if cell.value is not None:

                            length = len(
                                str(cell.value)
                            )

                            if length > max_length:

                                max_length = length

                    sheet.column_dimensions[
                        column_letter
                    ].width = min(
                        max(max_length + 3, 10),
                        40
                    )

                # Freeze dòng đầu tiên

                sheet.freeze_panes = "A2"

            # --------------------------------------------------
            # Định dạng riêng sheet Theo ngày
            # --------------------------------------------------

            for cell in sheet_ngay[1]:

                cell.font = header_font

                cell.alignment = center_alignment

                cell.border = thin_border

            for row in sheet_ngay.iter_rows(
                min_row=2
            ):

                for cell in row:

                    cell.border = thin_border

                row[2].number_format = (
                    '#,##0 "đ"'
                )

            # --------------------------------------------------
            # Định dạng riêng sheet Theo người
            # --------------------------------------------------

            for cell in sheet_nguoi[1]:

                cell.font = header_font

                cell.alignment = center_alignment

                cell.border = thin_border

            for row in sheet_nguoi.iter_rows(
                min_row=2
            ):

                for cell in row:

                    cell.border = thin_border

                row[2].number_format = (
                    '#,##0 "đ"'
                )

            # --------------------------------------------------
            # Định dạng sheet Tổng quan
            # --------------------------------------------------

            sheet_tong_quan["A1"].font = Font(
                bold=True,
                size=16
            )

            sheet_tong_quan["A1"].alignment = (
                center_alignment
            )

            sheet_tong_quan.column_dimensions[
                "A"
            ].width = 25

            sheet_tong_quan.column_dimensions[
                "B"
            ].width = 30

            sheet_tong_quan["B8"].number_format = (
                '#,##0 "đ"'
            )

            sheet_tong_quan["B9"].number_format = (
                '#,##0 "đ"'
            )

            # ==================================================
            # LƯU FILE
            # ==================================================

            workbook.save(
                file_path
            )

            return {
                "success": True,
                "message": "Xuất Excel thành công.",
                "file_path": str(file_path)
            }

        except Exception as error:

            return {
                "success": False,
                "message": f"Không thể xuất Excel: {error}"
            }

    # ==========================================================
    # 3. XUẤT CSV
    # ==========================================================

    @staticmethod
    def xuat_csv(
        tu_ngay,
        den_ngay,
        file_path,
        ten_nguoi=""
    ):

        result = BaoCaoController.lay_du_lieu_bao_cao(
            tu_ngay,
            den_ngay,
            ten_nguoi
        )

        if not result["success"]:
            return result

        try:

            file_path = Path(file_path)

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow([
                    "Ngày",
                    "Họ tên",
                    "SĐT",
                    "Đã ăn",
                    "Số tiền phải trả",
                    "Ghi chú"
                ])

                for row in result["data"]:

                    writer.writerow([
                        BaoCaoController._format_ngay(
                            row[0]
                        ),
                        row[1],
                        row[2] or "",
                        "Có" if row[3] == 1 else "Không",
                        row[4] or 0,
                        row[5] or ""
                    ])

            return {
                "success": True,
                "message": "Xuất CSV thành công.",
                "file_path": str(file_path)
            }

        except Exception as error:

            return {
                "success": False,
                "message": f"Không thể xuất CSV: {error}"
            }

    # ==========================================================
    # 4. FORMAT NGÀY
    # ==========================================================

    @staticmethod
    def _format_ngay(
        ngay
    ):

        if not ngay:

            return ""

        ngay = str(ngay)

        if len(ngay) >= 10:

            return (
                f"{ngay[8:10]}/"
                f"{ngay[5:7]}/"
                f"{ngay[0:4]}"
            )

        return ngay