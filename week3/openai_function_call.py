from openai import OpenAI

client = OpenAI(
    api_key="sk-T6SlqfUnyFytejvA3c1584F87d6343878232185e26243b1d",
    base_url="https://api.apiyi.com/v1",
)


query = "查看 app=grafana 且关键字包含 Error 的日志"

messages = [
    {
        "role": "system",
        "content": "你是一个 Devops 专家，你可以通过自动化工具实现对资源进行配置，你可以调用多个函数来帮助用户完成任务",
    },
    {
        "role": "user",
        "content": query,
    },
]
tools = [
        # 增加 Function Calling 定义 modify_config 函数，入参：service_name，key，value
        {
            "type": "function",
            "function": {
                "name": "modify_config",
                "description": "修改配置文件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_name": {
                            "type": "string",
                            "description": "服务名称",
                        },
                        "key": {
                            "type": "string",
                            "description": "配置项",
                        },
                        "value": {
                            "type": "string",
                            "description": "配置值",
                        },
                    },
                    "required": ["service_name", "key", "value"],
                },
            }
        },
        # 增加 Function Calling 定义 restart_service 函数，入参：service_name
        {
            "type": "function",
            "function": {
                "name": "restart_service",
                "description": "重启服务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_name": {
                            "type": "string",
                            "description": "服务名称",
                        },
                    },
                    "required": ["service_name"],
                },
            }
        },
        # 增加 Function Calling 定义 apply_manifest 函数，入参：resource_type，image
        {
            "type": "function",
            "function": {
                "name": "apply_manifest",
                "description": "应用 Kubernetes 资源",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "资源类型",
                        },
                        "image": {
                            "type": "string",
                            "description": "镜像名称",
                        },
                    },
                    "required": ["resource_type", "image"],
                },
            }
        }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

print("\nChatGPT want to call function: ", tool_calls)