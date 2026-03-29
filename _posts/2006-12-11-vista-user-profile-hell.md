---
title: "Vista user profile hell"
date: 2006-12-11
categories: ["Computers and Internet", "Development"]
tags: []
original_url: "https://williamforney.com/2006/12/11/vista-user-profile-hell/"
---

Well, after a little while running Vista I’ve had a weird thing happen. My user profile fails to load on a fairly new install… Luckily I do most of my work in a VPC image or I’d have been rebuilding my stuff for a week. As it is I’m not sure exactly what the cause is but the event log gives me the awesome error message: The file is in use so we loaded a temporary profile that will get deleted when you log out. Thanks for playing, goodbye. Needless to say I’m a little pissed so I tracked down all the stuff I installed in the last week and removed it. Then I resorted to a file monitor and it looks like it’s either Microsoft Search or Windows OneCare. Guess I get to play with it until it comes back to life.

Anyway, last week was crazy… I’m not the only one who had issues… I had 3 clients’ servers bomb in one way or another and 2 others’ workstations crashed. Luckily nobody lost their data so far, it’s just a huge inconvenience. Hopefully this week will turn out better. Also, there was another LAN party this weekend… Photos to be posted shortly (as soon as I fix this thing enough to get my flash reader working).

Follow Up:

After some investigation I found that it was Mozy.com’s backup service client. They have since come out with a newer version that resolved the issue for me. I suggest that you try the file monitor (task manager > performance > resource monitor button at bottom) to see what is open if you can.
