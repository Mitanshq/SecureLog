const API_BASE = "/api";
const PAGE_SIZE = 20;

// --------------------
// URL → STATE (on load)
// --------------------
const urlParams = new URLSearchParams(window.location.search);
let currentSource = urlParams.get("source") || "all";
let currentPage = parseInt(urlParams.get("page")) || 1;
let currentLogs = [];

// --------------------
// MODAL ELEMENTS
// --------------------
const logModal = document.getElementById("logModal");
const logModalContent = document.getElementById("logModalContent");
const closeLogModalBtn = document.getElementById("closeLogModal");

// --------------------
// MODAL FUNCTIONS
// --------------------
function openLogModal(log) {
    logModalContent.textContent = log.content;

    const sourceEl = document.getElementById("modalSource");
    const typeEl = document.getElementById("modalType");
    const timeEl = document.getElementById("modalTime");
    const categoryEl = document.getElementById("modalCategory");

    sourceEl.textContent = log.source;
    typeEl.textContent = log.type;
    timeEl.textContent = log.time;
    categoryEl.textContent = log.category;

    // reset + apply source class
    sourceEl.className = "meta-badge " + log.source.toLowerCase();
    categoryEl.className = "meta-badge " + log.category.toLowerCase();

    logModal.classList.remove("hidden");
}


function closeLogModal() {
    logModal.classList.add("hidden");
}

closeLogModalBtn.addEventListener("click", closeLogModal);

logModal.addEventListener("click", (e) => {
    if (e.target === logModal) closeLogModal();
});

// --------------------
// FETCH + RENDER LOGS
// --------------------
async function loadLogHistory(page = 1) {
    const params = new URLSearchParams({
        page,
        page_size: PAGE_SIZE
    });

    if (currentSource !== "all") {
        params.append("source", currentSource);
    }

    const res = await fetch(`/api/dashboard/logs?${params}`);
    const data = await res.json();

    currentLogs = data.logs;

    const tbody = document.getElementById("logs-table");
    tbody.innerHTML = "";

    data.logs.forEach((log, index) => {
        const row = document.createElement("tr");
        row.setAttribute("data-index", index);
        row.innerHTML = `
            <td>${new Date(log.time).toLocaleString()}</td>
            <td>${log.source}</td>
            <td>${log.type}</td>
            <td><span class="meta-badge ${log.category.toLowerCase()}">${log.category}</span></td>
            <td class="log-preview">${log.content}</td>
        `;
        tbody.appendChild(row);
    });

    const totalPages = Math.max(1, Math.ceil(data.total / PAGE_SIZE));
    document.getElementById("pageInfo").innerText =
        `Page ${data.page} of ${totalPages}`;

    document.getElementById("prevPage").disabled = data.page <= 1;
    document.getElementById("nextPage").disabled = data.page >= totalPages;

    currentPage = data.page;
}

// --------------------
// EVENT DELEGATION (ROW CLICK)
// --------------------
const logsTableBody = document.getElementById("logs-table");

logsTableBody.addEventListener("click", (e) => {
    const row = e.target.closest("tr");
    if (!row) return;

    const index = parseInt(row.getAttribute("data-index"));
    if (isNaN(index) || !currentLogs[index]) return;

    openLogModal(currentLogs[index]);
});

// --------------------
// URL UPDATE HELPER
// --------------------
function updateUrl(page, source) {
    const url = new URL(window.location);
    url.searchParams.set("page", page);

    if (source && source !== "all") {
        url.searchParams.set("source", source);
    } else {
        url.searchParams.delete("source");
    }

    window.history.pushState({}, "", url);
}

// --------------------
// FILTER CHANGE
// --------------------
document.getElementById("sourceFilter").addEventListener("change", (e) => {
    currentSource = e.target.value;
    currentPage = 1;

    updateUrl(currentPage, currentSource);
    loadLogHistory(currentPage);
});

// --------------------
// PAGINATION
// --------------------
document.getElementById("prevPage").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        updateUrl(currentPage, currentSource);
        loadLogHistory(currentPage);
    }
});

document.getElementById("nextPage").addEventListener("click", () => {
    currentPage++;
    updateUrl(currentPage, currentSource);
    loadLogHistory(currentPage);
});

// --------------------
// BACK / FORWARD SUPPORT
// --------------------
window.addEventListener("popstate", () => {
    const params = new URLSearchParams(window.location.search);
    currentSource = params.get("source") || "all";
    currentPage = parseInt(params.get("page")) || 1;

    document.getElementById("sourceFilter").value = currentSource;
    loadLogHistory(currentPage);
});

// --------------------
// INITIAL LOAD
// --------------------
document.getElementById("sourceFilter").value = currentSource;
loadLogHistory(currentPage);
