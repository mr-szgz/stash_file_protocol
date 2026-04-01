# Research Summary

- Research Date: `2026-04-01`
- Official Version: Manifest V3 (MV3)
- Official Sources:
  - https://developer.chrome.com/docs/extensions
  - https://developer.chrome.com/docs/extensions/develop
  - https://developer.chrome.com/docs/extensions/reference/manifest
  - https://developer.chrome.com/docs/extensions/reference/api/permissions
  - https://developer.chrome.com/docs/web-platform/best-practices/url-protocol-handler
- Key Findings:
  - Chrome Extensions use Manifest V3 and declare `manifest_version: 3` in `manifest.json`.
  - Extension permissions and host permissions are declared in the manifest and gate API access.
  - Chrome’s official URL protocol handler guidance is for web apps (PWA) using web-platform features, not an extension manifest key.
- Compatibility Notes:
  - Handling `stash://` links via an extension typically requires intercepting clicks/navigation in pages and delegating to the OS protocol handler or a companion app; Chrome’s protocol handler guidance is web-app focused.
