import json

def convert_to_alpaca(input_path, output_path):
    """
    orin-mini.jsonl形式（IDをキーにしたQ&Aオブジェクト）を
    Alpacaデータセットフォーマット（instruction, input, outputのJSONL）に変換するスクリプト
    """
    with open(input_path, "r", encoding="utf-8") as infile:
        # 1行全体が巨大なJSONオブジェクト
        data = json.load(infile)

    with open(output_path, "w", encoding="utf-8") as outfile:
        for item in data.values():
            # 「东方」を「東方」に正規化
            question = item.get("question", "").replace("东方", "東方")
            answer = item.get("answer", "").replace("东方", "東方")
            # Alpacaフォーマットに変換
            alpaca_obj = {
                "instruction": question,
                "input": "",
                "output": answer
            }
            outfile.write(json.dumps(alpaca_obj, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    # 入出力ファイルパス
    input_file = "scripts/sample/orin-mini.jsonl"
    output_file = "scripts/sample/orin-mini-alpaca.jsonl"
    convert_to_alpaca(input_file, output_file)
