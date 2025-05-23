import boto3
import json
from botocore.exceptions import ClientError

# 创建一个 Bedrock Runtime 客户端
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

# 设置模型 ID，例如 nova
PRO_MODEL_ID = "us.amazon.nova-pro-v1:0"
LITE_MODEL_ID = "us.amazon.nova-lite-v1:0"
MICRO_MODEL_ID = "us.amazon.nova-micro-v1:0"

model_id = PRO_MODEL_ID  # 确保此模型 ID 是有效的

# 定义系统提示
system_prompt = [
    {
        "text": "你是一个SRE 工程师，你可以通过脚本对平台对象进行各种操作，你可以调用多个函数来帮助用户完成任务"
    }
]

# 定义消息列表
messages = [
    {
        "role": "user",
        "content": [
            {
                "text": "帮我修改 gateway 的配置,vendor 修改为 alipay"
            }
        ]
    }
]

# 定义工具配置
tools = [
    {
        "toolSpec": {
            "name": "modify_config",
            "description": "修改配置文件",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "service_name": {
                            "type": "string",
                            "description": "服务名称"
                        },
                        "key": {
                            "type": "string",
                            "description": "配置项"
                        },
                        "value": {
                            "type": "string",
                            "description": "配置值"
                        }
                    },
                    "required": ["service_name", "key", "value"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "restart_service",
            "description": "重启服务",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "service_name": {
                            "type": "string",
                            "description": "服务名称"
                        }
                    },
                    "required": ["service_name"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "apply_manifest",
            "description": "应用 Kubernetes 资源",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "资源类型"
                        },
                        "image": {
                            "type": "string",
                            "description": "镜像名称"
                        }
                    },
                    "required": ["resource_type", "image"]
                }
            }
        }
    }
]

# 定义请求负载
payload = {
    "system": system_prompt,
    "messages": messages,
    "inferenceConfig": {
        "max_new_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50
    },
    "toolConfig": {
        "tools": tools,
        "toolChoice": "any"
    }
}

try:
    # 调用模型并发送请求
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload),
        contentType='application/json'
    )

    # 读取响应内容
    response_body = response['body']
    response_data = json.loads(response_body)
    response_message = response_data['choices'][0]['message']['content']
    tool_calls = response_data['choices'][0]['tool_calls']

    print("\nChatGPT want to call function: ", tool_calls)

except ClientError as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

