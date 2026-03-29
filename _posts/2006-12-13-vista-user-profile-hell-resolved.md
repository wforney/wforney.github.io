---
title: "Vista user profile hell resolved"
date: 2006-12-13
categories: ["Computers and Internet"]
tags: []
original_url: "https://williamforney.com/2006/12/13/vista-user-profile-hell-resolved/"
---

Well after a bit of tracking things down and booting to safe mode a few times I figured out that the combination of mozy.com’s backup service and windows onecare is what caused the problem. Looks like mozy was trying to backup my registry file while onecare tried to scan it and poof… windows couldn’t access it when i logged in… or something like that anyway. I disabled mozy and logged in, then reconfigured it to not backup that file. Then everything went back to normal. Geesh…
