---
title: "Call For Help With The NewGenesis Portal Framework"
date: 2005-08-01
categories: ["NewGenesis Portal Framework"]
tags: []
original_url: "https://williamforney.com/2005/08/01/call-for-help-with-the-newgenesis-portal-framework/"
---

Last week I pushed some updates to the database script and a base set of classes that require some attention. Many of the problems in the current Rainbow Portal project v1.5/beta will be cleared up by use of this back end. The first steps to the future will be DAL and business class layers that replace all data access methods for module developers. Since the framework will use Gentle.NET and iBatis.NET for data access, porting it to any of their supported databases should be trivial for those who know how.

The class layout is structured around the idea of an atomic unit of data called an Item. The idea for this was taken from the file system and will eventually have Permissions and ACL-like properties as well. To support versioning and publishing controls there are several built-in attributes on each Item that allow for this. Language support is added by the concept of Content Items. You see, each Item can be of any type derived from the base Item class, so you see something like this…

Site: a site/installation of the framework

Portal: a single portal inside a Site (for multi-domain and multi-portal installation support)

Page: a page in a Portal (pages have a separate tree structure to allow for navigation to be stored in the database separate from the pages themselves)

Module: a module/WebPart (microsoft copyright?) in a page

Content: this is what makes multi-culture easy. Each Content Item can have a different language, version, etc… This way a Module can easily share content with other Modules in an Item hierarchy (not to be confused with navigation) and can be syndicated in many different ways.

Now that I have laid out the basis for the framework, I need other developers to help me fill in the gaps and fix up the code for testing and production. This initial push shouldn’t take very long to complete and will provide a sound base for the rest of the Module and portal developers to port their data storage to while we refine the framework further in the business layers.
