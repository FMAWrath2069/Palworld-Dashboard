// js/serverStorage.js

window.ServerStorage = {

    defaultServer: {
        id: "default",
        name: "Default Server",
        address: "127.0.0.1",
        port: 8212,
        password: "",

        poll_interval_seconds: 30,
        data_refresh_seconds: 60,
        max_pal_base_distance: "",

        use_ssh: false,
        ssh_host: "",
        ssh_port: 22,
        ssh_user: "",
        ssh_key: "",

        remote_host: "127.0.0.1",
        remote_port: 8212,

        apiUrl: ""
    },

    normalize(server, index) {

        const value =
            server && typeof server === "object"
                ? server
                : {};

        return {

            id: String(
                value.id ??
                `server-${index + 1}`
            ),

            name: String(
                value.name ??
                `Server ${index + 1}`
            ),

            address: String(
                value.address ??
                "127.0.0.1"
            ),

            port: Number(
                value.port ??
                8212
            ),

            password: String(
                value.password ??
                ""
            ),

            poll_interval_seconds: Number(
                value.poll_interval_seconds ?? 30
            ),

            data_refresh_seconds: Number(
                value.data_refresh_seconds ?? 60
            ),

            max_pal_base_distance:
                value.max_pal_base_distance ?? "",

            use_ssh: Boolean(
                value.use_ssh
            ),

            ssh_host: String(
                value.ssh_host ?? ""
            ),

            ssh_port: Number(
                value.ssh_port ?? 22
            ),

            ssh_user: String(
                value.ssh_user ?? ""
            ),

            ssh_key: String(
                value.ssh_key ?? ""
            ),

            remote_host: String(
                value.remote_host ??
                "127.0.0.1"
            ),

            remote_port: Number(
                value.remote_port ?? 8212
            ),

            apiUrl: String(
                value.apiUrl ??
                value.api_url ??
                ""
            )

        };

    },

    async load() {

        try {

            const response =
                await fetch("/api/servers");

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}`
                );
            }

            const servers =
                await response.json();

            const normalized =
                Array.isArray(servers)
                    ? servers.map(
                        (server, index) =>
                            this.normalize(
                                server,
                                index
                            )
                    )
                    : [];

            return normalized.length
                ? normalized
                : [
                    this.normalize(
                        this.defaultServer,
                        0
                    )
                ];

        } catch (error) {

            console.error(
                "Failed to load servers:",
                error
            );

            return [
                this.normalize(
                    this.defaultServer,
                    0
                )
            ];

        }

    },

    saveActive(serverId) {

        StorageService.saveValue(
            "palworld_active_server",
            serverId
        );

    },

    loadActive(servers) {

        const stored =
            StorageService.getValue(
                "palworld_active_server"
            );

        if (
            servers.some(
                s => s.id === stored
            )
        ) {
            return stored;
        }

        return servers.length
            ? servers[0].id
            : this.defaultServer.id;

    }

};