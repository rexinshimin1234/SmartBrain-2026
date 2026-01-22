from sentence_transformers import SentenceTransformer, util
print("正在加载本地模型 (local_model)...")
model = SentenceTransformer('./local_model')
knowledge_base = [
    "亚索（Yasuo）的克制方法：选出鳄鱼或者安妮这种带有硬控的英雄，在他滑步时直接控制。",
    "盲僧（Lee Sin）的回旋踢技巧：Q中敌人后，二段Q飞行途中插眼W到敌人身后，然后R踢回。",
    "提莫（Teemo）必须死：打提莫建议带扫描透镜，并且出门装选择多兰盾抗压。",
    "大龙（Baron）刷新时间：纳什男爵会在游戏时间25分钟时刷新。",
    "盖伦（Garen）连招：先Q加速沉默敌人，然后E转圈圈，最后R大宝剑收尾。",
    "辅助做眼技巧：在下路三角草丛插真眼可以有效防止打野绕后。"
]
print("正在为知识库建立索引 (向量化)...")
doc_embeddings =model.encode(knowledge_base)
user_query = "怎么克制亚索？"
print(f"\n用户提问: {user_query}")
query_embedding =model.encode(user_query)
hits = util.semantic_search(query_embedding, doc_embeddings, top_k=1)
best_match_idx = hits[0][0]['corpus_id']
best_score = hits[0][0]['score']
print("\n--- 🔍 检索结果 ---")
print(f"最匹配的文档: {knowledge_base[best_match_idx]}")
print(f"匹配度得分: {best_score:.4f}")

if best_score > 0.5:
    print(">> 系统判定：找到了可靠的答案！")
else:
    print(">> 系统判定：知识库里好像没有相关内容。")