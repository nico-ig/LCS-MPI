import subprocess
import tempfile
import time
import os
import yaml
import statistics

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def build_command_(script_path, args):
    if script_path.endswith('.py'):
        return ['python3', '-u', script_path] + args
    return [script_path] + args

def run_with_capture_(cmd, env):
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error running {cmd[0]}: {result.stderr}")
        return ""
    return result.stdout

def run_with_output_(cmd, env):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    try:
        for line in process.stdout:
            print(line, end='')
        process.wait()
        if process.returncode != 0:
            print(f"Error running {cmd[0]}")
            raise Exception(f"Error running {cmd[0]}")
    except KeyboardInterrupt:
        process.terminate()

def run_file(script_path, args=None, capture_output=False, env=None):
    if args is None:
        args = []

    args = list(map(str, args))
    cmd = build_command_(script_path, args)
    
    if capture_output:
        return run_with_capture_(cmd, env)
    else:
        run_with_output_(cmd, env)
    
def generate_sequence_file(length, seed, tmp_dir):
    os.makedirs(tmp_dir, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt', dir=tmp_dir) as f:
        filename = f.name
    output = run_file(
        "./scripts/utils/gen_sequence.py",
        ["--length", str(length), "--seed", str(seed)],
        capture_output=True
    )
    with open(filename, "w") as f:
        f.write(output)
    return filename

def compile_profile_binary(config):
    print("> Compiling profile binary...")
    env = os.environ.copy()
    env["TARGET"] = config['profile']['target']
    run_file(
        "./scripts/utils/compile.sh",
        [
            config["makefile"]["path"],
            "profile"
        ],
        capture_output=False,
        env=env
    )
    print("> Compilation done.")

def compile_release_binary(config):
    print("> Compiling release binary...")
    env = os.environ.copy()
    env["TARGET"] = config['release']['target']
    run_file(
        "./scripts/utils/compile.sh",
        [
            config["makefile"]["path"],
            "release"
        ],
        capture_output=False,
        env=env
    )
    print("> Compilation done.")

def wait_for_job(job_id, sleep_time):
    while True:
        result = run_file("squeue", ["-j", job_id], capture_output=True)
        if job_id not in result.split():
            print(f"> Job {job_id} finished.")
            break
        print(f"> Job {job_id} still running... waiting {sleep_time}s")
        time.sleep(sleep_time)

def submit_job(job_script, tmp_dir):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.sh', dir=tmp_dir) as job_file:
        job_file.write(job_script)
    result = run_file("sbatch", [job_file.name], capture_output=True)
    job_id = result.split()[-1]
    return job_id

def submit_and_wait_for_jobs(job_scripts, job_name_prefix, sleep_time, tmp_dir):
    for i, script in enumerate(job_scripts):
        job_name_part = f"{job_name_prefix}_part_{i}"
        print(f"> Submitting job for {job_name_part}...")
        job_id = submit_job(script, tmp_dir)
        wait_for_job(job_id, sleep_time)
        
def calculate_total_jobs(repeats, repeats_per_job, num_cases):
    total_repeats = repeats * num_cases
    jobs = total_repeats // repeats_per_job
    if total_repeats % repeats_per_job != 0:
        jobs += 1
    return jobs
    
def generate_sequence_files(length_cases, tmp_dir):
    input_files = {}
    for case in length_cases:
        length = case["length"]
        seed_a, seed_b = case["seeds"]

        input_a = generate_sequence_file(length, seed_a, tmp_dir)
        input_b = generate_sequence_file(length, seed_b, tmp_dir)
        input_files[length] = (input_a, input_b)
    return input_files

def create_remove_input_files_script(input_files, tmp_dir):
    script_content = "#!/bin/bash\n"
    for length, (input_a, input_b) in input_files.items():
        script_content += f"rm -rf {input_a} {input_b}\n"
    script_path = os.path.join(tmp_dir, "remove_input_files.sh")
    return script_content

def get_repeats_per_job(nodes, ntasks, repeats_per_job):
    if nodes == 1:
        return repeats_per_job * 2
    return repeats_per_job

def compute_mean_and_std(time_list):
    mean = statistics.mean(time_list)
    stdev = statistics.stdev(time_list)
    return round(mean, 3), round(stdev, 3)

def prepare_directories(config, dir_name):
    output_dir = config["benchmark"]["results_dir"] + f"/{dir_name}"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(config["benchmark"]["tmp_dir"], exist_ok=True)
    return output_dir