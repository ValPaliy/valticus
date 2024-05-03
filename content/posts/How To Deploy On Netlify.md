---
title: How To Deploy On Netlify
description: Learn how to create and deploy you website to Netlify.
published: 2021-03-31
author:
  - Val Paliy
keywords:
  - netlify
  - statiq
  - deploy
  - howto
tags:
  - netlify
  - statiq
  - deploy
  - howto
---

The official guide on how to deploy your website to [Netlify](https://www.netlify.com/), which can be found [here](https://www.netlify.com/blog/2016/09/29/a-step-by-step-guide-deploying-on-netlify/), explains the required steps:

- Step 1: Add Your New Site. Creating a new site on Netlify is simple.
- Step 2: Link to Your GitHub (or supported version-control tool of choice)
- Step 3: Authorize [Netlify](https://www.netlify.com/).
- Step 4: Select Your Repo.
- Step 5: Configure Your Settings.
- Step 6: Build Your Site.
- Step 7: All Done.

And it's really as simple as that. The very blog you are exploring at the moment is deployed on [Netlify](https://www.netlify.com/) too, and the score is pretty great, as you can see on [Test My Site](https://testmysite.io/6064bce9a7065f5be16d3cdf/valticus.pro):

{{< figure src="/images/testmysite-results-valticus.webp" title="TestMySite results for Valticus" alt="TestMySite results for Valticus" width="50%" height="50%" >}}

After I had set everything up on [Netlify](https://www.netlify.com/), all I had to do is generate a basic [Statiq](https://statiq.dev/web/) site and push it to the repository from which the this site is deployed via [Netlify](https://www.netlify.com/).

The steps for bootstrapping a Static website are as follows:

- Step 1: Install .NET Core
  Statiq Web consists of .NET Core libraries and installing the .NET Core SDK is the only prerequisite.

- Step 2: Create a .NET Core Console Application
  Create a new console application using the dotnet command-line interface:

`dotnet new console --name MySite`

- Step 3: Install Statiq.Web
  In same folder as your newly created project (i.e. MySite).

`dotnet add package Statiq.Web --version x.y.z`

Use [whatever is the most recent version](https://www.nuget.org/packages/Statiq.Web) of Statiq.Web. The --version flag is needed while the package is pre-release.

- Step 4: Create a Bootstrapper
  Creating a bootstrapper for Statiq Web initializes everything you’ll need to generate your web site. While you can certainly extend Statiq Web with new pipelines or custom modules, you shouldn’t need to for most sites. Add the following code in your Program.cs file:

```
using System.Threading.Tasks;
using Statiq.App;
using Statiq.Web;

namespace MySite
{
public class Program
{
public static async Task<int> Main(string[] args) =>
await Bootstrapper
.Factory
.CreateWeb(args)
.RunAsync();
}
}
```

- Step 5: Add Some Content
  Start adding content by creating Markdown files in your input folder, by default input folder is located in your project root.

To get something served you can add the following code as index.md file in your input folder.

```
## Title: My First Statiq page

# Hello World!

Hello from my first Statiq page.
```

- Step 6: Run it!

  Let the magic happen:

`dotnet run`

This will by default create an output folder in your project folder if it doesn't exists and generate static web site content based on what's in your input folder.

Or run it and preview the generated site:

`dotnet run -- preview`

(I actually did run the site with `--preview` to make sure everything works before I pushed the files to the dedicated repo.) And [as I've stated previously](https://valticus.pro/posts/why-i-dont-use-netlify-cms-yet), [Netlify CMS](https://www.netlifycms.org/) doesn't go well with [Statiq](https://statiq.dev/web/) yet, but I am sure it will change for the better soon enough.

I hope you found this article useful. Thank you very much for taking your time to read it!
