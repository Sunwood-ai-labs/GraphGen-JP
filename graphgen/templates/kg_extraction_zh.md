你是一个NLP专家, 擅长分析文本提取命名实体和关系.

-目标-
给定一个实体类型列表和可能与列表相关的文本, 从文本中识别所有这些类型的实体, 以及这些实体之间所有的关系.
使用{language}作为输出语言.

-步骤-
1. 识别所有实体. 对于每个识别的实体, 提取以下信息:
   - entity_name: 实体的名称, 首字母大写
   - entity_type: 以下类型之一: [{entity_types}]
   - entity_summary: 实体的属性与活动的全面总结
   将每个实体格式化为("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_summary>)
   
2. 从步骤1中识别的实体中, 识别所有(源实体, 目标实体)对, 这些实体彼此之间*明显相关*.
   对于每对相关的实体, 提取以下信息:
   - source_entity: 步骤1中识别的源实体名称
   - target_entity: 步骤1中识别的目标实体名称
   - relationship_summary: 解释为什么你认为这两个实体相关
   将每对关系格式化为("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_summary>)

3. 识别总结文本主要概念, 主题或话题的高层次关键词.
   格式为("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 用{language}输出所有识别的实体和关系, 使用**{record_delimiter}**作为分隔符.

5. 结束时输出{completion_delimiter}

################
-示例-
################
-Example 1-
Text:
################
在公元二世纪, 罗马帝国囊括了地球上最美丽的部分和最文明的人类. 这个庞大帝国的边疆由古老的声望和训练有素的勇气守卫. 法律和风俗的温和但强大的影响逐渐巩固了各省的统一. 和平的居民享受并滥用了财富和奢侈的好处. 自由宪法的形象被体面地保留: 罗马元老院似乎拥有最高权力, 并将所有行政权力下放给皇帝. 在八十多年的幸福时期, 国家管理由涅尔瓦, 图拉真, 哈德良和两位安东尼努斯的美德和能力进行.
################
Output:
("entity"{tuple_delimiter}"罗马帝国"{tuple_delimiter}"organization"{tuple_delimiter}"公元二世纪最强盛的帝国, 囊括了已知世界最发达的地区."){record_delimiter}
("entity"{tuple_delimiter}"罗马元老院"{tuple_delimiter}"organization"{tuple_delimiter}"罗马帝国名义上的立法机构."){record_delimiter}
("entity"{tuple_delimiter}"涅尔瓦"{tuple_delimiter}"person"{tuple_delimiter}"繁荣时期的皇帝之一."){record_delimiter}
("relationship"{tuple_delimiter}"罗马帝国"{tuple_delimiter}"罗马元老院"{tuple_delimiter}"元老院名义上拥有权威, 实际权力归皇帝所有."){record_delimiter}
("relationship"{tuple_delimiter}"涅尔瓦"{tuple_delimiter}"罗马帝国"{tuple_delimiter}"涅尔瓦是繁荣时期的皇帝."){record_delimiter}
("content_keywords"{tuple_delimiter}"罗马帝国, 繁荣, 皇帝, 元老院"){completion_delimiter}

################
-真实数据-
################
Entity_types: {entity_types}
Text: {input_text}
################
Output:
