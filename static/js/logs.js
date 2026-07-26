// js/logs.js

Object.assign(window.App, {
    showLog(type) {
        const modalId = `${type}-modal`;
        const list = document.getElementById(`${type}-list`);
        const entries = type === "kicked" ? this.kickedLog : this.bannedLog;

        if (!list) return;

        list.replaceChildren();

        if (!entries.length) {
            list.innerHTML = '<li class="empty-message">No entries found.</li>';
        } else {
            entries.forEach(entry => {
                const row = document.createElement("li");
                row.className = "log-row";

                const details = document.createElement("div");
                details.className = "log-details";

                const action = document.createElement("div");
                action.className = "log-action";
                action.textContent = entry.action || "Banned";

                if (entry.action === "Banned") action.style.color = "red";
                if (entry.action === "Unbanned") action.style.color = "green";

                const name = document.createElement("div");
                name.className = "log-name";
                name.textContent =
                    entry.name ||
                    entry.playerName ||
                    entry.nickname ||
                    "Unknown Player";

                const message = document.createElement("div");
                message.className = "log-message";
                message.textContent = entry.message || "";

                const time = document.createElement("div");
                time.className = "log-time";
                time.textContent = entry.time || entry.timestamp || "";

                details.append(action, name, time, message);

                if (type === "banned" && entry.action !== "Unbanned") {
                    const actions = document.createElement("div");
                    actions.className = "log-actions";

                    const unban = document.createElement("button");
                    unban.className = "unban-button";
                    unban.textContent = "Unban";
                    unban.addEventListener("click", () => this.openUnban(entry));

                    actions.appendChild(unban);
                    row.append(details, actions);
                } else {
                    row.appendChild(details);
                }

                list.appendChild(row);
            });
        }

        ModalService.open(modalId);
    },

    updateLogCounts() {
        this.setText("kicked-log-menu-button", `Kicked Log (${this.kickedLog.length})`);
        this.setText("banned-log-menu-button", `Banned Log (${this.bannedLog.length})`);
    }
});