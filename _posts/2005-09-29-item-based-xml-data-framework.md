---
title: "Item-based xml data framework"
date: 2005-09-29
categories: ["NewGenesis Portal Framework"]
tags: []
original_url: "https://williamforney.com/2005/09/29/item-based-xml-data-framework/"
---

After getting my feet wet with xslt and learning its ins and outs I started building an xml file with the structure for our item-based data framework. Once completed I can infer the schema from it and generate a set of sql structures that reflect what is being stored in the xml. After that a simple web service can handle the data link and the entire thing can be stored in most databases without too much effort. Tie this into the .NET v2 web parts and other features for security and we’ll be most of the way there. Here is the first run draft of the xml file I’m working on… Keep in mind it isn’t complete and will probably change a bit:

<?

xml version="1.0" encoding="utf-8" ?>  
<database>  
<items>  
<item id="{29C50162-DF78-4ff7-85E1-7AE0BE0E1CC6}"

typeId="{4CE15CC7-147F-4db8-B077-EA09A109A092}"

templateId="{B4DC911D-3E87-4061-AC22-61A9C7E25949}"

statusId="{C2CF0809-3FF1-4fa3-AFE2-7070F6503635}"

international="en-US"

version="1"

creationUserId="{B29DA606-AE45-49ff-94BE-A144AE350A08}"

creationDate=""

isEncrypted="false">

<

settings>

<

setting name="name">value</setting>

</

settings>

<

permissions>

<

permission id="0">

<

allowed>

<

user id="{B29DA606-AE45-49ff-94BE-A144AE350A08}" />

<

group id="{E3423DBD-398D-4e85-8ED3-FC4B4527B43C}" />

</

allowed>

<

denied>

<!–

<user id="{B29DA606-AE45-49ff-94BE-A144AE350A08}" />–>

<

group id="{BD326688-AC38-4026-96D1-234428462243}" />

</

denied>

</

permission>

</

permissions>

<

content><![CDATA]></content>

</

item>

</

items>

<

itemTypes>

<

itemType id="{81AA36D5-893E-4848-9DC7-C1732447AED3}" name="Site"

description="A single application installation which may contain multiple portals" />

<

itemType id="{6BFFDCEC-77F4-40d9-98E6-23636055AF47}" name="Portal"

description="A portal or subsite within a Site" />

<

itemType id="{AACC3CC9-6665-45a9-8DF6-F105A662ADD6}" name="Page"

description="A page within a Portal" />

<

itemType id="{BE5974A1-F881-47f5-8B95-D278D422AD0F}" name="Module"

description="A module or WebPart" />

<

itemType id="{4CE15CC7-147F-4db8-B077-EA09A109A092}" name="Content"

description="A content object which is associated with a Module" />

</

itemTypes>

<

itemTemplates>

<

itemTemplate id="{B4DC911D-3E87-4061-AC22-61A9C7E25949}"

itemTypeId="{4CE15CC7-147F-4db8-B077-EA09A109A092}"

statusId="{C2CF0809-3FF1-4fa3-AFE2-7070F6503635}"

name="Content Template"

international="en-US"

version="1"

creationUserId="{B29DA606-AE45-49ff-94BE-A144AE350A08}"

creationDate=""

isEncrypted="false">

<

categories>

<

category id="{1C5903DA-21F0-44e8-9CA9-308B1795EFDB}" />

</

categories>

<

content><![CDATA]></content>

</

itemTemplate>

</

itemTemplates>

<

statuses>

<

status id="{C2CF0809-3FF1-4fa3-AFE2-7070F6503635}" name="Active">

<

categories>

<

category id="{1C5903DA-21F0-44e8-9CA9-308B1795EFDB}" />

</

categories>

</

status>

</

statuses>

<

categories>

<

category id="{1C5903DA-21F0-44e8-9CA9-308B1795EFDB}" name="General"

description="General / Generic Category" />

</

categories>

<

permissions>

<

permission id="0" name="Read" description="Access to read from an object" />

<

permission id="1" name="Write" description="Access to write to an object" />

<

permission id="2" name="Modify" description="Access to modify an object" />

<

permission id="3" name="Delete" description="Access to delete an object" />

</

permissions>

<

users>

<

user id="{B29DA606-AE45-49ff-94BE-A144AE350A08}"

displayName="William Forney" firstName="William" middleName="Lee" lastName="Forney"

emailAddress="[email address redacted]"

password="" />

</

users>

<

groups>

<

group id="{BD326688-AC38-4026-96D1-234428462243}" displayName="Users">

<

members>

<

user id="{B29DA606-AE45-49ff-94BE-A144AE350A08}" />

<

group id="{E3423DBD-398D-4e85-8ED3-FC4B4527B43C}" />

</

members>

</

group>

<

group id="{E3423DBD-398D-4e85-8ED3-FC4B4527B43C}" displayName="Administrators" />

</

groups>

</

database>
