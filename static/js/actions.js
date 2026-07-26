// js/actions.js

Object.assign(window.App, {
    async submitAnnouncement(event) {
        event.preventDefault();

        const message = document.getElementById("announcement-message")?.value ?? "";

        try {
            await ApiService.submitAnnouncement(message);
            event.target.reset();
            ModalService.close("announcement-modal");
        } catch (error) {
            console.error(error);
        }
    },

    async submitShutdown(event) {
        event.preventDefault();

        const waitTime = Number(document.getElementById("shutdown-waittime")?.value ?? 0);
        const message = document.getElementById("shutdown-message")?.value ?? "";

        try {
            await ApiService.shutdown({ waitTime, message });
            ModalService.close("shutdown-modal");
        } catch (error) {
            console.error(error);
        }
    },

    async saveWorld() {
        try {
            await ApiService.saveWorld();
        } catch (error) {
            console.error(error);
        }
    },

    async emergencyStop() {
        if (!window.confirm("Emergency stop the server?")) return;

        try {
            await ApiService.emergencyStop();
        } catch (error) {
            console.error(error);
        }
    }
});