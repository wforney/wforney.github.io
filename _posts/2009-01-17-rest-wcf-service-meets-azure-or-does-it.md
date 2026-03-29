---
title: "REST WCF Service Meets Azure… or does it?"
date: 2009-01-17
categories: ["Development", "Computers and Internet"]
tags: ["REST", "WCF", "Azure", "Message", "Bus", "DestinationUnreachable", "AddressFilter", "EndpointAddress", "EndpointDispatcher", "OperationContext.Current", "AspNetCompatibility"]
original_url: "https://williamforney.com/2009/01/17/rest-wcf-service-meets-azure-or-does-it/"
---

I’ve been playing with a REST WCF service for a bit and noticed when I attempted to add it to Azure’s service bus that it blew up on me. It even goes so far as to kill the development web server in VS2008.

After a little debugging I traced it back to a small bug in the Microsoft.ServiceModel.Web code from the starter kit. Turns out the code relies on the OperationContext.Current which is null unless AspNetCompatibility mode is Allowed or Required, which doesn’t work on Azure (at least not that I could see). So… I fixed that bug and all was well, sort of…

You see, it seems that now I have an endpoint disagreement somewhere because I’m getting this now:

a:DestinationUnreachableThe message with To ‘http://servicebus.windows.net/services/improvGroup/Manager/Contacts/help?apikey=bigGuidHereSnipped’ cannot be processed at the receiver, due to an AddressFilter mismatch at the EndpointDispatcher. Check that the sender and receiver’s EndpointAddresses agree.

I guess I’ll poke around with it later when I have a few hours. Any suggestions?

FOLLOWUP NOTE: I was able to get the service working on Azure if I disable the interceptor that adds the API key check. So, it seems maybe I only partially fixed the previous issue in the starter kit.

Technorati Tags: (http://technorati.com/tags/REST),(http://technorati.com/tags/WCF),(http://technorati.com/tags/Azure),(http://technorati.com/tags/Message),(http://technorati.com/tags/Bus),(http://technorati.com/tags/DestinationUnreachable),(http://technorati.com/tags/AddressFilter),(http://technorati.com/tags/EndpointAddress),(http://technorati.com/tags/EndpointDispatcher),[OperationContext.Current](http://technorati.com/tags/OperationContext.Current),(http://technorati.com/tags/AspNetCompatibility)
