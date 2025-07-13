import json
import argparse
import os
from pathlib import Path
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi, login
import pandas as pd
from dotenv import load_dotenv
import random
from loguru import logger
import sys

# .envファイルを読み込み
load_dotenv()

# ログ設定
logger.remove()  # デフォルトのハンドラーを削除
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add("upload_dataset.log", rotation="10 MB", retention="10 days", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}")

def load_jsonl(file_path):
    """JSONLファイルを読み込んでリストとして返す"""
    logger.info(f"JSONLファイルを読み込み中: {file_path}")
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    logger.warning(f"行 {line_num} でJSONデコードエラー: {e}")
                    continue
    logger.success(f"データ読み込み完了: {len(data)} サンプル")
    return data

def split_data(data, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1, seed=42):
    """データをtrain/validation/testに分割"""
    # 浮動小数点数の精度問題を解決
    total_ratio = round(train_ratio + val_ratio + test_ratio, 10)
    if abs(total_ratio - 1.0) > 1e-9:
        raise ValueError(f"train_ratio + val_ratio + test_ratio must equal 1.0, got {total_ratio}")
    
    logger.info(f"データ分割開始 - Train: {train_ratio}, Val: {val_ratio}, Test: {test_ratio}, Seed: {seed}")
    
    # データをシャッフル
    random.seed(seed)
    shuffled_data = data.copy()
    random.shuffle(shuffled_data)
    
    total_samples = len(shuffled_data)
    train_end = int(total_samples * train_ratio)
    val_end = int(total_samples * (train_ratio + val_ratio))
    
    train_data = shuffled_data[:train_end]
    val_data = shuffled_data[train_end:val_end]
    test_data = shuffled_data[val_end:] if test_ratio > 0 else []
    
    logger.info(f"分割完了 - Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")
    return train_data, val_data, test_data

def create_dataset_from_jsonl(file_path, split_data_flag=False, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1, seed=42):
    """JSONLファイルからHugging Face Datasetを作成"""
    data = load_jsonl(file_path)
    
    # データの構造を確認
    logger.info(f"データ数: {len(data)}")
    if data:
        logger.info(f"データの例: {data[0]}")
        logger.info(f"カラム: {list(data[0].keys())}")
    
    if split_data_flag:
        # データを分割
        train_data, val_data, test_data = split_data(data, train_ratio, val_ratio, test_ratio, seed)
        
        logger.info(f"分割結果:")
        logger.info(f"  Train: {len(train_data)} samples")
        logger.info(f"  Validation: {len(val_data)} samples")
        if test_data:
            logger.info(f"  Test: {len(test_data)} samples")
        
        # DatasetDictを作成
        dataset_dict = DatasetDict({
            'train': Dataset.from_pandas(pd.DataFrame(train_data)),
            'validation': Dataset.from_pandas(pd.DataFrame(val_data))
        })
        
        if test_data:
            dataset_dict['test'] = Dataset.from_pandas(pd.DataFrame(test_data))
        
        logger.success("DatasetDict作成完了")
        return dataset_dict, data
    else:
        # 単一のデータセットとして作成
        df = pd.DataFrame(data)
        dataset = Dataset.from_pandas(df)
        logger.success("Dataset作成完了")
        return dataset, data

def generate_readme(data, dataset_name, file_path, columns, split_info=None):
    """READMEを自動生成"""
    logger.info("README生成開始")
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
    
    # スプリット情報を生成
    if split_info:
        splits_yaml = []
        for split_name, split_data in split_info.items():
            split_bytes = estimated_bytes * (len(split_data) / total_samples)
            splits_yaml.append(f"""  - name: {split_name}
    num_bytes: {int(split_bytes)}
    num_examples: {len(split_data)}""")
        splits_section = "\n".join(splits_yaml)
    else:
        splits_section = f"""  - name: train
    num_bytes: {estimated_bytes}
    num_examples: {total_samples}"""
    
    # YAML frontmatterを生成
    yaml_frontmatter = f"""---
dataset_info:
  features:
{chr(10).join(f"  - name: {col}" + chr(10) + "    dtype: string" for col in columns)}
  splits:
{splits_section}
  download_size: {estimated_bytes // 2}
  dataset_size: {estimated_bytes}
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
{chr(10).join(f"  - split: {split_name}" + chr(10) + f"    path: data/{split_name}-*" for split_name in split_info.keys() if split_name != 'train') if split_info else ""}
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

    # スプリット情報セクション
    split_stats = ""
    if split_info:
        split_stats = f"""
### Data Splits

{chr(10).join(f"- **{split_name}**: {len(split_data):,} samples" for split_name, split_data in split_info.items())}
"""

    readme_content = f"""{yaml_frontmatter}

# {dataset_name}

## Dataset Description

This dataset contains {total_samples:,} samples in instruction-following format, suitable for training conversational AI models.

## Dataset Structure

### Data Fields

{chr(10).join(f"- **{col}**: {'Input instruction' if col == 'instruction' else 'Additional input context' if col == 'input' else 'Expected output/response'}" for col in columns)}
{split_stats}
### Data Statistics

- **Total samples**: {total_samples:,}
{chr(10).join(f"- **{col}**: Avg length {column_stats[col]['avg_length']:.1f} chars, Max {column_stats[col]['max_length']} chars, Min {column_stats[col]['min_length']} chars" for col in column_stats)}

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("{'username'}/{dataset_name}")

# アクセス方法:
{'train_data = dataset["train"]' if split_info else 'train_data = dataset["train"]'}
{chr(10).join(f'{split_name}_data = dataset["{split_name}"]' for split_name in split_info.keys() if split_name != 'train') if split_info else ''}
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
    
    logger.success("README生成完了")
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
    logger.info(f"Hugging Faceへのアップロード開始: {repo_name}")
    
    # 環境変数からトークンを取得（引数で指定されていない場合）
    if token is None:
        token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_TOKEN')
        if not token:
            logger.error("Hugging Face APIトークンが見つかりません。")
            logger.error(".envファイルにHF_TOKENを設定するか、--tokenオプションを使用してください。")
            return False
    
    # ログイン
    try:
        logger.info("Hugging Face にログイン中...")
        login(token=token)
        logger.success("ログイン成功")
    except Exception as e:
        logger.error(f"ログインエラー: {e}")
        return False
    
    # データセットをHugging Face Hubにプッシュ
    try:
        logger.info("データセットをプッシュ中...")
        dataset.push_to_hub(
            repo_id=repo_name,
            private=private,
            token=token
        )
        logger.success("データセットプッシュ完了")
    except Exception as e:
        logger.error(f"データセットプッシュエラー: {e}")
        return False
    
    # READMEをアップロード
    if readme_content:
        try:
            logger.info("README.mdをアップロード中...")
            api = HfApi()
            api.upload_file(
                path_or_fileobj=readme_content.encode('utf-8'),
                path_in_repo="README.md",
                repo_id=repo_name,
                repo_type="dataset",
                token=token
            )
            logger.success("README.mdアップロード完了")
        except Exception as e:
            logger.warning(f"README.mdのアップロードでエラーが発生しました: {e}")
    
    logger.success(f"データセットが正常にアップロードされました: https://huggingface.co/datasets/{repo_name}")
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
    
    # データ分割関連のオプション
    parser.add_argument('--split', action='store_true', help='データをtrain/validationに分割')
    parser.add_argument('--train-ratio', type=float, default=0.7, help='訓練データの割合（デフォルト: 0.7）')
    parser.add_argument('--val-ratio', type=float, default=0.2, help='検証データの割合（デフォルト: 0.2）')
    parser.add_argument('--test-ratio', type=float, default=0.1, help='テストデータの割合（デフォルト: 0.1）')
    parser.add_argument('--seed', type=int, default=42, help='データ分割時のランダムシード（デフォルト: 42）')
    
    args = parser.parse_args()
    
    # 分割比率の検証
    if args.split:
        total_ratio = round(args.train_ratio + args.val_ratio + args.test_ratio, 10)
        if abs(total_ratio - 1.0) > 1e-9:
            logger.error(f"分割比率の合計が1.0になりません: {total_ratio}")
            logger.error(f"Train: {args.train_ratio}, Val: {args.val_ratio}, Test: {args.test_ratio}")
            return
    
    # ファイルの存在確認
    file_path = Path(args.file_path)
    if not file_path.exists():
        logger.error(f"ファイル '{args.file_path}' が見つかりません")
        return
    
    # ユーザー名を取得
    username = args.username or os.getenv('HF_USERNAME') or os.getenv('HUGGINGFACE_USERNAME')
    if not username:
        logger.error("ユーザー名が指定されていません。")
        logger.error(".envファイルにHF_USERNAMEを設定するか、--usernameオプションを使用してください。")
        return
    
    # データセット名を決定
    if args.dataset_name:
        dataset_name = args.dataset_name
    else:
        # ファイル名から自動生成（拡張子を除去）
        dataset_name = file_path.stem
        logger.info(f"データセット名が指定されていないため、ファイル名から自動生成しました: {dataset_name}")
    
    # リポジトリ名を構築
    repo_name = f"{username}/{dataset_name}"
    logger.info(f"リポジトリ名: {repo_name}")
    
    # private/publicの設定
    if args.public:
        private = False
        logger.info("パブリックリポジトリとして作成します")
    else:
        private = True  # デフォルトはプライベート
        logger.info("プライベートリポジトリとして作成します")
    
    try:
        # データセットを作成
        print("JSONLファイルを読み込み中...")
        dataset, data = create_dataset_from_jsonl(
            file_path, 
            split_data_flag=args.split,
            train_ratio=args.train_ratio,
            val_ratio=args.val_ratio,
            test_ratio=args.test_ratio,
            seed=args.seed
        )
        
        # READMEを生成
        readme_content = None
        if not args.no_readme:
            print("README.mdを生成中...")
            columns = list(data[0].keys()) if data else []
            
            # スプリット情報を準備
            split_info = None
            if args.split and isinstance(dataset, DatasetDict):
                split_info = {}
                if args.split:
                    total_samples = len(data)
                    train_end = int(total_samples * args.train_ratio)
                    val_end = int(total_samples * (args.train_ratio + args.val_ratio))
                    
                    split_info['train'] = data[:train_end]
                    split_info['validation'] = data[train_end:val_end]
                    if args.test_ratio > 0:
                        split_info['test'] = data[val_end:]
            
            readme_content = generate_readme(data, dataset_name, file_path, columns, split_info)
            
            # READMEをローカルにも保存
            readme_path = Path("README.md")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print(f"README.mdをローカルに保存しました: {readme_path}")

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

1. 基本的な使用方法（分割なし）:
python upload_dataset.py path/to/your/file.jsonl

2. データをtrain/validationに分割（8:2の割合）:
python upload_dataset.py path/to/your/file.jsonl --split

3. カスタム分割比率（train:val:test = 7:2:1）:
python upload_dataset.py path/to/your/file.jsonl --split --train-ratio 0.7 --val-ratio 0.2 --test-ratio 0.1

4. データセット名を指定して分割:
python upload_dataset.py path/to/your/file.jsonl my-dataset --split

5. パブリックリポジトリとして作成（分割あり）:
python upload_dataset.py path/to/your/file.jsonl --split --public

6. ランダムシードを指定（再現性のため）:
python upload_dataset.py path/to/your/file.jsonl --split --seed 123

7. あなたのファイルの場合（分割あり）:
python upload_dataset.py "C:\Prj\GraphGen\cache\20250712_234723_0842\output-alpaca.jsonl" Orin-Instruct-Alpaca-JP --split --public

データセットの使用方法:
```python
from datasets import load_dataset

# 分割されたデータセットの場合
dataset = load_dataset("username/dataset-name")
train_data = dataset["train"]
val_data = dataset["validation"]

# 各分割に対する操作
print(f"Train samples: {len(train_data)}")
print(f"Validation samples: {len(val_data)}")
```

注意事項:
- --splitオプションを使用すると、データは自動的にシャッフルされます
- デフォルトの分割比率は train:validation = 8:2 です
- --test-ratioを指定すると、テストセットも作成されます
- 分割比率の合計は必ず1.0になる必要があります
- --seedオプションで再現性を確保できます
"""
