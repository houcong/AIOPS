# Amazon Bedrock Claude Fine-tuning 步骤指南

本指南详细说明如何使用Amazon Bedrock对Claude模型进行微调，以创建专门的日志分析模型。

## 准备工作

1. 已创建S3桶：`hcong-s3-aiops-tf-state`
2. 已准备训练数据和验证数据
3. 已安装必要的Python依赖：`boto3`

## 步骤1：运行微调脚本

使用以下命令创建微调任务：

```bash
python bedrock_fine_tuning.py create --training logs_training_data.jsonl --validation logs_validation_data.jsonl --name "log-analysis-expert"
```

这个命令会：
- 自动创建一个IAM角色，授予Bedrock访问S3的权限
- 将训练数据和验证数据上传到S3桶
- 创建微调任务
- 将任务ARN保存到`fine_tuning_job.txt`文件中

如果您已有适当权限的IAM角色，可以使用`--role-arn`参数指定：

```bash
python bedrock_fine_tuning.py create --training logs_training_data.jsonl --validation logs_validation_data.jsonl --name "log-analysis-expert" --role-arn "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_ROLE_NAME"
```

## 步骤2：监控微调任务状态

微调任务创建后，您可以使用以下命令检查其状态：

```bash
# 使用保存的ARN
python bedrock_fine_tuning.py status --job-arn $(cat fine_tuning_job.txt)

# 或列出所有微调任务
python bedrock_fine_tuning.py list
```

微调过程可能需要几个小时甚至更长时间，请耐心等待。

## 步骤3：测试微调后的模型

一旦微调完成，您将获得一个新的模型ID。使用以下命令测试模型：

```bash
python test_fine_tuned_model.py --model-id <微调后的模型ID> --log "[2024-05-12 14:30:22] Database backup failed with error code 500."
```

您可以从微调任务的详细信息中获取模型ID，或者使用以下AWS CLI命令：

```bash
aws bedrock list-custom-models
```

## 数据存储位置

所有数据都存储在您的S3桶中，具体路径如下：

- 训练数据：`s3://hcong-s3-aiops-tf-state/fine-tuning/<job-name>/training.jsonl`
- 验证数据：`s3://hcong-s3-aiops-tf-state/fine-tuning/<job-name>/validation.jsonl`
- 输出数据：`s3://hcong-s3-aiops-tf-state/fine-tuning/<job-name>/output/`

## 故障排除

1. **权限错误**：确保IAM角色有足够的权限访问S3桶
2. **模型不可用**：确保您选择的基础模型在您的区域可用
3. **数据格式错误**：确保训练数据和验证数据格式正确
4. **任务失败**：检查任务详细信息以获取失败原因

## 清理资源

微调完成后，您可能需要清理以下资源：

1. S3桶中的训练数据和输出数据
2. 不再需要的IAM角色和策略
3. 不再需要的微调模型（注意：删除模型可能会产生额外费用）

## 注意事项

1. 微调会产生额外费用，请查阅Amazon Bedrock的定价页面
2. 微调后的模型有效期通常为90天
3. 确保您的AWS账户有足够的权限来创建和管理微调任务
