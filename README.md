# William Forney's GitHub Pages

See **[billforney.com](https://www.billforney.com/)** for my blog.

## Useful links

- [ASP.NET Core](https://www.microsoft.com/net/download/core)

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

## ASP.NET Core

- Publish command
```
dotnet publish -c Release
```

## Notes to self...
---
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
