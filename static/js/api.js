// static/js/api.js

window.ApiService = {
    currentServerId: "default",

    routes: {
        announce: "/api/announce",
        kick: "/api/kick",
        ban: "/api/ban",
        unban: "/api/unban",
        saveWorld: "/api/save-world",
        shutdown: "/api/shutdown",
        emergencyStop: "/api/emergency-stop"
    },

    setServer(serverId) {
        this.currentServerId = serverId;
    },

    async request(path, options = {}) {
        const response = await fetch(path, {
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            },
            ...options
        });

        if (!response.ok) {
            let message = `API request failed: ${response.status}`;

            try {
                const errorBody = await response.json();
                if (errorBody?.error) {
                    message += ` - ${errorBody.error}`;
                }
            } catch {}

            throw new Error(message);
        }

        const contentType = response.headers.get("content-type") || "";
        return contentType.includes("application/json") ? response.json() : response.text();
    },

    send(method, path, body = null) {
		const options = { method };

        if (method === "GET") {
            const separator = path.includes("?") ? "&" : "?";
            path = `${path}${separator}serverId=${encodeURIComponent(this.currentServerId)}`;
        } else if (body !== null) {
            options.body = JSON.stringify({
                serverId: this.currentServerId,
                ...body
            });
        }

        return this.request(path, options);
    },

    gameSend(method, gamePath, body = null) {
        return this.send(
            method,
            `/api/game/${String(gamePath).replace(/^\/+/, "")}`,
            body
        );
    },

    get(path) { return this.send("GET", path); },
    post(path, body = {}) { return this.send("POST", path, body); },
    put(path, body = {}) { return this.send("PUT", path, body); },
    patch(path, body = {}) { return this.send("PATCH", path, body); },
    delete(path, body = {}) { return this.send("DELETE", path, body); },

    getStatus() { return this.get("/api/status"); },
    getBases() { return this.get("/api/bases"); },
    getPlayers() { return this.get("/api/players"); },
    getStats() { return this.get("/api/stats"); },
    getAllData() { return this.get("/api/data"); },
	getServerStatus() { return this.request("/api/server-status"); },

    submitAnnouncement(messageOrPayload) {
        return this.post(
            this.routes.announce,
            typeof messageOrPayload === "string"
                ? { message: messageOrPayload }
                : messageOrPayload || {}
        );
    },

    kickPlayer(payload = {}) { return this.post(this.routes.kick, payload); },
    banPlayer(payload = {}) { return this.post(this.routes.ban, payload); },
    unbanPlayer(payload = {}) { return this.post(this.routes.unban, payload); },
    saveWorld(payload = {}) { return this.post(this.routes.saveWorld, payload); },
    shutdown(payload = {}) { return this.post(this.routes.shutdown, payload); },
    emergencyStop(payload = {}) { return this.post(this.routes.emergencyStop, payload); },

    gameGet(gamePath) { return this.gameSend("GET", gamePath); },
    gamePost(gamePath, body = {}) { return this.gameSend("POST", gamePath, body); },
    gamePut(gamePath, body = {}) { return this.gameSend("PUT", gamePath, body); },
    gamePatch(gamePath, body = {}) { return this.gameSend("PATCH", gamePath, body); },
    gameDelete(gamePath, body = {}) { return this.gameSend("DELETE", gamePath, body); }
};