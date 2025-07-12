import os

def _read_template(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding="utf-8") as f:
        return f.read()

TEMPLATE_EN = _read_template("description_rephrasing_en.md")
ANTI_TEMPLATE_EN = _read_template("description_rephrasing_en_anti.md")
TEMPLATE_ZH = _read_template("description_rephrasing_zh.md")
ANTI_TEMPLATE_ZH = _read_template("description_rephrasing_zh_anti.md")
TEMPLATE_JA = _read_template("description_rephrasing_ja.md")
ANTI_TEMPLATE_JA = _read_template("description_rephrasing_ja_anti.md")

DESCRIPTION_REPHRASING_PROMPT = {
    "English": {
        "ANTI_TEMPLATE": ANTI_TEMPLATE_EN,
        "TEMPLATE": TEMPLATE_EN
    },
    "Chinese": {
        "ANTI_TEMPLATE": ANTI_TEMPLATE_ZH,
        "TEMPLATE": TEMPLATE_ZH
    },
    "Japanese": {
        "ANTI_TEMPLATE": ANTI_TEMPLATE_JA,
        "TEMPLATE": TEMPLATE_JA
    }
}
