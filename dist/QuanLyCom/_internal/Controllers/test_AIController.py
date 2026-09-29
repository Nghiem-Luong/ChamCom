# -*- coding: utf-8 -*-

from Controllers.AIController import (
    lay_so_nguoi_an,
    lay_so_suat_an,
    lay_tong_tien_phai_tra
)


print("===== TEST AI CONTROLLER =====")

print(
    "Số người ăn hôm nay:",
    lay_so_nguoi_an()
)

print(
    "Số suất ăn hôm nay:",
    lay_so_suat_an()
)

print(
    "Tổng tiền phải thu:",
    lay_tong_tien_phai_tra()
)

print("==============================")