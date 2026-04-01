(() => {
  const STASH_PREFIX = "stash://";

  function findStashLink(target) {
    if (!(target instanceof Element)) {
      return null;
    }
    return target.closest(`a[href^="${STASH_PREFIX}"]`);
  }

  document.addEventListener(
    "click",
    (event) => {
      const link = findStashLink(event.target);
      if (!link) {
        return;
      }

      const url = link.getAttribute("href");
      if (!url) {
        return;
      }

      event.preventDefault();
      event.stopPropagation();
      chrome.runtime.sendMessage({ type: "open-stash", url });
    },
    true
  );
})();
