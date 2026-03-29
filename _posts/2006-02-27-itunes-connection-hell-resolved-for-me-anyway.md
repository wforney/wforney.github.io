---
title: "iTunes connection hell resolved… for me anyway…"
date: 2006-02-27
categories: ["Entertainment"]
tags: []
original_url: "https://williamforney.com/2006/02/27/itunes-connection-hell-resolved-for-me-anyway/"
---

After a few weeks without being able to connect to the iTunes Music Store using Apple’s software, I have discovered the cause. Apparrently when the ISA Server 2004 SP2 was released it disabled HTTP Compression, which iTunes relies on to transfer the music store pages.

To fix it go to ISA Server Management > Configuration > General, click on the Define HTTP Compression and add a rule for External to and for/from to Enable it. Then try it. If it doesn’t work it’s probably a setting on one of the other two tabs there.

I found this in the user forums at Apple’s site. Apple themselves are a bunch of nonresponsive, good-for-nothings in my opinion since they didn’t address this AT ALL. Well, there we have it, fixed for now. Of course I’m sure that Apple will blame Microsoft for this mess, but it’s their own fault for not supporting uncompressed HTTP in their application. They’re probably using some proprietary request/response object instead of the windows built-in classes for this. Anyway, good luck to anybody who finds this with a connection issue and I hope it helps solve your problem.
