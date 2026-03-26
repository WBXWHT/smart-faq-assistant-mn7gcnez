import json
import time
from datetime import datetime
from typing import List, Dict, Optional

class FAQDatabase:
    """模拟FAQ知识库存储和检索"""
    
    def __init__(self):
        # 模拟FAQ知识库数据
        self.faq_data = [
            {"id": 1, "question": "如何重置密码？", "answer": "请访问登录页面点击'忘记密码'链接，按照提示操作。"},
            {"id": 2, "question": "支持哪些支付方式？", "answer": "我们支持支付宝、微信支付和银行卡支付。"},
            {"id": 3, "question": "退货政策是什么？", "answer": "商品签收后7天内可无理由退货，需保持商品完好。"},
            {"id": 4, "question": "运费如何计算？", "answer": "订单满99元包邮，不满99元收取10元运费。"},
            {"id": 5, "question": "客服工作时间？", "answer": "人工客服工作时间为每天9:00-21:00。"}
        ]
        
    def search_similar_questions(self, user_query: str, top_k: int = 3) -> List[Dict]:
        """简单关键词匹配搜索相似问题（模拟向量检索）"""
        query_lower = user_query.lower()
        results = []
        
        for faq in self.faq_data:
            # 简单关键词匹配（实际项目中会使用向量检索）
            score = 0
            for keyword in query_lower.split():
                if keyword in faq["question"].lower():
                    score += 1
                if keyword in faq["answer"].lower():
                    score += 0.5
            
            if score > 0:
                results.append({
                    "question": faq["question"],
                    "answer": faq["answer"],
                    "score": score
                })
        
        # 按匹配度排序并返回top_k个结果
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

class LLMClient:
    """模拟大语言模型客户端"""
    
    def __init__(self):
        self.conversation_history = []
        
    def generate_response(self, user_query: str, context: List[Dict]) -> str:
        """基于检索到的上下文生成回答（模拟大模型调用）"""
        
        # 构建提示词
        context_text = "\n".join([
            f"Q: {item['question']}\nA: {item['answer']}" 
            for item in context
        ])
        
        prompt = f"""基于以下FAQ知识库内容，回答用户问题：

{context_text}

用户问题：{user_query}

请提供专业、友好的回答："""
        
        # 模拟大模型处理延迟
        time.sleep(0.5)
        
        # 模拟大模型生成回答的逻辑
        if context:
            # 如果有相关上下文，基于上下文生成回答
            best_match = context[0]
            answer = f"根据我们的知识库：{best_match['answer']}"
            
            # 如果还有其他相关信息，可以补充
            if len(context) > 1:
                answer += f"\n\n其他相关信息："
                for i, item in enumerate(context[1:], 1):
                    answer += f"\n{i}. {item['question']}: {item['answer']}"
        else:
            # 如果没有找到相关信息
            answer = "抱歉，我没有找到相关的信息。您可以尝试重新表述问题，或联系人工客服获取帮助。"
        
        # 记录对话历史
        self.conversation_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_query": user_query,
            "response": answer,
            "context_used": [item["question"] for item in context]
        })
        
        return answer
    
    def get_conversation_stats(self) -> Dict:
        """获取对话统计信息"""
        return {
            "total_conversations": len(self.conversation_history),
            "last_conversation": self.conversation_history[-1] if self.conversation_history else None
        }

class SmartFAQAssistant:
    """智能FAQ助手主类"""
    
    def __init__(self):
        self.faq_db = FAQDatabase()
        self.llm_client = LLMClient()
        self.user_feedback = []
        
    def process_query(self, user_query: str) -> str:
        """处理用户查询的主要流程"""
        print(f"\n用户提问：{user_query}")
        
        # 1. 检索相关FAQ
        print("正在检索知识库...")
        relevant_faqs = self.faq_db.search_similar_questions(user_query)
        
        if relevant_faqs:
            print(f"找到 {len(relevant_faqs)} 条相关记录")
            for i, faq in enumerate(relevant_faqs, 1):
                print(f"  {i}. {faq['question']} (匹配度：{faq['score']})")
        
        # 2. 调用大模型生成回答
        print("正在生成回答...")
        response = self.llm_client.generate_response(user_query, relevant_faqs)
        
        return response
    
    def collect_feedback(self, query: str, response: str, is_helpful: bool):
        """收集用户反馈用于优化"""
        feedback = {
            "query": query,
            "response": response,
            "is_helpful": is_helpful,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.user_feedback.append(feedback)
        
        print(f"感谢您的反馈！当前收集到 {len(self.user_feedback)} 条反馈数据。")

def main():
    """主函数 - 智能FAQ助手演示"""
    print("=" * 50)
    print("智能FAQ助手 v1.0")
    print("=" * 50)
    
    # 初始化助手
    assistant = SmartFAQAssistant()
    
    # 演示对话
    demo_queries = [
        "忘记密码怎么办？",
        "你们接受哪些付款方式？",
        "我想退货",
        "什么时候可以联系客服？",
        "产品保修期多久？"  # 这个问题不在FAQ中
    ]
    
    for query in demo_queries:
        # 处理查询
        response = assistant.process_query(query)
        
        print(f"\n助手回答：{response}")
        print("-" * 50)
        
        # 模拟用户反馈（前两个有用，后三个无用）
        is_helpful = query in ["忘记密码怎么办？", "你们接受哪些付款方式？"]
        assistant.collect_feedback(query, response, is_helpful)
        
        # 短暂暂停
        time.sleep(1)
    
    # 显示统计信息
    print("\n" + "=" * 50)
    print("对话统计：")
    stats = assistant.llm_client.get_conversation_stats()
    print(f"总对话次数：{stats['total_conversations']}")
    
    print(f"\n收集的反馈数量：{len(assistant.user_feedback)}")
    helpful_count = sum(1 for fb in assistant.user_feedback if fb["is_helpful"])
    print(f"有帮助的反馈：{helpful_count}/{len(assistant.user_feedback)}")
    
    print("\n演示结束！")

if __name__ == "__main__":
    main()