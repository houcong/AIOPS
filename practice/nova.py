import boto3
import json
import base64
import datetime

PRO_MODEL_ID = "us.amazon.nova-pro-v1:0"
LITE_MODEL_ID = "us.amazon.nova-lite-v1:0"
MICRO_MODEL_ID = "us.amazon.nova-micro-v1:0"

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Define your system prompt(s).
system_list = [
    { "text": "请用中文回答" }
]

# Define one or more messages using the "user" and "assistant" roles.
message_list = [
    {"role": "user", "content": [{"text": "tell me a joke"}]},
]

# Configure the inference parameters.
inf_params = {"max_new_tokens": 300, "top_p": 0.9, "top_k": 20, "temperature": 0.7}

native_request = {
    "messages": message_list,
    "system": system_list,
    "inferenceConfig": inf_params,
}

# Invoke the model and extract the response body.
response = client.invoke_model(modelId=LITE_MODEL_ID, body=json.dumps(native_request))
request_id = response["ResponseMetadata"]["RequestId"]
print(f"Request ID: {request_id}")
model_response = json.loads(response["body"].read())

# Pretty print the response JSON.
print("\n[Full Response]")
print(json.dumps(model_response, indent=2))

# Print the text content for easy readability.
content_text = model_response["output"]["message"]["content"][0]["text"]
print("\n[Response Content Text]")
print(content_text)