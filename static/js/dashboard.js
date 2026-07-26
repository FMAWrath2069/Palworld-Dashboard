// js/dashboard.js
Object.assign(window.App, {
	async refresh() {
		try {

			ServerService.serverStatuses =
				await ApiService.getServerStatus();

			ServerRenderer.renderConfiguredServers(
				ServerService
			);

			this.renderPayload(
				await ApiService.getStatus()
			);

		} catch (error) {
			console.error(error);
		}
	},

    renderPayload(payload = {}) {
		const refreshSeconds =
			payload.data_refresh_seconds ?? 60;

		if (this.dataRefreshSeconds !== refreshSeconds) {
			this.dataRefreshSeconds = refreshSeconds;
			this.startRefreshTimer();
		}

		const bases = Array.isArray(payload.bases)
			? payload.bases
			: [];

        const players = this.normalizePlayers(
            payload.onlinePlayers ??
            payload.online_players ??
            payload.players ??
            payload
        );

        const stats =
            payload.statistics && typeof payload.statistics === "object"
                ? payload.statistics
                : payload.stats && typeof payload.stats === "object"
                    ? payload.stats
                    : payload;

        const playerCount = this.getPlayerCount(payload, stats, players);

        const basePalCount = this.getValue(
            stats,
            ["basePals", "base_pals", "totalBasePals", "total_base_pals"],
            0
        );

        const wildNpcCount = this.getValue(
            stats,
            ["wildNpcs", "wild_npcs", "totalWildNpcs", "total_wild_npcs"],
            0
        );

        const baseCount = this.getValue(
            stats,
            ["bases", "totalBases", "total_bases"],
            bases.length
        );

        const guildCount = this.getValue(
            stats,
            ["guilds", "totalGuilds", "total_guilds"],
            this.getUniqueGuildCount(bases)
        );

        this.setText("total-base-pals", basePalCount);
        this.setText("total-players", playerCount);
        this.setText("total-wild-npcs", wildNpcCount);
        this.setText("total-bases", baseCount);
        this.setText("total-guilds", guildCount);
        this.setText("last-updated", new Date().toLocaleTimeString());

        this.onlinePlayers = players;
        this.baseMarkers = bases;

        this.kickedLog = Array.isArray(payload.kickedLog ?? payload.kicked_log)
            ? payload.kickedLog ?? payload.kicked_log
            : StorageService.getArray("palworld_kicked_log");

        this.bannedLog = Array.isArray(payload.bannedLog ?? payload.banned_log)
            ? payload.bannedLog ?? payload.banned_log
            : StorageService.getArray("palworld_banned_log");

        MapService.renderBases(this.baseMarkers);
        this.updateLogCounts();
    },

    getValue(source, keys, fallback = 0) {
        if (!source || typeof source !== "object") return fallback;

        for (const key of keys) {
            const value = source[key];

            if (typeof value === "number" && Number.isFinite(value)) return value;

            if (
                typeof value === "string" &&
                value.trim() !== "" &&
                Number.isFinite(Number(value))
            ) {
                return Number(value);
            }
        }

        return fallback;
    },

    getUniqueGuildCount(bases) {
        if (!Array.isArray(bases)) return 0;

        const guildIds = new Set();

        bases.forEach(base => {
            if (!base || typeof base !== "object") return;

            const guildId = base.guildID ?? base.guildId ?? base.guild_id;

            if (
                guildId !== undefined &&
                guildId !== null &&
                String(guildId).trim() !== ""
            ) {
                guildIds.add(String(guildId).trim());
            }
        });

        return guildIds.size;
    },

    getPlayerNickname(player) {
        if (!player || typeof player !== "object") return "Unknown Player";

        return (
            player.NickName ??
            player.nickname ??
            player.name ??
            player.playerName ??
            "Unknown Player"
        );
    },

    getPlayerId(player) {
        if (!player || typeof player !== "object") return null;

        return (
            player.userid ??
            player.user_id ??
            player.UserID ??
            player.userId ??
            player.id ??
            null
        );
    },

    isPlayerObject(value) {
        if (!value || typeof value !== "object") return false;

        const playerId = this.getPlayerId(value);
        const nickname = this.getPlayerNickname(value);

        return (
            (value.Type === "Character" && value.UnitType === "Player") ||
            (playerId !== null && nickname !== "Unknown Player")
        );
    },

    extractPlayers(value, players = [], visited = new WeakSet()) {
        if (value === null || value === undefined) return players;

        if (typeof value === "object") {
            if (visited.has(value)) return players;
            visited.add(value);
        }

        if (this.isPlayerObject(value)) {
            players.push(value);
            return players;
        }

        if (Array.isArray(value)) {
            value.forEach(item => this.extractPlayers(item, players, visited));
            return players;
        }

        if (typeof value === "object") {
            Object.values(value).forEach(item => this.extractPlayers(item, players, visited));
        }

        return players;
    },

    normalizePlayers(value) {
        const players = this.extractPlayers(value);
        const uniquePlayers = new Map();

        players.forEach(player => {
            const playerId = this.getPlayerId(player);

            if (
                playerId !== null &&
                playerId !== undefined &&
                String(playerId).trim() !== ""
            ) {
                const id = String(playerId).trim();

                if (!uniquePlayers.has(id)) {
                    uniquePlayers.set(id, {
                        ...player,
                        name: this.getPlayerNickname(player),
                        nickname: this.getPlayerNickname(player),
                        userid: id
                    });
                }
            }
        });

        return [...uniquePlayers.values()];
    },

    getPlayerCount(payload, stats, players) {
        const possibleCounts = [
            payload.players_count,
            payload.player_count,
            payload.total_players,
            payload.online_player_count,
            payload.totalPlayers,
            stats?.players,
            stats?.player_count,
            stats?.players_count,
            stats?.total_players,
            stats?.online_players,
            stats?.online_player_count,
            stats?.totalPlayers
        ];

        for (const value of possibleCounts) {
            if (typeof value === "number" && Number.isFinite(value)) return value;

            if (
                typeof value === "string" &&
                value.trim() !== "" &&
                Number.isFinite(Number(value))
            ) {
                return Number(value);
            }
        }

        return players.length;
    },

    setText(id, value) {
        const element = document.getElementById(id);
        if (element) element.textContent = String(value ?? 0);
    }
});