# SSH Troubleshooting Guide

This guide covers common SSH issues when connecting the Palworld Dashboard to remote servers.

Before troubleshooting, verify that SSH works manually from the machine running the dashboard:

```bash
ssh username@hostname
```

If manual SSH authentication does not work, the dashboard will not be able to create an SSH tunnel.

---

# SSH Connection Checklist

Verify:

- SSH service is running on the remote server
- SSH host is correct
- SSH port is correct
- SSH username is correct
- Private key path is correct
- Public key is installed on the remote server
- Firewall allows SSH traffic
- Remote REST API is running

---

# Permission Denied (publickey)

Example error:

```
Permission denied (publickey).
```

Common causes:

- Wrong SSH username
- Wrong private key configured
- Public key was not copied correctly
- Public key was installed for a different user
- SSH is using a different key than expected
- File permissions are incorrect

---

## Verify the Correct Key Is Being Used

Test manually with the private key:

Linux:

```bash
ssh -i ~/.ssh/id_ed25519 username@hostname
```

Windows PowerShell:

```powershell
ssh -i $env:USERPROFILE\.ssh\id_ed25519 username@hostname
```

If this works, the dashboard should use the same private key.

---

# Debug SSH Authentication

Use verbose SSH logging:

```bash
ssh -vvv username@hostname
```

Look for:

Successful:

```
Offering public key
Server accepts key
Authenticated to hostname
```

Failure:

```
Offering public key
Server refused our key
Permission denied (publickey)
```

---

# SSH Service Not Running

## Linux

Check SSH status:

```bash
sudo systemctl status ssh
```

Restart:

```bash
sudo systemctl restart ssh
```

---

## Windows

Check SSH service:

```powershell
Get-Service sshd
```

Restart:

```powershell
Restart-Service sshd
```

---

# Connection Refused

Example:

```
ssh: connect to host hostname port 22: Connection refused
```

Common causes:

- SSH service is stopped
- Incorrect SSH port
- Firewall blocking SSH
- Server is offline

Check listening ports.

Linux:

```bash
sudo ss -tlnp | grep ssh
```

Windows:

```powershell
Get-NetTCPConnection -LocalPort 22
```

---

# Connection Timeout

Example:

```
Connection timed out
```

Common causes:

- Firewall blocking SSH
- Port forwarding not configured
- Server is unreachable
- Incorrect IP address or hostname

Test connectivity:

```bash
ping hostname
```

Test SSH port:

Linux:

```bash
nc -zv hostname 22
```

Windows PowerShell:

```powershell
Test-NetConnection hostname -Port 22
```

---

# Linux Permission Issues

SSH requires strict permissions.

Incorrect:

```
~/.ssh                 755
authorized_keys        644
```

Correct:

```
~/.ssh                 700
authorized_keys        600
```

Fix:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Verify ownership:

```bash
ls -la ~/.ssh
```

Fix ownership:

```bash
sudo chown -R username:username ~/.ssh
```

---

# Linux Root Login Problems

Root SSH access is disabled by default on many distributions.

Check:

```
/etc/ssh/sshd_config
```

Verify:

```
PubkeyAuthentication yes
```

For root login:

```
PermitRootLogin prohibit-password
```

Restart SSH:

```bash
sudo systemctl restart ssh
```

Using a dedicated SSH user is recommended instead of root.

---

# Windows Administrator Key Problems

Windows administrator accounts use:

```
C:\ProgramData\ssh\administrators_authorized_keys
```

instead of:

```
C:\Users\<username>\.ssh\authorized_keys
```

Verify:

```
C:\ProgramData\ssh\sshd_config
```

Contains:

```
Match Group administrators
       AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

Check permissions:

```powershell
icacls C:\ProgramData\ssh\administrators_authorized_keys
```

Restart SSH:

```powershell
Restart-Service sshd
```

---

# SSH Works But Dashboard Cannot Connect

If manual SSH works but the dashboard fails:

Verify:

- Dashboard is using the same private key
- Dashboard username matches the working SSH username
- SSH host matches the manual test
- SSH port matches the manual test
- Remote REST API host is correct
- Remote REST API port is correct

---

# SSH Tunnel Works But REST API Fails

Symptoms:

- SSH authentication succeeds
- Dashboard cannot retrieve server data

Check:

## Remote REST API Status

Linux:

```bash
curl http://127.0.0.1:<api-port>
```

Example:

```bash
curl http://127.0.0.1:8212
```

Verify:

- REST API is enabled
- REST API port is correct
- Palworld server is running
- Firewall rules allow access

---

# Collecting Debug Information

When reporting an SSH issue, include:

SSH test:

```bash
ssh -vvv username@hostname
```

Also include:

- Operating system of dashboard machine
- Operating system of remote server
- SSH username
- SSH port
- Error message
- Whether manual SSH login works
- Whether the REST API works locally on the remote server

Do not share:

- Private keys
- Passwords
- Tokens
- Configuration secrets
