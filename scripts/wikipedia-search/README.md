# 🌟 Wikipedia検索・マークダウン保存ツール

## 📝 概要
このツールは、指定したキーワードでWikipediaを検索し、記事内容をマークダウン形式で保存します。  
日本語・英語に対応し、関連記事の自動保存や詳細なログ出力も可能です。

---

## 🚀 インストール方法

### Poetryを利用する場合
```bash
poetry install
```

### 直接pipでインストールする場合
```bash
pip install -r requirements.txt
```
※ 必要なPythonバージョン: 3.10以上

---

## ⚙️ 使い方

### 基本コマンド
```bash
python wikipedia_search.py "検索キーワード"
```

### 主なオプション
- `--lang`, `-l` : 言語設定（ja=日本語, en=英語）  
- `--sentences`, `-s` : 概要の文数（デフォルト: 3）
- `--save-related`, `-r` : 関連記事も保存
- `--max-related`, `-m` : 保存する関連記事の最大数（デフォルト: 5）
- `--output-dir`, `-o` : 出力ディレクトリ（デフォルト: ./wikipedia_search）
- `--verbose`, `-v` : 詳細ログを表示

### 実行例
```bash
python wikipedia_search.py "人工知能"
python wikipedia_search.py "machine learning" --lang en --sentences 5
python wikipedia_search.py "量子コンピュータ" --output-dir ./articles --verbose
python wikipedia_search.py "火焔猫燐" --save-related --max-related 3
```

---

## 📂 出力内容

- メイン記事:  
  - `出力ディレクトリ/記事タイトル.md`（マークダウン形式）
  - `出力ディレクトリ/記事タイトル.json`（メタデータ）

- 関連記事（`--save-related`指定時）:  
  - `出力ディレクトリ/記事タイトル_関連記事/関連_記事タイトル.md`

- ログファイル:  
  - `出力ディレクトリ/wikipedia_search.log`（INFO/DEBUGレベル）

---

## 🧩 依存パッケージ

- [loguru](https://github.com/Delgan/loguru)
- [wikipedia](https://pypi.org/project/wikipedia/)

---

## 🛡️ 注意事項

- Wikipedia APIの仕様変更や記事内容によっては、取得できない場合があります。
- ファイル名に使用できない文字は自動で除去されます。
- 取得した記事・関連情報は自動生成されるため、内容の正確性は保証されません。

---

## 📄 ライセンス

本ツールはMITライセンスで提供されています。

---

## 🖊️ 更新履歴

- 2025-07-13: README.md 初版整備

---

## 🙏 謝辞

- [loguru](https://github.com/Delgan/loguru)
- [wikipedia](https://pypi.org/project/wikipedia/)
