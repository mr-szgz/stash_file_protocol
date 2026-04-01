# Research Summary

- Research Date: `2026-04-01`
- Official Version: Windows App SDK API docs target `windows-app-sdk-1.8` (plus UWP manifest schema and archived Win32 registry guidance).
- Key Findings:
  - Packaged Windows apps (UWP/WinUI/MSIX) register custom URI schemes using the package manifest `windows.protocol` extension with a `uap:Protocol` element, then handle activation via `ProtocolActivatedEventArgs` (UWP) or `AppInstance` activation APIs (Windows App SDK). The protocol name must be lowercase and follow schema constraints. (Sources: handle-uri-activation, AppX Protocol schema)
  - Packaged desktop apps with package identity can use manifest extensions to integrate with Windows (including protocol handling) as part of the desktop-to-UWP extension set. (Source: desktop-to-uwp-extensions)
  - Unpackaged apps can use Windows App SDK AppLifecycle rich activation and `ActivationRegistrationManager.RegisterForProtocolActivation` to register protocol activation triggered by `ShellExecute`, `Launcher.LaunchUriAsync`, or the command line; registrations are per-user. Unpackaged apps can also use traditional registry registration. (Sources: rich activation, ActivationRegistrationManager API)
  - Classic Win32 registration for custom URI schemes uses `HKEY_CLASSES_ROOT\<scheme>` with a `URL Protocol` value and `shell\open\command` to launch the handler; the URI arrives on the command line and must be treated as untrusted input. (Source: Registering an Application to a URI Scheme)
  - Windows maintains a reserved list of URI schemes and file types; attempts to register a reserved scheme are ignored. (Source: reserved-uri-scheme-names)
  - App URI handlers (“Apps for websites”) let apps claim http/https links for verified domains via `windows.appUriHandler` in the manifest plus a website association file; this complements custom scheme handling but targets web links. (Source: web-to-app-linking)
- Compatibility Notes:
  - Packaged apps register protocols via manifest; unpackaged apps register via Windows App SDK APIs or traditional registry keys. (Rich activation doc)
  - Protocol registrations are per-user; multi-user installations must register per user. (Rich activation doc)
  - Reserved URI schemes cannot be claimed by third-party apps. (Reserved schemes doc)
  - Treat URI payloads as untrusted input; validate and avoid implicit privileged actions. (Handle URI activation + Win32 registry doc)
