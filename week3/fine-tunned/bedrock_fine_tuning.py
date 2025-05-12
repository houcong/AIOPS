#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amazon Bedrock Fine-tuning示例脚本 - 简化版
用于创建和管理Nova模型的微调任务
"""

import boto3
import json
import time
import argparse
import os
from datetime import datetime

def create_fine_tuning_job(training_file, validation_file=None, model_id="amazon.nova-lite-v1:0:300k", 
                           job_name=None, role_arn=None, s3_bucket="hcong-bedrock-finetuning", region="us-east-1"):
    """
    创建一个新的微调任务
    
    参数:
        training_file: 训练数据文件路径
        validation_file: 验证数据文件路径（可选）
        model_id: 基础模型ID
        job_name: 任务名称（可选）
        role_arn: IAM角色ARN，用于授予Bedrock访问S3的权限
        s3_bucket: S3存储桶名称，用于存储训练数据和输出结果
        region: AWS区域
    
    返回:
        job_arn: 微调任务ARN
    """
    # 初始化Bedrock和S3客户端
    bedrock = boto3.client('bedrock', region_name=region)
    s3 = boto3.client('s3', region_name=region)
    
    # 生成任务名称
    if not job_name:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        job_name = f"nova-fine-tuning-{timestamp}"
    
    # 自定义模型名称
    custom_model_name = f"{job_name}-model"
    
    # 上传训练数据到S3
    training_s3_key = f"fine-tuning/{job_name}/training.jsonl"
    s3.upload_file(training_file, s3_bucket, training_s3_key)
    training_s3_uri = f"s3://{s3_bucket}/{training_s3_key}"
    
    # 准备请求参数
    request_params = {
        'baseModelIdentifier': model_id,
        'customModelName': custom_model_name,
        'roleArn': role_arn,
        'jobName': job_name,
        'trainingDataConfig': {
            's3Uri': training_s3_uri
        },
        'outputDataConfig': {
            's3Uri': f"s3://{s3_bucket}/fine-tuning/{job_name}/output/"
        },
        'hyperParameters': {
            'epochCount': '3',
            'batchSize': '1',
            'learningRate': '0.0001'
        }
    }
    
    # 添加验证数据（如果提供）
    if validation_file:
        validation_s3_key = f"fine-tuning/{job_name}/validation.jsonl"
        s3.upload_file(validation_file, s3_bucket, validation_s3_key)
        validation_s3_uri = f"s3://{s3_bucket}/{validation_s3_key}"
        request_params['validationDataConfig'] = {
            'validators': [
                {
                    's3Uri': validation_s3_uri
                }
            ]
        }
    
    # 创建微调任务
    response = bedrock.create_model_customization_job(**request_params)
    
    return response['jobArn']

def create_iam_role(s3_bucket="hcong-bedrock-finetuning"):
    """
    创建用于Bedrock微调的IAM角色
    
    返回:
        role_arn: IAM角色ARN
    """
    iam = boto3.client('iam')
    
    # 角色名称
    role_name = "BedrockFineTuningRole"
    
    # 检查角色是否已存在
    try:
        response = iam.get_role(RoleName=role_name)
        print(f"使用现有IAM角色: {role_name}")
        return response['Role']['Arn']
    except iam.exceptions.NoSuchEntityException:
        pass
    
    # 创建信任策略
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "bedrock.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    # 创建角色
    response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description="Role for Amazon Bedrock fine-tuning"
    )
    
    role_arn = response['Role']['Arn']
    
    # 创建S3访问策略
    policy_name = "BedrockS3AccessPolicy"
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{s3_bucket}",
                    f"arn:aws:s3:::{s3_bucket}/*"
                ]
            }
        ]
    }
    
    # 创建策略
    try:
        policy_response = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        policy_arn = policy_response['Policy']['Arn']
    except iam.exceptions.EntityAlreadyExistsException:
        # 如果策略已存在，获取其ARN
        account_id = boto3.client('sts').get_caller_identity().get('Account')
        policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
    
    # 附加策略到角色
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )
    
    print(f"已创建IAM角色: {role_name}")
    print(f"已附加策略: {policy_name}")
    
    # 等待IAM角色传播
    print("等待IAM角色传播...")
    time.sleep(10)
    
    return role_arn

def main():
    parser = argparse.ArgumentParser(description='Amazon Bedrock Fine-tuning工具 - 简化版')
    parser.add_argument('--training', required=True, help='训练数据文件路径')
    parser.add_argument('--validation', help='验证数据文件路径')
    parser.add_argument('--model', default='amazon.nova-lite-v1:0:300k', help='基础模型ID')
    parser.add_argument('--name', help='任务名称')
    parser.add_argument('--region', default='us-east-1', help='AWS区域')
    parser.add_argument('--bucket', default='hcong-bedrock-finetuning', help='S3桶名称')
    
    args = parser.parse_args()
    
    # 创建IAM角色
    role_arn = create_iam_role(args.bucket)
    
    # 创建微调任务
    job_arn = create_fine_tuning_job(
        training_file=args.training,
        validation_file=args.validation,
        model_id=args.model,
        job_name=args.name,
        role_arn=role_arn,
        s3_bucket=args.bucket,
        region=args.region
    )
    
    print(f"已创建微调任务，ARN: {job_arn}")
    
    # 保存任务ARN到文件
    with open('fine_tuning_job.txt', 'w') as f:
        f.write(job_arn)

if __name__ == "__main__":
    main()
