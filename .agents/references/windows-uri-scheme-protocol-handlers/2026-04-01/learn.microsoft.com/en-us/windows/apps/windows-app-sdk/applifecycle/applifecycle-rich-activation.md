<!--
source: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/applifecycle/applifecycle-rich-activation
retrieved: 2026-04-01T21:31:08.921525+00:00
final_url: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/applifecycle/applifecycle-rich-activation
content_type: text/markdown
-->

---
layout: Conceptual
title: Rich activation with the app lifecycle API (Windows App SDK) - Windows apps | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/applifecycle/applifecycle-rich-activation
ms.service: windows-app-sdk
recommendations: true
ROBOTS: INDEX, FOLLOW
author: jwmsft
ms.author: jimwalk
Search.Product: eADQiWindows 10XVcnh
uhfHeaderId: MSDocsHeader-WinDevCenter
breadcrumb_path: /windows/breadcrumbs/toc.json
feedback_product_url: https://github.com/microsoft/WindowsAppSDK/issues
feedback_system: OpenSource
ms.subservice: app-lifecycle
ms.update-cycle: 365-days
description: Describes how to use rich activation features with the app lifecycle API in unpackaged apps (Windows App SDK).
ms.topic: article
ms.date: 2025-07-14T00:00:00.0000000Z
keywords: AppLifecycle, Windows, activation, activation contracts, rich activation, win32, win32 activation, unpackaged app, unpackaged app activation
ms.localizationpriority: medium
locale: en-us
document_id: 2d56a3de-3af1-6b72-ab58-c4cecf7b7dc7
document_version_independent_id: ef4aff1b-9f9c-2300-34c8-dff5e54aceb6
updated_at: 2026-02-28T05:05:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/windows-dev-docs-pr/blob/live/hub/apps/windows-app-sdk/applifecycle/applifecycle-rich-activation.md
gitcommit: https://github.com/MicrosoftDocs/windows-dev-docs-pr/blob/496fde4e76c812665447fe224012dd29df5129f4/hub/apps/windows-app-sdk/applifecycle/applifecycle-rich-activation.md
git_commit_id: 496fde4e76c812665447fe224012dd29df5129f4
site_name: Docs
depot_name: MSDN.windows-uwp-hub
page_type: conceptual
toc_rel: ../../develop/toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/MSDN.windows-uwp-hub/{branchName}{pdfName}
feedback_help_link_type: ''
feedback_help_link_url: ''
word_count: 1273
asset_id: apps/windows-app-sdk/applifecycle/applifecycle-rich-activation
moniker_range_name: 
monikers: []
item_type: Content
source_path: hub/apps/windows-app-sdk/applifecycle/applifecycle-rich-activation.md
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/b3627ad5-057f-488f-8b97-08be347b4be5
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/caf7ae9a-a42c-4d10-83cf-bad1844d884d
platformId: b1186491-f1bd-39ef-62fa-3ef604996644
---

# Rich activation with the app lifecycle API (Windows App SDK) - Windows apps | Microsoft Learn

In the Windows App SDK, the app lifecycle API brings support for UWP-style rich activation behavior to all apps, packaged and unpackaged alike. This first release focuses on bringing the most commonly-used activation kinds to unpackaged apps, and future releases aim to support more of UWP's [44 activation kinds](/en-us/uwp/api/Windows.ApplicationModel.Activation.ActivationKind).

Supporting rich activations requires two steps:

- Tell the system that your app supports one or more rich activation kinds.
- Receive and process the rich activation payloads your app receives when it is activated.

## Prerequisites

To use the app lifecycle API in the Windows App SDK:

1. Download and install the latest release of the Windows App SDK. For more information, see [Get started with WinUI 3](../../get-started/start-here).
2. Follow the instructions to [Create your first WinUI project](../../winui/winui3/create-your-first-winui3-app) or to [use the Windows App SDK in an existing project](../use-windows-app-sdk-in-existing-project).

## Activation details for unpackaged apps

The current version of the Windows App SDK supports the four most common activation kinds to unpackaged apps. These activation kinds are defined by the [ExtendedActivationKind](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.extendedactivationkind) enum.

| Activation kind | Description |
| --- | --- |
| `Launch` | Activate the app from the command line, when the user double-clicks the app's icon, or programmatically via [ShellExecute](/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecuteexw) or [CreateProcess](/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw). |
| `File` | Activate an app that has registered for a file type when a file of the type is opened via [ShellExecute](/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecuteexw), [Launcher.LaunchFileAsync](/en-us/uwp/api/windows.system.launcher.launchfileasync), or the command line. |
| `Protocol` | Activate an app that has registered for a protocol when a string of that protocol is executed via [ShellExecute](/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecuteexw), [Launcher.LaunchUriAsync](/en-us/uwp/api/windows.system.launcher.launchuriasync), or the command-line. |
| `StartupTask` | Activate the app when the user logs into Windows, either because of a registry key, or because of a shortcut in a well-known startup folder. |

Each type of unpackaged app retrieves its command line arguments in different ways. For example, C++ Win32 apps expect to receive activation arguments to be passed into `WinMain` in the form of a string (though they also have the option to call [GetCommandLineW](/en-us/windows/win32/api/processenv/nf-processenv-getcommandlinew)). Windows Forms apps, however, *must* call [Environment.GetCommandLineArgs](/en-us/dotnet/api/system.environment.getcommandlineargs), because arguments will not be automatically passed to them.

## Activation details for packaged apps

Packaged apps that use the Windows App SDK support all 44 of UWP's [activation kinds](/en-us/uwp/api/Windows.ApplicationModel.Activation.ActivationKind). Each activation kind has its own corresponding implementation of [IActivatedEventArgs](/en-us/uwp/api/windows.applicationmodel.activation.iactivatedeventargs) which contain properties relevant to that specific kind of activation.

Packaged apps will always receive activation event arguments in their [AppInstance.Activated](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.appinstance.activated) event handler, and also have the option of calling [AppInstance.GetActivatedEventArgs](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.appinstance.getactivatedeventargs).

### Activation registration

All apps support the `Launch` activation kind by default. Unlike UWP, the Windows App SDK `Launch` activation kind includes command line launches. Apps can register for additional activation kinds in several ways.

- Unpackaged apps that use the Windows App SDK can register (and unregister) for additional activation kinds via the app lifecycle API in the Windows App SDK.
- Unpackaged apps can continue to register for additional activation kinds using the traditional method of writing registry keys.
- Packaged apps can register for additional activation kinds via entries in their application manifest.

Activation registrations are per-user. If your app is installed for multiple users, you will need to re-register activations for each user.

## Examples

### Register for rich activation

Although apps can call the registration APIs at any time, the most common scenario is checking registrations on app startup.

This example shows how an unpackaged app can use the following static methods of the [ActivationRegistrationManager](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager) class to register for several activation kinds when the app is launched:

- [RegisterForFileTypeActivation](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.registerforfiletypeactivation)
- [RegisterForProtocolActivation](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.registerforprotocolactivation)
- [RegisterForStartupActivation](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.registerforstartupactivation)

This example also demonstrates how to use the [MddBootstrapInitialize](/en-us/windows/windows-app-sdk/api/win32/mddbootstrap/nf-mddbootstrap-mddbootstrapinitialize) and [MddBootstrapShutdown](/en-us/windows/windows-app-sdk/api/win32/mddbootstrap/nf-mddbootstrap-mddbootstrapshutdown) functions to initialize and clean up references to the Windows App SDK framework package. All unpackaged app must do this to use APIs provided by the Windows App SDK. For more information, see [Use the Windows App SDK runtime for apps packaged with external location or unpackaged](../use-windows-app-sdk-run-time).

Note

This example registers associations with three image file types at once. This is convenient, but the outcome is the same as registering each file type individually; registering new image types does not overwrite previous registrations. However, if an app re-registers an already registered file type with a different set of verbs, the previous set of verbs will be overwritten for that file type.

```c
const UINT32 majorMinorVersion{ WINDOWSAPPSDK_RELEASE_MAJORMINOR };
PCWSTR versionTag{ WINDOWSAPPSDK_RELEASE_VERSION_TAG_W };
const PACKAGE_VERSION minVersion{ WINDOWSAPPSDK_RUNTIME_VERSION_UINT64 };
WCHAR szExePath[MAX_PATH]{};
WCHAR szExePathAndIconIndex[MAX_PATH + 8]{};

int APIENTRY wWinMain(
    _In_ HINSTANCE hInstance, _In_opt_ HINSTANCE hPrevInstance,
    _In_ LPWSTR lpCmdLine, _In_ int nCmdShow)
{
    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(lpCmdLine);

    // Initialize Windows App SDK framework package for unpackaged apps.
    HRESULT hr{ MddBootstrapInitialize(majorMinorVersion, versionTag, minVersion) };
    if (FAILED(hr))
    {
        wprintf(L"Error 0x%X in MddBootstrapInitialize(0x%08X, %s, %hu.%hu.%hu.%hu)\n",
            hr, majorMinorVersion, versionTag, minVersion.Major, 
            minVersion.Minor, minVersion.Build, minVersion.Revision);
        return hr;
    }

    // Get the current executable filesystem path, so we can
    // use it later in registering for activation kinds.
    GetModuleFileName(NULL, szExePath, MAX_PATH);
    wcscpy_s(szExePathAndIconIndex, szExePath);
    wcscat_s(szExePathAndIconIndex, L",1");

    LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
    LoadStringW(hInstance, IDC_CLASSNAME, szWindowClass, MAX_LOADSTRING);
    RegisterWindowClass(hInstance);
    if (!InitInstance(hInstance, nCmdShow))
    {
        return FALSE;
    }

    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // Uninitialize Windows App SDK.
    MddBootstrapShutdown();
    return (int)msg.wParam;
}

void RegisterForActivation()
{
    OutputMessage(L"Registering for rich activation");

    // Register one or more supported filetypes, specifying 
    // an icon (specified by binary file path plus resource index),
    // a display name to use in Shell and Settings,
    // zero or more verbs for the File Explorer context menu,
    // and the path to the EXE to register for activation.
    hstring myFileTypes[3] = { L".foo", L".foo2", L".foo3" };
    hstring verbs[2] = { L"view", L"edit" };
    ActivationRegistrationManager::RegisterForFileTypeActivation(
        myFileTypes,
        szExePathAndIconIndex,
        L"Contoso File Types",
        verbs,
        szExePath
    );

    // Register a URI scheme for protocol activation,
    // specifying the scheme name, icon, display name and EXE path.
    ActivationRegistrationManager::RegisterForProtocolActivation(
        L"foo",
        szExePathAndIconIndex,
        L"Contoso Foo Protocol",
        szExePath
    );

    // Register for startup activation.
    // As we're registering for startup activation multiple times,
    // and this is a multi-instance app, we'll get multiple instances
    // activated at startup.
    ActivationRegistrationManager::RegisterForStartupActivation(
        L"ContosoStartupId",
        szExePath
    );

    // If we don't specify the EXE, it will default to this EXE.
    ActivationRegistrationManager::RegisterForStartupActivation(
        L"ContosoStartupId2",
        L""
    );
}
```

### Get rich activation event arguments

Once activated, an app must retrieve its activation event arguments. In this example, an unpackaged app calls the [AppInstance.GetActivatedEventArgs](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.appinstance.getactivatedeventargs) method to get the event args for the activation event and then uses the [AppActivationArguments.Kind](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.appactivationarguments.kind) property to retrieve the event args for different types of activations.

Note

Win32 apps typically get command-line arguments very early their `WinMain` method. Similarly, these apps should call [AppInstance.GetActivatedEventArgs](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.appinstance.getactivatedeventargs) in the same place where they previously would have used the supplied the `lpCmdLine` parameter or called `GetCommandLineW`.

```c
void GetActivationInfo()
{
    AppActivationArguments args = AppInstance::GetCurrent().GetActivatedEventArgs();
    ExtendedActivationKind kind = args.Kind();
    if (kind == ExtendedActivationKind::Launch)
    {
        ILaunchActivatedEventArgs launchArgs = 
            args.Data().as<ILaunchActivatedEventArgs>();
        if (launchArgs != NULL)
        {
            winrt::hstring argString = launchArgs.Arguments().c_str();
            std::vector<std::wstring> argStrings = split_strings(argString);
            OutputMessage(L"Launch activation");
            for (std::wstring s : argStrings)
            {
                OutputMessage(s.c_str());
            }
        }
    }
    else if (kind == ExtendedActivationKind::File)
    {
        IFileActivatedEventArgs fileArgs = 
            args.Data().as<IFileActivatedEventArgs>();
        if (fileArgs != NULL)
        {
            IStorageItem file = fileArgs.Files().GetAt(0);
            OutputFormattedMessage(
                L"File activation: %s", file.Name().c_str());
        }
    }
    else if (kind == ExtendedActivationKind::Protocol)
    {
        IProtocolActivatedEventArgs protocolArgs = 
            args.Data().as<IProtocolActivatedEventArgs>();
        if (protocolArgs != NULL)
        {
            Uri uri = protocolArgs.Uri();
            OutputFormattedMessage(
                L"Protocol activation: %s", uri.RawUri().c_str());
        }
    }
    else if (kind == ExtendedActivationKind::StartupTask)
    {
        IStartupTaskActivatedEventArgs startupArgs = 
            args.Data().as<IStartupTaskActivatedEventArgs>();
        if (startupArgs != NULL)
        {
            OutputFormattedMessage(
                L"Startup activation: %s", startupArgs.TaskId().c_str());
        }
    }
}
```

### Unregister

This example demonstrates how an unpackaged app can unregister for specific activation kinds dynamically, using the following static methods of the [ActivationRegistrationManager](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager) class:

- [UnregisterForFileTypeActivation](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.unregisterforfiletypeactivation)
- [UnregisterForProtocolActivation](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.unregisterforprotocolactivation)
- [UnregisterForStartupActivation](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.activationregistrationmanager.unregisterforstartupactivation)

Note

When unregistering for startup activation, the app must use the same taskId that it used when it originally registered.

```c
void UnregisterForActivation()
{
    OutputMessage(L"Unregistering for rich activation");
    
    // Unregister one or more registered filetypes.
    try
    {
        hstring myFileTypes[3] = { L".foo", L".foo2", L".foo3" };
        ActivationRegistrationManager::UnregisterForFileTypeActivation(
            myFileTypes,
            szExePath
        );
    }
    catch (...)
    {
        OutputMessage(L"Error unregistering file types");
    }

    // Unregister a protocol scheme.
    ActivationRegistrationManager::UnregisterForProtocolActivation(
        L"foo",
        L"");

    // Unregister for startup activation.
    ActivationRegistrationManager::UnregisterForStartupActivation(
        L"ContosoStartupId");
    ActivationRegistrationManager::UnregisterForStartupActivation(
        L"ContosoStartupId2");
}
```
