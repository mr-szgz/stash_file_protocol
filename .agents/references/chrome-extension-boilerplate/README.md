# Stash Protocol Bridge (Chrome Extension)

This is a minimal Manifest V3 extension that intercepts clicks on `stash://` links inside web pages and forwards them to Chrome for handling by the OS protocol handler.

## Load Unpacked

1. Open `chrome://extensions` in Chrome.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select this `chrome-extension` folder.

## What It Does

- Content script captures clicks on `stash://` links.
- Background service worker asks the tab to navigate to the `stash://` URL, letting Chrome delegate to the OS handler.

## Limitations

- Chrome Extensions do not register custom protocol handlers themselves.
- This only intercepts link clicks in pages; it does not handle manual address bar entry or external app launches.
- The OS must already have a `stash://` handler installed for navigation to succeed.
