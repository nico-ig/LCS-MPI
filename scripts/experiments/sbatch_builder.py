import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import scripts.utils.utils as utils

def read_sbatch_template():
    with open("./scripts/cluster/sbatch.sh", "r") as f:
        return f.read()

def split_sbatch_template(sbatch_template):
    sbatch_lines = sbatch_template.splitlines()
    sbatch_lines = [line for line in sbatch_lines if line.strip()]
    sbatch_header = "\n".join(sbatch_lines[:-2])
    sbatch_body = sbatch_lines[-2:]
    return sbatch_header, sbatch_body

def build_sbatch_header(sbatch_header):
    return sbatch_header + "\n"

def split_hosts(sbatch_body, index):
    job_body = ''
    if index == 0:
        job_body = "wait\n"
    index = 1 - index
    return job_body, index

def generate_job_body(sbatch_body, repeats_in_job, nodes, ntasks):
    job_body = sbatch_body[0] + "\n"
    job_body += "IFS=',' read -ra HOST_ARRAY <<< \"$HOST_LIST\"\n"
    i = 0
    for r in range(repeats_in_job):
        if r == 0 or nodes > 1:
            job_body_split = ''
        else:
            job_body_split, i = split_hosts(sbatch_body, i)
        job_body += f"export MPI_PROFILE_NAME={{MPI_PROFILE_NAME}}\n"
        job_body += f"HOSTS=${{{{HOST_ARRAY[{i}]}}}}\n" if nodes == 1 else f"HOSTS=$HOST_LIST\n"
        job_body += sbatch_body[1]
        job_body += "\n" if nodes > 1 else " &\n"
        job_body += job_body_split
    return job_body

def build_sbatch_body(sbatch_body, repeats, repeats_per_job, num_length_cases, nodes, ntasks):
    script_body_list = []
    total_jobs = utils.calculate_total_jobs(repeats, repeats_per_job, num_length_cases)
    remaining = repeats * num_length_cases
    for _ in range(total_jobs):
        repeats_in_job = min(repeats_per_job, remaining)
        remaining -= repeats_in_job
        job_body = generate_job_body(sbatch_body, repeats_in_job, nodes, ntasks)
        script_body_list.append(job_body)
    return script_body_list

def mount_sbatch_scripts(sbatch_header, sbatch_body):
    sbatch_script_list = []
    for i, job_body in enumerate(sbatch_body):
        sbatch_script = sbatch_header + job_body
        sbatch_script_list.append(sbatch_script)
    return sbatch_script_list

def create_sbatch_scripts(sbatch_template, repeats, repeats_per_job, num_length_cases, nodes, ntasks):
    sbatch_header, sbatch_body = split_sbatch_template(sbatch_template)
    sbatch_header = build_sbatch_header(sbatch_header)
    sbatch_body = build_sbatch_body(sbatch_body, repeats, repeats_per_job, num_length_cases, nodes, ntasks)
    sbatch_scripts = mount_sbatch_scripts(sbatch_header, sbatch_body)
    return sbatch_scripts

def format_sbatch_header(sbatch_scripts, job_name, output_file, error_file, config, extra_fields=None):
    formatted_scripts = []
    node_multiplier = 2 if config['nodes'] == 1 else 1
    for i, script in enumerate(sbatch_scripts):
        fields = {
            "JOB_NAME": f"{job_name}_part_{i}",
            "OUTPUT_FILE": f"{output_file}_part_{i}.out",
            "ERROR_FILE": f"{error_file}_part_{i}.err",
            "NODES": config['nodes'] * node_multiplier,
            "NTASKS": config['ntasks'] * node_multiplier,
            "NTASKS_PER_NODE": config['ntasks_per_node'],
            "MEM": config['memory'],
            "HOST_ARRAY": "{HOST_ARRAY}",
        }
        if extra_fields:
            index = 0
            for key, value in extra_fields.items():
                if "<INDEX>" in value:
                    extra_fields[key] = extra_fields[key].replace("<INDEX>", str(index))
                    index = index + 1
            fields.update(extra_fields)
        formatted_script = script.format(**fields)
        formatted_scripts.append(formatted_script)
    return formatted_scripts

def format_sbatch_lines(lines, input_files, binary, config):
    formatted_lines = []
    num_inputs = len(input_files)
    for i, line in enumerate(lines):
        input_a, input_b = input_files[i % num_inputs]
        if "{FILE_A}" in line or "{FILE_B}" in line:
            formatted_line = line.format(
                NODES=config['nodes'],
                NTASKS=config['ntasks'],
                NTASKS_PER_NODE=config['ntasks_per_node'],
                CPU_LIST=",".join(str(c) for c in config['cpu_list']),
                BIND_TO=config['bind_to'],
                BINARY=binary,
                FILE_A=input_a,
                FILE_B=input_b,
            )
        else:
            formatted_line = line
        formatted_lines.append(formatted_line)
    formatted_lines.append("\n")
    return formatted_lines

def format_sbatch_body(sbatch_scripts, input_files, binary, config):
    formatted_scripts = []
    input_files = list(input_files.values())
    for script in sbatch_scripts:
        lines = script.splitlines()
        formatted_lines = format_sbatch_lines(lines, input_files, binary, config)
        formatted_scripts.append("\n".join(formatted_lines))
    return formatted_scripts