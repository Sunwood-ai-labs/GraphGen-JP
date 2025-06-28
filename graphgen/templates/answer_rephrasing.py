TEMPLATE_CONTEXT_EN: str = """---Role---

You are an NLP expert responsible for generating a logically structured and coherent rephrased version of the TEXT based on ENTITIES and RELATIONSHIPS provided below. You may refer to the original text to assist in generating the rephrased version, but ensure that the final output text meets the requirements.
Use {language} as output language.

---Goal---
To generate a version of the text that is rephrased and conveys the same meaning as the original entity and relationship descriptions, while:
1. Following a clear logical flow and structure
2. Establishing proper cause-and-effect relationships
3. Ensuring temporal and sequential consistency
4. Creating smooth transitions between ideas using conjunctions and appropriate linking words like "firstly," "however," "therefore," etc.

---Instructions---
1. Analyze the provided ENTITIES and RELATIONSHIPS carefully to identify:
   - Key concepts and their hierarchies
   - Temporal sequences and chronological order
   - Cause-and-effect relationships
   - Dependencies between different elements

2. Organize the information in a logical sequence by:
   - Starting with foundational concepts
   - Building up to more complex relationships
   - Grouping related ideas together
   - Creating clear transitions between sections

3. Rephrase the text while maintaining:
   - Logical flow and progression
   - Clear connections between ideas
   - Proper context and background
   - Coherent narrative structure

4. Review and refine the text to ensure:
   - Logical consistency throughout
   - Clear cause-and-effect relationships

################
-ORIGINAL TEXT-
################
{original_text}

################
-ENTITIES-
################
{entities}

################
-RELATIONSHIPS-
################
{relationships}

"""

TEMPLATE_EN: str = """---Role---

You are an NLP expert responsible for generating a logically structured and coherent rephrased version of the TEXT based on ENTITIES and RELATIONSHIPS provided below.
Use {language} as output language.

---Goal---
To generate a version of the text that is rephrased and conveys the same meaning as the original entity and relationship descriptions, while:
1. Following a clear logical flow and structure
2. Establishing proper cause-and-effect relationships
3. Ensuring temporal and sequential consistency
4. Creating smooth transitions between ideas using conjunctions and appropriate linking words like "firstly," "however," "therefore," etc.

---Instructions---
1. Analyze the provided ENTITIES and RELATIONSHIPS carefully to identify:
   - Key concepts and their hierarchies
   - Temporal sequences and chronological order
   - Cause-and-effect relationships
   - Dependencies between different elements

2. Organize the information in a logical sequence by:
   - Starting with foundational concepts
   - Building up to more complex relationships
   - Grouping related ideas together
   - Creating clear transitions between sections

3. Rephrase the text while maintaining:
   - Logical flow and progression
   - Clear connections between ideas
   - Proper context and background
   - Coherent narrative structure

4. Review and refine the text to ensure:
   - Logical consistency throughout
   - Clear cause-and-effect relationships

################
-ENTITIES-
################
{entities}

################
-RELATIONSHIPS-
################
{relationships}

"""

TEMPLATE_ZH: str = """---角色---

你是一位NLP专家，负责根据下面提供的实体和关系生成逻辑结构清晰且连贯的文本重述版本。
使用{language}作为输出语言。

---目标---

生成文本的重述版本，使其传达与原始实体和关系描述相同的含义，同时：
1. 遵循清晰的逻辑流和结构
2. 建立适当的因果关系
3. 确保时间和顺序的一致性
4. 使用连词和适当的连接词(如"首先"、"然而"、"因此"等)创造流畅的过渡

---说明---
1. 仔细分析提供的实体和关系，以识别：
    - 关键概念及其层级关系
    - 时间序列和时间顺序
    - 因果关系
    - 不同元素之间的依赖关系
2. 通过以下方式将信息组织成逻辑顺序：
    - 从基础概念开始
    - 逐步建立更复杂的关系
    - 将相关的想法分组在一起
    - 在各部分之间创建清晰的过渡
3. 重述文本时保持：
    - 逻辑流畅
    - 概念之间的清晰联系
    - 适当的上下文和背景
    - 连贯的叙述结构
4. 检查和完善文本以确保：
    - 整体逻辑一致性
    - 清晰的因果关系

################
-实体-
################
{entities}

################
-关系-
################
{relationships}

"""

TEMPLATE_CONTEXT_JA: str = """---役割---

あなたはNLPの専門家として、下記のENTITIES（エンティティ）とRELATIONSHIPS（関係）に基づき、論理的で一貫性のあるリフレーズ文を生成します。必要に応じて元のテキストも参照して構いませんが、最終的な出力が要件を満たすようにしてください。
出力言語は{language}とします。

---目的---
エンティティと関係の記述が持つ意味を損なわず、以下の条件を満たすリフレーズ文を生成してください：
1. 論理的な流れと構造を持つこと
2. 適切な因果関係を明示すること
3. 時系列や順序の一貫性を保つこと
4. 「まず」「しかし」「したがって」などの接続詞を用いて、アイデア間のスムーズなつながりを作ること

---手順---
1. 提供されたENTITIESとRELATIONSHIPSをよく分析し、以下を特定する：
   - 主要な概念とその階層
   - 時系列や順序
   - 因果関係
   - 各要素間の依存関係

2. 情報を論理的な順序で整理する：
   - 基本的な概念から始める
   - より複雑な関係へと展開する
   - 関連するアイデアをまとめる
   - 各セクション間に明確なつながりを作る

3. リフレーズ文を作成する際は、以下を維持する：
   - 論理的な流れと展開
   - アイデア間の明確なつながり
   - 適切な文脈と背景
   - 一貫したナラティブ構造

4. 最後に、以下を確認・修正する：
   - 全体を通じた論理的一貫性
   - 明確な因果関係

################
-元のテキスト-
################
{original_text}

################
-エンティティ-
################
{entities}

################
-関係-
################
{relationships}

"""

TEMPLATE_JA: str = """---役割---

あなたはNLPの専門家として、下記のENTITIES（エンティティ）とRELATIONSHIPS（関係）に基づき、論理的で一貫性のあるリフレーズ文を生成します。
出力言語は{language}とします。

---目的---
エンティティと関係の記述が持つ意味を損なわず、以下の条件を満たすリフレーズ文を生成してください：
1. 論理的な流れと構造を持つこと
2. 適切な因果関係を明示すること
3. 時系列や順序の一貫性を保つこと
4. 「まず」「しかし」「したがって」などの接続詞を用いて、アイデア間のスムーズなつながりを作ること

---手順---
1. 提供されたENTITIESとRELATIONSHIPSをよく分析し、以下を特定する：
   - 主要な概念とその階層
   - 時系列や順序
   - 因果関係
   - 各要素間の依存関係

2. 情報を論理的な順序で整理する：
   - 基本的な概念から始める
   - より複雑な関係へと展開する
   - 関連するアイデアをまとめる
   - 各セクション間に明確なつながりを作る

3. リフレーズ文を作成する際は、以下を維持する：
   - 論理的な流れと展開
   - アイデア間の明確なつながり
   - 適切な文脈と背景
   - 一貫したナラティブ構造

4. 最後に、以下を確認・修正する：
   - 全体を通じた論理的一貫性
   - 明確な因果関係

################
-エンティティ-
################
{entities}

################
-関係-
################
{relationships}

"""

REQUIREMENT_JA = """
################
下記に一貫性のあるリフレーズ文のみを直接出力してください。余計な内容は一切出力しないでください。

リフレーズ文:
"""

REQUIREMENT_EN = """
################
Please directly output the coherent rephrased text below, without any additional content.

Rephrased Text:
"""

REQUIREMENT_ZH = """
################
请在下方直接输出连贯的重述文本，不要输出任何额外的内容。

重述文本:
"""

ANSWER_REPHRASING_PROMPT= {
    "English": {
        "TEMPLATE": TEMPLATE_EN + REQUIREMENT_EN,
        "CONTEXT_TEMPLATE": TEMPLATE_CONTEXT_EN + REQUIREMENT_EN
    },
    "Chinese": {
        "TEMPLATE": TEMPLATE_ZH + REQUIREMENT_ZH,
        "CONTEXT_TEMPLATE": TEMPLATE_CONTEXT_ZH + REQUIREMENT_ZH if 'TEMPLATE_CONTEXT_ZH' in globals() else TEMPLATE_ZH + REQUIREMENT_ZH
    },
    "Japanese": {
        "TEMPLATE": TEMPLATE_JA + REQUIREMENT_JA,
        "CONTEXT_TEMPLATE": TEMPLATE_CONTEXT_JA + REQUIREMENT_JA
    }
}
