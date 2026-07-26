// js/events.js

Object.assign(window.App, {
    bindEvents() {
        document.getElementById("server-menu-button")?.addEventListener("click", event => {
            event.stopPropagation();

            const menu = document.getElementById("server-menu");
            const button = document.getElementById("server-menu-button");

            menu.classList.toggle("visible");
            button.classList.toggle("active");
            button.setAttribute("aria-expanded", menu.classList.contains("visible"));
        });

        document.addEventListener("click", event => {
            const container = document.getElementById("server-menu-container");

            if (container && !container.contains(event.target)) {
                document.getElementById("server-menu")?.classList.remove("visible");
                document.getElementById("server-menu-button")?.classList.remove("active");
            }
        });

        document.getElementById("server-selector")?.addEventListener("change", async event => {
            await ServerService.setActive(event.target.value);
            await this.refresh();
        });

        document.getElementById("total-players")
            ?.addEventListener("click", () => this.showPlayers());

        document.getElementById("total-players")?.addEventListener("keydown", event => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                this.showPlayers();
            }
        });

        document.getElementById("announce-menu-button")
            ?.addEventListener("click", () => ModalService.open("announcement-modal"));

        document.getElementById("shutdown-menu-button")
            ?.addEventListener("click", () => ModalService.open("shutdown-modal"));

        document.getElementById("server-configuration-menu-button")
            ?.addEventListener("click", () => ServerService.openConfigurationModal());

        // SSH configuration
        document.getElementById("config-use-ssh")
            ?.addEventListener(
                "change",
                () => ServerService.updateSshVisibility()
            );

        document.getElementById("kicked-log-menu-button")
            ?.addEventListener("click", () => this.showLog("kicked"));

        document.getElementById("banned-log-menu-button")
            ?.addEventListener("click", () => this.showLog("banned"));

        ModalService.bindCloseButton("close-players", "players-modal");
        ModalService.bindCloseButton("close-kicked", "kicked-modal");
        ModalService.bindCloseButton("close-banned", "banned-modal");
        ModalService.bindCloseButton("close-announcement", "announcement-modal");
        ModalService.bindCloseButton("close-shutdown", "shutdown-modal");
        ModalService.bindCloseButton("close-player-action", "player-action-modal");
        ModalService.bindCloseButton("close-unban", "unban-confirm-modal");
        ModalService.bindCloseButton("close-configuration", "configuration-modal");

        document.querySelectorAll(".modal").forEach(modal => {
            ModalService.bindBackdropClose(modal.id);
        });

        document.querySelectorAll("[id^='cancel-']").forEach(button => {
            button.addEventListener("click", () => {
                const modal = button.closest(".modal");
                if (modal) {
                    ModalService.close(modal.id);
                }
            });
        });

        document.getElementById("announcement-form")
            ?.addEventListener("submit", event => this.submitAnnouncement(event));

        document.getElementById("shutdown-form")
            ?.addEventListener("submit", event => this.submitShutdown(event));

        document.getElementById("player-action-form")
            ?.addEventListener("submit", event => this.submitPlayerAction(event));

        document.getElementById("unban-form")
            ?.addEventListener("submit", event => this.submitUnban(event));

        document.getElementById("configuration-form")
            ?.addEventListener("submit", event => ServerService.saveServer(event));

        document.getElementById("emergency-stop-menu-button")
            ?.addEventListener("click", () => this.emergencyStop());

        document.getElementById("save-world-menu-button")
            ?.addEventListener("click", () => this.saveWorld());

        document.getElementById("configure-from-unavailable")
            ?.addEventListener("click", () => {
                ModalService.close("api-unavailable-modal");
                ServerService.openConfigurationModal();
            });

        document.getElementById("start-api-button")
            ?.addEventListener("click", () => this.startApi());

        document.addEventListener("keydown", event => {
            if (event.key === "Escape") {
                ModalService.closeActive();
            }
        });
    }
});