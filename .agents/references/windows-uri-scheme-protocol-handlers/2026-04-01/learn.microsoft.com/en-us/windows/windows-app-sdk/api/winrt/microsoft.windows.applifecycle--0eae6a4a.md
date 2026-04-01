<!--
source: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager
retrieved: 2026-04-01T21:31:09.992525+00:00
final_url: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager?view=windows-app-sdk-1.8
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
title: ActivationRegistrationManager Class (Microsoft.Windows.AppLifecycle) - Windows App SDK | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager?view=windows-app-sdk-1.8
uid: Microsoft.Windows.AppLifecycle.ActivationRegistrationManager
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
- Microsoft.Windows.AppLifecycle.ActivationRegistrationManager
topic_type:
- apiref
api_type:
- Assembly
locale: en-us
document_id: 0f02a48f-59b1-c747-32e0-a34f5f07704f
document_version_independent_id: e566e41b-18e8-b5ba-d63f-7c9be0d79d22
updated_at: 2026-02-14T23:47:00.0000000Z
original_content_git_url: https://cpubwin.visualstudio.com/DefaultCollection/windows-uwp/_git/winapps-winrt-api-build?path=/winapps-winrt-build/xml/Microsoft.Windows.AppLifecycle/ActivationRegistrationManager.xml&version=GBlive&_a=contents
gitcommit: https://cpubwin.visualstudio.com/DefaultCollection/windows-uwp/_git/winapps-winrt-api-build/commit/ef4a6baa84781f4ef46b69bad043336e5cdbfd6f?path=/winapps-winrt-build/xml/Microsoft.Windows.AppLifecycle/ActivationRegistrationManager.xml&_a=contents
git_commit_id: ef4a6baa84781f4ef46b69bad043336e5cdbfd6f
default_moniker: windows-app-sdk-1.8
site_name: Docs
depot_name: Win.winapps-winrt-api-build
page_type: dotnet
page_kind: class
ms.assetid: Microsoft.Windows.AppLifecycle.ActivationRegistrationManager
description: 'Provides static methods you can use to register and unregister for certain types of activations for your app. '
toc_rel: winapps-winrt-api/toc.json
search.mshattr.devlang: csharp vb cppcx cppwinrt
asset_id: microsoft.windows.applifecycle.activationregistrationmanager
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
platformId: c013b3d1-b1bd-8322-be94-4dcc63a215a3
---

# ActivationRegistrationManager Class

## Definition

- Namespace:
    - [Microsoft.Windows.AppLifecycle](microsoft.windows.applifecycle)

Provides static methods you can use to register and unregister for certain types of activations for your app.

```cppcx
public ref class ActivationRegistrationManager abstract sealed
```

```cppwinrt
/// [Windows.Foundation.Metadata.Experimental]
/// [Windows.Foundation.Metadata.MarshalingBehavior(Windows.Foundation.Metadata.MarshalingType.Agile)]
/// [Windows.Foundation.Metadata.Threading(Windows.Foundation.Metadata.ThreadingModel.Both)]
/// [Windows.Foundation.Metadata.Version(1)]
class ActivationRegistrationManager final
```

```cppwinrt
/// [Windows.Foundation.Metadata.MarshalingBehavior(Windows.Foundation.Metadata.MarshalingType.Agile)]
/// [Windows.Foundation.Metadata.Threading(Windows.Foundation.Metadata.ThreadingModel.Both)]
/// [Windows.Foundation.Metadata.ContractVersion(Microsoft.Windows.AppLifecycle.AppLifecycleContract, 65536)]
class ActivationRegistrationManager final
```

```csharp
[Windows.Foundation.Metadata.Experimental]
[Windows.Foundation.Metadata.MarshalingBehavior(Windows.Foundation.Metadata.MarshalingType.Agile)]
[Windows.Foundation.Metadata.Threading(Windows.Foundation.Metadata.ThreadingModel.Both)]
[Windows.Foundation.Metadata.Version(1)]
public static class ActivationRegistrationManager
```

```csharp
[Windows.Foundation.Metadata.MarshalingBehavior(Windows.Foundation.Metadata.MarshalingType.Agile)]
[Windows.Foundation.Metadata.Threading(Windows.Foundation.Metadata.ThreadingModel.Both)]
[Windows.Foundation.Metadata.ContractVersion(typeof(Microsoft.Windows.AppLifecycle.AppLifecycleContract), 65536)]
public static class ActivationRegistrationManager
```

```vb
Public Class ActivationRegistrationManager
```

- Inheritance
    - [Object](/en-us/dotnet/api/system.object)Platform::ObjectIInspectableActivationRegistrationManager

- Attributes
    - [ExperimentalAttribute](/en-us/uwp/api/windows.foundation.metadata.experimentalattribute)[MarshalingBehaviorAttribute](/en-us/uwp/api/windows.foundation.metadata.marshalingbehaviorattribute)[ThreadingAttribute](/en-us/uwp/api/windows.foundation.metadata.threadingattribute)[VersionAttribute](/en-us/uwp/api/windows.foundation.metadata.versionattribute)[ContractVersionAttribute](/en-us/uwp/api/windows.foundation.metadata.contractversionattribute)

## Examples

For code examples that demonstrsate how to use this class, see [Rich activation](/en-us/windows/apps/windows-app-sdk/applifecycle/applifecycle-rich-activation).

## Remarks

For more information about using this class, see [Rich activation](/en-us/windows/apps/windows-app-sdk/applifecycle/applifecycle-rich-activation).

## Methods

| Name | Description |
| --- | --- |
| [RegisterForFileTypeActivation(String\[\], String, String, String\[\], String)](microsoft.windows.applifecycle.activationregistrationmanager.registerforfiletypeactivation#microsoft-windows-applifecycle-activationregistrationmanager-registerforfiletypeactivation%28system-string%28%29-system-string-system-string-system-string%28%29-system-string%29) | Registers to activate the app when the specified file type is opened via [ShellExecute](/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecuteexw), [Launcher.LaunchFileAsync](/en-us/uwp/api/windows.system.launcher.launchfileasync), or the command-line. |
| [RegisterForProtocolActivation(String, String, String, String)](microsoft.windows.applifecycle.activationregistrationmanager.registerforprotocolactivation#microsoft-windows-applifecycle-activationregistrationmanager-registerforprotocolactivation%28system-string-system-string-system-string-system-string%29) | Registers to activate the app when the specified URI scheme is executed via [ShellExecute](/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecuteexw), [Launcher.LaunchUriAsync](/en-us/uwp/api/windows.system.launcher.launchuriasync), or the command-line. |
| [RegisterForStartupActivation(String, String)](microsoft.windows.applifecycle.activationregistrationmanager.registerforstartupactivation#microsoft-windows-applifecycle-activationregistrationmanager-registerforstartupactivation%28system-string-system-string%29) | Registers to activate the app when when the app is started by the user logging into the Windows OS, either because of a registry key, or because of a shortcut in a well-known startup folder. |
| [UnregisterForFileTypeActivation(String\[\], String)](microsoft.windows.applifecycle.activationregistrationmanager.unregisterforfiletypeactivation#microsoft-windows-applifecycle-activationregistrationmanager-unregisterforfiletypeactivation%28system-string%28%29-system-string%29) | Unregisters a file type activation that was registered earlier by using the [RegisterForFileTypeActivation](microsoft.windows.applifecycle.activationregistrationmanager.registerforfiletypeactivation#microsoft-windows-applifecycle-activationregistrationmanager-registerforfiletypeactivation%28system-string%28%29-system-string-system-string-system-string%28%29-system-string%29) method. |
| [UnregisterForProtocolActivation(String, String)](microsoft.windows.applifecycle.activationregistrationmanager.unregisterforprotocolactivation#microsoft-windows-applifecycle-activationregistrationmanager-unregisterforprotocolactivation%28system-string-system-string%29) | Unregisters a protocol activation that was registered earlier by using the [RegisterForProtocolActivation](microsoft.windows.applifecycle.activationregistrationmanager.registerforprotocolactivation#microsoft-windows-applifecycle-activationregistrationmanager-registerforprotocolactivation%28system-string-system-string-system-string-system-string%29) method. |
| [UnregisterForStartupActivation(String)](microsoft.windows.applifecycle.activationregistrationmanager.unregisterforstartupactivation#microsoft-windows-applifecycle-activationregistrationmanager-unregisterforstartupactivation%28system-string%29) | Unregisters a startup activation that was registered earlier by using the [RegisterForStartupActivation](microsoft.windows.applifecycle.activationregistrationmanager.registerforstartupactivation#microsoft-windows-applifecycle-activationregistrationmanager-registerforstartupactivation%28system-string-system-string%29) method. |

## Applies to
