---
title: "Item Types"
date: 2005-08-01
categories: ["NewGenesis Portal Framework"]
tags: []
original_url: "https://williamforney.com/2005/08/01/item-types/"
---

As well as those basic types, Items in this new framework can be anything you like. Take files for example since I mentioned the file system was where I got the idea. A class called File could be derived from Item and expose custom properties that are just hooked up to the Attributes and Properties Dictionaries/Lists of the Item type. What needs to happen now is the plumbing to make this possible. I intend to add a few new functions to the Item type to Add/Update and Remove Properties and Attributes without having to manually do the checking if it exists in the dictionary and such. Then our custom properties just use the Item.AddProperty(name,value) function for example in its set and a simple Item.GetProperty(name) in its get. If anyone has a better way to do this, I’m all ears, but this seems the most logical to me at the moment.
