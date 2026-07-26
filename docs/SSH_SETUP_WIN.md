# Windows SSH Remote Server Setup

The Palworld Dashboard uses SSH tunnels to securely connect to remote Palworld servers.

The remote Windows server requires OpenSSH Server, and the dashboard machine requires an SSH private key that matches a public key installed on the remote server.

---

# 1. Configure the Remote Windows Server

Install OpenSSH Server.

Open **PowerShell as Administrator**:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

Enable and start the SSH service:

```powershell
Set-Service -Name sshd -StartupType Automatic
Start-Service sshd
```

Verify SSH is running:

```powershell
Get-Service sshd
```

The status should show:

```
Running
```

---

# 2. Create the SSH User

Create or use the Windows account that the dashboard will connect with.

Example:

```
Username:
palserver
```

The dashboard will authenticate using this account.

---

# 3. Generate an SSH Key on the Dashboard Machine

The SSH key must be generated on the machine running the Palworld Dashboard.

Open PowerShell:

```powershell
ssh-keygen -t ed25519
```

Press **ENTER** to accept the default location.

The keys will be created:

```
C:\Users\<dashboard-user>\.ssh\
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

This key is copied to the remote Windows server.

---

# 4. Copy the Public Key to the Remote Windows Server

From the dashboard machine:

```powershell
ssh-copy-id -i $env:USERPROFILE\.ssh\id_ed25519.pub username@hostname
```

Example:

```powershell
ssh-copy-id -i $env:USERPROFILE\.ssh\id_ed25519.pub palserver@192.168.1.50
```

For a standard Windows user, the key will be installed to:

```
C:\Users\palserver\.ssh\authorized_keys
```

---

# Windows Administrator User Configuration

**Using an administrator account for SSH access is not recommended.**

A compromised SSH private key or misconfigured SSH service could provide an attacker with full administrative access to the entire server.

For improved security, create a dedicated Windows user with only the permissions required by the dashboard.

---

When connecting as a Windows user that is a member of the local Administrators group, OpenSSH uses a different authorized key file.

The public key must be installed here:

```
C:\ProgramData\ssh\administrators_authorized_keys
```

The file must contain the public key generated on the dashboard machine.

---

## Configure OpenSSH for Administrator Keys

Open the SSH configuration file:

```
C:\ProgramData\ssh\sshd_config
```

Ensure the following settings exist:

```
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
```

Add or update the administrator group configuration (Place at end of file):

```
Match Group administrators
       AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

Save the file.

---

## Configure Administrator Key Permissions

Open PowerShell as Administrator.

Remove inherited permissions:

```powershell
icacls C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r
```

Grant access to SYSTEM:

```powershell
icacls C:\ProgramData\ssh\administrators_authorized_keys /grant SYSTEM:F
```

Grant access to Administrators:

```powershell
icacls C:\ProgramData\ssh\administrators_authorized_keys /grant Administrators:F
```

---

## Restart SSH Service

After changing SSH configuration:

```powershell
Restart-Service sshd
```

---

## Test Administrator SSH Access

From the dashboard machine:

```powershell
ssh Administrator@hostname
```

Example:

```powershell
ssh palserver@192.168.1.50
```

If configured correctly, authentication should succeed using the private key without requesting a password.

---

# 6. Configure the Dashboard

Use the private key generated earlier:

```
C:\Users\<dashboard-user>\.ssh\id_ed25519
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
