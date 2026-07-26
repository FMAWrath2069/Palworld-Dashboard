// static/js/map.js
 
window.MapService = {
    map: null,
    markers: [],
 
    tileSize: 512,
    mapSize: 4096,
    tileZoom: 0,
 
    gameMinX: -1920,
    gameMaxX: 1235,
    gameMinY: -2125,
    gameMaxY: 1030,
 
    emptyTileUrl: "/static/images/empty-tile.webp",
 
    xControlPoints: [
        { game: -644.9, leaflet: 1654 },
        { game: 84.62, leaflet: 2590 },
        { game: 105.82, leaflet: 2633 },
        { game: 188.43, leaflet: 2738 }
    ],
 
    yControlPoints: [
        { game: -430.16, leaflet: 2273 },
        { game: -330.13, leaflet: 2333 },
        { game: -37.82, leaflet: 2708 },
        { game: 269.53, leaflet: 3113 }
    ],
 
    initialize() {
        const PixelCRS = L.extend({}, L.CRS.Simple, {
            transformation: new L.Transformation(
                1,
                0,
                -1,
                this.mapSize
            ),
            scale: zoom => Math.pow(2, zoom)
        });
 
        this.map = L.map("map", {
            crs: PixelCRS,
            minZoom: -2,
            maxZoom: 1,
            zoom: this.tileZoom,
            zoomControl: true,
            noWrap: true
        });
 
        L.tileLayer(
            "/map/{z}/{x}/{y}.webp",
            {
                tileSize: this.tileSize,
                minZoom: -2,
                maxZoom: 1,
                noWrap: true,
                bounds: [
                    [0, 0],
                    [this.mapSize, this.mapSize]
                ],
                errorTileUrl: this.emptyTileUrl
            }
        ).addTo(this.map);
 
        const tileMapBounds = L.latLngBounds(
            [0, 0],
            [this.mapSize, this.mapSize]
        );
 
        this.map.fitBounds(tileMapBounds);
    },
 
    linearInterpolate(value, point1, point2) {
        return point1.leaflet +
            (value - point1.game) *
            (point2.leaflet - point1.leaflet) /
            (point2.game - point1.game);
    },
 
    interpolate(value, points) {
        const sortedPoints = [...points].sort(
            (point1, point2) => point1.game - point2.game
        );
 
        if (value <= sortedPoints[0].game) {
            return this.linearInterpolate(
                value,
                sortedPoints[0],
                sortedPoints[1]
            );
        }
 
        if (
            value >= sortedPoints[sortedPoints.length - 1].game
        ) {
            return this.linearInterpolate(
                value,
                sortedPoints[sortedPoints.length - 2],
                sortedPoints[sortedPoints.length - 1]
            );
        }
 
        for (
            let index = 0;
            index < sortedPoints.length - 1;
            index++
        ) {
            const point1 = sortedPoints[index];
            const point2 = sortedPoints[index + 1];
 
            if (
                value >= point1.game &&
                value <= point2.game
            ) {
                return this.linearInterpolate(
                    value,
                    point1,
                    point2
                );
            }
        }
 
        throw new Error(
            `Unable to interpolate value: ${value}`
        );
    },
 
    gameToLeaflet(gameX, gameY) {
        const leafletX = this.interpolate(
            Number(gameX),
            this.xControlPoints
        );
 
        const leafletY = this.interpolate(
            Number(gameY),
            this.yControlPoints
        );
 
        return [leafletY, leafletX];
    },
 
    escapeHtml(value) {
        const element = document.createElement("div");
        element.textContent = value ?? "";
        return element.innerHTML;
    },
 
createPalHtml(pals) {
    let palHtml = '<div class="pal-list-container"><ul class="pal-list">';
 
    if (!pals || pals.length === 0) {
        palHtml += "<li>No working Pals</li>";
    } else {
        pals.forEach(pal => {
            palHtml += `
                <li>
                    <b>${this.escapeHtml(pal.nickname)}</b>
                    Lv.${this.escapeHtml(pal.level)},
                    HP ${this.escapeHtml(pal.hp)}/${this.escapeHtml(pal.max_hp)}
                    <br>
                    <i>${this.escapeHtml(pal.class)}</i>
                </li>
            `;
        });
    }
 
    palHtml += "</ul></div>";
    return palHtml;
},
 
    createBaseMarker(base) {
        if (!this.map || !base) {
            return null;
        }
 
        const gameX = Number(base.map_x);
        const gameY = Number(base.map_y);
 
        if (
            !Number.isFinite(gameX) ||
            !Number.isFinite(gameY)
        ) {
            return null;
        }
 
        const leafletPoint = this.gameToLeaflet(
            gameX,
            gameY
        );
 
        const marker = L.marker(leafletPoint).addTo(this.map);
 
        const baseNumber =
            base.display_number ??
            `${base.base_number} / ${base.total_bases}`;
 
        const guildName = this.escapeHtml(
            base.guild_name ?? "Unknown"
        );
 
        const palCount = base.pal_count ?? 0;
 
        marker.bindTooltip(
            `<b>${guildName}</b><br>` +
            `Base ${this.escapeHtml(baseNumber)}<br>` +
            `Pals: ${this.escapeHtml(palCount)}<br>` +
            "Base Coordinates: " +
            `${this.escapeHtml(gameX)}x, ` +
            `${this.escapeHtml(gameY)}y`
        );
 
        marker.bindPopup(`
            <h3>${guildName}</h3>
            <p>
                <b>Base:</b>
                ${this.escapeHtml(baseNumber)}
            </p>
            <p>
                <b>Working Pals:</b>
                ${this.escapeHtml(palCount)}
            </p>
            <div>
                ${this.createPalHtml(base.pals)}
            </div>
        `);
 
        this.markers.push(marker);
 
        return marker;
    },
 
    clearMarkers() {
        this.markers.forEach(marker => {
            this.map.removeLayer(marker);
        });
 
        this.markers = [];
    },
 
    clearBaseMarkers() {
        this.clearMarkers();
    },
 
    renderBases(bases = []) {
        this.clearMarkers();
 
        bases.forEach(base => {
            this.createBaseMarker(base);
        });
    }
};