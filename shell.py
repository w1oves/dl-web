import sh
import os
import logging

logging.basicConfig(level=logging.INFO)
# tensorboard=sh.Command("~/.conda/envs/enseg/bin/tensorboard")
train_script = "/home/wzx/weizhixiang/ensegment/tools/train.py"
test_script = "/home/wzx/weizhixiang/ensegment/tools/test.py"
config = "/home/wzx/weizhixiang/ensegment/configs/autoencoder/autoencoder_L2.py"
log_dir = "/home/wzx/dl2/dl2"
gpus = "6,7"
port = 29500
interpreter = "/home/wzx/.conda/envs/enseg/bin/python"
python = sh.Command(interpreter)
os.chdir("/home/wzx/weizhixiang/ensegment/configs/ugev2")
sh.cd("/home/wzx/weizhixiang/ensegment/configs/ugev2")
new_env = os.environ.copy()
new_env["CUDA_VISIBLE_DEVICES"] = gpus

python(
    "-m",
    "torch.distributed.launch",
    f'--nproc_per_node={len(gpus.split(","))}',
    f"--master_port={port}",
    train_script,
    config,
    "--launcher",
    "pytorch",
    '--debug',
    _env={'CUDA_VISIBLE_DEVICES':gpus},
    _fg=True,
)
