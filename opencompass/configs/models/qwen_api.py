from opencompass.models import OpenAISDK

models = [
    dict(
        abbr='Qwen3-Max-Preview',
        type=OpenAISDK,
        path='qwen3-max-preview',
        key='sk-b1ba35174a46487086152a4d439307fc',
        openai_api_base='https://dashscope.aliyuncs.com/compatible-mode/v1',
        query_per_second=1,
        batch_size=4,
        temperature=0.6,
        tokenizer_path='gpt-4',
        max_out_len=4096,
        max_seq_len=32768,
        retry=0,  # 遇到错误不重试
        continue_on_error=True,  # 遇到错误继续处理下一个
    )
]