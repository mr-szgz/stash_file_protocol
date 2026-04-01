<!--
source: https://learn.microsoft.com/en-us/windows/apps/develop/launch/handle-uri-activation
retrieved: 2026-04-01T21:31:05.804031+00:00
final_url: https://learn.microsoft.com/en-us/windows/apps/develop/launch/handle-uri-activation
content_type: text/markdown
-->

---
layout: Conceptual
title: Handle URI activation with a Windows app - Windows apps | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/windows/apps/develop/launch/handle-uri-activation
ms.service: windows-app-sdk
recommendations: true
ROBOTS: INDEX, FOLLOW
author: jwmsft
ms.author: jimwalk
Search.Product: eADQiWindows 10XVcnh
uhfHeaderId: MSDocsHeader-WinDevCenter
breadcrumb_path: /windows/breadcrumbs/toc.json
feedback_product_url: https://www.microsoft.com/en-us/windowsinsider/feedbackhub/fb
feedback_system: OpenSource
ms.subservice: apps
ms.update-cycle: 365-days
description: Learn how to register a Windows app to become the default handler for a Uniform Resource Identifier (URI) scheme name.
ms.date: 2025-02-11T00:00:00.0000000Z
ms.topic: how-to
keywords: windows 10, uwp, windows 11
ms.localizationpriority: medium
locale: en-us
document_id: 0e617095-3c59-4a4d-1f73-d91d8e98e74f
document_version_independent_id: 0e617095-3c59-4a4d-1f73-d91d8e98e74f
updated_at: 2026-03-26T05:03:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/windows-dev-docs-pr/blob/live/hub/apps/develop/launch/handle-uri-activation.md
gitcommit: https://github.com/MicrosoftDocs/windows-dev-docs-pr/blob/f8d1b0323ffcd0da4dfb852a03ed2984db48b633/hub/apps/develop/launch/handle-uri-activation.md
git_commit_id: f8d1b0323ffcd0da4dfb852a03ed2984db48b633
site_name: Docs
depot_name: MSDN.windows-uwp-hub
page_type: conceptual
toc_rel: ../toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/MSDN.windows-uwp-hub/{branchName}{pdfName}
feedback_help_link_type: ''
feedback_help_link_url: ''
word_count: 1455
asset_id: apps/develop/launch/handle-uri-activation
moniker_range_name: 
monikers: []
item_type: Content
source_path: hub/apps/develop/launch/handle-uri-activation.md
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/cd440f3c-1b78-40a7-97ba-aa00a1d79df7
- https://authoring-docs-microsoft.poolparty.biz/devrel/bcbcbad5-4208-4783-8035-8481272c98b8
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/34504444-f407-4677-9da1-33515ff235e4
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c828f7e0-89b4-459c-9bae-d7ab1c4bd9ad
- https://authoring-docs-microsoft.poolparty.biz/devrel/43b2e5aa-8a6d-4de2-a252-692232e5edc8
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/d6246312-ca66-4402-b754-a68ddc46eec0
platformId: 53b602f3-42f3-02c0-2f04-e23521d0a14c
---

# Handle URI activation with a Windows app - Windows apps | Microsoft Learn

Learn how to register an app to become the default handler for a Uniform Resource Identifier (URI) scheme name. WinUI apps can register to be a default handler for a URI scheme name. If the user chooses your app as the default handler for a URI scheme name, your app will be activated every time that type of URI is launched.

We recommend that you only register for a URI scheme name if you expect to handle all URI launches for that type of URI scheme. If you do choose to register for a URI scheme name, you must provide the end user with the functionality that is expected when your app is activated for that URI scheme. For example, an app that registers for the mailto: URI scheme name should open to a new e-mail message so that the user can compose a new e-mail. For more info on URI associations, see [Files, folders, and libraries](../files/).

These steps show how to register for a custom URI scheme name, `alsdk://`, and how to activate your app when the user launches a `alsdk://` URI.

## Important APIs

The following APIs are used in this topic:

- [Windows.ApplicationModel.Activation.ProtocolActivatedEventArgs](/en-us/uwp/api/Windows.ApplicationModel.Activation.ProtocolActivatedEventArgs)
- [Windows.UI.Xaml.Application.OnActivated](/en-us/uwp/api/windows.ui.xaml.application.onactivated)
- [AppInstance.GetActivatedEventArgs](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.appinstance.getactivatedeventargs)

Note

In Windows, certain URIs and file extensions are reserved for use by built-in apps and the operating system. Attempts to register your app with a reserved URI or file extension will be ignored. See [Reserved URI scheme names and file types](reserved-uri-scheme-names) for an alphabetic list of Uri schemes that you can't register for your apps because they are either reserved or forbidden.

## Step 1: Specify the extension point in the package manifest

The app receives activation events only for the URI scheme names listed in the package manifest. Here's how you indicate that your app handles the `alsdk` URI scheme name.

1. In the **Solution Explorer**, double-click package.appxmanifest to open the manifest designer. Select the **Declarations** tab and in the **Available Declarations** drop-down, select **Protocol** and then click **Add**.

    Here is a brief description of each of the fields that you may fill in the manifest designer for the Protocol (see [AppX Package Manifest](/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-uap-extension) for details):

| Field | Description |
| --- | --- |
| **Logo** | Specify the logo that is used to identify the URI scheme name in the [Set Default Programs](/en-us/windows/desktop/shell/default-programs) on the **Control Panel**. If no Logo is specified, the small logo for the app is used. |
| **Display Name** | Specify the display name to identify the URI scheme name in the [Set Default Programs](/en-us/windows/desktop/shell/default-programs) on the **Control Panel**. |
| **Name** | Choose a name for the Uri scheme. |
|  | **Note** The Name must be in all lower case letters. |
|  | **Reserved and forbidden file types** See [Reserved URI scheme names and file types](reserved-uri-scheme-names) for an alphabetic list of Uri schemes that you can't register for your Windows apps because they are either reserved or forbidden. |
| **Executable** | Specifies the default launch executable for the protocol. If not specified, the app's executable is used. If specified, the string must be between 1 and 256 characters in length, must end with ".exe", and cannot contain these characters: &gt;, &lt;, :, ", |, ?, or \*. If specified, the **Entry point** is also used. If the **Entry point** isn't specified, the entry point defined for the app is used. |
| **Entry point** | Specifies the task that handles the protocol extension. This is normally the fully namespace-qualified name of a Windows Runtime type. If not specified, the entry point for the app is used. |
| **Start page** | The web page that handles the extensibility point. |
| **Resource group** | A tag that you can use to group extension activations together for resource management purposes. |
| **Desired View** (Windows-only) | Specify the **Desired View** field to indicate the amount of space the app's window needs when it is launched for the URI scheme name. The possible values for **Desired View** are **Default**, **UseLess**, **UseHalf**, **UseMore**, or **UseMinimum**.**Note** Windows takes into account multiple different factors when determining the target app's final window size, for example, the preference of the source app, the number of apps on screen, the screen orientation, and so on. Setting **Desired View** doesn't guarantee a specific windowing behavior for the target app.**Mobile device family: Desired View** isn't supported on the mobile device family. |

1. Enter `images\Icon.png` as the **Logo**.
2. Enter `SDK Sample URI Scheme` as the **Display name**
3. Enter `alsdk` as the **Name**.
4. Press Ctrl+S to save the change to package.appxmanifest.

    This adds an [Extension](/en-us/uwp/schemas/appxpackage/appxmanifestschema/element-1-extension) element like this one to the package manifest. The **windows.protocol** category indicates that the app handles the `alsdk` URI scheme name.

```xml
    <Applications>
        <Application Id= ... >
            <Extensions>
                <uap:Extension Category="windows.protocol">
                  <uap:Protocol Name="alsdk">
                    <uap:Logo>images\icon.png</uap:Logo>
                    <uap:DisplayName>SDK Sample URI Scheme</uap:DisplayName>
                  </uap:Protocol>
                </uap:Extension>
          </Extensions>
          ...
        </Application>
   </Applications>
```

## Step 2: Add the proper icons

Apps that become the default for a URI scheme name have their icons displayed in various places throughout the system such as in the Default programs control panel. Include a 44x44 icon with your project for this purpose. Match the look of the app tile logo and use your app's background color rather than making the icon transparent. Have the logo extend to the edge without padding it. Test your icons on white backgrounds. See [App icons and logos](/en-us/windows/apps/design/style/app-icons-and-logos) for more details about icons.

## Step 3: Handle the activated event

Note

In a WinUI app, in App.OnLaunched (or in fact at any time) you can call ([AppInstance.GetActivatedEventArgs](/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.applifecycle.appinstance.getactivatedeventargs)) to retrieve the activated event args, and check them to determine how the app was activated. See [Application lifecycle functionality migration](/en-us/windows/apps/windows-app-sdk/migrate-to-windows-app-sdk/guides/applifecycle) for more information about lifecycle differences between UWP and WinUI apps.

In UWP apps, the [OnActivated](/en-us/uwp/api/windows.ui.xaml.application.onactivated) event handler receives all activation events. The **Kind** property indicates the type of activation event. This example is set up to handle [Protocol](/en-us/uwp/api/Windows.ApplicationModel.Activation.ActivationKind) activation events.

```csharp
public partial class App
{
   protected override void OnActivated(IActivatedEventArgs args)
  {
      if (args.Kind == ActivationKind.Protocol)
      {
         ProtocolActivatedEventArgs eventArgs = args as ProtocolActivatedEventArgs;
         // TODO: Handle URI activation
         // The received URI is eventArgs.Uri.AbsoluteUri
      }
   }
}
```

```cppwinrt
void App::OnActivated(Windows::ApplicationModel::Activation::IActivatedEventArgs const& args)
{
    if (args.Kind() == Windows::ApplicationModel::Activation::ActivationKind::Protocol)
    {
        auto protocolActivatedEventArgs{ args.as<Windows::ApplicationModel::Activation::ProtocolActivatedEventArgs>() };
        // TODO: Handle URI activation  
        auto receivedURI{ protocolActivatedEventArgs.Uri().RawUri() };
    }
}
```

```cpp
void App::OnActivated(Windows::ApplicationModel::Activation::IActivatedEventArgs^ args)
{
   if (args->Kind == Windows::ApplicationModel::Activation::ActivationKind::Protocol)
   {
      Windows::ApplicationModel::Activation::ProtocolActivatedEventArgs^ eventArgs =
          dynamic_cast<Windows::ApplicationModel::Activation::ProtocolActivatedEventArgs^>(args);
      
      // TODO: Handle URI activation  
      // The received URI is eventArgs->Uri->RawUri
   }
}
```

Note

When launched via Protocol Contract, make sure that Back button takes the user back to the screen that launched the app and not to the app's previous content.

The following code programmatically launches the app via its URI:

```csharp
   // Launch the URI
   var uri = new Uri("alsdk:");
   var success = await Windows.System.Launcher.LaunchUriAsync(uri)
```

For more details about how to launch an app via a URI, see [Launch the default app for a URI](launch-default-app).

It is recommended that apps create a new XAML [Frame](/en-us/uwp/api/Windows.UI.Xaml.Controls.Frame) for each activation event that opens a new page. This way, the navigation backstack for the new XAML **Frame** will not contain any previous content that the app might have on the current window when suspended. Apps that decide to use a single XAML **Frame** for Launch and File Contracts should clear the pages on the **Frame** navigation journal before navigating to a new page.

When launched via Protocol activation, apps should consider including UI that allows the user to go back to the top page of the app.

## Remarks

Any app or website can use your URI scheme name, including malicious ones. So any data that you get in the URI could come from an untrusted source. We recommend that you never perform a permanent action based on the parameters that you receive in the URI. For example, URI parameters could be used to launch the app to a user's account page, but we recommend that you never use them to directly modify the user's account.

Note

If you are creating a new URI scheme name for your app, be sure to follow the guidance in [RFC 4395](https://tools.ietf.org/html/rfc4395). This ensures that your name meets the standards for URI schemes.

Note

When a UWP app is launched via Protocol Contract, make sure that Back button takes the user back to the screen that launched the app and not to the app's previous content.

We recommend that apps create a new XAML [**Frame**](/en-us/uwp/api/Windows.UI.Xaml.Controls.Frame) for each activation event that opens a new Uri target. This way, the navigation backstack for the new XAML **Frame** will not contain any previous content that the app might have on the current window when suspended.

If you decide that you want your apps to use a single XAML [**Frame**](/en-us/uwp/api/Windows.UI.Xaml.Controls.Frame) for Launch and Protocol Contracts, clear the pages on the **Frame** navigation journal before navigating to a new page. When launched via Protocol Contract, consider including UI into your apps that allows the user to go back to the top of the app.
