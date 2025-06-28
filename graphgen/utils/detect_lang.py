def detect_main_language(text):
    """
    识别文本的主要语言

    :param text:
    :return:
    """
    assert isinstance(text, str)
    def is_chinese_char(char):
        return '\u4e00' <= char <= '\u9fff'

    def is_english_char(char):
        return char.isascii() and char.isalpha()

    def is_japanese_char(char):
        # ひらがな
        if '\u3040' <= char <= '\u309f':
            return True
        # カタカナ
        if '\u30a0' <= char <= '\u30ff':
            return True
        # 漢字（中国語と重複するが、日本語にも使われる）
        if '\u4e00' <= char <= '\u9fff':
            return True
        # 全角カタカナ
        if '\uff66' <= char <= '\uff9f':
            return True
        return False

    # 空白・記号除去
    text = ''.join(char for char in text if char.strip())

    chinese_count = sum(1 for char in text if is_chinese_char(char))
    english_count = sum(1 for char in text if is_english_char(char))
    japanese_count = sum(1 for char in text if is_japanese_char(char))

    total = chinese_count + english_count + japanese_count
    if total == 0:
        return 'en'

    # 日本語比率が高ければja
    japanese_ratio = japanese_count / total
    if japanese_ratio >= 0.5:
        return 'ja'

    chinese_ratio = chinese_count / total
    if chinese_ratio >= 0.5:
        return 'zh'

    return 'en'

def detect_if_chinese(text):
    """
    判断文本是否包含有中文

    :param text:
    :return:
    """

    assert isinstance(text, str)
    return any('\u4e00' <= char <= '\u9fff' for char in text)
