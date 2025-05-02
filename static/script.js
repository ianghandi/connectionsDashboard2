// script.js

const environments = ["Dev", "QA", "Stage", "Prod", "Sandbox", "PA-DEV", "PA-QA", "PA-PROD"];
const pingAccessEnvironments = ["PA-DEV", "PA-QA", "PA-PROD"];

const environmentSelect = document.getElementById("environmentSelect");
const connectionTypeSelect = document.getElementById("connectionTypeSelect");
const loadButton = document.getElementById("loadButton");
const downloadCsvButton = document.getElementById("downloadCsv");
const errorBanner = document.getElementById("errorBanner");
const loadingSpinner = document.getElementById("loadingSpinner");
const columnSelector = document.getElementById("columnSelector");
const globalSearchInput = document.getElementById("globalSearchInput");

let table = null;
const apiCache = {}; // frontend cache

// Signing Key Owner Mapping
const signingKeyOwnerMap = {
  "g0t7grow21iko1fhef8g8u810": "Alice",
  "tmmc2ofka2v145u74vol50hf1": "Bob",
  "0o42t0uup6apkv069v3ia7mga": "Charlie"
};

// Column Definitions
const columnsSAML = [
  { title: "Name", field: "name", resizable: true, widthGrow: 1 },
  { title: "Entity ID", field: "entityId", resizable: true, widthGrow: 1 },
  { title: "Active", field: "active", resizable: true, widthGrow: 1 },
  { title: "Protocol", field: "spBrowserSso.protocol", resizable: true, widthGrow: 1 },
  { title: "Enabled Profiles", field: "spBrowserSso.enabledProfiles", formatter: "array", resizable: true, widthGrow: 1 },
  { title: "Incoming Bindings", field: "spBrowserSso.incomingBindings", formatter: "array", resizable: true, widthGrow: 1 },
  { title: "SSO Application Endpoint", field: "spBrowserSso.ssoApplicationEndpoint", resizable: true, widthGrow: 1 },
  { title: "Signing Key Owner", formatter: function(cell) {
      const signingKeyId = cell.getRow().getData()?.credentials?.signingSettings?.signingKeyPairRef?.id || "";
      return signingKeyOwnerMap[signingKeyId] || signingKeyId || "Unknown";
    },
    resizable: true, widthGrow: 1 
  },
    {
    title: "Extended Properties",
    formatter: function(cell) {
      const props = cell.getRow().getData()?.extendedProperties || {};
      return Object.entries(props)
        .map(([key, val]) => `${key}:${val.values?.[0] || ""}`)
        .join("\n");
    },
    resizable: true, widthGrow: 1 
  },
  { title: "Modification Date", field: "modificationDate", resizable: true, widthGrow: 1 },
  { title: "Replication Status", field: "replicationStatus", resizable: true, widthGrow: 1 },
  { title: "Target Type", field: "connectionTargetType", resizable: true, widthGrow: 1 }
];

const columnsOAuth = [
  { title: "Client ID", field: "clientId", resizable: true, widthGrow: 1 },
  { title: "Name", field: "name", resizable: true, widthGrow: 1 },
  { title: "Enabled", field: "enabled", resizable: true, widthGrow: 1 },
  { title: "Grant Types", field: "grantTypes", formatter: "array", resizable: true, widthGrow: 1 },
  { title: "Redirect URIs", field: "redirectUris", formatter: "array", resizable: true, widthGrow: 1 },
  { title: "Allowed Scopes", field: "allowedScopes", formatter: "array", resizable: true, widthGrow: 1 },
  { title: "AD ID", formatter: function(cell) {
      const desc = cell.getRow().getData().description || "";
      const cleanDesc = desc.replace(/\s+/g, ' ');
      const match = cleanDesc.match(/AD\d+/);
      return match ? match[0] : "";
    },
    resizable: true, widthGrow: 1 
  },
  { title: "Creation Date", field: "creationDate", resizable: true, widthGrow: 1 },
  { title: "Modification Date", field: "modificationDate", resizable: true, widthGrow: 1 }
];

// Make sure table respects column resizing and dragging
const tableOptions = {
  layout: "fitDataStretch",
  movableColumns: true,
  resizableColumns: true,
  responsiveLayout: true,
  pagination: false,
  scrollVertical: true
};

// Function to initialize table with selected columns and data
function initializeTable(data, columns) {
  if (table) {
    table.destroy();
  }
  table = new Tabulator("#connectionTable", {
    ...tableOptions,
    data: data,
    columns: columns
  });
}

const columnsPingAccess = [
  { title: "App Name", field: "appName", resizable: true, widthGrow: 1 },
  { title: "Target", field: "target", resizable: true, widthGrow: 1 },
  { title: "Virtual Host", field: "host", resizable: true, widthGrow: 1 },
  { title: "Active", field: "active", resizable: true, widthGrow: 1 }
];

// Populate environment dropdown
environments.forEach(env => {
  const option = document.createElement("option");
  option.value = env;
  option.textContent = env;
  environmentSelect.appendChild(option);
});

// Dynamic Connection Type filtering based on environment
environmentSelect.addEventListener("change", function() {
  const selectedEnv = environmentSelect.value;
  const typeDropdown = connectionTypeSelect;

  // Clear current connection type options
  typeDropdown.innerHTML = "";

  // Add default "-- Choose Type --" option
  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = "-- Choose Type --";
  typeDropdown.appendChild(defaultOption);

  if (pingAccessEnvironments.includes(selectedEnv)) {
    // PingAccess environment: Only show PingAccess
    const option = document.createElement("option");
    option.value = "pingaccess";
    option.textContent = "PingAccess";
    typeDropdown.appendChild(option);
  } else if (selectedEnv) {
    // PingFederate environment: Show SAML and OAuth
    const samlOption = document.createElement("option");
    samlOption.value = "saml";
    samlOption.textContent = "SAML";
    typeDropdown.appendChild(samlOption);

    const oauthOption = document.createElement("option");
    oauthOption.value = "oauth";
    oauthOption.textContent = "OAuth";
    typeDropdown.appendChild(oauthOption);
  }
});

// Rebuild column selector when connection type changes
connectionTypeSelect.addEventListener("change", () => {
  if (connectionTypeSelect.value) {
    populateColumnSelector(connectionTypeSelect.value);
  }
});

// Column Selector
function populateColumnSelector(type) {
  columnSelector.innerHTML = '';
  let columns = [];
  if (type === "saml") columns = columnsSAML;
  else if (type === "oauth") columns = columnsOAuth;
  else if (type === "pingaccess") columns = columnsPingAccess;

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

function setLoading(isLoading) {
  loadingSpinner.classList.toggle("hidden", !isLoading);
}

function showError(message) {
  errorBanner.textContent = message;
  errorBanner.classList.remove("hidden");
}

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
  wrapper.classList.add("opacity-0");

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

    const selectedColumns = [];
    const checkboxes = columnSelector.querySelectorAll("input[type=checkbox]");
    let fullColumns = [];

    if (type === "saml") fullColumns = columnsSAML;
    else if (type === "oauth") fullColumns = columnsOAuth;
    else if (type === "pingaccess") fullColumns = columnsPingAccess;

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
      pagination: false,
      scrollVertical: true,
      responsiveLayout: true
    });

    wrapper.classList.remove("opacity-0");

  } catch (error) {
    console.error(error);
    showError("Failed to fetch connections.");
  } finally {
    setLoading(false);
  }
});

downloadCsvButton.addEventListener("click", () => {
  if (table) {
    table.download("csv", "connections.csv");
  } else {
    showError("No data to export.");
  }
});

// Global Search
globalSearchInput.addEventListener("input", function() {
  const searchTerm = this.value.toLowerCase();

  if (table) {
    table.setFilter(function(data, filterParams) {
      return Object.values(data).some(value =>
        String(value).toLowerCase().includes(searchTerm)
      );
    });
  }
});

// Dark Mode
const darkModeToggle = document.getElementById("darkModeToggle");
darkModeToggle.addEventListener("change", function() {
  document.documentElement.classList.toggle("dark", darkModeToggle.checked);
});

// Fetch user email and set it
fetch('/api/userinfo')
  .then(res => res.json())
  .then(data => {
    document.getElementById("userEmail").textContent = data.email || "Unknown User";
  });

// Toggle dropdown
const userMenuButton = document.getElementById("userMenuButton");
const userDropdown = document.getElementById("userDropdown");

userMenuButton.addEventListener("click", () => {
  userDropdown.classList.toggle("hidden");
});