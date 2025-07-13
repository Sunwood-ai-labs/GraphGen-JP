---
dataset_info:
  features:
  - name: instruction
    dtype: string
  - name: input
    dtype: string
  - name: output
    dtype: string
  splits:
  - name: train
    num_bytes: 328957
    num_examples: 446
  - name: validation
    num_bytes: 94409
    num_examples: 128
  - name: test
    num_bytes: 47204
    num_examples: 64
  download_size: 235285
  dataset_size: 470571
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: validation
    path: data/validation-*
  - split: test
    path: data/test-*
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
pretty_name: Orin Instruct Alpaca Jp
size_categories:
- n<1K
---

# Orin-Instruct-Alpaca-JP

## Dataset Description

This dataset contains 638 samples in instruction-following format, suitable for training conversational AI models.

## Dataset Structure

### Data Fields

- **instruction**: Input instruction
- **input**: Additional input context
- **output**: Expected output/response

### Data Splits

- **train**: 446 samples
- **validation**: 128 samples
- **test**: 64 samples

### Data Statistics

- **Total samples**: 638
- **instruction**: Avg length 83.4 chars, Max 518 chars, Min 16 chars
- **input**: Avg length 0.0 chars, Max 0 chars, Min 0 chars
- **output**: Avg length 114.4 chars, Max 352 chars, Min 17 chars

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("username/Orin-Instruct-Alpaca-JP")

# アクセス方法:
train_data = dataset["train"]
validation_data = dataset["validation"]
test_data = dataset["test"]
```

## Data Sample

```json
{
  "instruction": "ゲーム「2023年 チュウニズム サン」に登場するリー・メイメイは、どのような役割を担っていますか？\n",
  "input": "",
  "output": "ゲーム「2023年 チュウニズム サン」において、リー・メイメイは主要なキャラクターとして登場します。\n"
}
```

## Source

- **Original file**: `output-alpaca.jsonl`
- **Generated on**: 2025-07-13 21:24:02

## License

Please refer to the original data source for licensing information.

## Citation

If you use this dataset, please cite the original source appropriately.
