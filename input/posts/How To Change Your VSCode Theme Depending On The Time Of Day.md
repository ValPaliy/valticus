---
Title: How To Change Your VSCode Theme Depending On The Time Of Day
Description: Would you like to learn how to change your Visual Studio Code theme as time goes by? Read on!
Published: 2021-06-28
Author:
  - Val Paliy
Keywords:
  - visual studio code
  - vscode
  - editor
  - IDE
  - theme
Tags:
  - visual studio code
  - vscode
  - editor
  - IDE
  - theme
---

## How To Change Your VSCode Theme Depending On The Time Of Day

Eye comfort is very important, especially to programmers, who spend most of their day looking at code in their favorite editor.

I've already mentioned a few [themes](https://valticus.pro/tags/theme/) I like, and today I am going to teach you how to set your editor up in such away that the theme changes automatically depending on what time of day it is.

Take a look at the three screenshots above:

<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/theme-morning.png' loading='lazy' alt='Night Owl Light' title='Night Owl Light' class="align_center"><a href="https://marketplace.visualstudio.com/items?itemName=sdras.night-owl"><br />Night Owl Light</a>.</div>

<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/theme-afternoon.png' loading='lazy' alt='Cobalt2' title='Cobalt2' class="align_center"><a href="https://marketplace.visualstudio.com/items?itemName=wesbos.theme-cobalt2"><br />Cobalt2</a>.</div>

<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/theme-night.png' loading='lazy' alt='Night Owl' title='Night Owl' class="align_center"><a href="https://marketplace.visualstudio.com/items?itemName=sdras.night-owl"><br />Night Owl</a>.</div>

The above are the three wonderful editor themes I use throughout the day (**_Night Owl Light_** is in effect from 6am to noon, **_Cobalt2_** is noon to 6pm and **_Night Owl_** is my go to theme from 6pm to 6am, because it's, well, perfect for us night owls out there).

To achieve the same you will need to install the two themes plus two additional extensions ([Theme Switcher](https://marketplace.visualstudio.com/items?itemName=savioserra.theme-switcher) by _Sávio Santos Serra_ & [Theme switcher](https://marketplace.visualstudio.com/items?itemName=JanBn.vscode-theme-switcher) by _JanBn_), as well as add a couple of lines to your vscode configuration file:

```
  "themeSwitcher.themesList": "Night Owl Light, Cobalt2, Night Owl",
  "themeswitcher.utcOffset": 3,
  "themeswitcher.mappings": [
    {
      "time": "06:00",
      "theme": "Night Owl Light"
    },
    {
      "time": "12:00",
      "theme": "Cobalt2"
    },
    {
      "time": "18:00",
      "theme": "Night Owl"
    }
  ]
```

_Note: I am using a 24h clock format in this example._

Technically, the very first line is only necessary if you are planning to also switch between themes via shortcuts, like I do:

```
  {
    "key": "f5",
    "command": "themeSwitcher.previousSelectedTheme"
  },
  {
    "key": "f6",
    "command": "themeSwitcher.nextSelectedTheme"
  }

```

One other tweak I've added to the config file is something to make the sidebar stand out when using **_Night Owl Light_**:

```
  "workbench.colorCustomizations": {
    "[Night Owl Light]": {
      "sideBar.foreground": "#000000"
    },
    "[Night Owl Light (No Italics)]": {
      "sideBar.foreground": "#000000"
    }
  }
```

That's it. Now, depending on the time of day, your IDE will look different, and you will not have to worry about your eyes getting tired.

Few updates: there's yet another, a little different theme by [Sarah Drasner](https://sarahdrasnerdesign.com/) called [In Bed by 7pm](https://marketplace.visualstudio.com/items?itemName=sdras.inbedby7pm), which you can easily integrate into your theme switching routine as a fourth theme like I did:

```
  "themeswitcher.mappings": [
    {
      "time": "06:00",
      "theme": "Night Owl Light"
    },
    {
      "time": "12:00",
      "theme": "Cobalt2"
    },
    {
      "time": "18:00",
      "theme": "In Bed by 7pm"
    },
    {
      "time": "00:00",
      "theme": "Night Owl"
    }
```

I might end up using just the **_Night Owl_** and **_In Bed by 7pm_**.

\*I'd like to thank **_Sarah Drasner_** and **_Wes Boss_** for the themes, as well as **_Sávio Santos Serra_** and **_JanBn_** for their theme switching extensions. And I'd like to thank you, **_dear reader_**, for taking your time to read this article.\* **_Thank you!_**
