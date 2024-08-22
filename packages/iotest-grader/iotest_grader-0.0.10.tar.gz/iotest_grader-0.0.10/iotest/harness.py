import pathlib
import pexpect
import inspect
import subprocess
import os

def find_cases():
    caller_dir = pathlib.Path(inspect.stack()[1][1]).parent
    cases_dir = caller_dir / 'testcases'
    return [x.name for x in cases_dir.iterdir() if x.is_dir()]


def execute(testcase_dirname, mainfile_relpath='main.py'):
    caller_dir = pathlib.Path(inspect.stack()[1][1]).parent
    mainfile =  caller_dir / mainfile_relpath
    testcase_basedir = caller_dir / 'testcases'

    expected_file = testcase_basedir / testcase_dirname / 'expected.txt'
    actual_file = testcase_basedir / testcase_dirname / 'actual.txt'
    input_file = testcase_basedir / testcase_dirname / 'input.txt'

    with open(expected_file.resolve(), 'r') as exfile:
        expected = [x.strip() for x in exfile.readlines()]
    with open(input_file, 'r') as inpfile:
        inp = [x.strip() for x in inpfile.readlines()]

    child = pexpect.spawn(f'python {mainfile.resolve()}', echo=False)
    for i in inp:
        child.sendline(i)

    actual = [x.strip() for x in child.read().decode('ascii').split('\r\n') if x]
    with open(actual_file, 'w') as outfile:
        # Workaround for https://github.com/microsoft/vscode/issues/224498
        outfile.writelines([x + '\n' for x in actual])
    
    in_vscode = 'USER' in os.environ.keys() and os.environ['USER'] == 'vscode'
    if in_vscode and (actual != expected):
        my_env = os.environ.copy()
        if "ELECTRON_RUN_AS_NODE" in my_env:
            del my_env["ELECTRON_RUN_AS_NODE"]
        subprocess.run(['code', '-d', expected_file, actual_file], env=my_env)

    assert actual == expected, f"Comparison failed, run this command to see the differences:\ncode -d {expected_file} {actual_file}"
