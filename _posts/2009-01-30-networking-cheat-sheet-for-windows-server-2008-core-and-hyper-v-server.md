---
title: "Networking Cheat Sheet for Windows Server 2008 Core and Hyper-V Server"
date: 2009-01-30
categories: ["Computers and Internet", "Hyper-V", "Microsoft"]
tags: ["Disable a NIC", "Disabling a network adapter", "Hyper-V", "Server Core", "Windows Server 2008"]
original_url: "https://williamforney.com/2009/01/30/networking-cheat-sheet-for-windows-server-2008-core-and-hyper-v-server/"
---

Recently I setup a Hyper-V Server and ran into a few issues around networking and setting up a virtual firewall with ISA 2006. It turns out that Hyper-V creates a virtual network adapter for the physical computer and plugs it into the physical adapter which is turned into a de facto network switch. So, if you’re going to use a router or firewall inside a virtual machine you will end up with two network adapters plugged into the “switch” on the external side of your firewall. That might be fine, but it poses a small problem when used in conjunction with Comcast because they see it as two computers and the physical computer may win out and get the external IP while Comcast ignores the other network adapter.

The solution is to disable the virtual adapter that was auto-created for the physical host on your external physical adapter “switch”. Thus Comcast will only see one computer and all will be happy. Searching around for the commands to do this in a Core/Hyper-V console only install of server 2008 proved to be a bit of a trek. After a few days and a few Google searches later I found the answer. Here it is…

Rename a network connection:
    
    
    netsh interface set interface name=”Local Area Connection 3” newname=”Internet Connection”

Disable a network connection:
    
    
    netsh interface set interface name=”Internet Connection” disabled

Pretty simple, but my install of Hyper-V Server also suffered from a bug that luckily has a hot fix. It was showing no interfaces when I ran this:
    
    
    netsh interface show interface

…which is a bug. After I found the patch for that though the rest was done in no time.
