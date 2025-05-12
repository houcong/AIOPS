#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amazon Claude RAG (检索增强生成) 示例
使用Amazon Bedrock Claude模型和向量数据库实现RAG
"""

import os
import boto3
import json
import numpy as np
from typing import List, Dict, Any
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 配置常量
CLAUDE_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"  # Claude 3 Sonnet
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v1"  # Amazon Titan Embedding模型
REGION_NAME = "us-east-1"  # AWS区域
KNOWLEDGE_DIR = "knowledge"  # 知识库文件夹
CHUNK_SIZE = 1000  # 文档分块大小
CHUNK_OVERLAP = 100  # 文档分块重叠大小
TOP_K = 3  # 检索结果数量

class ClaudeRAG:
    """使用Amazon Claude 3.7和向量数据库实现的RAG系统"""
    
    def __init__(self):
        """初始化RAG系统"""
        # 初始化Bedrock客户端
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=REGION_NAME
        )
        
        # 初始化Embedding模型
        self.embeddings = BedrockEmbeddings(
            client=self.bedrock_runtime,
            model_id=EMBEDDING_MODEL_ID
        )
        
        # 初始化向量数据库
        self.vector_db = None
        
    def load_documents(self, directory: str = KNOWLEDGE_DIR) -> None:
        """
        加载文档并创建向量数据库
        
        参数:
            directory: 包含知识文档的目录
        """
        # 确保知识库目录存在
        os.makedirs(directory, exist_ok=True)
        
        # 加载文档
        try:
            loader = DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader)
            documents = loader.load()
            print(f"已加载 {len(documents)} 个文档")
            
            if not documents:
                print(f"警告: 目录 '{directory}' 中没有找到文本文件")
                return
            
            # 分割文档
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP
            )
            chunks = text_splitter.split_documents(documents)
            print(f"文档已分割为 {len(chunks)} 个块")
            
            # 创建向量数据库
            self.vector_db = FAISS.from_documents(chunks, self.embeddings)
            print("向量数据库创建完成")
            
        except Exception as e:
            print(f"加载文档时出错: {str(e)}")
    
    def save_vector_db(self, path: str = "faiss_index") -> None:
        """
        保存向量数据库到磁盘
        
        参数:
            path: 保存路径
        """
        if self.vector_db:
            self.vector_db.save_local(path)
            print(f"向量数据库已保存到 {path}")
        else:
            print("没有向量数据库可保存")
    
    def load_vector_db(self, path: str = "faiss_index") -> None:
        """
        从磁盘加载向量数据库
        
        参数:
            path: 加载路径
        """
        if os.path.exists(path):
            self.vector_db = FAISS.load_local(path, self.embeddings)
            print(f"已从 {path} 加载向量数据库")
        else:
            print(f"路径 {path} 不存在，无法加载向量数据库")
    
    def retrieve(self, query: str, top_k: int = TOP_K) -> List[str]:
        """
        检索与查询相关的文档
        
        参数:
            query: 用户查询
            top_k: 返回的相关文档数量
            
        返回:
            相关文档内容列表
        """
        if not self.vector_db:
            print("向量数据库未初始化，请先加载文档")
            return []
        
        # 执行相似性搜索
        results = self.vector_db.similarity_search(query, k=top_k)
        
        # 提取文档内容
        contexts = [doc.page_content for doc in results]
        return contexts
    
    def generate_response(self, query: str, contexts: List[str]) -> str:
        """
        使用Claude 3生成回答
        
        参数:
            query: 用户查询
            contexts: 相关上下文列表
            
        返回:
            生成的回答
        """
        # 构建提示
        system_prompt = """你是一个专业的AI助手，使用提供的上下文信息回答用户问题。
如果上下文中没有足够的信息来回答问题，请诚实地说你不知道，不要编造信息。
回答时请引用上下文中的具体信息，并保持简洁、准确。"""
        
        # 将上下文合并为一个字符串
        context_text = "\n\n".join([f"文档 {i+1}:\n{context}" for i, context in enumerate(contexts)])
        
        # 构建消息 - 修改为Bedrock Claude支持的格式
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=CLAUDE_MODEL_ID,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "system": system_prompt,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"基于以下上下文回答我的问题:\n\n{context_text}\n\n问题: {query}"
                        }
                    ]
                })
            )
            
            # 解析响应
            response_body = json.loads(response.get('body').read())
            answer = response_body['content'][0]['text']
            return answer
            
        except Exception as e:
            print(f"调用Claude模型时出错: {str(e)}")
            return f"生成回答时出错: {str(e)}"
    
    def query(self, query: str) -> str:
        """
        执行完整的RAG流程：检索 + 生成
        
        参数:
            query: 用户查询
            
        返回:
            生成的回答
        """
        # 检索相关文档
        contexts = self.retrieve(query)
        
        if not contexts:
            return "无法找到相关信息，请确保已加载知识库。"
        
        # 生成回答
        return self.generate_response(query, contexts)


def main():
    """主函数"""
    # 创建RAG系统
    rag = ClaudeRAG()
    
    # 检查知识库目录是否存在
    if not os.path.exists(KNOWLEDGE_DIR) or not os.listdir(KNOWLEDGE_DIR):
        print(f"知识库目录 '{KNOWLEDGE_DIR}' 不存在或为空，创建示例文件...")
        os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
        
        # 创建示例知识文件
        with open(f"{KNOWLEDGE_DIR}/aws_services.txt", "w", encoding="utf-8") as f:
            f.write("""Amazon Web Services (AWS) 提供了多种云计算服务。
Amazon S3 (Simple Storage Service) 是一种对象存储服务，提供行业领先的可扩展性、数据可用性、安全性和性能。
Amazon EC2 (Elastic Compute Cloud) 是一种提供可调整计算容量的web服务。
Amazon RDS (Relational Database Service) 使在云中设置、操作和扩展关系数据库变得简单。
Amazon Lambda 是一项无服务器计算服务，可运行代码而无需预置或管理服务器。
Amazon Bedrock 是一项全托管服务，提供来自领先AI公司的高性能基础模型。""")
            
        with open(f"{KNOWLEDGE_DIR}/claude_models.txt", "w", encoding="utf-8") as f:
            f.write("""Claude是由Anthropic开发的一系列大型语言模型。
Claude 3系列包括三个模型：Haiku、Sonnet和Opus，它们在能力和价格之间提供不同的平衡。
Claude 3.7 Sonnet是Claude 3系列的最新版本，提供了更强的推理能力和更好的指令遵循能力。
Claude模型可以通过Amazon Bedrock服务访问，这使开发者能够轻松集成这些模型到他们的应用中。
Claude 3.7的上下文窗口大小为200K tokens，支持多模态输入，包括文本和图像。""")
    
    # 加载文档并创建向量数据库
    rag.load_documents()
    
    # 保存向量数据库（可选）
    rag.save_vector_db()
    
    # 交互式查询
    print("\n=== Claude RAG 系统已准备就绪 ===")
    print("输入问题进行查询，输入'exit'退出")
    
    while True:
        query = input("\n请输入您的问题: ")
        if query.lower() in ['exit', 'quit', '退出']:
            break
            
        # 执行RAG查询
        answer = rag.query(query)
        print("\n回答:")
        print("-" * 80)
        print(answer)
        print("-" * 80)


if __name__ == "__main__":
    main()
