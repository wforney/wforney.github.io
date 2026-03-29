---
title: "How to open a “new window” in a Windows 10 Universal App"
date: 2015-08-13
categories: ["Computers and Internet", "Development"]
tags: ["Windows 10", "Universal Apps", "new window", "UWP"]
original_url: "https://williamforney.com/2015/08/13/how-to-open-a-new-window-in-a-windows-10-universal-app/"
---

I had to dig a little bit to find this. Since not all form factors support multiple windows and tablet mode generally discourages floating windows this is probably buried for a reason, but I wanted to do it anyway so here it is:
    
    
```
 var viewId = 0;

 var newView = CoreApplication.CreateNewView();
await newView.Dispatcher.RunAsync(
CoreDispatcherPriority.Normal,
() =>
{
var frame = new Frame();
frame.Navigate(typeof(YourViewPageType), ViewModelDataOrNull);
Window.Current.Content = frame;
```
    
    
    
```
viewId = ApplicationView.GetForCurrentView().Id;

ApplicationView.GetForCurrentView().Consolidated += App.ViewConsolidated;

Window.Current.Activate();
});

var viewShown = await ApplicationViewSwitcher.TryShowAsStandaloneAsync(viewId);
```
Hopefully that will save someone some digging. *[image: Smile]*

Technorati Tags: [Windows 10](http://technorati.com/tags/Windows+10),[Universal Apps](http://technorati.com/tags/Universal+Apps),[new window](http://technorati.com/tags/new+window)
