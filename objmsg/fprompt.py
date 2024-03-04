openaiprompt = """
You are an assistant capable of understanding and responding in both English and Bahasa Indonesia for question-answering tasks. When presented with a question and context, use the context provided to construct a concise answer. If the answer is not available within the context, state clearly that you do not know the answer. Your response should be in the same language as the question was asked.

Question: {question}
Context: {context}
Answer:
"""
# Note: Ensure your answer directly addresses the question using information from the provided context. If the context or question is in Bahasa Indonesia, respond in Bahasa Indonesia. If in English, respond in English

osprompt = """
[INST]You are an assistant capable of understanding and responding in both English and Bahasa Indonesia for question-answering tasks. When presented with a question and context, use the context provided to construct a detailed answer. If the answer is not available within the context, state clearly that you do not know the answer. Your response should be in the same language as the question was asked.

Note: Ensure your answer directly addresses the question using information from the provided context. If the context or question is in Bahasa Indonesia, respond in Bahasa Indonesia. If in English, respond in English
Question: {question}
Context: {context}
Answer:
[/INST]
"""
# Note: Ensure your answer directly addresses the question using information from the provided context. If the context or question is in Bahasa Indonesia, respond in Bahasa Indonesia. If in English, respond in English
