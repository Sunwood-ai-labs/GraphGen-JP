あなたはNLPの専門家であり、テキストから固有表現とその関係を抽出することに長けています。

-目標-
与えられたテキストとエンティティタイプのリストから、該当するすべてのエンティティとその関係を抽出してください。
出力言語として{language}を使用してください。

-手順-
1. すべてのエンティティを特定し、以下の情報を抽出してください:
- entity_name: エンティティ名（入力テキストと同じ言語で）
- entity_type: 次のいずれか [{entity_types}]
- entity_summary: エンティティの属性や活動の要約
各エンティティは("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_summary>)の形式で出力

2. ステップ1で特定したエンティティ同士の*明確な関係*をすべて抽出し、以下の情報を記載してください:
- source_entity: 関係の出発点となるエンティティ名
- target_entity: 関係の到達点となるエンティティ名
- relationship_summary: 2つのエンティティが関係している理由の説明
各関係は("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_summary>)の形式で出力

3. テキスト全体の主要なキーワード（主題やトピック）を抽出し、("content_keywords"{tuple_delimiter}<high_level_keywords>)の形式で出力

4. ステップ1,2で抽出したすべてのエンティティと関係を{language}で1つのリストとして返してください。リストの区切りには**{record_delimiter}**を使用してください。

5. 最後に{completion_delimiter}を出力してください

################
-例-
################
-Example 1-
Text:
################
ローマ帝国は2世紀に最盛期を迎え、広大な領土と高度な文明を誇った。元老院は名目上の権威を持ち、実権は皇帝に委ねられていた。ネルウァ、トラヤヌス、ハドリアヌス、アントニヌスらの治世は繁栄の時代だった。
################
Output:
("entity"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"organization"{tuple_delimiter}"2世紀に最盛期を迎えた支配的な帝国。"){record_delimiter}
("entity"{tuple_delimiter}"元老院"{tuple_delimiter}"organization"{tuple_delimiter}"ローマ帝国の名目上の立法機関。"){record_delimiter}
("entity"{tuple_delimiter}"ネルウァ"{tuple_delimiter}"person"{tuple_delimiter}"繁栄期の皇帝の一人。"){record_delimiter}
("relationship"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"元老院"{tuple_delimiter}"元老院は名目上の権威を持ち、実権は皇帝に委ねられていた。"){record_delimiter}
("relationship"{tuple_delimiter}"ネルウァ"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"ネルウァは繁栄期の皇帝であった。"){record_delimiter}
("content_keywords"{tuple_delimiter}"ローマ帝国, 繁栄, 皇帝, 元老院"){completion_delimiter}

################
-実データ-
################
Entity_types: {entity_types}
Text: {input_text}
################
Output:
