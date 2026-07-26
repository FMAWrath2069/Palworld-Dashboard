import os
import sys
import time
import requests
import concurrent.futures
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_PATH = r"C:\palworld_base_tracker\map"
BASE_URL = "https://cdn.paldb.cc/image/map8"
FORMAT = "webp"

# Seconds to wait before retrying failed downloads
RETRY_DELAY = 5

# Worker threads
MAX_WORKERS = 1

# Logging
DEBUG = True

ZOOM_LEVELS = {
    3: 7,
    4: 15
}

retry_strategy = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Referer": "https://paldb.cc/",
    "Accept": "image/webp,*/*",
}


def log(message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()


def create_directory_structure():
    for z, max_coord in ZOOM_LEVELS.items():
        zoom_path = os.path.join(BASE_PATH, str(z))
        os.makedirs(zoom_path, exist_ok=True)

        for x in range(max_coord + 1):
            os.makedirs(os.path.join(zoom_path, str(x)), exist_ok=True)


def download_tile(z, x, y):
    url = f"{BASE_URL}/z{z}x{x}y{y}.{FORMAT}"
    save_path = os.path.join(BASE_PATH, str(z), str(x), f"{y}.{FORMAT}")

    if os.path.exists(save_path):
        if DEBUG:
            log(f"SKIP: z={z} x={x} y={y}")
        return "exists"

    try:
        if DEBUG:
            log(f"FETCH: {url}")

        response = session.get(
            url,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True,
        )

        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)

            if DEBUG:
                log(f"SAVED: z={z} x={x} y={y}")

            return "success"

        elif response.status_code == 404:
            # Permanent failure
            if DEBUG:
                log(f"MISSING: z={z} x={x} y={y}")
            return "missing"

        elif response.status_code == 403:
            # Treat as TEMPORARY.
            # Do NOT mark missing. Retry forever.
            log(f"TEMP 403: z={z} x={x} y={y}")
            return "retry"

        else:
            log(f"HTTP {response.status_code}: z={z} x={x} y={y}")
            return "retry"

    except requests.exceptions.RequestException as e:
        log(f"NETWORK ERROR: {e} z={z} x={x} y={y}")
        return "retry"

    except Exception as e:
        log(f"EXCEPTION: {type(e).__name__}: {e} z={z} x={x} y={y}")
        return "retry"


def download_all_tiles():
    create_directory_structure()

    tasks = []

    for z, max_coord in ZOOM_LEVELS.items():
        for x in range(max_coord + 1):
            for y in range(max_coord + 1):
                tasks.append((z, x, y))

    total_tiles = len(tasks)

    log(f"Total tiles: {total_tiles}")

    attempt = 1

    while tasks:

        log("=" * 60)
        log(f"PASS #{attempt}")
        log(f"Tiles remaining: {len(tasks)}")
        log("=" * 60)

        retry_tasks = []

        stats = {
            "success": 0,
            "exists": 0,
            "missing": 0,
            "retry": 0,
        }

        completed = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            future_map = {
                executor.submit(download_tile, *task): task
                for task in tasks
            }

            for future in concurrent.futures.as_completed(future_map):

                task = future_map[future]
                completed += 1

                try:
                    result = future.result()
                except Exception:
                    result = "retry"

                stats[result] += 1

                if result == "retry":
                    retry_tasks.append(task)

                if completed % 10 == 0 or completed == len(tasks):
                    log(
                        f"Progress {completed}/{len(tasks)} | "
                        f"Retry Queue: {len(retry_tasks)}"
                    )

        log("")
        log("Pass Summary")
        log(f"Downloaded : {stats['success']}")
        log(f"Existing   : {stats['exists']}")
        log(f"Missing    : {stats['missing']}")
        log(f"Retry      : {stats['retry']}")
        log("")

        if not retry_tasks:
            break

        tasks = retry_tasks
        attempt += 1

        log(f"Sleeping {RETRY_DELAY} seconds before next retry pass...")
        time.sleep(RETRY_DELAY)

    log("=" * 60)
    log("FINISHED")
    log(f"Total tiles: {total_tiles}")
    log("=" * 60)


if __name__ == "__main__":
    log("=" * 60)
    log("Starting Palworld Map Tile Downloader")
    log(f"Destination: {BASE_PATH}")
    log(f"Zoom Levels: {list(ZOOM_LEVELS.keys())}")
    log("=" * 60)

    start = time.time()

    try:
        download_all_tiles()

    except KeyboardInterrupt:
        log("Cancelled by user.")

    except Exception as e:
        log(f"FATAL: {type(e).__name__}: {e}")

    finally:
        elapsed = time.time() - start
        log(f"Elapsed: {elapsed:.2f} seconds")