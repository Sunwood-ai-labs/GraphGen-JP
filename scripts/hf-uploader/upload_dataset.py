import json
import argparse
import os
from pathlib import Path
from datasets import Dataset
from huggingface_hub import HfApi, login
import pandas as pd
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

def load_jsonl(file_path):
    """JSONLファイルを読み込んでリストとして返す"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def create_dataset_from_jsonl(file_path):
    """JSONLファイルからHugging Face Datasetを作成"""
    data = load_jsonl(file_path)
    
    # データの構造を確認
    print(f"データ数: {len(data)}")
    if data:
        print(f"データの例: {data[0]}")
        print(f"カラム: {list(data[0].keys())}")
    
    # DatasetをPandasのDataFrameから作成
    df = pd.DataFrame(data)
    dataset = Dataset.from_pandas(df)
    
    return dataset, data

def generate_readme(data, dataset_name, file_path, columns):
    """READMEを自動生成"""
    file_name = Path(file_path).name
    
    # データの統計情報を取得
    total_samples = len(data)
    
    # 各カラムの統計
    column_stats = {}
    for col in columns:
        if col in data[0]:
            # 文字数の統計（テキストカラムの場合）
            lengths = [len(str(item.get(col, ''))) for item in data]
            column_stats[col] = {
                'avg_length': sum(lengths) / len(lengths),
                'max_length': max(lengths),
                'min_length': min(lengths)
            }
    
    # データサイズを計算（概算）
    total_chars = sum(len(json.dumps(item, ensure_ascii=False)) for item in data)
    estimated_bytes = total_chars * 3  # UTF-8での概算
    
    # YAML frontmatterを生成
    yaml_frontmatter = f"""---
dataset_info:
  features:
{chr(10).join(f"  - name: {col}" + chr(10) + "    dtype: string" for col in columns)}
  splits:
  - name: train
    num_bytes: {estimated_bytes}
    num_examples: {total_samples}
  download_size: {estimated_bytes // 2}
  dataset_size: {estimated_bytes}
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
language:
- ja
tags:
- instruction-following
- conversational-ai
- japanese
license: unknown
task_categories:
- text-generation
- question-answering
pretty_name: {dataset_name.replace('-', ' ').title()}
size_categories:
- {get_size_category(total_samples)}
---"""

    readme_content = f"""{yaml_frontmatter}

# {dataset_name}

## Dataset Description

This dataset contains {total_samples:,} samples in instruction-following format, suitable for training conversational AI models.

## Dataset Structure

### Data Fields

{chr(10).join(f"- **{col}**: {'Input instruction' if col == 'instruction' else 'Additional input context' if col == 'input' else 'Expected output/response'}" for col in columns)}

### Data Statistics

- **Total samples**: {total_samples:,}
{chr(10).join(f"- **{col}**: Avg length {column_stats[col]['avg_length']:.1f} chars, Max {column_stats[col]['max_length']} chars, Min {column_stats[col]['min_length']} chars" for col in column_stats)}

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("{'username'}/{dataset_name}")
```

## Data Sample

```json
{json.dumps(data[0], ensure_ascii=False, indent=2)}
```

## Source

- **Original file**: `{file_name}`
- **Generated on**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## License

Please refer to the original data source for licensing information.

## Citation

If you use this dataset, please cite the original source appropriately.
"""
    
    return readme_content

def get_size_category(num_samples):
    """サンプル数に基づいてサイズカテゴリを決定"""
    if num_samples < 1000:
        return "n<1K"
    elif num_samples < 10000:
        return "1K<n<10K"
    elif num_samples < 100000:
        return "10K<n<100K"
    elif num_samples < 1000000:
        return "100K<n<1M"
    else:
        return "n>1M"

def upload_to_huggingface(dataset, repo_name, token=None, private=True, readme_content=None):
    """Hugging Faceにデータセットをアップロード"""
    
    # 環境変数からトークンを取得（引数で指定されていない場合）
    if token is None:
        token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_TOKEN')
        if not token:
            print("エラー: Hugging Face APIトークンが見つかりません。")
            print(".envファイルにHF_TOKENを設定するか、--tokenオプションを使用してください。")
            return False
    
    # ログイン
    try:
        login(token=token)
    except Exception as e:
        print(f"ログインエラー: {e}")
        return False
    
    # データセットをHugging Face Hubにプッシュ
    dataset.push_to_hub(
        repo_id=repo_name,
        private=private,
        token=token
    )
    
    # READMEをアップロード
    if readme_content:
        try:
            api = HfApi()
            api.upload_file(
                path_or_fileobj=readme_content.encode('utf-8'),
                path_in_repo="README.md",
                repo_id=repo_name,
                repo_type="dataset",
                token=token
            )
            print("README.mdも正常にアップロードされました。")
        except Exception as e:
            print(f"README.mdのアップロードでエラーが発生しました: {e}")
    
    print(f"データセットが正常にアップロードされました: https://huggingface.co/datasets/{repo_name}")
    return True

def main():
    parser = argparse.ArgumentParser(description='JSONLファイルをHugging Face Datasetsにアップロード')
    parser.add_argument('file_path', help='JSONLファイルのパス')
    parser.add_argument('dataset_name', nargs='?', help='データセット名（指定しない場合はファイル名から自動生成）')
    parser.add_argument('--username', help='Hugging Faceのユーザー名（指定しない場合は.envから取得）')
    parser.add_argument('--token', help='Hugging Face APIトークン（指定しない場合は.envから取得）')
    parser.add_argument('--private', action='store_true', help='プライベートリポジトリとして作成')
    parser.add_argument('--public', action='store_true', help='パブリックリポジトリとして作成')
    parser.add_argument('--no-readme', action='store_true', help='READMEファイルを生成しない')
    
    args = parser.parse_args()
    
    # ファイルの存在確認
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"エラー: ファイル '{args.file_path}' が見つかりません")
        return
    
    # ユーザー名を取得
    username = args.username or os.getenv('HF_USERNAME') or os.getenv('HUGGINGFACE_USERNAME')
    if not username:
        print("エラー: ユーザー名が指定されていません。")
        print(".envファイルにHF_USERNAMEを設定するか、--usernameオプションを使用してください。")
        return
    
    # データセット名を決定
    if args.dataset_name:
        dataset_name = args.dataset_name
    else:
        # ファイル名から自動生成（拡張子を除去）
        dataset_name = file_path.stem
        print(f"データセット名が指定されていないため、ファイル名から自動生成しました: {dataset_name}")
    
    # リポジトリ名を構築
    repo_name = f"{username}/{dataset_name}"
    print(f"リポジトリ名: {repo_name}")
    
    # private/publicの設定
    if args.public:
        private = False
    else:
        private = True  # デフォルトはプライベート
    
    try:
        # データセットを作成
        print("JSONLファイルを読み込み中...")
        dataset, data = create_dataset_from_jsonl(file_path)
        
        # READMEを生成
        readme_content = None
        if not args.no_readme:
            print("README_datacard.mdを生成中...")
            columns = list(data[0].keys()) if data else []
            readme_content = generate_readme(data, dataset_name, file_path, columns)
            
            # READMEをローカルにも保存
            readme_path = Path("README_datacard.md")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print(f"README_datacard.mdをローカルに保存しました: {readme_path}")

        # アップロード
        print("Hugging Faceにアップロード中...")
        success = upload_to_huggingface(dataset, repo_name, args.token, private, readme_content)
        
        if not success:
            return
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()

# 使用例をコメントで記載
"""
使用方法:

1. 基本的な使用方法（.envファイルから設定を取得、READMEも自動生成）:
python upload_dataset.py path/to/your/file.jsonl

2. データセット名を指定:
python upload_dataset.py path/to/your/file.jsonl my-dataset

3. READMEを生成しない場合:
python upload_dataset.py path/to/your/file.jsonl --no-readme

4. ユーザー名を明示的に指定:
python upload_dataset.py path/to/your/file.jsonl --username your_username

5. パブリックリポジトリとして作成:
python upload_dataset.py path/to/your/file.jsonl --public

6. あなたのファイルの場合:
python upload_dataset.py "C:\Prj\GraphGen\cache\20250712_234723_0842\output-alpaca.jsonl" Orin-Instruct-Alpaca-JP --public

事前に必要な依存関係のインストール:
pip install datasets huggingface_hub pandas python-dotenv

.envファイルの作成 (プロジェクトルートに配置):
HF_TOKEN=your_huggingface_token_here
HF_USERNAME=your_huggingface_username_here

.envファイルの例:
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HF_USERNAME=myusername

生成されるREADME機能:
- データセットの統計情報（サンプル数、各カラムの文字数統計）
- データ構造の説明
- 使用方法のコード例
- データサンプルの表示
- 元ファイル情報と生成日時

注意:
- Hugging Face APIトークンは https://huggingface.co/settings/tokens で取得できます
- データセット名を指定しない場合、ファイル名から自動生成されます
- READMEはHugging Faceにアップロードされ、ローカルにも保存されます
- 環境変数名は HF_TOKEN/HF_USERNAME または HUGGINGFACE_TOKEN/HUGGINGFACE_USERNAME が使用可能
- コマンドライン引数は .env ファイルの設定より優先されます
- デフォルトではプライベートリポジトリとして作成されます
"""
