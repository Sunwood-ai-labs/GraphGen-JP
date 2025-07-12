#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌟 Wikipedia検索・マークダウン保存・JSONL変換スクリプト 🌟
指定されたキーワードでWikipediaを検索し、結果をマークダウンファイルに保存し、
さらにJSONL形式でコンテンツを結合できます。
"""

import wikipedia
import os
import re
from datetime import datetime
from pathlib import Path
import argparse
import sys
from typing import Dict, Optional, List
from loguru import logger
import json
import glob


class WikipediaSearcher:
    """Wikipedia検索とマークダウン保存を行うクラス"""
    
    def __init__(self, output_dir: str = "./wikipedia_search"):
        self.output_dir = Path(output_dir)
        self.setup_logging()
        self.setup_output_directory()
    
    def setup_logging(self):
        """ログ設定を初期化"""
        # デフォルトのログ設定を削除
        logger.remove()
        
        # コンソール出力用の設定（カラフル）
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>",
            level="INFO",
            colorize=True,
            backtrace=True,
            diagnose=True
        )
        
        # ファイル出力用の設定
        log_file = self.output_dir / "wikipedia_search.log"
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        logger.info("🚀 Wikipedia検索ツールを開始しました")
    
    def setup_output_directory(self):
        """出力ディレクトリを作成"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.success(f"📁 出力ディレクトリを準備しました: {self.output_dir}")
        except Exception as e:
            logger.error(f"❌ 出力ディレクトリの作成に失敗しました: {e}")
            raise
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """ファイル名に使用できない文字を削除する"""
        logger.debug(f"🔧 ファイル名を安全化中: {filename}")
        
        # Windows/Linuxで使用できない文字を削除
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # 連続するスペースを単一のスペースに置換
        filename = re.sub(r'\s+', ' ', filename)
        # 先頭・末尾のスペースを削除
        filename = filename.strip()
        # 長すぎるファイル名は切り詰める
        if len(filename) > 100:
            filename = filename[:100]
            logger.warning(f"⚠️ ファイル名が長すぎるため切り詰めました: {filename}")
        
        logger.debug(f"✅ 安全化されたファイル名: {filename}")
        return filename
    
    def format_markdown_content(self, title: str, summary: str, content: str, url: str, metadata: Dict) -> str:
        """マークダウン形式のコンテンツを生成する"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        markdown_content = f"""#  {title}


---

## 概要

{summary}

---

## 詳細内容

{content}

---

## 関連候補

{self._format_related_topics(metadata.get('search_results', []))}

---

<div align="center">
<em>🤖 このファイルは Wikipedia検索ツールによって自動生成されました</em><br>
<em>⚡ Powered by loguru & wikipedia-api</em>
</div>
"""
        return markdown_content
    
    def _format_related_topics(self, search_results: List[str]) -> str:
        """関連トピックをマークダウンリスト形式で整形"""
        if len(search_results) <= 1:
            return "*関連トピックはありません*"
        
        related_topics = []
        for i, topic in enumerate(search_results[1:6], 1):  # 最大5件
            related_topics.append(f"{i}. **{topic}**")
        
        return "\n".join(related_topics)
    
    def search_wikipedia(self, keyword: str, lang: str = 'ja', sentences: int = 3) -> Dict:
        """
        Wikipediaでキーワードを検索し、結果を取得する
        
        Args:
            keyword: 検索キーワード
            lang: 言語設定（'ja'=日本語, 'en'=英語）
            sentences: 概要の文数
        
        Returns:
            検索結果の辞書
        """
        logger.info(f"🔍 Wikipedia検索を開始: キーワード='{keyword}', 言語={lang}")
        
        try:
            # Wikipedia言語設定
            wikipedia.set_lang(lang)
            logger.debug(f"🌐 言語設定を変更しました: {lang}")
            
            # 検索実行
            with logger.contextualize(keyword=keyword):
                logger.info(f"🔎 '{keyword}'を検索中...")
                
                # 検索候補を取得
                search_results = wikipedia.search(keyword, results=10)
                
                if not search_results:
                    logger.warning(f"⚠️ '{keyword}'に関する記事が見つかりませんでした")
                    return {
                        'success': False,
                        'error': f"'{keyword}'に関する記事が見つかりませんでした。"
                    }
                
                logger.success(f"✅ {len(search_results)}件の検索結果を取得しました")
                logger.debug(f"📝 検索結果: {search_results[:5]}")
                
                # 最初の候補を取得
                page_title = search_results[0]
                logger.info(f"📄 記事を取得中: {page_title}")
                
                # ページの詳細情報を取得
                page = wikipedia.page(page_title)
                logger.debug(f"📊 記事サイズ: {len(page.content)} 文字")
                
                # 概要を取得
                summary = wikipedia.summary(page_title, sentences=sentences)
                logger.debug(f"📝 概要サイズ: {len(summary)} 文字")
                
                logger.success(f"🎉 '{page.title}'の取得が完了しました")
                
                return {
                    'success': True,
                    'title': page.title,
                    'summary': summary,
                    'content': page.content,
                    'url': page.url,
                    'search_results': search_results,
                    'metadata': {
                        'keyword': keyword,
                        'lang': lang,
                        'sentences': sentences,
                        'content_length': len(page.content),
                        'summary_length': len(summary)
                    }
                }
                
        except wikipedia.exceptions.DisambiguationError as e:
            logger.warning(f"🔀 曖昧さ回避が必要です: {len(e.options)}件の候補")
            logger.debug(f"📋 候補一覧: {e.options[:5]}")
            
            try:
                # 最初の候補を使用
                page = wikipedia.page(e.options[0])
                summary = wikipedia.summary(e.options[0], sentences=sentences)
                
                logger.info(f"🎯 最初の候補を使用しました: {page.title}")
                
                return {
                    'success': True,
                    'title': page.title,
                    'summary': summary,
                    'content': page.content,
                    'url': page.url,
                    'search_results': e.options[:10],
                    'metadata': {
                        'keyword': keyword,
                        'lang': lang,
                        'sentences': sentences,
                        'disambiguation': True,
                        'content_length': len(page.content),
                        'summary_length': len(summary)
                    }
                }
            except Exception as inner_e:
                logger.error(f"❌ 曖昧さ回避の処理中にエラーが発生: {inner_e}")
                return {
                    'success': False,
                    'error': f"曖昧さ回避の処理中にエラーが発生しました: {str(inner_e)}"
                }
        
        except wikipedia.exceptions.PageError as e:
            logger.error(f"❌ ページが見つかりませんでした: {keyword}")
            return {
                'success': False,
                'error': f"'{keyword}'のページが見つかりませんでした。"
            }
        
        except Exception as e:
            logger.error(f"❌ 予期しないエラーが発生: {e}")
            logger.exception("詳細なエラー情報:")
            return {
                'success': False,
                'error': f"検索中にエラーが発生しました: {str(e)}"
            }
    
    def save_to_markdown(self, result: Dict) -> str:
        """
        検索結果をマークダウンファイルに保存する
        
        Args:
            result: 検索結果の辞書
        
        Returns:
            保存されたファイルのパス
        """
        logger.info(f"💾 マークダウンファイルを保存中: {result['title']}")
        
        try:
            # ファイル名を生成
            safe_title = self.sanitize_filename(result['title'])
            filename = f"{safe_title}.md"
            filepath = self.output_dir / filename
            
            # マークダウンコンテンツを生成
            markdown_content = self.format_markdown_content(
                result['title'],
                result['summary'],
                result['content'],
                result['url'],
                result.get('metadata', {})
            )
            
            # ファイルに保存
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # メタデータも保存
            metadata_file = filepath.with_suffix('.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(result.get('metadata', {}), f, indent=2, ensure_ascii=False)
            
            logger.success(f"✅ ファイル保存完了: {filepath}")
            logger.info(f"📊 ファイルサイズ: {filepath.stat().st_size:,} bytes")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ ファイル保存中にエラーが発生: {e}")
            logger.exception("詳細なエラー情報:")
            raise
    
    def search_related_articles(self, search_results: List[str], lang: str = 'ja', max_articles: int = 5) -> List[Dict]:
        """関連記事を検索して取得"""
        related_articles = []
        
        # メイン記事は除外して処理
        for i, title in enumerate(search_results[1:max_articles+1], 1):
            try:
                logger.info(f"🔗 関連記事を取得中 ({i}/{min(max_articles, len(search_results)-1)}): {title}")
                
                page = wikipedia.page(title)
                summary = wikipedia.summary(title, sentences=2)
                
                related_articles.append({
                    'title': page.title,
                    'summary': summary,
                    'content': page.content,
                    'url': page.url,
                    'metadata': {
                        'lang': lang,
                        'content_length': len(page.content),
                        'summary_length': len(summary),
                        'is_related': True
                    }
                })
                
                logger.success(f"✅ 関連記事取得完了: {page.title}")
                
            except Exception as e:
                logger.warning(f"⚠️ 関連記事の取得に失敗: {title} - {e}")
                continue
        
        return related_articles
    
    def save_related_articles(self, related_articles: List[Dict], main_keyword: str) -> List[str]:
        """関連記事をマークダウンファイルに保存"""
        saved_files = []
        related_dir = self.output_dir / f"{self.sanitize_filename(main_keyword)}_関連記事"
        related_dir.mkdir(exist_ok=True)
        
        logger.info(f"📁 関連記事用ディレクトリを作成: {related_dir}")
        
        for article in related_articles:
            try:
                safe_title = self.sanitize_filename(article['title'])
                filename = f"関連_{safe_title}.md"
                filepath = related_dir / filename
                
                # 関連記事用のマークダウンコンテンツを生成
                markdown_content = self.format_markdown_content(
                    f"[関連記事] {article['title']}",
                    article['summary'],
                    article['content'],
                    article['url'],
                    article.get('metadata', {})
                )
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                saved_files.append(str(filepath))
                logger.debug(f"📄 関連記事を保存: {filepath}")
                
            except Exception as e:
                logger.error(f"❌ 関連記事の保存に失敗: {article['title']} - {e}")
                continue
        
        return saved_files
    
    def extract_content_from_markdown(self, markdown_file: Path) -> str:
        """マークダウンファイルから全コンテンツを抽出する"""
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # 余分な改行を削除し、段落を適切に結合
            content = re.sub(r'\n\s*\n', '\n', content)
            content = content.replace('\n', ' ').strip()
            
            logger.debug(f"✅ コンテンツ抽出完了: {len(content)} 文字")
            return content
                
        except Exception as e:
            logger.error(f"❌ マークダウンファイルの読み込みエラー: {markdown_file} - {e}")
            return ""
    
    def convert_to_jsonl(self, input_dir: Optional[str] = None, output_file: str = "wikipedia_content.jsonl") -> str:
        """
        マークダウンファイルをJSONL形式に変換して結合する
        
        Args:
            input_dir: 入力ディレクトリ（Noneの場合は出力ディレクトリを使用）
            output_file: 出力JSONLファイル名
        
        Returns:
            出力ファイルのパス
        """
        if input_dir is None:
            input_dir = self.output_dir
        else:
            input_dir = Path(input_dir)
        
        output_path = self.output_dir / output_file
        
        logger.info(f"📄 JSONL変換を開始: {input_dir} -> {output_path}")
        
        # マークダウンファイルを再帰的に検索
        markdown_files = []
        for pattern in ['**/*.md', '*.md']:
            markdown_files.extend(input_dir.glob(pattern))
        
        # 重複を除去し、ファイル名でソート
        markdown_files = sorted(list(set(markdown_files)))
        
        if not markdown_files:
            logger.warning(f"⚠️ マークダウンファイルが見つかりません: {input_dir}")
            return ""
        
        logger.info(f"📚 {len(markdown_files)}個のマークダウンファイルを発見しました")
        
        converted_count = 0
        
        try:
            with open(output_path, 'w', encoding='utf-8') as jsonl_file:
                for md_file in markdown_files:
                    logger.debug(f"🔄 処理中: {md_file}")
                    
                    # マークダウンファイルからコンテンツを抽出
                    content = self.extract_content_from_markdown(md_file)
                    
                    if content:
                        # JSONLエントリを作成
                        entry = {
                            "content": content
                        }
                        
                        # JSONLファイルに書き込み
                        jsonl_file.write(json.dumps(entry, ensure_ascii=False) + '\n')
                        converted_count += 1
                        logger.debug(f"✅ 変換完了: {md_file.name} ({len(content)} 文字)")
                    else:
                        logger.warning(f"⚠️ コンテンツが空です: {md_file}")
            
            # 各ファイルの詳細情報を表示
            logger.info(f"📋 変換されたファイル一覧:")
            for i, md_file in enumerate(markdown_files, 1):
                content = self.extract_content_from_markdown(md_file)
                if content:
                    logger.info(f"   {i:2d}. {md_file.name} ({len(content):,} 文字)")
            
            logger.success(f"🎉 JSONL変換完了: {converted_count}件のエントリを保存しました")
            logger.info(f"📂 出力ファイル: {output_path}")
            logger.info(f"📊 ファイルサイズ: {output_path.stat().st_size:,} bytes")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ JSONL変換中にエラーが発生: {e}")
            logger.exception("詳細なエラー情報:")
            return ""
    
    def search_and_save(self, keyword: str, lang: str = 'ja', sentences: int = 3, save_related: bool = False, max_related: int = 5) -> Optional[str]:
        """検索から保存までの一連の処理を実行"""
        logger.info(f"🚀 検索・保存処理を開始: {keyword}")
        
        # 検索実行
        result = self.search_wikipedia(keyword, lang, sentences)
        
        if not result['success']:
            logger.error(f"❌ 検索失敗: {result['error']}")
            return None
        
        # メイン記事の保存
        try:
            filepath = self.save_to_markdown(result)
            logger.success(f"🎉 メイン記事の保存完了: {filepath}")
            
            # 関連記事の処理
            related_files = []
            if save_related and len(result.get('search_results', [])) > 1:
                logger.info(f"🔍 関連記事の検索を開始 (最大{max_related}件)")
                
                related_articles = self.search_related_articles(
                    result['search_results'], 
                    lang, 
                    max_related
                )
                
                if related_articles:
                    related_files = self.save_related_articles(related_articles, keyword)
                    logger.success(f"📚 関連記事を{len(related_files)}件保存しました")
                else:
                    logger.warning("⚠️ 関連記事が取得できませんでした")
            
            # 統計情報を表示
            metadata = result.get('metadata', {})
            logger.info(f"📈 統計情報:")
            logger.info(f"   📝 メインコンテンツ長: {metadata.get('content_length', 0):,} 文字")
            logger.info(f"   📄 概要長: {metadata.get('summary_length', 0):,} 文字")
            logger.info(f"   🔗 検索結果: {len(result.get('search_results', [])):,} 件")
            if save_related:
                logger.info(f"   📚 保存された関連記事: {len(related_files)} 件")
            
            return filepath
            
        except Exception as e:
            logger.error(f"❌ 保存処理で予期しないエラー: {e}")
            return None


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='🌟 Wikipediaからキーワードを検索してマークダウンで保存し、JSONLに変換',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 基本的な検索
  python wikipedia_search.py "人工知能"
  
  # 英語で検索
  python wikipedia_search.py "machine learning" --lang en --sentences 5
  
  # 関連記事も保存
  python wikipedia_search.py "量子コンピュータ" --save-related --max-related 3
  
  # JSONL変換のみ実行
  python wikipedia_search.py --convert-only --input-dir ./articles --jsonl-output combined.jsonl
  
  # 検索 + JSONL変換
  python wikipedia_search.py "火焔猫燐" --save-related --convert-jsonl
        """
    )
    
    parser.add_argument('keyword', nargs='?', help='🔍 検索キーワード')
    parser.add_argument('--lang', '-l', default='ja', 
                       choices=['ja', 'en'], 
                       help='🌐 言語設定 (ja=日本語, en=英語)')
    parser.add_argument('--sentences', '-s', type=int, default=3,
                       help='📝 概要の文数')
    parser.add_argument('--save-related', '-r', action='store_true',
                       help='🔗 関連記事も保存する')
    parser.add_argument('--max-related', '-m', type=int, default=5,
                       help='📚 保存する関連記事の最大数 (デフォルト: 5)')
    parser.add_argument('--output-dir', '-o', default='./wikipedia_search',
                       help='📁 出力ディレクトリ')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='🔍 詳細ログを表示')
    
    # JSONL変換関連のオプション
    parser.add_argument('--convert-jsonl', action='store_true',
                       help='📄 検索後にJSONL変換も実行する')
    parser.add_argument('--convert-only', action='store_true',
                       help='🔄 JSONL変換のみを実行する（検索はしない）')
    parser.add_argument('--input-dir', type=str,
                       help='📂 JSONL変換用の入力ディレクトリ（convert-onlyの場合）')
    parser.add_argument('--jsonl-output', default='wikipedia_content.jsonl',
                       help='📝 出力JSONLファイル名')
    
    args = parser.parse_args()
    
    # convert-onlyの場合はkeywordは不要
    if not args.convert_only and not args.keyword:
        parser.error("検索キーワードが必要です（--convert-onlyの場合は除く）")
    
    # 詳細ログの設定
    if args.verbose:
        logger.remove()
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>",
            level="DEBUG",
            colorize=True
        )
    
    # Wikipedia検索ツールを初期化
    searcher = WikipediaSearcher(args.output_dir)
    
    # JSONL変換のみの場合
    if args.convert_only:
        logger.info("🔄 JSONL変換モードで実行します")
        jsonl_path = searcher.convert_to_jsonl(
            input_dir=args.input_dir,
            output_file=args.jsonl_output
        )
        
        if jsonl_path:
            logger.success(f"🎊 JSONL変換が正常に完了しました!")
            logger.info(f"📂 保存場所: {jsonl_path}")
            return 0
        else:
            logger.error(f"💥 JSONL変換が失敗しました")
            return 1
    
    # 通常の検索・保存実行
    filepath = searcher.search_and_save(
        args.keyword, 
        args.lang, 
        args.sentences,
        args.save_related,
        args.max_related
    )
    
    if filepath:
        logger.success(f"🎊 検索・保存処理が正常に完了しました!")
        logger.info(f"📂 保存場所: {filepath}")
        
        # JSONL変換も実行する場合
        if args.convert_jsonl:
            logger.info("📄 JSONL変換を開始します...")
            jsonl_path = searcher.convert_to_jsonl(output_file=args.jsonl_output)
            
            if jsonl_path:
                logger.success(f"🎉 JSONL変換も完了しました!")
                logger.info(f"📂 JSONLファイル: {jsonl_path}")
            else:
                logger.warning("⚠️ JSONL変換に失敗しましたが、検索・保存は成功しています")
        
        return 0
    else:
        logger.error(f"💥 処理が失敗しました")
        return 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        logger.warning("⏹️ ユーザーによって処理が中断されました")
        exit(130)
    except Exception as e:
        logger.critical(f"💀 予期しない致命的エラー: {e}")
        logger.exception("詳細なエラー情報:")
        exit(1)
