// js/serverRenderer.js

window.ServerRenderer = {

    statusIcon(status) {

        switch ((status ?? "").toLowerCase()) {

            case "online":
                return "🟢";

            case "connecting":
                return "🟡";

            case "offline":
            case "error":
                return "🔴";

            default:
                return "⚪";
        }
    },

    renderSelector(servers, activeServerId, statuses = null) {

        statuses ??= window.ServerService?.serverStatuses ?? {};

        const selector =
            document.getElementById(
                "server-selector"
            );

        if (!selector) {
            return;
        }

        selector.replaceChildren();

        servers.forEach(server => {

            const option =
                document.createElement(
                    "option"
                );

            option.value = server.id;

            const status =
                statuses[server.id]?.status;

            option.textContent =
                `${this.statusIcon(status)} ${server.name} (${server.address}:${server.port})`;

            selector.appendChild(option);

        });

        selector.value = activeServerId;

    },

    renderConfiguredServers(service, statuses = null) {

        statuses ??= service.serverStatuses ?? {};

        const container =
            document.getElementById(
                "configured-servers"
            );

        if (!container) {
            return;
        }

        container.replaceChildren();

        service.servers.forEach(server => {

            const card =
                document.createElement("div");

            card.className =
                "server-card";

            const header =
                document.createElement("div");

            header.className =
                "server-card-header";

            const title =
                document.createElement("h4");

            title.className =
                "server-card-title";

            const status =
                statuses[server.id]?.status;

            title.textContent =
                `${this.statusIcon(status)} ${server.name}`;

            const details =
                document.createElement("div");

            details.className =
                "server-card-details";

            details.textContent =
                `${server.address}:${server.port}`;

            const actions =
                document.createElement("div");

            actions.className =
                "server-card-actions";

            const activate =
                document.createElement("button");

            activate.type = "button";
            activate.className =
                "success-button";

            activate.textContent =
                server.id === service.activeServerId
                    ? "Active"
                    : "Use Server";

            activate.disabled =
                server.id === service.activeServerId;

            activate.addEventListener(
                "click",
                () => service.setActive(server.id)
            );

            const edit =
                document.createElement("button");

            edit.type = "button";
            edit.className =
                "primary-button";

            edit.textContent = "Edit";

            edit.addEventListener(
                "click",
                () => service.fillConfigurationForm(server)
            );

            const del =
                document.createElement("button");

            del.type = "button";
            del.className =
                "danger-button";

            del.textContent = "Delete";

            del.disabled =
                service.servers.length <= 1;

            del.addEventListener(
                "click",
                () => service.deleteServer(server.id)
            );

            header.append(
                title,
                activate
            );

            actions.append(
                edit,
                del
            );

            card.append(
                header,
                details,
                actions
            );

            container.appendChild(card);

        });

    }

};