# -*- coding: utf-8 -*-

from Models.bo_phan_model import BoPhanModel


class BoPhanController:

    @staticmethod
    def them_bo_phan(ten_bo_phan):
        return BoPhanModel.them_bo_phan(ten_bo_phan)

    @staticmethod
    def lay_tat_ca():
        return BoPhanModel.lay_tat_ca()

    @staticmethod
    def lay_dang_hoat_dong():
        return BoPhanModel.lay_dang_hoat_dong()

    @staticmethod
    def tim_theo_id(bo_phan_id):
        return BoPhanModel.tim_theo_id(bo_phan_id)

    @staticmethod
    def tim_theo_ten(ten_bo_phan):
        return BoPhanModel.tim_theo_ten(ten_bo_phan)

    @staticmethod
    def cap_nhat(bo_phan_id, ten_bo_phan):
        return BoPhanModel.cap_nhat(
            bo_phan_id,
            ten_bo_phan
        )

    @staticmethod
    def ngung_hoat_dong(bo_phan_id):
        return BoPhanModel.ngung_hoat_dong(
            bo_phan_id
        )

    @staticmethod
    def kich_hoat_lai(bo_phan_id):
        return BoPhanModel.kich_hoat_lai(
            bo_phan_id
        )