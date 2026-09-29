# -*- coding: utf-8 -*-

import ollama


# ============================================================
# CẤU HÌNH OLLAMA
# ============================================================

MODEL_OLLAMA = "qwen2.5:3b"


# ============================================================
# SYSTEM PROMPT CHO DÂU TÂY
# ============================================================

SYSTEM_PROMPT = """
Bạn là Dâu Tây, trợ lý AI của ứng dụng Quản Lý Chấm Cơm.

Nhiệm vụ của bạn:
- Trả lời bằng tiếng Việt.
- Nói chuyện tự nhiên, lịch sự, thân thiện.
- Trả lời ngắn gọn, dễ hiểu.
- Hỗ trợ người dùng sử dụng ứng dụng Quản Lý Chấm Cơm.
- Khi người dùng hỏi về dữ liệu chấm cơm, công nợ,
  số người ăn, số suất ăn hoặc thống kê, không được tự
  bịa số liệu. Những dữ liệu đó sẽ được cung cấp từ
  hệ thống cơ sở dữ liệu ở bước tích hợp sau.
- Không tự nhận mình là con người.
- Tên của bạn là Dâu Tây.
"""


# ============================================================
# GỌI QWEN
# ============================================================

def hoi_qwen(cau_hoi, lich_su=None):

    """
    Gửi câu hỏi tới Qwen thông qua Ollama.

    Parameters
    ----------
    cau_hoi : str
        Câu hỏi hiện tại của người dùng.

    lich_su : list | None
        Lịch sử hội thoại.

    Returns
    -------
    str
        Câu trả lời của Qwen.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # ========================================================
    # THÊM LỊCH SỬ
    # ========================================================

    if lich_su:

        for tin_nhan in lich_su:

            vai_tro = tin_nhan.get(
                "vai_tro"
            )

            noi_dung = tin_nhan.get(
                "noi_dung"
            )

            if vai_tro in (
                "user",
                "assistant"
            ) and noi_dung:

                messages.append(
                    {
                        "role": vai_tro,
                        "content": noi_dung
                    }
                )

    # ========================================================
    # CÂU HỎI HIỆN TẠI
    # ========================================================

    messages.append(
        {
            "role": "user",
            "content": cau_hoi
        }
    )

    # ========================================================
    # GỌI OLLAMA
    # ========================================================

    try:

        response = ollama.chat(
            model=MODEL_OLLAMA,
            messages=messages
        )

        noi_dung = (
            response
            .get("message", {})
            .get("content", "")
        )

        if not noi_dung:

            return (
                "Xin lỗi chị, em chưa nhận được "
                "nội dung trả lời từ Qwen."
            )

        return noi_dung.strip()

    except Exception as e:

        return (
            "⚠️ Không thể kết nối với Ollama.\n\n"
            "Chị hãy kiểm tra Ollama đang hoạt động "
            "và model **qwen2.5:3b** đã được cài đặt.\n\n"
            f"`{e}`"
        )