// js/players.js
Object.assign(window.App, {
    showPlayers() {
        this.renderPlayers();
        ModalService.open("players-modal");
    },

    renderPlayers() {
        const list = document.getElementById("players-list");
        if (!list) return;

        list.replaceChildren();

        if (!this.onlinePlayers.length) {
            list.innerHTML = '<li class="empty-message">No players online.</li>';
            return;
        }

        this.onlinePlayers.forEach(player => {
            const row = document.createElement("li");
            row.className = "player-row";

            const name = document.createElement("span");
            name.className = "player-name";
            name.textContent = this.getPlayerNickname(player);

            const actions = document.createElement("div");
            actions.className = "player-actions";

            const kick = document.createElement("button");
            kick.className = "kick-button";
            kick.textContent = "Kick";
            kick.addEventListener("click", () => this.openPlayerAction(player, "kick"));

            const ban = document.createElement("button");
            ban.className = "ban-button";
            ban.textContent = "Ban";
            ban.addEventListener("click", () => this.openPlayerAction(player, "ban"));

            actions.append(kick, ban);
            row.append(name, actions);
            list.appendChild(row);
        });
    },

    createLogEntry(action, player, message = "") {
        return {
            action,
            userid: this.getPlayerId(player),
            name: this.getPlayerNickname(player),
            message,
            time: new Date().toLocaleString()
        };
    },

    openPlayerAction(player, action) {
        this.pendingPlayerAction = { player, action };

        const description = document.getElementById("player-action-description");
        if (description) {
            description.textContent =
                `Are you sure you want to ${action} ${this.getPlayerNickname(player)}?`;
        }

        const confirmButton = document.getElementById("confirm-player-action");
        if (confirmButton) {
            confirmButton.className = `form-button ${
                action === "ban" ? "danger-button" : "warning-button"
            }`;
        }

        ModalService.open("player-action-modal");
    },

    openUnban(entry) {
        this.pendingUnbanEntry = entry;

        const description = document.getElementById("unban-confirm-description");
        if (description) {
            description.textContent =
                `Are you sure you want to unban ${this.getPlayerNickname(entry)}?`;
        }

        const messageElement = document.getElementById("unban-message");
        if (messageElement) {
            messageElement.value = "";
        }

        ModalService.open("unban-confirm-modal");
    },

    async submitPlayerAction(event) {
        event.preventDefault();

        if (!this.pendingPlayerAction) return;

        const { player, action } = this.pendingPlayerAction;
        const message = document.getElementById("player-action-message")?.value ?? "";

        try {
            if (action === "kick") {
                await ApiService.kickPlayer({
                    userid: this.getPlayerId(player),
                    message
                });
            } else {
                await ApiService.banPlayer({
                    userid: this.getPlayerId(player),
                    message
                });
            }

            ModalService.close("player-action-modal");
            await this.refresh();

            const logEntry = this.createLogEntry(
                action === "ban" ? "Banned" : "Kicked",
                player,
                message
            );

            if (action === "kick") {
                this.kickedLog.unshift(logEntry);
                StorageService.saveObject("palworld_kicked_log",this.kickedLog);
            } else {
                this.bannedLog.unshift(logEntry);
                StorageService.saveObject("palworld_banned_log",this.bannedLog);
            }

            this.updateLogCounts();
            this.pendingPlayerAction = null;
        } catch (error) {
            console.error(error);
        }
    },

    async submitUnban(event) {
        event.preventDefault();

        if (!this.pendingUnbanEntry) return;

        const userid = this.getPlayerId(this.pendingUnbanEntry);
        const message = document.getElementById("unban-message")?.value ?? "";

        try {
            await ApiService.unbanPlayer({ userid });

            ModalService.close("unban-confirm-modal");
            await this.refresh();

            this.bannedLog.unshift(
                this.createLogEntry("Unbanned",this.pendingUnbanEntry,message)
            );

            StorageService.saveObject("palworld_banned_log",this.bannedLog);

            this.updateLogCounts();
            this.pendingUnbanEntry = null;
        } catch (error) {
            console.error(error);
        }
    }
});