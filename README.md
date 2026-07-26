# Palworld Dashboard

A web-based administration dashboard for **Palworld Dedicated Servers**.

Palworld Dashboard provides a centralized interface for monitoring and administering one or more Palworld dedicated servers. It supports both local and remote servers through SSH tunneling and provides live information about players, bases, and server status.

**Repository:**
https://github.com/FMAWrath2069/Palworld-Dashboard

---

## Features

* Multi-server management
* Live interactive base map
* Player monitoring
* Real-time server statistics
* Automatic polling
* SSH tunnel support for remote servers
* Automatic SSH tunnel recovery
* Broadcast announcements
* Kick, Ban, and Unban players
* World Save
* Graceful Shutdown
* Emergency Stop
* Per-server configuration
* Automatic local data caching
* Live server status indicators

---

## Requirements

* Python 3.11 or newer
* Git
* OpenSSH Client (required for remote server management)
* A Palworld Dedicated Server with the REST API and GAME-DATA API enabled

---

## Clone the Repository

```bash
git clone https://github.com/FMAWrath2069/Palworld-Dashboard.git

cd Palworld-Dashboard
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

If a `requirements.txt` file is included:

```bash
pip install -r requirements.txt
```

Otherwise install the required packages manually:

```bash
pip install flask
pip install requests
pip install waitress
pip install pyyaml
```

---

## Project Structure

```text
Palworld-Dashboard/

app.py
config.yaml

core/
routes/
services/
static/
templates/

data/
map/
```

---

## Configuration

Edit **config.yaml**.

Example:

```yaml
server:
  host: 0.0.0.0
  port: 5000
  debug: true
```

---

## Running the Dashboard

Start the application:

```bash
python app.py
```

Open your browser and navigate to:

```
http://localhost:5000
```

---

## Adding a Server

Open the **Configuration** window and enter:

* Server Name
* Server Address
* REST API Port
* Administrator Password

Optional settings include:

* Poll Interval
* Data Refresh Interval
* Maximum Base Distance

---

## Remote Servers

Remote servers may be managed through SSH.

Enable **Use SSH** and configure:

* SSH Host
* SSH Port
* SSH Username
* SSH Private Key
* Remote Host
* Remote REST API Port

The dashboard automatically creates and maintains an SSH tunnel.

If the SSH connection is interrupted, the dashboard automatically attempts to reconnect.

---

## Server Status

Each configured server reports its current status.

**🟢 Online**

The server is reachable and responding.

**🟡 Connecting**

The dashboard is establishing or restoring an SSH connection.

**🔴 Offline**

The server cannot be reached.

**⚪ Unknown**

The server has not yet been contacted.

---

## Data Storage

Each configured server maintains its own data directory.

```text
data/
└── servers/
    ├── default/
    ├── server-12345/
    └── server-67890/
```

Each directory contains cached information such as:

```text
bases.json
players.json
pals.json
stats.json
metadata.json
```

Deleting a server automatically:

* Stops its polling thread
* Closes any active SSH tunnel
* Removes status information
* Deletes all cached data
* Removes the server configuration

---

## Troubleshooting

### 401 Unauthorized

Verify that the administrator password configured in the dashboard matches the administrator password configured on the Palworld server.

---

### SSH Tunnel Fails

Verify:

* SSH Host
* SSH Username
* Private Key
* Firewall configuration
* Remote REST API Port

Test the connection manually:

```bash
ssh username@hostname
```

---

### No Bases or Players Displayed

Verify that:

* The Palworld REST API is enabled.
* The server is online.
* The configured administrator password is correct.
* The polling interval has elapsed.

---

### Connection Refused

Verify:

* Server IP address
* REST API Port
* Firewall rules
* REST API is enabled

---

## Updating

Pull the latest changes:

```bash
git pull
```

If dependencies have changed:

```bash
pip install -r requirements.txt
```

Restart the application.

---

## Project Layout

### `core/`

Application configuration, storage, and shared server state.

### `routes/`

Flask API endpoints.

### `services/`

Business logic including:

* Polling
* REST API communication
* SSH tunnel management
* Parsing
* Caching
* Status tracking

### `static/`

JavaScript, CSS, images, and client-side assets.

### `templates/`

HTML templates.

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

Please use the GitHub Issues page:

https://github.com/FMAWrath2069/Palworld-Dashboard/issues

---

## License

This project is licensed under the AGPL 3.0 License. See the LICENSE file for details.
