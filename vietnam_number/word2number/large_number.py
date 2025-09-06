from vietnam_number.word2number.data import hundreds_words, special_word
from vietnam_number.word2number.hundreds import process_hundreds
from vietnam_number.word2number.utils.large_number import LargeNumber


def pre_process_large_number(words: list) -> LargeNumber:
    """Tiền xữ lý danh sách chữ số đầu vào.

    Giúp tiền xữ lý dữ liệu đầu vào bao gồm như định dang lại danh sách, kiểm tra tính hợp lệ
    của danh sách...

    Args:
        words (list): Danh dách chữ số dùng để tiền xữ lý.

    Returns:
        Trả về một instance sau khi đã được xữ lý
        Nếu có lỗi sẽ trả về lỗi.

    """
    large_number = LargeNumber.format_words(words)

    # Kiểm tra tính hợp lệ của danh sách chữ số.
    large_number.validate()

    return large_number


def process_large_number_normal(words: list):
    """Xữ lý chử số lớn.

    Hàm xữ lý chuyển đổi dành cho trường hợp các chữ số lớn hơn
    hàng trăm. Bao gồm các số hàng nghìn, triệu, tỷ

    Args:
        words (list): Danh sách chữ số đầu vào.

    Returns:
        Chuổi số lớn

    """
    # Tiền xữ lý danh sách chữ số đầu vào.
    large_number = pre_process_large_number(words)

    # Xữ lý chữ số hàng trăm.
    clean_words_number = large_number.words_number

    # Lấy vị trí index của từ khóa hàng chục
    billion_index = large_number.get_keyword_index['billion_index']
    million_index = large_number.get_keyword_index['million_index']
    thousand_index = large_number.get_keyword_index['thousand_index']

    billion_million_thousand_positions: tuple[None | int, None | int, None | int] = (
        billion_index,
        million_index,
        thousand_index,
    )

    start: int = 0
    number_segments: list[list[str]] = []

    for index in billion_million_thousand_positions:
        if index is None:
            number_segments.append([])
        else:
            number_segments.append(clean_words_number[start:index])
            start = index + 1

    number_segments.append(clean_words_number[start:])

    _value_of_billion, value_of_million, value_of_thousand, _value_of_hundreds = (
        number_segments
    )

    if not value_of_thousand and thousand_index:
        value_of_thousand.append("một")
    if not value_of_million and million_index:
        value_of_million.append("một")

    total_number: str = "".join(map(process_hundreds, number_segments))

    return int(total_number)


def process_large_number_special(words: list):
    size = len(words)

    idx_list = [i for i, value in enumerate(words) if value in special_word]
    number_list = (
        words[i + 1 : j]
        for i, j in zip(
            [-1] + idx_list, idx_list + ([size] if idx_list[-1] != size else [])
        )
    )

    total_number = 0
    for element in number_list:
        total_number += int(process_large_number_normal(element))

    return total_number


def process_large_number(words: list):
    # Trường hợp có từ khóa đặc biệt 'lẽ'
    # nếu từ 'lẽ' đứng sau từ 'trăm'
    idx_list = (i for i, value in enumerate(words) if value in special_word)
    for idx in idx_list:
        if words[idx - 1] in hundreds_words:
            words[idx] = 'không'

    if "lẽ" not in words:
        return process_large_number_normal(words)
    else:
        return process_large_number_special(words)


if __name__ == '__main__':
    print(
        process_large_number(
            ['tỷ', 'lẽ', 'tám', 'trăm', 'năm', 'mươi', 'triệu', 'sáu', 'trăm', 'lẽ', 'ba', 'nghìn', 'hai', 'trăm'],
        ),
    )
