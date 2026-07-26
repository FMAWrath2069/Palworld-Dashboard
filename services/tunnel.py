# services/tunnel.py

import platform
import socket
import subprocess
import threading
import time

from services.server_status import set_status


_tunnels = {}
_lock = threading.RLock()


def tunnel_is_alive(tunnel):

    try:
        with socket.create_connection(
            ("127.0.0.1", tunnel["local_port"]),
            timeout=2,
        ):
            return True

    except OSError:
        return False


def _find_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def _ssh_executable():
    return "ssh.exe" if platform.system() == "Windows" else "ssh"


def _process_alive(process):
    return process is not None and process.poll() is None


def _build_command(server, local_port):

    command = [
        _ssh_executable(),
        "-N",
        "-o", "ExitOnForwardFailure=yes",
        "-o", "ServerAliveInterval=30",
        "-o", "ServerAliveCountMax=3",
        "-o", "StrictHostKeyChecking=accept-new",
        "-L",
        (
            f"{local_port}:"
            f"{server.get('remote_host', '127.0.0.1')}:"
            f"{server.get('remote_port', 8212)}"
        ),
        "-p",
        str(server.get("ssh_port", 22)),
    ]

    key = server.get("ssh_key", "").strip()

    if key:
        command.extend(["-i", key])

    command.append(
        f"{server['ssh_user']}@{server['ssh_host']}"
    )

    return command


def start_tunnel(server):

    if not server.get("use_ssh", False):
        return None

    server_id = server["id"]

    set_status(server_id, "connecting")

    with _lock:

        existing = _tunnels.get(server_id)

        if (
            existing
            and _process_alive(existing["process"])
            and tunnel_is_alive(existing)
        ):
            return existing

        if existing:
            stop_tunnel(server_id)

        local_port = _find_free_port()
        command = _build_command(server, local_port)

        creationflags = (
            subprocess.CREATE_NO_WINDOW
            if platform.system() == "Windows"
            else 0
        )

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            text=True,
            creationflags=creationflags,
        )

        for _ in range(20):

            if process.poll() is not None:

                stdout, stderr = process.communicate()

                set_status(server_id, "offline")

                raise RuntimeError(
                    "\n"
                    "SSH tunnel exited immediately.\n\n"
                    f"Exit Code: {process.returncode}\n\n"
                    f"Command:\n{' '.join(command)}\n\n"
                    f"STDOUT:\n{stdout}\n\n"
                    f"STDERR:\n{stderr}"
                )

            try:
                with socket.create_connection(
                    ("127.0.0.1", local_port),
                    timeout=0.25,
                ):
                    break

            except OSError:
                time.sleep(0.25)

        else:

            process.kill()

            stdout, stderr = process.communicate()

            set_status(server_id, "offline")

            raise RuntimeError(
                "\n"
                f"SSH tunnel never opened localhost:{local_port}\n\n"
                f"Command:\n{' '.join(command)}\n\n"
                f"STDOUT:\n{stdout}\n\n"
                f"STDERR:\n{stderr}"
            )

        tunnel = {
            "process": process,
            "local_port": local_port,
        }

        _tunnels[server_id] = tunnel

        set_status(server_id, "online")

        print(
            f"[SSH] Tunnel started for "
            f"{server.get('name', server_id)} "
            f"(localhost:{local_port})"
        )

        return tunnel


def get_tunnel(server):

    if not server.get("use_ssh", False):
        return None

    server_id = server["id"]

    with _lock:
        tunnel = _tunnels.get(server_id)

    if tunnel:

        if not _process_alive(tunnel["process"]):
            stop_tunnel(server_id)
            return start_tunnel(server)

        if not tunnel_is_alive(tunnel):
            print(f"[SSH] Tunnel lost for {server_id}, reconnecting...")
            stop_tunnel(server_id)
            return start_tunnel(server)

        return tunnel

    return start_tunnel(server)


def stop_tunnel(server_id):

    with _lock:
        tunnel = _tunnels.pop(server_id, None)

    if not tunnel:
        return

    process = tunnel["process"]

    if _process_alive(process):

        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

    set_status(server_id, "offline")

    print(f"[SSH] Tunnel stopped for '{server_id}'")


def stop_all_tunnels():

    with _lock:
        server_ids = list(_tunnels.keys())

    for server_id in server_ids:
        stop_tunnel(server_id)


def get_connection(server):

    if not server.get("use_ssh", False):
        return (
            server.get("address", "127.0.0.1"),
            int(server.get("port", 8212)),
        )

    tunnel = get_tunnel(server)

    return (
        "127.0.0.1",
        tunnel["local_port"],
    )