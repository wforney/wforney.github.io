---
title: "Getting Started with Aurelia on ASP.NET Core"
date: 2017-05-22
categories: ["Computers and Internet", "Development"]
tags: ["ASP.NET Core", "Aurelia", "TypeScript", "SPA", "ASP.NET"]
original_url: "https://williamforney.com/2017/05/22/getting-started-with-aurelia-on-asp-net-core/"
---

(http://www.aurelia.io/), one of the leading JavaScript client frameworks for single page applications (SPAs), has been around for a while now and there are a number of resources for getting started with it. Rather than try to make yet another demo, I thought it might be fun to create a site repository that could be used as a template with a few more bells and whistles already setup. It is my hope that this will be useful not just to me, but to anyone else who wants to start a project. We’re going to use the command line tools to do this, but you can use (http://www.visualstudio.com/) if you want as well.

## Setting up the ASP.NET Core Project

**Prerequisites**

  * [Node.js](https://nodejs.org/en/) (preferably current)
  * [ASP.NET Core SDK](https://www.microsoft.com/net/core#windowscmd)

**Steps**

  1. Create a folder for your project.
  2. Open a command prompt (cmd) in that folder.
  3. Install the SPA templates with the following command:   

         
         dotnet new --install Microsoft.AspNetCore.SpaTemplates::*

  
[!(https://cdn.billforney.com/posts/files/8b3319ec-e312-4eeb-9563-6c3346824f4a.png)](https://www.billforney.com/posts/files/154a197a-19ee-4157-a105-2f2d112fee1e.png)   

  4. Create the Aurelia project like this:   

         
         dotnet new Aurelia 

  
[!(https://cdn.billforney.com/posts/files/b82a15d9-1c79-4f0f-a9ad-50198bcf6ded.png)](https://www.billforney.com/posts/files/980c3012-e173-4f36-98eb-ffb66fe7a49e.png)   

  5. Prepare the environment to run using these commands, ignoring any warnings from npm as they are expected…   

         
         dotnet restore
         npm install
         setx ASPNETCORE_ENVIRONMENT "Development"

  
[!(https://cdn.billforney.com/posts/files/364730d1-299c-4d28-9882-4755d0bc193b.png)](https://www.billforney.com/posts/files/72c213e6-3bb9-4a0b-8b1b-f2d62d6c8f50.png)   
[!(https://cdn.billforney.com/posts/files/95490758-98b2-4472-b73c-b2b712228082.png)](https://www.billforney.com/posts/files/360c2c5f-4d3a-4e7b-84ef-ebd3004d017c.png)   
[!(https://cdn.billforney.com/posts/files/681fd176-2a30-42c3-8e9f-62377d9cfe4a.png)](https://www.billforney.com/posts/files/334108f7-3756-47fa-8726-dbaaf71520af.png)   

  6. Restart your command prompt to ensure that the environment change takes effect.
  7. Run your new app with the command line   

         
         dotnet run

  
[!(https://cdn.billforney.com/posts/files/fff4a40b-422f-476f-b5d7-01fe75a26160.png)](https://www.billforney.com/posts/files/5066c1b8-af88-4800-8ce9-ff500566c0c6.png)

These steps should give you a bare bones ASP.NET Core site with a basic Aurelia setup that looks like this…

[!(https://cdn.billforney.com/posts/files/9ffcad10-0c8a-448d-baed-92dc878ef2cf.png)](https://www.billforney.com/posts/files/955d3a59-a706-42f3-95f7-379f8e15c720.png)

## 

## 

## Publishing to a Host

Now that you have a working site you’ll want to publish it to an actual server somewhere. To do that you’ll perform a publish. You can do this by running this command:
    
    
    dotnet publish -c Release

This command compiles the server side C# code and runs a (https://webpack.js.org/) production build on the TypeScript and client assets. You can then find the files to upload to your host in the **_bin\Release\netcoreapp1.1\publish_** folder.

## Exploring the Template

This template takes care of a lot of things that you would have to setup manually and makes a good starting point for adding more functionality, such as logging with Application Insights or another logging provider, fleshing out an administration interface for user management and authentication/authorization using (https://identityserver.io/), or any number of other useful additions that are widely available.

To get started understanding what we’ve got here, you’ll want to take a look into the files in your new project. You’ll notice that in Startup.cs we have setup a fallback route that allows anything not dealt with by a static file or MVC route to be sent to the Home Index view. This is the secret sauce that lets all your links work even though they aren’t configured individually.
    
    
    routes.MapSpaFallbackRoute(
    name: "spa-fallback",
    defaults: new { controller = "Home", action = "Index" });

To be continued…

Technorati Tags: [ASP.NET Core](http://technorati.com/tags/ASP.NET+Core),(http://technorati.com/tags/Aurelia),(http://technorati.com/tags/TypeScript),(http://technorati.com/tags/SPA)
