import subprocess
import tempfile

def run_file(script_path, args=None, capture_output=False):
    if args is None:
        args = []

    if script_path.endswith('.py'):
        cmd = ['python3', '-u', script_path] + args
    else:
        cmd = [script_path] + args

    if capture_output:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running {script_path}: {result.stderr}")
            raise Exception(f"Error running {script_path}: {result.stderr}")
        return result.stdout
    else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')
        process.wait()

        if process.returncode != 0:
            print(f"Error running {script_path}")
            raise Exception(f"Error running {script_path}")

def generate_sequence_file(length, seed):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as f:
        filename = f.name
    output = run_file(
        "./scripts/utils/gen_sequence.py",
        ["--length", str(length), "--seed", str(seed)],
        capture_output=True
    )
    with open(filename, "w") as f:
        f.write(output)
    return filename