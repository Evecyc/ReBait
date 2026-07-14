const BACKEND_BASE_URL = "http://127.0.0.1:8000";

const DEFAULT_SETTINGS = {
  highlightEnabled: true,
  rewriteEnabled: true
};

const SUPPORTED_HOSTS = [
  "tw.news.yahoo.com",
  "www.ettoday.net",
  "ettoday.net",
  "udn.com",
  "www.udn.com"
];

const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

const supportedContent = document.getElementById("supported-content");
const unsupportedMessage = document.getElementById("unsupported-message");

const scannedCount = document.getElementById("scanned-count");
const clickbaitCount = document.getElementById("clickbait-count");
const rewrittenCount = document.getElementById("rewritten-count");

const highlightToggle = document.getElementById("highlight-toggle");
const rewriteToggle = document.getElementById("rewrite-toggle");


function isSupportedUrl(urlString) {
  try {
    const url = new URL(urlString);
    return SUPPORTED_HOSTS.includes(url.hostname);
  } catch {
    return false;
  }
}


function showUnsupportedState() {
  statusDot.className = "status-dot unsupported";
  statusText.textContent = "Website Not Supported";

  supportedContent.classList.add("hidden");
  unsupportedMessage.classList.remove("hidden");
}


function showSupportedState() {
  supportedContent.classList.remove("hidden");
  unsupportedMessage.classList.add("hidden");
}


async function checkBackendStatus() {
  try {
    const response = await fetch(`${BACKEND_BASE_URL}/health`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    statusDot.className = "status-dot connected";
    statusText.textContent = "Backend Connected";
  } catch {
    statusDot.className = "status-dot disconnected";
    statusText.textContent = "Backend Disconnected";
  }
}


async function loadSettings() {
  const settings = await chrome.storage.local.get(DEFAULT_SETTINGS);

  highlightToggle.checked = settings.highlightEnabled;
  rewriteToggle.checked =
    settings.highlightEnabled && settings.rewriteEnabled;

  rewriteToggle.disabled = !settings.highlightEnabled;

  if (!settings.highlightEnabled && settings.rewriteEnabled) {
    await chrome.storage.local.set({
      rewriteEnabled: false
    });
  }
}


async function getActiveTab() {
  const [activeTab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  return activeTab;
}


async function sendSettingsToTab(settings) {
  const activeTab = await getActiveTab();

  if (!activeTab?.id) {
    return;
  }

  try {
    await chrome.tabs.sendMessage(activeTab.id, {
      action: "settingsUpdated",
      settings
    });
  } catch {
    // The content script may not exist on unsupported pages.
  }
}


async function saveSettings(settings) {
  await chrome.storage.local.set(settings);
  await sendSettingsToTab(settings);
}


async function loadPageStats() {
  const activeTab = await getActiveTab();

  if (!activeTab?.id) {
    return;
  }

  try {
    const response = await chrome.tabs.sendMessage(activeTab.id, {
      action: "getPageStats"
    });

    scannedCount.textContent = response?.scanned ?? 0;
    clickbaitCount.textContent = response?.clickbait ?? 0;
    rewrittenCount.textContent = response?.rewritten ?? 0;
  } catch {
    scannedCount.textContent = "—";
    clickbaitCount.textContent = "—";
    rewrittenCount.textContent = "—";
  }
}


highlightToggle.addEventListener("change", async () => {
  const highlightEnabled = highlightToggle.checked;

  if (!highlightEnabled) {
    rewriteToggle.checked = false;
    rewriteToggle.disabled = true;

    await saveSettings({
      highlightEnabled: false,
      rewriteEnabled: false
    });

    return;
  }

  rewriteToggle.disabled = false;

  await saveSettings({
    highlightEnabled: true
  });
});


rewriteToggle.addEventListener("change", async () => {
  if (!highlightToggle.checked) {
    rewriteToggle.checked = false;
    return;
  }

  await saveSettings({
    rewriteEnabled: rewriteToggle.checked
  });
});


async function initializePopup() {
  const activeTab = await getActiveTab();

  if (!isSupportedUrl(activeTab?.url || "")) {
    showUnsupportedState();
    return;
  }

  showSupportedState();

  await Promise.all([
    checkBackendStatus(),
    loadSettings(),
    loadPageStats()
  ]);
}


initializePopup();