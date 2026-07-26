// js/servers.js

window.ServerService = {
    servers: [],
    activeServerId: null,

    async load() {

        this.servers =
            await ServerStorage.load();

        this.activeServerId =
            ServerStorage.loadActive(
                this.servers
            );

        ApiService.setServer(
            this.activeServerId
        );

        ServerStorage.saveActive(
            this.activeServerId
        );

        ServerRenderer.renderSelector(
            this.servers,
            this.activeServerId
        );

        ServerRenderer.renderConfiguredServers(
            this
        );
    },

    async refresh() {
        await this.load();
    },

    async save() {
        ServerStorage.saveActive(
            this.activeServerId
        );
    },

    async setActive(serverId) {

        if (
            !this.servers.some(
                server => server.id === serverId
            )
        ) {
            return;
        }

        this.activeServerId = serverId;

        ApiService.setServer(serverId);

        await this.save();

        ServerRenderer.renderSelector(
            this.servers,
            this.activeServerId
        );

        ServerRenderer.renderConfiguredServers(
            this
        );

        if (window.App?.refresh) {
            await window.App.refresh();
        }
    },

    getActive() {
        return (
            this.servers.find(
                server =>
                    server.id ===
                    this.activeServerId
            ) ||
            this.servers[0] ||
            ServerStorage.defaultServer
        );
    },

    openConfigurationModal() {

        ServerRenderer.renderSelector(
            this.servers,
            this.activeServerId
        );

        ServerRenderer.renderConfiguredServers(
            this
        );

        this.clearConfigurationForm();

        ModalService.open(
            "configuration-modal"
        );
    },

    clearConfigurationForm() {

        const form =
            document.getElementById(
                "configuration-form"
            );

        if (form) {
            form.dataset.editingId = "";
        }

        Object.entries(
            ServerStorage.defaultServer
        ).forEach(([key, value]) => {

            const element =
                document.getElementById(
                    `config-${key.replaceAll("_", "-")}`
                );

            if (!element) {
                return;
            }

            if (element.type === "checkbox") {
                element.checked = Boolean(value);
            } else {
                element.value = value ?? "";
            }
        });

        this.updateSshVisibility();
    },

    updateSshVisibility() {

        const enabled =
            document.getElementById(
                "config-use-ssh"
            )?.checked;

        const section =
            document.getElementById(
                "ssh-options"
            );

        if (section) {
            section.style.display =
                enabled ? "" : "none";
        }
    },

    setInputValue(id, value) {

        const element =
            document.getElementById(id);

        if (!element) {
            return;
        }

        if (element.type === "checkbox") {
            element.checked = Boolean(value);
        } else {
            element.value = value ?? "";
        }
    },

    fillConfigurationForm(server) {

        const form =
            document.getElementById(
                "configuration-form"
            );

        if (form) {
            form.dataset.editingId =
                server.id;
        }

        this.setInputValue(
            "config-server-name",
            server.name
        );

        this.setInputValue(
            "config-server-address",
            server.address
        );

        this.setInputValue(
            "config-server-port",
            server.port
        );

        this.setInputValue(
            "config-server-password",
            ""
        );

        this.setInputValue(
            "config-poll-interval",
            server.poll_interval_seconds
        );

        this.setInputValue(
            "config-refresh-interval",
            server.data_refresh_seconds
        );

        this.setInputValue(
            "config-max-distance",
            server.max_pal_base_distance
        );

        this.setInputValue(
            "config-use-ssh",
            server.use_ssh
        );

        this.setInputValue(
            "config-ssh-host",
            server.ssh_host
        );

        this.setInputValue(
            "config-ssh-port",
            server.ssh_port
        );

        this.setInputValue(
            "config-ssh-user",
            server.ssh_user
        );

        this.setInputValue(
            "config-ssh-key",
            server.ssh_key
        );

        this.setInputValue(
            "config-remote-host",
            server.remote_host
        );

        this.setInputValue(
            "config-remote-port",
            server.remote_port
        );

        this.updateSshVisibility();

        ModalService.open(
            "configuration-modal"
        );
    },

    async saveServer(event) {

        event.preventDefault();

        const form = event.target;

        const editingId =
            form.dataset.editingId;

        const server = {

            id:
                editingId ||
                `server-${Date.now()}`,

            name:
                document
                    .getElementById(
                        "config-server-name"
                    )
                    .value.trim(),

            address:
                document
                    .getElementById(
                        "config-server-address"
                    )
                    .value.trim(),

            port: Number(
                document
                    .getElementById(
                        "config-server-port"
                    )
                    .value
            ),

            password:
                document
                    .getElementById(
                        "config-server-password"
                    )
                    .value.trim(),

            poll_interval_seconds: Number(
                document
                    .getElementById(
                        "config-poll-interval"
                    )
                    .value
            ),

            data_refresh_seconds: Number(
                document
                    .getElementById(
                        "config-refresh-interval"
                    )
                    .value
            ),

            max_pal_base_distance:
                document
                    .getElementById(
                        "config-max-distance"
                    )
                    .value,

            use_ssh:
                document
                    .getElementById(
                        "config-use-ssh"
                    )
                    .checked,

            ssh_host:
                document
                    .getElementById(
                        "config-ssh-host"
                    )
                    .value.trim(),

            ssh_port: Number(
                document
                    .getElementById(
                        "config-ssh-port"
                    )
                    .value
            ),

            ssh_user:
                document
                    .getElementById(
                        "config-ssh-user"
                    )
                    .value.trim(),

            ssh_key:
                document
                    .getElementById(
                        "config-ssh-key"
                    )
                    .value.trim(),

            remote_host:
                document
                    .getElementById(
                        "config-remote-host"
                    )
                    .value.trim(),

            remote_port: Number(
                document
                    .getElementById(
                        "config-remote-port"
                    )
                    .value
            )
        };

        try {

            if (editingId) {

                await ApiService.put(
                    `/api/servers/${editingId}`,
                    server
                );

            } else {

                await ApiService.post(
                    "/api/servers",
                    server
                );

            }

            await this.refresh();

            if (!this.activeServerId) {
                await this.setActive(
                    server.id
                );
            }

            ModalService.close(
                "configuration-modal"
            );

            if (window.App?.refresh) {
                await window.App.refresh();
            }

        } catch (error) {

            console.error(error);

            alert(
                "Failed to save server configuration."
            );
        }
    },

    async deleteServer(id) {

        if (this.servers.length <= 1) {
            return;
        }

        if (
            !window.confirm(
                "Delete this server configuration?"
            )
        ) {
            return;
        }

        try {

            await ApiService.delete(
                `/api/servers/${id}`
            );

            await this.refresh();

            if (
                this.activeServerId === id &&
                this.servers.length
            ) {
                await this.setActive(
                    this.servers[0].id
                );
            }

            if (window.App?.refresh) {
                await window.App.refresh();
            }

        } catch (error) {

            console.error(error);

            alert(
                "Failed to delete server."
            );
        }
    }
};