# Linux SSH Remote Server Setup

The Palworld Dashboard can utilize SSH tunnels to securely connect to remote Palworld servers.

The remote server can be configured for SSH access, and the dashboard machine requires an SSH private key that matches a public key installed on the remote server.

---

# 1. Configure the Remote Linux Server

Install OpenSSH Server:

## Debian / Ubuntu

```bash
sudo apt update
sudo apt install openssh-server
```

Enable and start SSH:

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

Verify SSH is running:

```bash
sudo systemctl status ssh
```

---

# 2. Create the SSH User

Create the user that the dashboard will use to connect:

```bash
sudo adduser palserver
```

The dashboard will authenticate using this account.

Example:

```
SSH Username:
palserver
```

---

# 3. Generate an SSH Key on the Dashboard Machine

The SSH key must be generated on the machine running the Palworld Dashboard.

Generate the key:

```bash
ssh-keygen -t ed25519
```

Press **ENTER** to accept the default location.

The keys will be created:

```
/home/<dashboard-user>/.ssh/
```

Files:

```
id_ed25519
```

Private key.

Keep this file secure.

Do not share it.

```
id_ed25519.pub
```

Public key.

This key is copied to the remote server.

---

# 4. Copy the Public Key to the Remote Server

From the dashboard machine:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@hostname
```

Example:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub palserver@192.168.1.50
```

The key will be installed automatically to:

```
/home/palserver/.ssh/authorized_keys
```

---

# 5. Test SSH Authentication

From the dashboard machine:

```bash
ssh palserver@192.168.1.50
```

The connection should succeed without requesting a password.

If successful, SSH key authentication is working.

---

# Root User Configuration

**Using a root account for SSH access is not recommended.**

A compromised SSH private key or misconfigured SSH service could provide an attacker with full administrative access to the entire server.

For improved security, create a dedicated SSH user with only the permissions required by the dashboard.

If the dashboard connects as `root`, the public key location is different:

```
/root/.ssh/authorized_keys
```

Many Linux distributions disable direct root SSH login by default.

Additional configuration may be required in:

```
/etc/ssh/sshd_config
```

Example:

```
PermitRootLogin prohibit-password
PubkeyAuthentication yes
```

After changing SSH configuration:

```bash
sudo systemctl restart ssh
```

---

# 6. Configure the Dashboard

Use the private key generated earlier:

```
/home/<dashboard-user>/.ssh/id_ed25519
```

Configure:

```
SSH Host
SSH Port
SSH Username
SSH Private Key
Remote REST API Host
Remote REST API Port
```

The dashboard will use the private key to authenticate with the public key installed on the remote server.
