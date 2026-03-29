---
title: "Aurelia with TypeScript on ASP.NET Core"
date: 2016-03-08
categories: ["Computers and Internet", "Development"]
tags: ["ASP.NET"]
original_url: "https://williamforney.com/2016/03/08/aurelia-with-typescript-on-asp-net-core/"
---

![Custom Case Fan Mod](/assets/img/posts/1624452984_9de317e37b1.jpg)

I’ve been tracking the [ASP.NET](https://docs.asp.net/en/latest/ "ASP.NET documentation") betas and release candidates over the past year or more and it’s coming along nicely. I like the separation of client side and server side in the new folder structure and the unification of the [ASP.NET MVC](https://docs.asp.net/en/latest/mvc/index.html) and WebAPI controllers. For the past few years I’ve used [jsViews](http://www.jsviews.com/), [Kendo UI](http://www.telerik.com/kendo-ui), [Angular](https://angular.io/), [Durandal](http://durandaljs.com/), [Knockout](http://knockoutjs.com/), and [Aurelia](http://aurelia.io/) for front end JavaScript development.

A while ago I was using TypeScript with these to help with intellisense and typing issues across the libraries and sites I worked on. I often find myself introducing whatever team I’m on to these technologies in one way or another. I’ve been working with the combination of ASP.NET Core, formerly ASP.NET 5, and Aurelia with TypeScript and Web Components.

I start with the yoeman generator for ASP.NET and add the pieces as I go. I use ASP.NET MVC for the API and plain old HTML and TypeScript for the UI. The client tool chain consists of the usual npm, jspm, and gulp. When the new ASP.NET bits are done I’ll make a template for all this and post it to github. In the meantime I’m considering doing a short video or slide deck walking through the setup if anyone is interested.
