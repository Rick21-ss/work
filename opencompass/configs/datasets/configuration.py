# Azure_fixed.py
from mmengine.config import read_base
from opencompass.datasets import first_capital_postprocess

import json
import os

# ===== 在 read_base() 外部处理所有复杂逻辑 =====

# 1. 加载配置文件
config_path = "/Users/shuishui/Desktop/opencompass/config.json"
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 2. 从JSON中获取所有配置
dataset_templates = config.get("dataset", {})
inference_templates = config.get("inference", {})
evaluation_templates = config.get("evaluation_templates", {})
ceval_subject_mapping = config.get("all_sets", {})

# 3. 创建数据集配置列表
datasets = []

# 4. 使用JSON中的映射批量创建数据集
for dataset_name, subject_info in ceval_subject_mapping.items():
    english_name = subject_info[0]
    chinese_name = subject_info[1]
    category = subject_info[2]
    
    dataset_template = dataset_templates["custom"]
    inference_template = inference_templates["multiple_choice"]
    evaluation_template = evaluation_templates["standard_accuracy"]
    
    # 动态替换提示词中的学科名称
    prompt = inference_template['prompt_template'].replace('{subject}', chinese_name)
    
    # 构建数据集配置
    dataset_config = dict(
        type=CEvalDataset,
        path=dataset_template['path'],
        name=dataset_name,
        abbr=f"ceval-{dataset_name}",
        reader_cfg=dict(
            input_columns=dataset_template['input_columns'],
            output_column=dataset_template['output_column'],
            train_split='dev',
            test_split='val'
        ),
        infer_cfg=dict(
            ice_template=dict(
                type=PromptTemplate,
                template=dict(
                    begin='</E>',
                    round=[
                        dict(role='HUMAN', prompt=prompt),
                        dict(role='BOT', prompt='{answer}')
                    ]
                ),
                ice_token='</E>',
            ),
            retriever=dict(
                type=FixKRetriever,
                fix_id_list=list(range(inference_template['shot_count']))
            ),
            inferencer=dict(type=GenInferencer),
        ),
        eval_cfg=dict(
            evaluator=dict(type=AccEvaluator),
            pred_postprocessor=dict(type=first_capital_postprocess)
        )
    )
    datasets.append(dataset_config)

# ===== 现在使用 read_base() 只做必要的导入 =====
with read_base():
    from opencompass.openicl.icl_prompt_template import PromptTemplate
    from opencompass.openicl.icl_retriever import FixKRetriever
    from opencompass.openicl.icl_inferencer import GenInferencer
    from opencompass.openicl.icl_evaluator import AccEvaluator
    from opencompass.datasets import CEvalDataset



print(f"✅ 从JSON配置创建了 {len(datasets)} 个数据集")