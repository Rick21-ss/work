from opencompass.models import OpenAISDK

models = [
    dict(
        abbr='ernie-x1.1-preview',
        type=OpenAISDK,
        path='ernie-x1.1-preview',
        key='bce-v3/ALTAK-uARdaVcSqYLhSSlIovGNJ/7206fbda503b0f144e8d1e03626b165152e54c94',
        openai_api_base='https://qianfan.baidubce.com/v2',
        query_per_second=1,
        batch_size=4,
        temperature=0.001,
        tokenizer_path='gpt-4',
        max_out_len=16384,
        max_seq_len=32768,
        retry=0,  # 遇到错误不重试
        continue_on_error=True,  # 遇到错误继续处理下一个
        temperature=0.6,
    )
]