<!--
source: https://learn.microsoft.com/en-us/windows/apps/develop/launch/reserved-uri-scheme-names
retrieved: 2026-04-01T21:31:06.393625+00:00
final_url: https://learn.microsoft.com/en-us/windows/apps/develop/launch/reserved-uri-scheme-names
content_type: text/markdown
-->

---
layout: Conceptual
title: Reserved file and URI scheme names in Windows - Windows apps | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/windows/apps/develop/launch/reserved-uri-scheme-names
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
description: This topic lists the reserved file and URI scheme names that are not available to your Windows app.
ms.date: 2025-02-11T00:00:00.0000000Z
ms.topic: concept-article
keywords: windows 10, uwp, winui, windows 11
ms.localizationpriority: medium
locale: en-us
document_id: 816c6627-5e24-f091-3a4f-4593aa5dfcaa
document_version_independent_id: 816c6627-5e24-f091-3a4f-4593aa5dfcaa
updated_at: 2026-03-06T18:51:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/windows-dev-docs-pr/blob/live/hub/apps/develop/launch/reserved-uri-scheme-names.md
gitcommit: https://github.com/MicrosoftDocs/windows-dev-docs-pr/blob/b29358a19a4eea7ac0621362ad609a994910c973/hub/apps/develop/launch/reserved-uri-scheme-names.md
git_commit_id: b29358a19a4eea7ac0621362ad609a994910c973
site_name: Docs
depot_name: MSDN.windows-uwp-hub
page_type: conceptual
toc_rel: ../toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/MSDN.windows-uwp-hub/{branchName}{pdfName}
feedback_help_link_type: ''
feedback_help_link_url: ''
word_count: 512
asset_id: apps/develop/launch/reserved-uri-scheme-names
moniker_range_name: 
monikers: []
item_type: Content
source_path: hub/apps/develop/launch/reserved-uri-scheme-names.md
cmProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/cd440f3c-1b78-40a7-97ba-aa00a1d79df7
- https://authoring-docs-microsoft.poolparty.biz/devrel/bcbcbad5-4208-4783-8035-8481272c98b8
spProducts:
- https://microsoft-devrel.poolparty.biz/DevRelOfferingOntology/c828f7e0-89b4-459c-9bae-d7ab1c4bd9ad
- https://authoring-docs-microsoft.poolparty.biz/devrel/43b2e5aa-8a6d-4de2-a252-692232e5edc8
platformId: 655f705c-8f24-d417-e70d-65016bd32862
---

# Reserved file and URI scheme names in Windows - Windows apps | Microsoft Learn

You can use URI associations to automatically launch your app when another app launches a specific URI scheme. But there are some URI associations that you can’t use because they are reserved. If your app registers for a reserved association, that registration will be ignored. This topic lists the reserved file and URI scheme names that are not available to your app.

## Reserved file types

There are two types of reserved file types: file types reserved for built-in apps and file types reserved for the operating system. When a file type reserved for a built-in app is launched, only the built-in app will launch. Any attempt to register your app with that file type is ignored. Similarly, any attempt to register your app with a file type reserved for the operating system also will be ignored.

File types reserved for built-in apps:

| File type | File type | File type | File type |
| --- | --- | --- | --- |
| .aac | .icon | .pem | .wdp |
| .aetx | .jpeg | .png | .wmv |
| .asf | .jxr | .pptm | .xap |
| .bmp | .m4a | .pptx | .xht |
| .cer | .m4r | .qcp | .xhtml |
| .dotm | .m4v | .rtf | .xltm |
| .dotx | .mov | .tif | .xltx |
| .gif | .mp3 | .tiff | .xml |
| .hdp | .mp4 | .txt | .xsl |
| .htm | .one | .url | .zip |
| .html | .onetoc2 | .vcf |  |
| .ico | .p7b | .wav |  |

## File types reserved for the operating system

The following file types are reserved for the operating system:

| File type | File type | File type | File type |
| --- | --- | --- | --- |
| .accountpicture-ms | .its | .ops | .url |
| .ade | .jar | .pcd | .vb |
| .adp | .js | .pif | .vbe |
| .app | .jse | .pl | .vbp |
| .appx | .ksh | .plg | .vbs |
| .application | .lnk | .plsc | .vhd |
| .appref-ms | .mad | .prf | .vhdx |
| .asp | .maf | .prg | .vsmacros |
| .bas | .mag | .printerexport | .vsw |
| .bat | .mam | .provxml | .webpnp |
| .cab | .maq | .ps1 | .ws |
| .chm | .mar | .ps1xml | .wsc |
| .cmd | .mas | .ps2 | .wsf |
| .cnt | .mat | .ps2xml | .wsh |
| .com | .mau | .psc1 | .xaml |
| .cpf | .mav | .psc2 | .xdp |
| .cpl | .maw | .psm1 | .xip |
| .crd | .mcf | .pst | .xnk |
| .crds | .mda | .pvw |  |
| .crt | .mdb | .py |  |
| .csh | .mde | .pyc |  |
| .der | .mdt | .pyo |  |
| .dll | .mdw | .rb |  |
| .drv | .mdz | .rbw |  |
| .exe | .msc | .rdp |  |
| .fxp | .msh | .reg |  |
| .fon | .msh1 | .rgu |  |
| .gadget | .msh1xml | .scf |  |
| .grp | .msh2 | .scr |  |
| .hlp | .msh2xml | .shb |  |
| .hme | .mshxml | .shs |  |
| .hpj | .msi | .sys |  |
| .hta | .msp | .theme |  |
| .inf | .mst | .tmp |  |
| .ins | .msu | .tsk |  |
| .isp | .ocx | .ttf |  |

## Reserved URI scheme names

The following URI scheme names are reserved and can't be used by your app:

| URI scheme | URI scheme | URI scheme | URI scheme |
| --- | --- | --- | --- |
| application.manifest | inffile | ms-settings:network-dialup | scrfile |
| application.reference | insfile | ms-settings:network-ethernet | scriptletfile |
| batfile | internetshortcut | ms-settings:network-mobilehotspot | shbfile |
| bing | javascript | ms-settings:network-proxy | shcmdfile |
| blob | jscript | ms-settings:network-wifi | shsfile |
| callto | jsefile | ms-settings:nfctransactions | smb |
| cerfile | ldap | ms-settings:notifications | stickynotes |
| chm.file | lnkfile | ms-settings:personalization | sysfile |
| cmdfile | mailto | ms-settings:privacy-calendar | tel |
| comfile | maps | ms-settings:privacy-contacts | telnet |
| cplfile | microsoft.powershellscript.1 | ms-settings:privacy-customdevices | tn3270 |
| dllfile | ms-accountpictureprovider | ms-settings:privacy-feedback | ttffile |
| drvfile | ms-appdata | ms-settings:privacy-location | unknown |
| dtmf | ms-appx | ms-settings:privacy-messaging | usertileprovider |
| exefile | ms-autoplay | ms-settings:privacy-microphone | vbefile |
| explorer.assocactionid.burnselection | ms-excel | ms-settings:privacy-speechtyping | vbscript |
| explorer.assocactionid.closesession | msi.package | ms-settings:privacy-webcam | vbsfile |
| explorer.assocactionid.erasedisc | msi.patch | ms-settings:proximity | wallet |
| explorer.assocactionid.zipselection | ms-powerpoint | ms-settings:regionlanguage | windows.gadget |
| explorer.assocprotocol.search-ms | ms-settings | ms-settings:screenrotation | windowsmediacenterapp |
| explorer.burnselection | ms-settings:batterysaver | ms-settings:speech | windowsmediacenterssl |
| explorer.burnselectionexplorer.closesession | ms-settings:batterysaver-settings | ms-settings:storagesense | windowsmediacenterweb |
| explorer.closesession | ms-settings:batterysaver-usagedetails | ms-settings:windowsupdate | wmp11.assocprotocol.mms |
| explorer.erasedisc | ms-settings:bluetooth | ms-settings:workplace | wsffile |
| explorer.zipselection | ms-settings:connecteddevices | ms-windows-store | wsfile |
| file | ms-settings:cortanasearch | ms-word | wshfile |
| fonfile | ms-settings:datasense | ocxfile | xbls |
| hlpfile | ms-settings:dateandtime | office | zune |
| htafile | ms-settings:display | onenote |  |
| http | ms-settings:lockscreen | piffile |  |
| https | ms-settings:maps | regfile |  |
| iehistory | ms-settings:network-airplanemode | res |  |
| ierss | ms-settings:network-cellular | rlogin |  |
