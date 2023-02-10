import argparse
import paramiko
from paramiko.client import SSHClient


pr = argparse.ArgumentParser()
pr.add_argument('--host', type=str, required=True)
pr.add_argument('--port', type=int, required=True)
pr.add_argument('--username', type=str, required=False)
pr.add_argument('--password', type=str, required=False)


args = pr.parse_args()


def ssh_client():
    try:
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(args.host, port=args.port, username=args.username, password=args.password, timeout=float(5))
        print("'Connection established'\n"+"#"*10+"\n" + args.host+":"+str(args.port))
    except paramiko.ssh_exception.AuthenticationException:
        print("'Authentication failed | Check required inputs'")
        exit()
    while True:
        try:
            commands = str(input("Execute >> "))
            stdin, stdout, stderr = client.exec_command(command=commands)
            outlines = stdout.readlines()
            resp = ''.join(outlines)
            print(resp)
        except KeyboardInterrupt:
            client.close()
            print("\n'Connection terminated'")
            return False


ssh_client()
