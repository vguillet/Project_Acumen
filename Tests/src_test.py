import os
import pexpect
import subprocess
from subprocess import PIPE


def main():
    process = subprocess.Popen('echo %USERNAME%', stdout=PIPE, shell=True)
    subprocess.call("Generators_settings.py", shell=True)
    username = process.communicate()[0]
    print(username) #prints the username of the account you're logged in as

    process = subprocess.call('python py1.py --help', shell=True)

if __name__ == '__main__':
    main()

# os.system("Generators_settings.py")
