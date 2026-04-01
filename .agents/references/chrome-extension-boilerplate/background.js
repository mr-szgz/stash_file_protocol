chrome.runtime.onMessage.addListener((message, sender) => {
  if (!message || message.type !== "open-stash" || !message.url) {
    return;
  }

  const tabId = sender && sender.tab ? sender.tab.id : undefined;
  if (tabId !== undefined) {
    chrome.tabs.update(tabId, { url: message.url });
  } else {
    chrome.tabs.create({ url: message.url });
  }
});
