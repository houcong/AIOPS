import boto3
import json
from botocore.exceptions import ClientError

# 设置模型 ID，例如 nova
PRO_MODEL_ID = "us.amazon.nova-pro-v1:0"
LITE_MODEL_ID = "us.amazon.nova-lite-v1:0"
MICRO_MODEL_ID = "us.amazon.nova-micro-v1:0"

# 创建一个 Bedrock Runtime 客户端
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# 定义系统提示
system_list = [
    { "text": "你是一个SRE 工程师，你可以通过脚本对平台对象进行各种操作，你可以调用多个函数来帮助用户完成任务" }
]

# 定义消息列表
message_list = [
    {"role": "user", "content": [{"text": "帮我修改 gateway 的配置,vendor 修改为 alipay"}]},
]

# 配置推理参数
inf_params = {"max_new_tokens": 300, "top_p": 0.9, "top_k": 20, "temperature": 0.7}

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

# 构建请求负载
native_request = {
    "messages": message_list,
    "system": system_list,
    "inferenceConfig": inf_params,
    "toolConfig": {
        "tools": tools,
        "toolChoice": "any",
    }
}

try:
    # 调用模型并发送请求
    response = client.invoke_model(
        modelId=LITE_MODEL_ID,
        body=json.dumps(native_request),
        contentType='application/json'
    )

    # 读取响应内容
    response_body = response['body'].read().decode('utf-8')
    model_response = json.loads(response_body)

    # 美化打印响应 JSON
    print("\n[Full Response]")
    print(json.dumps(model_response, indent=2))

    # 打印文本内容以便于阅读
    content_text = model_response["output"]["message"]["content"][0]["text"]
    print("\n[Response Content Text]")
    print(content_text)

except ClientError as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")