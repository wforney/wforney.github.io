---
title: "Getting Started with Aurelia on ASP.NET Core"
date: 2017-05-22
categories: ["Computers and Internet", "Development"]
tags: ["ASP.NET Core", "Aurelia", "TypeScript", "SPA", "ASP.NET"]
original_url: "https://williamforney.com/2017/05/22/getting-started-with-aurelia-on-asp-net-core/"
---

[Aurelia](http://www.aurelia.io/), one of the leading JavaScript client frameworks for single page applications (SPAs), has been around for a while now and there are a number of resources for getting started with it. Rather than try to make yet another demo, I thought it might be fun to create a site repository that could be used as a template with a few more bells and whistles already setup. It is my hope that this will be useful not just to me, but to anyone else who wants to start a project. We’re going to use the command line tools to do this, but you can use [Visual Studio](http://www.visualstudio.com/) if you want as well.

## Setting up the ASP.NET Core Project

**Prerequisites**

  * [Node.js](https://nodejs.org/en/) (preferably current)
  * [ASP.NET Core SDK](https://www.microsoft.com/net/core#windowscmd)

**Steps**

  1. Create a folder for your project.
  2. Open a command prompt (cmd) in that folder.
  3. Install the SPA templates with the following command:   

         
         dotnet new --install Microsoft.AspNetCore.SpaTemplates::*

  
![screenshot](/assets/img/posts/aurelia-step3.png)

  4. Create the Aurelia project like this:   

         
         dotnet new Aurelia 

  
![screenshot](/assets/img/posts/aurelia-step4.png)

  5. Prepare the environment to run using these commands, ignoring any warnings from npm as they are expected…   

         
         dotnet restore
         npm install
         setx ASPNETCORE_ENVIRONMENT "Development"

  
![screenshot](/assets/img/posts/aurelia-step5a.png)
![screenshot](/assets/img/posts/aurelia-step5b.png)
![screenshot](/assets/img/posts/aurelia-step5c.png)

  6. Restart your command prompt to ensure that the environment change takes effect.
  7. Run your new app with the command line   

         
         dotnet run

  
![screenshot](/assets/img/posts/aurelia-step7.png)

These steps should give you a bare bones ASP.NET Core site with a basic Aurelia setup that looks like this…

![screenshot](/assets/img/posts/aurelia-finish.png)

## Publishing to a Host

Now that you have a working site you’ll want to publish it to an actual server somewhere. To do that you’ll perform a publish. You can do this by running this command:
    
    
    dotnet publish -c Release

This command compiles the server side C# code and runs a [webpack](https://webpack.js.org/) production build on the TypeScript and client assets. You can then find the files to upload to your host in the **_bin\Release\netcoreapp1.1\publish_** folder.

## Exploring the Template

This template takes care of a lot of things that you would have to setup manually and makes a good starting point for adding more functionality, such as logging with Application Insights or another logging provider, fleshing out an administration interface for user management and authentication/authorization using [IdentityServer](https://identityserver.io/), or any number of other useful additions that are widely available.

To get started understanding what we’ve got here, you’ll want to take a look into the files in your new project. You’ll notice that in Startup.cs we have setup a fallback route that allows anything not dealt with by a static file or MVC route to be sent to the Home Index view. This is the secret sauce that lets all your links work even though they aren’t configured individually.
    
    
    routes.MapSpaFallbackRoute(
    name: "spa-fallback",
    defaults: new { controller = "Home", action = "Index" });

To be continued…

