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
    num_bytes: 29784
    num_examples: 40
  download_size: 14892
  dataset_size: 29784
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
pretty_name: Orin Instruct Alpaca Jp
size_categories:
- n<1K
---

# Orin-Instruct-Alpaca-JP

## Dataset Description

This dataset contains 40 samples in instruction-following format, suitable for training conversational AI models.

## Dataset Structure

### Data Fields

- **instruction**: Input instruction
- **input**: Additional input context
- **output**: Expected output/response

### Data Statistics

- **Total samples**: 40
- **instruction**: Avg length 82.2 chars, Max 150 chars, Min 30 chars
- **input**: Avg length 0.0 chars, Max 0 chars, Min 0 chars
- **output**: Avg length 118.0 chars, Max 258 chars, Min 29 chars

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("username/Orin-Instruct-Alpaca-JP")
```

## Data Sample

```json
{
  "instruction": "生成AIは、どのような分野の進化に大きな影響を与えていると言えますか？\n",
  "input": "",
  "output": "生成AIは、テキスト生成モデルの進化を大きく後押しする役割を果たしています。\n"
}
```

## Source

- **Original file**: `output-alpaca.jsonl`
- **Generated on**: 2025-07-13 01:35:09

## License

Please refer to the original data source for licensing information.

## Citation

If you use this dataset, please cite the original source appropriately.
