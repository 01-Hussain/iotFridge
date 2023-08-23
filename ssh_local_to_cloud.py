import paramiko

hostname = "ssh.community.saturnenterprise.io"
username = "w-ssh-alial-trainingapiserver-308f4b40402c4d15a31b6d831a39df67"

session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # For simplicity. Don't use in production

try:
    key_file = paramiko.ed25519key.Ed25519Key.from_private_key_file("id_ed25519")
    session.connect(hostname,username=username,pkey=key_file,look_for_keys=False,allow_agent=False)
    stdin, stdout, stderr = session.exec_command("ls")
    print(stdout.read().decode())
finally:
    session.close()
