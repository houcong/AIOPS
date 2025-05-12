# Amazon Claude 3.7 RAG 示例

这个项目演示了如何使用Amazon Bedrock的Claude 3.7模型和向量数据库实现检索增强生成(RAG)系统。

## 功能特点

- 使用Amazon Claude 3.7 Sonnet模型进行生成
- 使用Amazon Titan Embedding模型进行文本嵌入
- 使用FAISS作为向量数据库
- 支持加载、分割和索引本地文档
- 支持保存和加载向量数据库
- 提供简单的交互式查询界面

## 前提条件

1. AWS账户，并已启用Amazon Bedrock服务
2. 已配置AWS凭证（通过AWS CLI或环境变量）
3. Python 3.8+

## 安装

1. 克隆此仓库或下载代码
2. 安装依赖项：

```bash
pip install -r requirements_rag.txt
```

## 使用方法

### 1. 准备知识库

将您的文本文档(.txt文件)放入`knowledge`目录。如果目录不存在或为空，程序会自动创建示例文件。

### 2. 运行RAG系统

```bash
python claude_rag_example.py
```

程序会：
1. 加载知识库文档
2. 将文档分割成小块
3. 创建向量数据库
4. 启动交互式查询界面

### 3. 查询

在提示符下输入您的问题，系统会：
1. 检索与问题最相关的文档片段
2. 将这些片段与问题一起发送给Claude 3.7
3. 显示生成的回答

输入`exit`退出程序。

## 代码结构

- `claude_rag_example.py`: 主程序文件
- `knowledge/`: 存放知识库文档的目录
- `faiss_index/`: 保存向量数据库的目录(自动创建)

## 自定义配置

您可以在代码顶部修改以下常量：

```python
CLAUDE_MODEL_ID = "anthropic.claude-3-7-sonnet-20240229-v1:0"  # Claude模型ID
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v1"  # Embedding模型ID
REGION_NAME = "us-east-1"  # AWS区域
KNOWLEDGE_DIR = "knowledge"  # 知识库目录
CHUNK_SIZE = 1000  # 文档分块大小
CHUNK_OVERLAP = 100  # 文档分块重叠大小
TOP_K = 3  # 检索结果数量
```

## 注意事项

- 使用Amazon Bedrock服务会产生费用，请查阅AWS定价页面
- 确保您的AWS账户有权限访问指定的模型
- 对于大型知识库，可能需要更多的内存和处理时间

## 扩展建议

- 添加网页爬取功能，自动获取最新信息
- 实现PDF、Word等格式的文档加载
- 添加图形用户界面
- 集成到Web应用或聊天机器人中
- 添加记忆功能，保存对话历史
