# Copyright ZettaBlock Labs 2024

lf_template = """# Code framework configuration
framework: llama-factory


# Base model configurations
base_model:
  # The name for the base model, can be a local path or repository name
  name: meta-llama/Meta-Llama-3-8B-Instruct
  # Where the model is sourced from. Choose one from zettahub, local
  source: zettahub


# Base datasets configuration
base_datasets:
  # Known datasets. Simply specify dataset name if it is available in [dataset_info.json](https://github.com/hiyouga/LLaMA-Factory/blob/main/data/dataset_info.json).
  - name: alpaca-cleaned
    source: huggingface
    path: yahma/alpaca-cleaned


# Output model configurations
output_model_name: "{}"
output_model_fee: 10


# Fine-tune parameters configurations (compatible with llama-factory framework)
### method
stage: sft
do_train: true
finetuning_type: lora
lora_target: all

### dataset
template: llama3  # for now we will limit templates only to those pre-defined in template.py
cutoff_len: 1024
max_samples: 1000
overwrite_cache: true
preprocessing_num_workers: 16

### output
output_dir: saves/llama3-8b/lora/sft
logging_steps: 10
save_steps: 500
plot_loss: true
overwrite_output_dir: true

### train
per_device_train_batch_size: 8
gradient_accumulation_steps: 1
learning_rate: 1.0e-5
num_train_epochs: 1.0
weight_decay: 0.1
lr_scheduler_type: cosine
warmup_ratio: 0.1
bf16: true
ddp_timeout: 180000000

### eval
eval_on_start: False
val_size: 0.1
per_device_eval_batch_size: 1
eval_strategy: steps
eval_steps: 100
"""
