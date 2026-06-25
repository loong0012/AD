import subprocess, os
os.chdir(r'd:\Desktop\Alzheimer-diagnostic system')
subprocess.run(['git', 'add', '-A'], capture_output=True)
subprocess.run(['git', 'commit', '-m', 'fix: rename Dockerfile, use direct uvicorn for Render'], capture_output=True)
r = subprocess.run(['git', 'push', 'ad', 'with-models'], capture_output=True, timeout=60)
print('PUSH:', r.returncode, r.stderr.decode('utf-8', errors='replace')[-200:] if r.stderr else '')
r = subprocess.run(['git', 'push', 'ad', 'with-models:main', '--force'], capture_output=True, timeout=60)
print('PUSH main:', r.returncode, r.stderr.decode('utf-8', errors='replace')[-200:] if r.stderr else '')