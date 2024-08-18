# Copyright ZettaBlock Labs 2024
import json
import os
import requests
from typing import Any
import yaml

from zetta.config_templates import lf_template

WORKER_HOST = "http://98.81.106.81:8000"


def worker_health():
    url = f"{WORKER_HOST}/healthz"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get health: [{response.status_code}] {response.text}")


def worker_get_jobs(json_output=False):
    url = f"{WORKER_HOST}/lf/jobs"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if json_output:
            return json.dumps(data, indent=2)
        else:
            return yaml.dump(data, default_flow_style=False)
    else:
        raise Exception(f"Failed to get jobs: [{response.status_code}] {response.text}")


def worker_get_job(uuid, json_output=False):
    url = f"{WORKER_HOST}/lf/jobs/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if json_output:
            return json.dumps(data, indent=2)
        else:
            return yaml.dump(data, default_flow_style=False)
    else:
        raise Exception(f"Failed to get job: [{response.status_code}] {response.text}")


def worker_log_job(uuid):
    url = f"{WORKER_HOST}/logs/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["logs"]
    else:
        raise Exception(f"Failed to log job: [{response.status_code}] {response.text}")


def worker_run_job(
    config: dict[str, Any]
):
    url = f"{WORKER_HOST}/lf/jobs"
    data = {
        "framework": "llama-factory",
        "config": config,
        "config_file_type": "json",
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to submit job: [{response.status_code}] {response.text}")


def safe_load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def safe_load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def process_zetta_job_config(config_path):
    raw_cfg = safe_load_yaml(config_path)
    output_model_name = raw_cfg["output_model_name"]
    output_model_fee = raw_cfg["output_model_fee"]
    print(f"Output model name: {output_model_name}, fee: {output_model_fee}")
    
    base_datasets = raw_cfg["base_datasets"]
        
    # dump llama-factory config.yml
    lf_config = dict(
        model_name_or_path=raw_cfg["base_model"]["name"],
        ### method
        stage=raw_cfg["stage"],
        do_train=raw_cfg["do_train"],
        finetuning_type=raw_cfg["finetuning_type"],
        lora_target=raw_cfg["lora_target"],
        # datasets
        dataset=','.join([i["name"] for i in base_datasets]),
        template=raw_cfg["template"],
        cutoff_len=raw_cfg["cutoff_len"],
        max_samples=raw_cfg["max_samples"],
        overwrite_cache=raw_cfg["overwrite_cache"],
        preprocessing_num_workers=raw_cfg["preprocessing_num_workers"],
        ### output
        output_dir=raw_cfg["output_dir"],
        logging_steps=raw_cfg["logging_steps"],
        save_steps=raw_cfg["save_steps"],
        plot_loss=raw_cfg["plot_loss"],
        overwrite_output_dir=raw_cfg["overwrite_output_dir"],
        ### train
        per_device_train_batch_size=raw_cfg["per_device_train_batch_size"],
        gradient_accumulation_steps=raw_cfg["gradient_accumulation_steps"],
        learning_rate=raw_cfg["learning_rate"],
        num_train_epochs=raw_cfg["num_train_epochs"],
        lr_scheduler_type=raw_cfg["lr_scheduler_type"],
        warmup_ratio=raw_cfg["warmup_ratio"],
        bf16=raw_cfg["bf16"],
        ddp_timeout=raw_cfg["ddp_timeout"],
        ### eval
        val_size=raw_cfg["val_size"],
        per_device_eval_batch_size=raw_cfg["per_device_eval_batch_size"],
        eval_strategy=raw_cfg["eval_strategy"],
        eval_steps=raw_cfg["eval_steps"],
    )
    return lf_config


def init_zetta_job_config(project_name, location):
    if not os.path.exists(location):
        os.makedirs(location, exist_ok=True)
    path = f"{location}/config.yaml"
    with open(path, 'w') as file:
        file.write(lf_template.format(project_name))
    return path


""" Gitea interactions"""

def run_command(c):
    """
    Run command and return all its output at a time
    :param c: command in string
    :return: command output or err
    """
    import subprocess
    try:
        p = subprocess.Popen(c, stdout=subprocess.PIPE, shell=True)
        print('process id is {}'.format(p.pid))
        out, err = p.communicate()
        return {'out': out, 'err': err}
    except Exception as e:
        return {'err': e}


GITEA_REPO = "https://c2dfc8357c7461343b83e8af68bd96222aa8cc99@gitea.stag-vxzy.zettablock.com/ruimins/test_repo.git"
GITEA_REPO_PUBLIC = "https://gitea.stag-vxzy.zettablock.com/ruimins/test_repo"
commands_template = """
git clone {} {};
cd {};
git checkout -b {};
cp {} .;
git add .;
git commit -m "Add files for job {}";
git push origin {};
cd -;
rm -rf {};
"""

def gitea_upload(config_path: str, job_id: str):
    config_path = os.path.abspath(config_path)
    tmp_path = os.path.abspath(f"{job_id}")
    os.makedirs(tmp_path, exist_ok=True)
    cmd = commands_template.format(GITEA_REPO, tmp_path, tmp_path, job_id, config_path, job_id, job_id, tmp_path)
    # return cmd
    try:
        res = run_command(cmd)
        if res["err"]:
            raise Exception(res["err"])
        # extract commit link
        out = res["out"].decode("utf-8")
        # example out: "[branch_name 33a1896] commit message"
        commit_hash = out.split("]")[0].split(" ")[-1]
        link = f"{GITEA_REPO_PUBLIC}/src/commit/{commit_hash}"
        return link
    except Exception as e:
        print(e)
        return None
