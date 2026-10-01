TRANSLATIONS = {
    "vi": {
        "home": "Trang chủ",
        "attendance": "Chấm cơm hôm nay",
        "people": "Quản lý người ăn",
        "payment": "Nộp tiền & công nợ",
        "statistics": "Thống kê",
        "report": "Xuất báo cáo",
        "system": "Trợ lý & Hệ thống",

        "present": "Có mặt",
        "absent": "Vắng",
        "late": "Muộn",

        "paid": "Đã thanh toán",
        "unpaid": "Chưa thanh toán",

        "language": "Ngôn ngữ",
        "vietnamese": "Tiếng Việt",
        "english": "English",
        "chinese": "中文",
    },

    "en": {
        "home": "Home",
        "attendance": "Today's Meal Attendance",
        "people": "Meal Management",
        "payment": "Payment & Debt",
        "statistics": "Statistics",
        "report": "Export Report",
        "system": "Assistant & System",

        "present": "Present",
        "absent": "Absent",
        "late": "Late",

        "paid": "Paid",
        "unpaid": "Unpaid",

        "language": "Language",
        "vietnamese": "Tiếng Việt",
        "english": "English",
        "chinese": "中文",
    },

    "zh": {
        "home": "首页",
        "attendance": "今日用餐",
        "people": "用餐人员管理",
        "payment": "缴费与欠款",
        "statistics": "统计",
        "report": "导出报表",
        "system": "助手与系统",

        "present": "出勤",
        "absent": "缺勤",
        "late": "迟到",

        "paid": "已付款",
        "unpaid": "未付款",

        "language": "语言",
        "vietnamese": "Tiếng Việt",
        "english": "English",
        "chinese": "中文",
    }
}


def t(key, language="vi"):
    """
    Lấy nội dung theo ngôn ngữ.
    Nếu không tìm thấy sẽ trả về key.
    """
    return TRANSLATIONS.get(language, TRANSLATIONS["vi"]).get(key, key)