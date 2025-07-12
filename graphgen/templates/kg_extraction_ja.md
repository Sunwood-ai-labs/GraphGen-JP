```
あなたはNLPの専門家であり、テキストを分析して固有表現とその関係を抽出することに長けています。

-目標-
この活動に関連する可能性のあるテキスト文書とエンティティタイプのリストが与えられた場合、テキストからそれらのタイプのすべてのエンティティと、特定されたエンティティ間のすべての関係を識別してください。
出力言語として{language}を使用してください。

-手順-
1. すべてのエンティティを特定してください。各エンティティについて、以下の情報を抽出してください:
- entity_name: エンティティの名前（入力テキストと同じ言語を使用。英語の場合は大文字で表記）
- entity_type: 次のいずれかのタイプ: [{entity_types}]
- entity_summary: エンティティの属性と活動の包括的な要約
各エンティティは("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_summary>)の形式で出力

2. ステップ1で特定したエンティティから、互いに*明確に関連している*すべての(source_entity, target_entity)のペアを特定してください。
関連するエンティティの各ペアについて、以下の情報を抽出してください:
- source_entity: ステップ1で特定されたソースエンティティの名前
- target_entity: ステップ1で特定されたターゲットエンティティの名前
- relationship_summary: ソースエンティティとターゲットエンティティが互いに関連していると思われる理由の説明
各関係は("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_summary>)の形式で出力

3. テキスト全体の主要な概念、テーマ、またはトピックを要約する高レベルなキーワードを特定してください。これらは文書に存在する包括的なアイデアを捉えるものでなければなりません。
コンテンツレベルのキーワードは("content_keywords"{tuple_delimiter}<high_level_keywords>)の形式で出力

4. ステップ1と2で特定したすべてのエンティティと関係を{language}で単一のリストとして返してください。リストの区切り文字として**{record_delimiter}**を使用してください。

5. 完了時に{completion_delimiter}を出力してください

################
-例-
################
-例1-
テキスト:
################
キリスト教時代の2世紀において、ローマ帝国は地上で最も美しい部分と、人類の最も文明化された部分を包含していた。その広大な君主制の国境は、古代の名声と規律ある勇気によって守られていた。法と慣習の穏やかだが強力な影響により、諸州の結合は徐々に固められた。平和な住民たちは富と贅沢の利益を享受し、また濫用した。自由な憲法のイメージは適切な敬意をもって保持されていた：ローマ元老院は主権を持っているように見え、政府のすべての執行権を皇帝に委ねた。80年以上の幸福な期間において、公的行政はネルウァ、トラヤヌス、ハドリアヌス、そして2人のアントニヌスの美徳と能力によって運営された。
################
出力:
("entity"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"organization"{tuple_delimiter}"2世紀キリスト教時代の支配的な帝国で、既知の世界の最も発展した地域を包含していた。"){record_delimiter}
("entity"{tuple_delimiter}"2世紀キリスト教時代"{tuple_delimiter}"date"{tuple_delimiter}"ローマ帝国が最盛期にあったキリスト教時代の時期。"){record_delimiter}
("entity"{tuple_delimiter}"ローマ"{tuple_delimiter}"location"{tuple_delimiter}"ローマ帝国の首都であり心臓部。"){record_delimiter}
("entity"{tuple_delimiter}"ローマ元老院"{tuple_delimiter}"organization"{tuple_delimiter}"ローマで主権を持っているように見えた立法機関。"){record_delimiter}
("entity"{tuple_delimiter}"ネルウァ"{tuple_delimiter}"person"{tuple_delimiter}"繁栄期に公的行政に貢献したローマ皇帝。"){record_delimiter}
("entity"{tuple_delimiter}"トラヤヌス"{tuple_delimiter}"person"{tuple_delimiter}"美徳と行政能力で知られるローマ皇帝。"){record_delimiter}
("entity"{tuple_delimiter}"ハドリアヌス"{tuple_delimiter}"person"{tuple_delimiter}"帝国の平和な期間を統治したローマ皇帝。"){record_delimiter}
("entity"{tuple_delimiter}"アントニヌス"{tuple_delimiter}"person"{tuple_delimiter}"繁栄と良き統治の時代に統治した2人のローマ皇帝。"){record_delimiter}
("entity"{tuple_delimiter}"ローマ法"{tuple_delimiter}"concept"{tuple_delimiter}"ローマ帝国の諸州を統一した法と慣習のシステム。"){record_delimiter}
("relationship"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"ローマ法"{tuple_delimiter}"帝国は法と慣習の影響により統一され維持された。"){record_delimiter}
("relationship"{tuple_delimiter}"ローマ元老院"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"元老院は主権を持っているように見え、執行権を皇帝に委ねた。"){record_delimiter}
("relationship"{tuple_delimiter}"ネルウァ"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"ネルウァは帝国の成功した行政に貢献した皇帝の一人であった。"){record_delimiter}
("relationship"{tuple_delimiter}"トラヤヌス"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"トラヤヌスは帝国の繁栄期に統治した皇帝の一人であった。"){record_delimiter}
("relationship"{tuple_delimiter}"ハドリアヌス"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"ハドリアヌスは帝国の行政を効果的に管理した皇帝の一人であった。"){record_delimiter}
("relationship"{tuple_delimiter}"アントニヌス"{tuple_delimiter}"ローマ帝国"{tuple_delimiter}"アントニヌスは統治を通じて帝国の繁栄維持に貢献した皇帝たちであった。"){record_delimiter}
("content_keywords"{tuple_delimiter}"ローマ統治, 帝国の繁栄, 法と秩序, 文明社会"){completion_delimiter}

-例2-
テキスト:
#############
全体として、OsDT11配列の解析により、このタンパク質がCRPファミリーに属することが実証された。OsDT11は分泌タンパク質であると予測されるため、OsDT11の細胞内局在は、OsDT11 ORFをp35S::RFPベクターのRFPに融合させ、アグロバクテリウム・ツメファシエンス媒介一過性アッセイを実行してNB表皮細胞でのin vivoタンパク質標的化により決定された。48時間のインキュベーション後、RFPシグナルは主にOsDT11-RFP形質転換細胞の細胞壁で検出されたが、対照細胞（RFP構築物で形質転換）では遍在するRFPシグナルが表示され、OsDT11が分泌シグナルペプチドであることが実証された。さらに、浸潤した葉切片を原形質分離させた場合、OsDT11-RFP融合タンパク質は細胞壁に位置していた。
#############
出力:
("entity"{tuple_delimiter}"OsDT11"{tuple_delimiter}"gene"{tuple_delimiter}"CRPファミリーに属するタンパク質配列で、細胞壁に局在する分泌シグナルペプチドであることが実証された。"){record_delimiter}
("entity"{tuple_delimiter}"CRPファミリー"{tuple_delimiter}"science"{tuple_delimiter}"OsDT11が属するタンパク質ファミリーで、特定の構造的および機能的特性を特徴とする。"){record_delimiter}
("entity"{tuple_delimiter}"RFP"{tuple_delimiter}"technology"{tuple_delimiter}"赤色蛍光タンパク質で、細胞内でのタンパク質局在を追跡するための融合マーカーとして使用される。"){record_delimiter}
("entity"{tuple_delimiter}"p35S::RFPベクター"{tuple_delimiter}"technology"{tuple_delimiter}"タンパク質発現と可視化研究に使用される遺伝子構築物で、35SプロモーターとRFPマーカーを含む。"){record_delimiter}
("entity"{tuple_delimiter}"NB表皮細胞"{tuple_delimiter}"nature"{tuple_delimiter}"タンパク質局在研究の実験系として使用される植物表皮細胞。"){record_delimiter}
("entity"{tuple_delimiter}"アグロバクテリウム・ツメファシエンス"{tuple_delimiter}"nature"{tuple_delimiter}"実験室実験で遺伝物質を植物細胞に転移させるために使用される細菌種。"){record_delimiter}
("relationship"{tuple_delimiter}"OsDT11"{tuple_delimiter}"CRPファミリー"{tuple_delimiter}"OsDT11は配列解析によりCRPファミリーのメンバーとして特定された。"){record_delimiter}
("relationship"{tuple_delimiter}"OsDT11"{tuple_delimiter}"RFP"{tuple_delimiter}"OsDT11はその細胞局在を研究するためにRFPに融合された。"){record_delimiter}
("relationship"{tuple_delimiter}"アグロバクテリウム・ツメファシエンス"{tuple_delimiter}"NB表皮細胞"{tuple_delimiter}"アグロバクテリウム・ツメファシエンスは一過性アッセイを通じてNB表皮細胞に遺伝物質を転移させるために使用された。"){record_delimiter}
("relationship"{tuple_delimiter}"OsDT11"{tuple_delimiter}"NB表皮細胞"{tuple_delimiter}"OsDT11の細胞内局在がNB表皮細胞で研究され、細胞壁標的化が示された。"){record_delimiter}
("content_keywords"{tuple_delimiter}"タンパク質局在, 遺伝子発現, 細胞生物学, 分子技術"){completion_delimiter}

################
-実データ-
################
Entity_types: {entity_types}
Text: {input_text}
################
出力:
```
