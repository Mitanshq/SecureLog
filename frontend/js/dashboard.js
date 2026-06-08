const API_BASE = "/api";
let logsBySourceChart = null;
let logsByRiskChart = null;

const glowOnChangePlugin = {
    id: "glowOnChange",
    beforeUpdate(chart) {
        if (chart.config.type !== "bar") return;
        const dataset = chart.data.datasets[0];
        const meta = chart.getDatasetMeta(0);

        if (!dataset._previousData) {
            dataset._previousData = [...dataset.data];
            return;
        }

        meta._glowInfo = dataset.data.map((val, i) => {
            const prev = dataset._previousData[i] ?? val;
            return {
                direction: val > prev ? "up" : val < prev ? "down" : "same",
                progress: 1
            };
        });

        dataset._previousData = [...dataset.data];
    },

    afterDatasetsDraw(chart) {
        if (chart.config.type !== "bar") return;
        const ctx = chart.ctx;
        const meta = chart.getDatasetMeta(0);
        const glowInfo = meta._glowInfo;
        if (!glowInfo) return;

        meta.data.forEach((bar, i) => {
            const info = glowInfo[i];
            if (!info || info.direction === "same") return;

            ctx.save();
            ctx.globalAlpha = info.progress * 0.35;
            info.progress -= 0.04;
            info.progress = Math.max(info.progress, 0);

            ctx.shadowBlur = 18;
            ctx.shadowColor =
                info.direction === "up"
                    ? "rgba(59,130,246,0.9)"   // blue glow
                    : "rgba(239,68,68,0.9)";  // red glow

            ctx.fillStyle =
                info.direction === "up"
                    ? "rgba(59,130,246,0.25)"
                    : "rgba(239,68,68,0.25)";

            const gradient = ctx.createLinearGradient(
                bar.x - bar.width / 2,
                bar.y,
                bar.x + bar.width / 2,
                bar.base
            );

            gradient.addColorStop(0, "rgba(255,255,255,0.0)");
            gradient.addColorStop(0.5, ctx.shadowColor);
            gradient.addColorStop(1, "rgba(255,255,255,0.0)");

            ctx.fillStyle = gradient;
            ctx.fillRect(
            bar.x - bar.width / 2,
            Math.min(bar.y, bar.base),
            bar.width,
            Math.abs(bar.base - bar.y)
        );

            ctx.restore();
        });
    }
};

Chart.register(glowOnChangePlugin);

async function loadSummary() {
    const res = await fetch(`${API_BASE}/dashboard/summary`);
    const data = await res.json();

    animateNumber(document.getElementById("total-logs"), data.total_logs);
    animateNumber(document.getElementById("alerts-count"), data.alerts);
    animateNumber(document.getElementById("active-pcs"), data.active_agents);

}

let lastAlertTimestamp = null;

async function loadAlerts() {
    try {
        const res = await fetch(`${API_BASE}/dashboard/alerts`);
        const alerts = await res.json();

        const tbody = document.getElementById("alerts-table");

        if (!alerts || alerts.length === 0) return;

        // Alerts are already sorted DESC from backend
        alerts.reverse(); // process oldest → newest

        alerts.forEach(alert => {
            // Skip alerts older than last seen
            if (
                lastAlertTimestamp &&
                new Date(alert.time) <= new Date(lastAlertTimestamp)
            ) {
                return;
            }

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${alert.pc_id}</td>
                <td class="sev-${alert.severity.toLowerCase()}">
                    ${alert.severity.toUpperCase()}
                </td>
                <td>${alert.message}</td>
                <td>${new Date(alert.time).toLocaleString()}</td>
            `;

            tbody.prepend(row);
            lastAlertTimestamp = alert.time;
        });

        // Cap visible rows (no flicker)
        const MAX_ROWS = 20;
        while (tbody.children.length > MAX_ROWS) {
            tbody.removeChild(tbody.lastChild);
        }
    } catch (err) {
        console.error("Alert refresh failed", err);
    }
}

async function register() {
    const res = await fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: document.getElementById("username").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    });

    const data = await res.json();
    console.log(data);
}

async function login() {
    const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    });

    const data = await res.json();
    console.log(data);
}

async function refreshDashboard() {
    await loadSummary();
    await loadAlerts();
    await loadLogsBySource();
    await loadLogsByRisk();
}

async function loadLogsBySource() {
    const res = await fetch(`${API_BASE}/dashboard/logs-by-source`);
    const data = await res.json();

    const labels = Object.keys(data);
    const values = Object.values(data);

    if (!logsBySourceChart) {
        // CREATE ONCE
        logsBySourceChart = new Chart(
            document.getElementById("logsBySourceChart"),
            {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Logs by Source",
                        data: values,
                        backgroundColor: "#3b82f6"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 600,
                        easing: "easeOutQuart"
                    },
                    plugins: {
                        legend: {
                            labels: { color: "#e5e7eb" }
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const value = context.raw;
                                    const dataset = context.dataset;

                                    const prev =
                                        dataset._previousData &&
                                        dataset._previousData[context.dataIndex] !== undefined
                                            ? dataset._previousData[context.dataIndex]
                                            : value;

                                    const diff = value - prev;

                                    if (diff > 0) {
                                        return [`Value: ${value}`, `▲ +${diff} since last update`];
                                    }
                                    if (diff < 0) {
                                        return [`Value: ${value}`, `▼ ${diff} since last update`];
                                    }
                                    return [`Value: ${value}`, `— no change`];
                                }
                            },
                            titleColor: "#f8fafc",
                            bodyColor: "#e5e7eb",
                            backgroundColor: "rgba(2,6,23,0.95)",
                            borderColor: "rgba(148,163,184,0.25)",
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: "#cbd5f5" },
                            grid: { color: "rgba(255,255,255,0.08)" }
                        },
                        y: {
                            ticks: { color: "#cbd5f5" },
                            grid: { color: "rgba(255,255,255,0.08)" }
                        }
                    }
                }
            }
        );
    } else {
        // UPDATE ONLY
        logsBySourceChart.data.labels = labels;
        logsBySourceChart.data.datasets[0].data = values;
        logsBySourceChart.update();
    }
}

async function loadLogsByRisk() {
    const res = await fetch(`${API_BASE}/dashboard/logs-by-risk`);
    const data = await res.json();

    // Sort labels in order: low, useless, high
    const order = ['low', 'useless', 'high'];
    const sortedLabels = order.filter(label => data.hasOwnProperty(label));
    const values = sortedLabels.map(label => data[label]);

    const getColor = (label) => {
        if (label === 'low') return '#22c55e';  // green
        if (label === 'useless') return '#facc15';  // yellow
        if (label === 'high') return '#ef4444';  // red
        return '#gray';
    };

    if (!logsByRiskChart) {
        // CREATE ONCE
        logsByRiskChart = new Chart(
            document.getElementById("logsByRiskChart"),
            {
                type: "pie",
                data: {
                    labels: sortedLabels,
                    datasets: [{
                        data: values,
                        backgroundColor: sortedLabels.map(label => getColor(label))
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: "#e5e7eb"
                            }
                        }
                    },
                    animation: {
                        duration: 600,
                        easing: "easeOutQuart"
                        },
                }
            }
        );
    } else {
        // UPDATE ONLY
        logsByRiskChart.data.labels = sortedLabels;
        logsByRiskChart.data.datasets[0].data = values;
        logsByRiskChart.data.datasets[0].backgroundColor = sortedLabels.map(label => getColor(label));
        logsByRiskChart.update();
    }
}

function animateNumber(element, newValue, duration = 500) {
    const startValue = parseInt(element.innerText) || 0;
    const diff = newValue - startValue;
    if (diff === 0) return;

    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        const progress = Math.min((timestamp - startTime) / duration, 1);
        element.innerText = Math.floor(startValue + diff * progress);

        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}

async function discoverLanPCs() {
    const msg = document.getElementById("discoveryMessage");
    const table = document.getElementById("pcsTable");
    const tbody = document.getElementById("pcsTableBody");
    const btn = document.getElementById("discoverBtn");

    msg.innerText = "Scanning local network...";
    table.style.display = "none";
    tbody.innerHTML = "";
    btn.disabled = true;

    let timeoutHit = false;

    const timeoutId = setTimeout(() => {
        timeoutHit = true;
        msg.innerText =
            "No LAN devices found.";
        btn.disabled = false;
    }, 10000); // ⏱ 10 seconds

    try {
        const res = await fetch("/api/deployment/discover");
        const data = await res.json();

        if (timeoutHit) return;

        clearTimeout(timeoutId);
        btn.disabled = false;

        if (!data.pcs || data.pcs.length === 0) {
            msg.innerText =
                "No LAN devices found. You may be on a hotspot or restricted network.";
            return;
        }

        msg.innerText = `Found ${data.count} device(s) on LAN`;
        table.style.display = "table";

        data.pcs.forEach(pc => {
            const row = document.createElement("tr");

            const installedClass = pc.agent_installed
                ? "badge-yes"
                : "badge-no";

            const statusText = pc.last_seen
                ? "Active"
                : pc.agent_installed
                ? "Offline"
                : "-";

            const statusClass = pc.last_seen
                ? "badge-yes"
                : pc.agent_installed
                ? "badge-offline"
                : "";

            row.innerHTML = `
                <td>${pc.hostname || "Unknown"}</td>
                <td>${pc.ip}</td>
                <td class="${installedClass}">
                    ${pc.agent_installed ? "Yes" : "No"}
                </td>
                <td class="${statusClass}">
                    ${statusText}
                </td>
            `;

            tbody.appendChild(row);
        });
    } catch (err) {
        if (!timeoutHit) {
            clearTimeout(timeoutId);
            msg.innerText = "Failed to discover LAN devices.";
            btn.disabled = false;
        }
    }
}

async function showRegisteredPCs() {
    const table = document.getElementById("registeredPcsTable");
    const body = document.getElementById("registeredPcsBody");
    const btn = document.getElementById("showRegisteredBtn");

    // Toggle behavior
    if (table.style.display === "table") {
        table.style.display = "none";
        btn.innerText = "Show Registered PCs";
        btn.innerHTML = 'Show Registered PCs<span class="arrow">↓</span>';
        return;
    }

    btn.innerText = "Loading...";
    btn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/dashboard/registered-pcs`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        
        const pcs = await res.json();
        body.innerHTML = "";

        pcs.forEach(pc => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${pc.hostname}</td>
                <td>${pc.ip}</td>
                <td>${pc.installed ? "Yes" : "No"}</td>
                <td>${pc.active ? "Online" : "Offline"}</td>
                <td>${pc.last_seen ? new Date(pc.last_seen).toLocaleString() : "-"}</td>
            `;
            body.appendChild(row);
        });

        table.style.display = "table";
        btn.innerText = "Hide Registered PCs";
        btn.innerHTML = 'Hide Registered PCs<span class="arrow">↑</span>';
    } catch (err) {
        alert("Failed to load PCs: " + err.message);
        console.error(err);
    } finally {
        btn.disabled = false;
    }
}



refreshDashboard();
setInterval(refreshDashboard, 5000); // refresh every 5 seconds
document
    .getElementById("discoverBtn")
    .addEventListener("click", discoverLanPCs);

document
  .getElementById("showRegisteredBtn")
  .addEventListener("click", showRegisteredPCs);
