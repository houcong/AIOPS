#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微调后的Amazon Bedrock Claude模型
"""

import boto3
import json
import argparse

def test_fine_tuned_model(model_id, test_log):
    """
    使用微调后的模型分析日志
    
    参数:
        model_id: 微调后的模型ID
        test_log: 测试日志内容
    
    返回:
        response: 模型响应
    """
    # 初始化Bedrock运行时客户端
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # 准备请求
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system", 
                "content": "你是一个专业的日志分析专家，能够准确判断日志的严重程度并分配优先级。P0表示最高优先级，需要立即处理的严重问题；P1表示高优先级，需要尽快处理；P2表示中等优先级；P3表示低优先级。"
            },
            {
                "role": "user",
                "content": test_log
            }
        ]
    }
    
    # 调用模型
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(request_body)
    )
    
    # 解析响应
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

def main():
    parser = argparse.ArgumentParser(description='测试微调后的Amazon Bedrock Claude模型')
    parser.add_argument('--model-id', required=True, help='微调后的模型ID')
    parser.add_argument('--log', required=True, help='要分析的日志内容')
    
    args = parser.parse_args()
    
    print(f"使用模型 {args.model_id} 分析日志...")
    response = test_fine_tuned_model(args.model_id, args.log)
    
    print("\n模型分析结果:")
    print("-" * 50)
    print(response)
    print("-" * 50)

if __name__ == "__main__":
    main()
