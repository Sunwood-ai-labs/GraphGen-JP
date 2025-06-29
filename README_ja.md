<div align="center">

[🇯🇵 日本語](README_ja.md) ｜ [🇬🇧 English](README.md)

</div>

<p align="center">
  <img src="resources/images/logo.png"/>
</p>

<!-- バッジ -->
[![stars](https://img.shields.io/github/stars/open-sciencelab/GraphGen.svg)](https://github.com/open-sciencelab/GraphGen)
[![forks](https://img.shields.io/github/forks/open-sciencelab/GraphGen.svg)](https://github.com/open-sciencelab/GraphGen)
[![open issues](https://img.shields.io/github/issues-raw/open-sciencelab/GraphGen)](https://github.com/open-sciencelab/GraphGen/issues)
[![issue resolution](https://img.shields.io/github/issues-closed-raw/open-sciencelab/GraphGen)](https://github.com/open-sciencelab/GraphGen/issues)
[![documentation](https://img.shields.io/badge/docs-latest-blue)](https://graphgen-cookbook.readthedocs.io/en/latest/)
[![wechat](https://img.shields.io/badge/wechat-brightgreen?logo=wechat&logoColor=white)](https://cdn.vansin.top/internlm/dou.jpg)
[![arXiv](https://img.shields.io/badge/Paper-arXiv-white)](https://arxiv.org/abs/2505.20416)
[![Hugging Face](https://img.shields.io/badge/Paper-on%20HF-white?logo=huggingface&logoColor=yellow)](https://huggingface.co/papers/2505.20416)
[![Hugging Face](https://img.shields.io/badge/Demo-on%20HF-blue?logo=huggingface&logoColor=yellow)](https://huggingface.co/spaces/chenzihong/GraphGen)
[![OpenXLab](https://img.shields.io/badge/Demo-on%20OpenXLab-blue?logo=openxlab&logoColor=yellow)](https://g-app-center-000704-6802-aerppvq.openxlab.space)

# 📝 GraphGenとは？

GraphGenは、知識グラフを活用した大規模言語モデル（LLM）向けの合成データ生成フレームワークです。  
詳細は[論文](https://arxiv.org/abs/2505.20416)や[ベストプラクティス](https://github.com/open-sciencelab/GraphGen/issues/17)をご参照ください。

- ソーステキストから細粒度な知識グラフを構築
- LLMの知識ギャップを特定し、価値の高いQAペアを優先生成
- 複雑な関係性を捉えるためのマルチホップ近傍サンプリング
- スタイル制御による多様なQAデータ生成

---

## 📚 目次

- 📝 [GraphGenとは？](#-graphgenとは)
- 🚀 [クイックスタート](#-クイックスタート)
- 📌 [最新情報](#-最新情報)
- 🏗️ [システム構成](#-システム構成)
- 🍀 [謝辞](#-謝辞)
- 📚 [引用](#-引用)
- 📜 [ライセンス](#-ライセンス)

---

## 🚀 クイックスタート

- [Webデモ](https://g-app-center-000704-6802-aerppvq.openxlab.space) または [バックアップWeb入口](https://openxlab.org.cn/apps/detail/tpoisonooo/GraphGen) から体験できます。
- 質問は[FAQ](https://github.com/open-sciencelab/GraphGen/issues/10)や[issue作成](https://github.com/open-sciencelab/GraphGen/issues)、[WeChatグループ](https://cdn.vansin.top/internlm/dou.jpg)でどうぞ。

### 準備

1. [uv](https://docs.astral.sh/uv/reference/installer/)のインストール

    ```bash
    # ネットワーク問題がある場合はpipxやpipも利用可能。詳細はuv公式ドキュメント参照
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

---

## 🏗️ システム構成

（※詳細は後日追記）

---

## 🍀 謝辞

本プロジェクトは多くのオープンソースコミュニティ・研究者の貢献に支えられています。

---

## 📚 引用

```
@article{GraphGen2024,
  title={GraphGen: Enhancing Supervised Fine-Tuning for LLMs with Knowledge-Driven Synthetic Data Generation},
  author={...},
  journal={arXiv preprint arXiv:2505.20416},
  year={2024}
}
```

---

## 📜 ライセンス

本プロジェクトはMITライセンスの下で公開されています。
