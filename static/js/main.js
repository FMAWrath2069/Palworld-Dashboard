// js/main.js

window.App = {
    refreshInterval: null,

    baseMarkers: [],
    onlinePlayers: [],
    kickedLog: [],
    bannedLog: [],

    pendingPlayerAction: null,
    pendingUnbanEntry: null,

    async initialize() {
        MapService.initialize();

        await ServerService.load();

        this.bindEvents();

        await this.refresh();

        this.startRefreshTimer();
    },

    startRefreshTimer() {
        this.stopRefreshTimer();

        const interval =
            (this.dataRefreshSeconds ?? 60) * 1000;

        this.refreshInterval = setInterval(
            () => this.refresh(),
            interval
        );
    },

    stopRefreshTimer() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    },

    async startApi() {
        try {
            await ApiService.post("/api/start");
            ModalService.close("api-unavailable-modal");
            await this.refresh();
        } catch (error) {
            console.error(error);
        }
    }
};

document.addEventListener(
    "DOMContentLoaded",
    () => App.initialize()
);