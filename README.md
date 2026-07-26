# Palworld Dashboard

A web-based administration dashboard for **Palworld Dedicated Servers**.

Palworld Dashboard provides a centralized interface for monitoring and administering one or more Palworld dedicated servers. It supports both local and remote servers through SSH tunneling and provides live information about players, bases, server statistics, and server connectivity status.

**Repository:**

https://github.com/FMAWrath2069/Palworld-Dashboard

---

# Features

* Multi-server management
* Live interactive base map
* Player monitoring
* Real-time server statistics
* Automatic polling
* Independent per-server polling threads
* Dynamic polling lifecycle management
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

# Requirements

* Python 3.11 or newer
* Git
* OpenSSH Client (required for remote server management)
* A Palworld Dedicated Server with the REST API and GAME-DATA API enabled

---

# Clone the Repository

```bash
git clone https://github.com/FMAWrath2069/Palworld-Dashboard.git

cd Palworld-Dashboard
```

---

# Create a Virtual Environment

## Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

## Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# Install Dependencies

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

# Project Structure

```text
## Project Layout

Palworld-Dashboard/

├── app.py                      # Application entry point. Initializes Flask, registers routes,
|                                 and starts background services.
├── config.yaml                 # Global dashboard configuration (API and web server settings).
├── requirements.txt            # Production Python dependencies.
├── requirements-dev.txt        # Development and testing dependencies.

├── core/                       # Core application infrastructure.
│   ├── config.py               # Loads application configuration and defines project paths.
│   ├── state.py                # Maintains thread-safe per-server runtime state.
│   └── storage.py              # Handles loading and saving cached server data.

├── routes/                     # Flask API route definitions.
│   ├── status.py               # Dashboard status and server information endpoints.
│   ├── servers.py              # Server configuration management endpoints.
│   ├── game.py                 # Palworld game administration endpoints.
│   ├── data.py                 # Cached data retrieval endpoints.
│   └── map.py                  # Map and base tracking endpoints.

├── services/                   # Application business logic.
│   ├── api.py                  # Handles communication with the Palworld REST API.
│   ├── polling/                # Per-server polling system.
│   │   ├── worker.py           # Background polling worker threads.
│   │   ├── status.py           # Tracks poller state and statistics.
│   │   └── __init__.py         # Polling service exports.
│   │
│   ├── servers.py              # Server configuration management.
│   ├── server_status.py        # Tracks online/offline/connection status.
│   ├── tunnel.py               # SSH tunnel creation and recovery.
│   ├── parser.py               # Processes and normalizes Palworld API data.
│   └── cache.py                # Handles cached data operations.

├── static/                     # Frontend assets.
│   ├── js/                     # Client-side JavaScript modules.
│   ├── css/                    # Stylesheets.
│   └── images/                 # Frontend image assets.

├── templates/                  # HTML templates used by Flask.

├── data/                       # Runtime server data storage.
│   └── servers/                # Individual data folders for each configured server.
│       ├── default/            # Default server cache.
│       └── server-id/          # Additional configured server caches.

├── map/                        # Map tile assets.
│   # Extract zipped map files directly into this directory.
│   # Do not rename files or folders as map loading depends on expected names.

└── .github/                    # GitHub project configuration.
    ├── workflows/              # GitHub Actions workflows.
    ├── ISSUE_TEMPLATE/         # Issue templates.
    └── pull_request_template.md # Pull request template.
```

---

# Backend Structure

## `core/`

Core application functionality.

Contains:

* Application configuration
* Shared server state management
* Data storage utilities

---

## `routes/`

Flask API endpoints.

Responsible for:

* Receiving HTTP requests
* Validating input
* Returning API responses

Routes delegate processing to services instead of containing business logic.

---

## `services/`

Application business logic.

Includes:

* Palworld REST API communication
* GAME-DATA API communication
* Server configuration management
* SSH tunnel management
* Server status tracking
* Data processing

---

## `services/polling/`

Handles independent server polling.

Each configured server receives its own polling worker.

Polling workers manage:

* Server connectivity checks
* Data refresh scheduling
* API polling
* Error tracking
* Polling status

---

# Frontend Structure

## `static/js/`

Client-side application code.

### Main Files

### `main.js`

Application startup and initialization.

### `api.js`

Handles communication between the frontend and Flask backend.

### `servers.js`

Manages:

* Server selection
* Server configuration
* Active server state

### `serverRenderer.js`

Handles rendering:

* Server lists
* Server selectors
* Status indicators

---

## `static/js/modules/`

Feature-specific dashboard modules.

Examples:

* Dashboard rendering
* Player management
* Server actions
* Logs
* Configuration handling

---

## `static/js/services/`

Frontend utility services.

Examples:

* Browser storage
* Map handling
* Modal management

---

# Configuration

Edit **config.yaml**.

Example:

```yaml
api:
  host: 127.0.0.1
  port: 8212
  password: ""

server:
  host: 0.0.0.0
  port: 5000
```

---

# Running the Dashboard

Start the application:

```bash
python app.py
```

Open your browser and navigate to:

```
http://localhost:5000
```

---

# Adding a Server

Open the **Configuration** window and enter:

* Server Name
* Server Address
* REST API Port
* Administrator Password

---

## Administrator Password

The administrator password should be provided **Base64 encoded**.

> Note: Base64 is an encoding format, not encryption. Do not use it as a replacement for proper password security.

### PowerShell Example

```powershell
$Text = "Hello World"
$Bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
$Base64 = [System.Convert]::ToBase64String($Bytes)
$Base64
```

Output:

```text
SGVsbG8gV29ybGQ=
```

---

# Optional Server Settings

The following settings are optional and can be adjusted based on your server requirements.

All optional settings have defaults that are shown when configuring a server.

---

## Poll Interval

Controls how often the dashboard polls the Palworld server for status updates.

* Lower values provide faster updates.
* Higher values reduce API requests and server load.

---

## Data Refresh Interval

Controls how often the dashboard refreshes stored server data.

* Lower values keep information more current.
* Higher values reduce processing overhead.

---

## Maximum Base Distance

Controls the maximum distance used when tracking Palworld bases.

* Set to `0` to disable Pal tracking for bases.
* Higher values allow tracking of Pals farther away from the Palbox location.

---

# Remote Servers

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

# Server Status

Each configured server reports its current status.

## 🟢 Online

The server is reachable and responding.

## 🟡 Connecting

The dashboard is establishing or restoring an SSH connection.

## 🔴 Offline

The server cannot be reached.

## ⚪ Unknown

The server has not yet been contacted.

---

# Polling Architecture

Each configured server runs its own independent polling thread.

When a server is added:

* A dedicated polling thread is created for that server.
* The thread begins monitoring the server using its configured polling interval.
* Server data is collected and cached independently from all other configured servers.

When a server configuration is updated:

* The existing polling thread is restarted.
* Updated settings such as polling interval, refresh interval, SSH configuration, and server connection details are applied.

When a server is removed:

* The server's polling thread is stopped.
* Any active SSH tunnel associated with that server is closed.
* Server-specific status tracking is removed.
* Cached server data is deleted.

This architecture allows multiple Palworld servers to be monitored simultaneously without one server affecting the polling or availability of another.

Each server maintains its own:

* Polling state
* Connection status
* Error tracking
* Data refresh schedule
* Cached server data
* SSH tunnel connection

---

# Data Storage

Each configured server maintains its own isolated data directory and polling state.

Server data, connection status, polling information, and cached API responses are managed independently for each server.

Example:

```text
data/
└── servers/
    ├── default/
    │   ├── bases.json      # Cached Palworld base/camp information: number of, locations,
    |   |                     player ownership, coordinates, and other base-related tracking data.
    │   ├── players.json    # Cached player information: known players, player IDs, names,
    |   |                     and player activity data. (Not working ATM)
    │   ├── pals.json       # Cached Pal tracking information and related data when base Pal
    |   |                     tracking is enabled.
    │   ├── stats.json      # Cached server statistics and server metrics gathered from the
    |   |                     Palworld API.
    │   └── metadata.json   # Server metadata, internal tracking information, timestamps, update
    |                         information, and other persistent server state data.
    │
    └── server-12345/
        ├── bases.json      # Cached Palworld base/camp information.
        ├── players.json    # Cached player information.
        ├── pals.json       # Cached Pal tracking information.
        ├── stats.json      # Cached server statistics and metrics.
        └── metadata.json   # Persistent server metadata and update tracking.
```

Deleting a server automatically:

* Stops its polling thread
* Closes any active SSH tunnel
* Removes status information
* Deletes all cached data
* Removes the server configuration

---

# Troubleshooting

## 401 Unauthorized

Verify that the administrator password configured in the dashboard matches the administrator password configured on the Palworld server.

---

## SSH Tunnel Fails

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

## No Bases or Players Displayed

Verify that:

* The Palworld REST API is enabled.
* The server is online.
* The configured administrator password is correct.
* The polling interval has elapsed.

---

## Connection Refused

Verify:

* Server IP address
* REST API Port
* Firewall rules
* REST API is enabled

---

# Updating

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

# Contributing

Contributions, bug reports, and feature requests are welcome.

Please use the GitHub Issues page:

https://github.com/FMAWrath2069/Palworld-Dashboard/issues

---

# License

This project is licensed under the AGPL 3.0 License. See the LICENSE file for details.
