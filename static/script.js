// script.js

const environments = ["Dev", "QA", "Stage", "Prod", "Sandbox"];
const environmentSelect = document.getElementById("environmentSelect");
const connectionTypeSelect = document.getElementById("connectionTypeSelect");
const loadButton = document.getElementById("loadButton");
const downloadCsvButton = document.getElementById("downloadCsv");
const errorBanner = document.getElementById("errorBanner");
const loadingSpinner = document.getElementById("loadingSpinner");
const columnSelector = document.getElementById("columnSelector");
let table = null;

// API response cache
const apiCache = {}; // { "Dev-saml": [data], ... }

// SAML Columns
const columnsSAML = [
  { title: "Name", field: "name" },
  { title: "Entity ID", field: "entityId" },
  { title: "Active", field: "active" },
  { title: "Protocol", field: "spBrowserSso.protocol" },
  { title: "Enabled Profiles", field: "spBrowserSso.enabledProfiles", formatter: "array" },
  { title: "Incoming Bindings", field: "spBrowserSso.incomingBindings", formatter: "array" },
  { title: "SSO Application Endpoint", field: "spBrowserSso.ssoApplicationEndpoint" },
  { title: "Creation Date", field: "creationDate" },
  { title: "Modification Date", field: "modificationDate" },
  { title: "Replication Status", field: "replicationStatus" },
  { title: "Target Type", field: "connectionTargetType" }
];

// OAuth Columns
const columnsOAuth = [
  { title: "Client ID", field: "clientId" },
  { title: "Name", field: "name" },
  { title: "Enabled", field: "enabled" },
  { title: "Grant Types", field: "grantTypes", formatter: "array" },
  { title: "Redirect URIs", field: "redirectUris", formatter: "array" },
  { title: "Allowed Scopes", field: "allowedScopes", formatter: "array" },
  { title: "AD ID", formatter: function(cell) {
      const desc = cell.getRow().getData().description || "";
      const cleanDesc = desc.replace(/\s+/g, ' '); // Normalize all whitespace
      const match = cleanDesc.match(/AD\d+/);
      return match ? match[0] : "";
    }
  },
  { title: "Creation Date", field: "creationDate" },
  { title: "Modification Date", field: "modificationDate" }
];

// Populate environment dropdown
environments.forEach(env => {
  const option = document.createElement("option");
  option.value = env;
  option.textContent = env;
  environmentSelect.appendChild(option);
});

// When connection type changes, rebuild column selector
connectionTypeSelect.addEventListener("change", () => {
  if (connectionTypeSelect.value) {
    populateColumnSelector(connectionTypeSelect.value);
  }
});

// Populate column selector dynamically
function populateColumnSelector(type) {
  columnSelector.innerHTML = '';
  const columns = type === "saml" ? columnsSAML : columnsOAuth;

  columns.forEach((col, idx) => {
    const wrapper = document.createElement("div");
    wrapper.className = "flex items-center";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = true;
    checkbox.value = idx;
    checkbox.className = "mr-2";

    const label = document.createElement("label");
    label.textContent = col.title;

    wrapper.appendChild(checkbox);
    wrapper.appendChild(label);
    columnSelector.appendChild(wrapper);
  });
}

// Show or hide loading spinner
function setLoading(isLoading) {
  loadingSpinner.classList.toggle("hidden", !isLoading);
}

// Show error
function showError(message) {
  errorBanner.textContent = message;
  errorBanner.classList.remove("hidden");
}

// Hide error
function hideError() {
  errorBanner.classList.add("hidden");
}

// Load Button Click Handler
loadButton.addEventListener("click", async () => {
  const environment = environmentSelect.value;
  const type = connectionTypeSelect.value;

  if (!environment || !type) {
    showError("Please select both environment and connection type.");
    return;
  }

  hideError();
  setLoading(true);

  const wrapper = document.getElementById("connectionTableWrapper");
  wrapper.classList.add("opacity-0"); // Prepare fade-in

  try {
    const cacheKey = `${environment}-${type}`;
    let data;

    if (apiCache[cacheKey]) {
      console.log(`Using cached data for ${cacheKey}`);
      data = apiCache[cacheKey];
    } else {
      console.log(`Fetching live data for ${cacheKey}`);
      const response = await fetch(`/api/get-connections?environment=${environment}&type=${type}`);
      data = await response.json();

      if (data.error) {
        showError(`Error: ${data.error}`);
        setLoading(false);
        return;
      }

      apiCache[cacheKey] = data;
    }

    let items = data.items || data;

    if (!Array.isArray(items)) {
      items = [];
    }

    // Get selected columns
    const selectedColumns = [];
    const checkboxes = columnSelector.querySelectorAll("input[type=checkbox]");
    const fullColumns = type === "saml" ? columnsSAML : columnsOAuth;

    checkboxes.forEach(checkbox => {
      if (checkbox.checked) {
        selectedColumns.push(fullColumns[parseInt(checkbox.value)]);
      }
    });

    if (table) {
      table.destroy();
    }

    table = new Tabulator("#connectionTable", {
      data: items,
      layout: "fitColumns",
      columns: selectedColumns,
      pagination: true,
      paginationSize: 10,
      responsiveLayout: true
    });

    wrapper.classList.remove("opacity-0"); // Trigger fade-in

  } catch (error) {
    console.error(error);
    showError("Failed to fetch connections.");
  } finally {
    setLoading(false);
  }
});

// Download CSV
downloadCsvButton.addEventListener("click", () => {
  if (table) {
    table.download("csv", "connections.csv");
  } else {
    showError("No data to export.");
  }
});

// Dark Mode Toggle
const darkModeToggle = document.getElementById("darkModeToggle");
darkModeToggle.addEventListener("change", function() {
  document.documentElement.classList.toggle("dark", darkModeToggle.checked);
});
