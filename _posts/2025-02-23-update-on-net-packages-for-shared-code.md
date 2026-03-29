---
title: "Update on .NET Packages for Shared Code"
date: 2025-02-23
categories: ["Development", "Computers and Internet"]
tags: [".NET", "GitHub", "NuGet", "shared code"]
original_url: "https://williamforney.com/2025/02/23/update-on-net-packages-for-shared-code/"
---

![abstract business code coder](https://williamforney.com/wp-content/uploads/2020/09/pexels-photo-270348.jpeg)

Hello all, it’s been a while. I have fixed the build for my (https://github.com/improvgroup/sharedcode) (https://www.nuget.org/profiles/wforney) and pushed a new package update targeting .NET 9 primarily. It should still work with .NET 8 as well. I dropped support for 6 and 7 since they are also out of support from Microsoft at this point. The .NET Core releases are going out much faster than in the old days, so I’ll try to keep these libraries relevant and working in newer versions. I may split some functionality and release a .NET Standard package that could support older projects when I have some free time.

Contributions and suggestions are always welcome. I try to add functionality that complements what’s out there and remove things that I find are better left to other libraries or the framework itself.

That is all for now. Please feel free to leave me issues or feedback on (https://github.com/improvgroup/sharedcode).
