<!--
source: https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/appxmanifestschema/element-protocol
retrieved: 2026-04-01T21:31:11.750395+00:00
final_url: https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/appxmanifestschema/element-protocol
content_type: text/markdown
-->

---
layout: Conceptual
title: Protocol (Windows 8 package schema) - Windows UWP applications | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/appxmanifestschema/element-protocol
ms.subservice: winrt-reference
ms.service: uwp
ROBOTS: INDEX, FOLLOW
author: drewbatgit
ms.author: drewbat
breadcrumb_path: /uwp/breadcrumbs/toc.json
feedback_system: Standard
feedback_product_url: https://github.com/microsoft/WindowsAppSDK
feedback_help_link_url: https://learn.microsoft.com/answers/tags/184/windows-app-sdk/
feedback_help_link_type: get-help-at-qna
uhfHeaderId: MSDocsHeader-WinDevCenter
keywords: windows 10, uwp, schema, package manifest
description: Declares an app extensibility point of type windows.protocol (Windows 8).
Search.Product: eADQiWindows 10XVcnh
ms.assetid: ac911c85-02eb-408c-8c4b-24a4e172df8b
ms.topic: reference
ms.date: 2017-04-05T00:00:00.0000000Z
locale: en-us
document_id: 373d4f4f-0e61-d6ef-d28c-ef33155170e0
document_version_independent_id: 994ba28b-318f-77ed-c0cd-d803a895a4d1
updated_at: 2021-09-20T18:08:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/winrt-related-pr/blob/live/winrt-related-src/schemas/appxpackage/appxmanifestschema/element-protocol.md
gitcommit: https://github.com/MicrosoftDocs/winrt-related-pr/blob/1b8f1d40a191af269148922e1a120d051abb6905/winrt-related-src/schemas/appxpackage/appxmanifestschema/element-protocol.md
git_commit_id: 1b8f1d40a191af269148922e1a120d051abb6905
site_name: Docs
depot_name: MSDN.winrt-related-pr
page_type: conceptual
toc_rel: ../../../toc.json
word_count: 219
asset_id: schemas/appxpackage/appxmanifestschema/element-protocol
moniker_range_name: 
monikers: []
item_type: Content
source_path: winrt-related-src/schemas/appxpackage/appxmanifestschema/element-protocol.md
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/bcbcbad5-4208-4783-8035-8481272c98b8
- https://authoring-docs-microsoft.poolparty.biz/devrel/caec7b7f-4941-4578-b79f-c63b1c1f5af4
- https://authoring-docs-microsoft.poolparty.biz/devrel/ffbd07f7-9210-4df5-8d53-23bfda298bc9
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/43b2e5aa-8a6d-4de2-a252-692232e5edc8
- https://authoring-docs-microsoft.poolparty.biz/devrel/754dea88-f800-4835-b6b5-280cb5d81e88
- https://authoring-docs-microsoft.poolparty.biz/devrel/660ba368-6350-428a-bf85-5ce82f92eed3
platformId: 726c68de-f6df-a707-66bc-7e437fdc9a7b
---

# Protocol (Windows 8 package schema) - Windows UWP applications | Microsoft Learn

Declares an app extensibility point of type **windows.protocol**. A URI association indicates that the app is registered to handle URIs with the specified scheme.

## Element hierarchy

- [&lt;Package&gt;](element-package)
    - - [&lt;Applications&gt;](element-applications)
    - - [&lt;Application&gt;](element-application)
    - - [&lt;Extensions&gt;](element-1-extensions)
    - - [&lt;Extension&gt;](element-1-extension)
    - **&lt;Protocol&gt;**

## Syntax

```syntax
<Protocol Name = A string between 3 and 39 characters in length that contains numbers, lowercased letters, or a hyphen ('-'). >

  <!-- Child elements -->
  ( Logo?
  & DisplayName?
  )

</Protocol>
```

### Key

`?` optional (zero or one)

`&` interleave connector (may occur in any order)

## Attributes and Elements

### Attributes

| Attribute | Description | Data type | Required | Default value |
| --- | --- | --- | --- | --- |
| **Name** | The name of the URI scheme, such as "mailto". This name must be unique for the package. | A string between 3 and 39 characters in length that contains numbers, lowercased letters, or a hyphen ('-'). | Yes |  |

### Child Elements

| Child Element | Description |
| --- | --- |
| [DisplayName](element-2-displayname) | A friendly name that can be displayed to users. |
| [Logo](element-2-logo) | A path to a file that contains an image. |

### Parent Elements

| Parent Element | Description |
| --- | --- |
| [Extension (in type: CT_ApplicationExtensions)](element-1-extension) | Declares an extensibility point for the app. |

## Examples

The following example is taken from the package manifest of one of the SDK samples.

```XML
<Applications>
  <Application Id="App" StartPage="default.html">
    <Extensions>
      <Extension Category="windows.protocol">
        <Protocol Name="alsdk" />
      </Extension>
    </Extensions>
  </Application>
</Applications>
```
