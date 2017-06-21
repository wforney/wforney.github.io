# See **[billforney.com](https://www.billforney.com/)** for my blog.

## Useful links

- [ASP.NET Core](https://www.microsoft.com/net/download/core)
- [Rufus](http://rufus.akeo.ie/)
- [Visual Studio](http://www.visualstudio.com/)
- [Developer Assistant](https://marketplace.visualstudio.com/items?itemName=OneCodeTeam.DeveloperAssistant-13032) for Visual Studio (_Microsoft_)
- [Universal Windows Platform (UWP) app samples](https://github.com/Microsoft/Windows-universal-samples)
- [Design toolkits and resources for UWP apps](https://docs.microsoft.com/en-us/windows/uwp/design-downloads/index)
- [ASP.NET Core (.csproj) Embedded Resources](https://codeopinion.com/asp-net-core-csproj-embedded-resources/)
- [Seven Tips For Using Swagger And AutoRest Together In ASP.NET Core Services](http://michaco.net/blog/TipsForUsingSwaggerAndAutorestInAspNetCoreMvcServices)
- [Productivity Power Tools 2017](https://marketplace.visualstudio.com/items?itemName=VisualStudioProductTeam.ProductivityPowerPack2017)

## Development Environment Setup

```
npm i -g --production windows-build-tools
npm i -g node-gyp
setx PYTHON "%USERPROFILE%\.windows-build-tools\python27\python.exe"
npm i -g typescript tslint
npm i -g eslint jshint
npm i -g aurelia-cli polymer-cli angular-cli
npm i -g yo generator-aspnet generator-polymer generator-aspnetcore-spa
dotnet new --install Microsoft.AspNetCore.SpaTemplates::*
```

### Windows 10 Developer Mode

Registry hack may be required:

Set these to DWORD value 1
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock\AllowAllTrustedApps
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock\AllowDevelopmentWithoutDevLicense
```

_Enable Hyper-V_ for mobile emulators and virtual machines

## ASP.NET Core

- Publish command
```
dotnet publish -c Release
```

## Notes to self about GitHub Markdown...
---
[Prose](http://prose.io/#wforney/wforney.github.io/edit/master/README.md)

You can use the [editor on GitHub](https://github.com/wforney/wforney.github.io/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

```markdown
Syntax highlighted code block

# H1
## H2
### H3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).
