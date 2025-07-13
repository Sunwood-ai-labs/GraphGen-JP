import networkx as nx
from pyvis.network import Network
import os

def create_interactive_graph_from_file(file_path):
    """
    指定されたGraphMLファイルを読み込み、インタラクティブなHTMLグラフを生成する関数。
    """
    # --- 1. GraphMLファイルの読み込み ---
    try:
        G = nx.read_graphml(file_path)
        print(f"GraphMLファイル '{file_path}' の読み込みに成功しました。")
        print(f"ノード数: {G.number_of_nodes()}, エッジ数: {G.number_of_edges()}")
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません。")
        return
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
        return

    # --- 2. Pyvisネットワークの初期化 ---
    net = Network(
        height='800px', 
        width='100%', 
        bgcolor='#222222', 
        font_color='white', 
        notebook=False
    )

    # --- 3. ノードとエッジの情報をPyvisネットワークに追加 ---
    color_map = {
        'PERSON': 'skyblue', 'LOCATION': 'lightgreen', 'ORGANIZATION': 'salmon',
        'CONCEPT': 'khaki', 'PRODUCT': 'plum', 'EVENT': 'orange',
        'ENTITY': 'wheat', 'STATUS': 'pink', 'UNKNOWN': 'lightgray'
    }

    for node, data in G.nodes(data=True):
        entity_type = data.get('entity_type', 'UNKNOWN')
        description = data.get('description', '説明なし')
        length = data.get('length', 10)
        color = color_map.get(entity_type, 'lightgray')
        size = length * 0.5 + 10
        
        # ★★★ 修正点：HTMLタグを削除し、プレーンテキストで情報を整理 ★★★
        title_text = f"""ID: {node}
Type: {entity_type}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Description:
{str(description).replace('<SEP>', ' | ')}"""
        
        net.add_node(node, label=node, color=color, size=size, title=title_text)
        
    for u, v, data in G.edges(data=True):
        description = data.get('description', '')
        net.add_edge(u, v, title=str(description))

    # --- 4. HTMLファイルの生成 ---
    net.show_buttons(filter_=['physics'])
    
    output_filename = "graph_interactive.html"
    try:
        net.show(output_filename, notebook=False)
        print(f"\nインタラクティブなグラフを '{output_filename}' として保存しました。")
        print("このHTMLファイルをWebブラウザで開いて確認してください。")
    except Exception as e:
        print(f"HTMLファイルの保存中にエラーが発生しました: {e}")


# カスタムHTMLテンプレートを使用したい場合の代替案
def create_interactive_graph_with_custom_html(file_path):
    """
    カスタムHTMLテンプレートを使用してより見やすいツールチップを作成する関数。
    """
    try:
        G = nx.read_graphml(file_path)
        print(f"GraphMLファイル '{file_path}' の読み込みに成功しました。")
        print(f"ノード数: {G.number_of_nodes()}, エッジ数: {G.number_of_edges()}")
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません。")
        return
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
        return

    net = Network(
        height='800px', 
        width='100%', 
        bgcolor='#222222', 
        font_color='white', 
        notebook=False
    )

    color_map = {
        'PERSON': 'skyblue', 'LOCATION': 'lightgreen', 'ORGANIZATION': 'salmon',
        'CONCEPT': 'khaki', 'PRODUCT': 'plum', 'EVENT': 'orange',
        'ENTITY': 'wheat', 'STATUS': 'pink', 'UNKNOWN': 'lightgray'
    }

    for node, data in G.nodes(data=True):
        entity_type = data.get('entity_type', 'UNKNOWN')
        description = data.get('description', '説明なし')
        length = data.get('length', 10)
        color = color_map.get(entity_type, 'lightgray')
        size = length * 0.5 + 10
        
        # プレーンテキストで見やすく整理
        title_text = f"""【{entity_type}】{node}
        
説明：{str(description).replace('<SEP>', ' | ')}"""
        
        net.add_node(node, label=node, color=color, size=size, title=title_text)
        
    for u, v, data in G.edges(data=True):
        description = data.get('description', '')
        net.add_edge(u, v, title=str(description))

    net.show_buttons(filter_=['physics'])
    
    output_filename = "graph_interactive_custom.html"
    net.show(output_filename, notebook=False)
    
    # HTMLファイルを修正してより見やすいツールチップを作成
    with open(output_filename, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # カスタムCSSを追加してツールチップのスタイルを改善
    custom_css = """
    <style>
    .vis-tooltip {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #666 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-size: 14px !important;
        max-width: 300px !important;
        white-space: pre-wrap !important;
        line-height: 1.4 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
    }
    </style>
    """
    
    # headタグ内にCSSを挿入
    html_content = html_content.replace('</head>', custom_css + '</head>')
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nカスタムスタイル付きのインタラクティブグラフを '{output_filename}' として保存しました。")
    print("このHTMLファイルをWebブラウザで開いて確認してください。")


if __name__ == "__main__":
    graph_file_path = r"C:\Prj\GraphGen\cache\20250713_024458_4174\graph.graphml"
    
    # 基本版
    print("=== 基本版を生成中 ===")
    create_interactive_graph_from_file(graph_file_path)
    
    # カスタムHTML版
    print("\n=== カスタムHTML版を生成中 ===")
    create_interactive_graph_with_custom_html(graph_file_path)
