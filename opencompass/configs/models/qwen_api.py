from opencompass.models import OpenAISDK

models = [
    dict(
        abbr='Qwen3-Max-Preview',
        type=OpenAISDK,
        path='qwen3-max-preview',
        key='sk-b1ba35174a46487086152a4d439307fc',
        base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
        query_per_second=16,
        batch_size=128,
        tokenizer_path='gpt-4',
        max_out_len=4096,
        max_seq_len=32768,
        temperature=0.1,
    )
]