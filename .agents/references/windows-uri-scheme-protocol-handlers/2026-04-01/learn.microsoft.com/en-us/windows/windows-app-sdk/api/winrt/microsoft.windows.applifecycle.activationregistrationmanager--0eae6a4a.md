<!--
source: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.registerforprotocolactivation
retrieved: 2026-04-01T21:31:10.792525+00:00
final_url: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.registerforprotocolactivation?view=windows-app-sdk-1.8
content_type: text/markdown
-->

---
layout: Reference
monikers:
- windows-app-sdk-1.0
- windows-app-sdk-1.1
- windows-app-sdk-1.2
- windows-app-sdk-1.3
- windows-app-sdk-1.4
- windows-app-sdk-1.5
- windows-app-sdk-1.6
- windows-app-sdk-1.7
- windows-app-sdk-1.8
- windows-app-sdk-2.0-experimental
- windows-app-sdk-2.0-preview
defaultMoniker: windows-app-sdk-1.8
versioningType: Ranged
title: ActivationRegistrationManager.RegisterForProtocolActivation Method (Microsoft.Windows.AppLifecycle) - Windows App SDK | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.registerforprotocolactivation?view=windows-app-sdk-1.8
uid: Microsoft.Windows.AppLifecycle.ActivationRegistrationManager.RegisterForProtocolActivation*
namespace: Microsoft.Windows.AppLifecycle
adobe-target: true
apiPlatform: dotnet
breadcrumb_path: /windows/windows-app-sdk/api/winrt/breadcrumb/toc.json
feedback_system: Standard
feedback_product_url: https://github.com/microsoft/WindowsAppSDK
feedback_help_link_url: https://learn.microsoft.com/answers/tags/184/windows-app-sdk/
feedback_help_link_type: get-help-at-qna
uhfHeaderId: MSDocsHeader-WinDevCenter
author: GrantMeStrength
ms.author: jken
ms.service: windows-app-sdk
ms.subservice: reunion-reference
ms.topic: reference
api_name:
- Microsoft.Windows.AppLifecycle.ActivationRegistrationManager.RegisterForProtocolActivation
topic_type:
- apiref
api_type:
- Assembly
locale: en-us
document_id: d3088157-b694-7c7f-fd22-b4dec04933ad
document_version_independent_id: 476fb3d0-2d87-7108-b2b8-6a014862e279
updated_at: 2026-02-14T23:47:00.0000000Z
original_content_git_url: https://cpubwin.visualstudio.com/DefaultCollection/windows-uwp/_git/winapps-winrt-api-build?path=/winapps-winrt-build/xml/Microsoft.Windows.AppLifecycle/ActivationRegistrationManager.xml&version=GBlive&_a=contents
gitcommit: https://cpubwin.visualstudio.com/DefaultCollection/windows-uwp/_git/winapps-winrt-api-build/commit/ef4a6baa84781f4ef46b69bad043336e5cdbfd6f?path=/winapps-winrt-build/xml/Microsoft.Windows.AppLifecycle/ActivationRegistrationManager.xml&_a=contents
git_commit_id: ef4a6baa84781f4ef46b69bad043336e5cdbfd6f
default_moniker: windows-app-sdk-1.8
site_name: Docs
depot_name: Win.winapps-winrt-api-build
page_type: dotnet
page_kind: method
ms.assetid: Microsoft.Windows.AppLifecycle.ActivationRegistrationManager.RegisterForProtocolActivation*
description: 'Registers to activate the app when the specified URI scheme is executed via ShellExecute, Launcher.LaunchUriAsync, or the command-line. '
toc_rel: winapps-winrt-api/toc.json
search.mshattr.devlang: csharp vb javascript cppcx cppwinrt
asset_id: microsoft.windows.applifecycle.activationregistrationmanager.registerforprotocolactivation
moniker_range_name: 480fb071fccef76c7b630ce745f3e0bd
monikers:
- windows-app-sdk-1.0
- windows-app-sdk-1.1
- windows-app-sdk-1.2
- windows-app-sdk-1.3
- windows-app-sdk-1.4
- windows-app-sdk-1.5
- windows-app-sdk-1.6
- windows-app-sdk-1.7
- windows-app-sdk-1.8
- windows-app-sdk-2.0-experimental
- windows-app-sdk-2.0-preview
item_type: Content
source_path: winapps-winrt-build/xml/Microsoft.Windows.AppLifecycle/ActivationRegistrationManager.xml
platformId: 16a1399f-88d9-61a4-681f-36d85f0d0a52
---

# ActivationRegistrationManager.RegisterForProtocolActivation Method

## Definition

- Namespace:
    - [Microsoft.Windows.AppLifecycle](microsoft.windows.applifecycle)

::: moniker range=" windows-app-sdk-1.0 windows-app-sdk-1.1 windows-app-sdk-1.2 windows-app-sdk-1.3 windows-app-sdk-1.4 windows-app-sdk-1.5 windows-app-sdk-1.6 windows-app-sdk-1.7 windows-app-sdk-1.8 windows-app-sdk-2.0-experimental windows-app-sdk-2.0-preview "

Registers to activate the app when the specified URI scheme is executed via [ShellExecute](/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecuteexw), [Launcher.LaunchUriAsync](/en-us/uwp/api/windows.system.launcher.launchuriasync), or the command-line.

```cppcx
public:
 static void RegisterForProtocolActivation(Platform::String ^ scheme, Platform::String ^ logo, Platform::String ^ displayName, Platform::String ^ exePath);
```

```cppwinrt
/// [Windows.Foundation.Metadata.Experimental]
 static void RegisterForProtocolActivation(winrt::hstring const& scheme, winrt::hstring const& logo, winrt::hstring const& displayName, winrt::hstring const& exePath);
```

```cppwinrt
 static void RegisterForProtocolActivation(winrt::hstring const& scheme, winrt::hstring const& logo, winrt::hstring const& displayName, winrt::hstring const& exePath);
```

```csharp
[Windows.Foundation.Metadata.Experimental]
public static void RegisterForProtocolActivation(string scheme, string logo, string displayName, string exePath);
```

```csharp
public static void RegisterForProtocolActivation(string scheme, string logo, string displayName, string exePath);
```

```javascript
function registerForProtocolActivation(scheme, logo, displayName, exePath)
```

```vb
Public Shared Sub RegisterForProtocolActivation (scheme As String, logo As String, displayName As String, exePath As String)
```

#### Parameters

- scheme
    - [String](/en-us/dotnet/api/system.string)
Platform::String

winrt::hstring

The URI scheme to register for activations, such as `https`.

- logo
    - [String](/en-us/dotnet/api/system.string)
Platform::String

winrt::hstring

The path to the image or resource used by Windows for the URI scheme. For packaged apps, this parameter is a package-relative path to an image file. For unpackaged, this parameter is a literal filepath to a binary file (DLL, EXE) plus a resource index.

- displayName
    - [String](/en-us/dotnet/api/system.string)
Platform::String

winrt::hstring

This display name used by Windows for the URI scheme.

- exePath
    - [String](/en-us/dotnet/api/system.string)
Platform::String

winrt::hstring

The path to the executable to be activated. If you pass an empty string, the current exectuable will be activated by default. Typically this parameter is specified if the caller of this method is the app's installer rather than the app itself.

- Attributes
    - [ExperimentalAttribute](/en-us/uwp/api/windows.foundation.metadata.experimentalattribute)

## Remarks

Packaged apps should continue to use their appx manifest to register for file-type, protocol or startup activation. They can then use either [Microsoft.Windows.AppLifecycle.AppInstance.GetActivatedEventArgs](microsoft.windows.applifecycle.appinstance.getactivatedeventargs#microsoft-windows-applifecycle-appinstance-getactivatedeventargs) or [Windows.ApplicationModel.AppInstance.GetActivatedEventArgs](/en-us/uwp/api/windows.applicationmodel.appinstance.getactivatedeventargs) to retrieve the arguments on activation.

## Applies to

## See also

- [UnregisterForProtocolActivation(String, String)](microsoft.windows.applifecycle.activationregistrationmanager.unregisterforprotocolactivation#microsoft-windows-applifecycle-activationregistrationmanager-unregisterforprotocolactivation%28system-string-system-string%29)

::: moniker-end
