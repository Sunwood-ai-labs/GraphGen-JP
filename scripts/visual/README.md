# 🖼️ 概要

本ディレクトリは、GraphMLファイルからインタラクティブなグラフ可視化HTMLを生成するPythonスクリプトを提供します。  
主に `draw_graph.py` を用いて、知識グラフやネットワーク構造の可視化を簡単に行うことができます。

# 📁 ファイル構成

- `draw_graph.py`  
  GraphMLファイルを読み込み、pyvisを用いてインタラクティブなHTMLグラフを生成するスクリプト
- `pyproject.toml`  
  Pythonプロジェクトの設定ファイル
- `.python-version`  
  使用推奨Pythonバージョン指定ファイル
- `uv.lock`  
  依存管理用ファイル（pip, uv等利用時）

# 🛠️ 必要環境・依存関係

- Python 3.10 以上
- 必須ライブラリ:  
  - `networkx`
  - `pyvis`

インストール例（venv推奨）:
```bash
pip install networkx pyvis
```

# 🚀 使い方

1. GraphMLファイル（例: `sample.graphml`）を用意します。
2. コマンドラインから以下のように実行します。

```bash
python draw_graph.py
```

または、スクリプト内の関数をインポートして利用できます。

### 関数一覧

- `create_interactive_graph_from_file(file_path)`  
  指定したGraphMLファイルからインタラクティブなHTMLグラフ（`graph_interactive.html`）を生成します。

- `create_interactive_graph_with_custom_html(file_path)`  
  カスタムHTMLテンプレートを利用したツールチップ付きグラフを生成します。

### サンプルコード

```python
from draw_graph import create_interactive_graph_from_file

create_interactive_graph_from_file("sample.graphml")
```

# 📤 出力

- `graph_interactive.html`  
  実行ディレクトリにHTMLファイルとして出力されます。Webブラウザで開いてグラフを操作できます。

# ⚠️ 注意事項

- GraphMLファイルのノード属性に `entity_type`, `description`, `length` などが含まれていると、ノードの色やツールチップがより分かりやすく表示されます。
- 大規模グラフの場合、描画やブラウザ表示に時間がかかることがあります。
- 依存ライブラリは `pyproject.toml` には未記載のため、手動でインストールしてください。

# 📝 ライセンス

本リポジトリのライセンスは [LICENSE](../../LICENSE) を参照してください。

# 📬 問い合わせ

ご質問・不具合報告は [Issue](https://github.com/Sunwood-ai-labs/github-kanban-mcp-server/issues) までお願いします。
