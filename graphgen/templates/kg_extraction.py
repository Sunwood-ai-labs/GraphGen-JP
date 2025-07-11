import os

def _read_template(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding="utf-8") as f:
        return f.read()

TEMPLATE_EN = _read_template("kg_extraction_en.md")
TEMPLATE_ZH = _read_template("kg_extraction_zh.md")
TEMPLATE_JA = _read_template("kg_extraction_ja.md")

KG_EXTRACTION_PROMPT = {
    "Chinese": {
        "TEMPLATE": TEMPLATE_ZH,
        "CONTINUE": "请继续抽取。",
        "IF_LOOP": "是否还有需要抽取的信息？（yes/no）",
    },
    "English": {
        "TEMPLATE": TEMPLATE_EN,
        "CONTINUE": "Continue extracting.",
        "IF_LOOP": "Is there more information to extract? (yes/no)",
    },
    "Japanese": {
        "TEMPLATE": TEMPLATE_JA,
        "CONTINUE": "続きを抽出してください。",
        "IF_LOOP": "さらに抽出すべき情報はありますか？（yes/noで答えてください）",
    },
    "FORMAT": {
        "language": "English",
        "tuple_delimiter": "<|>",
        "record_delimiter": "##",
        "completion_delimiter": "<|COMPLETE|>",
    },
}
