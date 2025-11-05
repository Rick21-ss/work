from opencompass.models import OpenAISDK

models = [
    dict(
        abbr='ernie-x1.1-preview',
        type=OpenAISDK,
        path='ernie-x1.1-preview',
        key='bce-v3/ALTAK-uARdaVcSqYLhSSlIovGNJ/7206fbda503b0f144e8d1e03626b165152e54c94',
        openai_api_base='https://qianfan.baidubce.com/v2',
        query_per_second=1,
        batch_size=1,
        temperature=0.001,
        max_out_len=16384,
        max_seq_len=32768,
    )
]