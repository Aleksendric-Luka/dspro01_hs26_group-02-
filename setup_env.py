"""Create or update .venv using requirements.txt next to this script.

Create/sync: python setup_env.py
Upgrade:    python setup_env.py --upgrade
Alternative requirements: python setup_env.py --requirements requirements-lock.txt
Uses only Python's standard library. Activation is not required to run it.
"""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upgrade', action='store_true',
                        help='Upgrade listed packages within requirements constraints.')
    parser.add_argument('--requirements', default='requirements.txt',
                        help='Requirements path, relative to the script directory.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    requirements = (root / args.requirements).resolve()
    env_dir = root / '.venv'
    env_python = env_dir / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not requirements.is_file():
        parser.error(f'Requirements file not found: {requirements}')
    if env_dir.exists():
        if not (env_dir / 'pyvenv.cfg').is_file() or not env_python.is_file():
            parser.error(f'{env_dir} is not a usable venv. Rename it and try again.')
        print(f'Using existing environment: {env_dir}', flush=True)
    else:
        print(f'Creating environment with Python {sys.version.split()[0]}: {env_dir}', flush=True)
        venv.EnvBuilder(with_pip=True).create(env_dir)
    command = [str(env_python), '-m', 'pip', 'install']
    if args.upgrade:
        command.append('--upgrade')
    command.extend(['-r', str(requirements)])
    subprocess.run(command, check=True)
    subprocess.run([str(env_python), '-m', 'pip', 'check'], check=True)
    print('\nEnvironment ready. Select .venv in your editor or activate it:')
    print(f'  macOS/Linux: source "{env_dir}/bin/activate"')
    print(f'  Windows PowerShell: & "{env_dir}/Scripts/Activate.ps1"')
    print(f'  Windows Command Prompt: "{env_dir}\\Scripts\\activate.bat"')


if __name__ == '__main__':
    try:
        main()
    except (subprocess.CalledProcessError, OSError) as error:
        print(f'Environment setup failed: {error}', file=sys.stderr)
        sys.exit(1)
