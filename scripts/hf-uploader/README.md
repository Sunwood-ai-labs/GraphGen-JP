# 📝 hf-uploader 利用ガイド

## 🗒️ 概要

本ディレクトリは、Hugging Face Hub へのデータセットアップロードを支援する Python スクリプト群を提供します。  
主に `upload_dataset.py` を用いて、JSONL 形式のデータセットを Hugging Face Hub へ変換・アップロードし、README も自動生成できます。

## ⚙️ セットアップ方法

1. Python 3.10 以上を用意してください。
2. 必要なパッケージは `pyproject.toml` で管理されています。  
   `uv` または `poetry` でインストールできます。

```bash
# uv の場合
uv pip install -r pyproject.toml

# poetry の場合
poetry install
```

3. `.env` ファイルを作成し、Hugging Face のアクセストークン等を設定してください。

例:
```
HF_TOKEN=your_huggingface_token
```

## 🚀 使い方

### データセットのアップロード

```bash
python upload_dataset.py --input <input_jsonlファイル> --repo <HuggingFaceリポジトリ名> [--readme <README出力先>]
```

- `--input` : アップロードするJSONLファイルのパス
- `--repo` : アップロード先のHugging Faceリポジトリ名（例: username/Orin-Instruct-Alpaca-JP）
- `--readme` : （任意）READMEを自動生成する場合の出力先パス

### 例

```bash
python upload_dataset.py --input output-alpaca.jsonl --repo username/Orin-Instruct-Alpaca-JP --readme README.md
```

## 📂 データセット説明

- サンプル数: 40
- 形式: instruction-following（指示応答型）
- カラム:
  - instruction: 入力指示
  - input: 追加コンテキスト
  - output: 期待される応答
- instruction: 平均82.2文字（最大150、最小30）
- input: 常に空
- output: 平均118.0文字（最大258、最小29）

#### サンプル

```json
{
  "instruction": "生成AIは、どのような分野の進化に大きな影響を与えていると言えますか？\n",
  "input": "",
  "output": "生成AIは、テキスト生成モデルの進化を大きく後押しする役割を果たしています。\n"
}
```

## 🪪 ライセンス・引用

- ライセンスは元データソースに準じます。詳細は元データをご確認ください。
- 利用時は必ず元データの出典を明記してください。
