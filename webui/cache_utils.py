import os
import uuid
from datetime import datetime
import random
import shutil

def setup_workspace(folder):
    # タイムスタンプ＋乱数4桁で一意なIDを生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rand_suffix = f"{random.randint(0, 9999):04d}"
    request_id = f"{timestamp}_{rand_suffix}"
    os.makedirs(folder, exist_ok=True)

    working_dir = os.path.join(folder, request_id)
    os.makedirs(working_dir, exist_ok=True)

    log_dir = os.path.join(folder, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{request_id}.log")

    return log_file, working_dir


def cleanup_workspace(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
