---
title: "How to open a “new window” in a Windows 10 Universal App"
date: 2015-08-13
categories: ["Computers and Internet", "Development"]
tags: ["Windows 10", "Universal Apps", "new window", "UWP"]
original_url: "https://williamforney.com/2015/08/13/how-to-open-a-new-window-in-a-windows-10-universal-app/"
---

![Custom Case Fan Mod](https://williamforney.com/wp-content/uploads/2007/10/1624452984_9de317e37b1.jpg)

I had to dig a little bit to find this. Since not all form factors support multiple windows and tablet mode generally discourages floating windows this is probably buried for a reason, but I wanted to do it anyway so here it is:
    
    
     var viewId = 0;
    
     var newView = CoreApplication.CreateNewView();
    await newView.Dispatcher.RunAsync(
    CoreDispatcherPriority.Normal,
    () =>
    {
    var frame = new Frame();
    frame.Navigate(typeof(YourViewPageType), ViewModelDataOrNull);
    Window.Current.Content = frame;
    
    
    
    
    viewId = ApplicationView.GetForCurrentView().Id;
    
    ApplicationView.GetForCurrentView().Consolidated += App.ViewConsolidated;
    
    Window.Current.Activate();
    });
    
    var viewShown = await ApplicationViewSwitcher.TryShowAsStandaloneAsync(viewId);

Hopefully that will save someone some digging. !(https://www.billforney.com/posts/files/036808d6-86a0-4dde-bf48-7542c71f5856.png)

Technorati Tags: (http://technorati.com/tags/Windows+10),(http://technorati.com/tags/Universal+Apps),(http://technorati.com/tags/new+window)
