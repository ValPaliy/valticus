---
Title: How To Change Your VSCode Theme Depending On The Time Of Day
Description: Would you like to learn how to change your Visual Studio Code theme as time goes by? Read on!
Published: 2021-06-28
Author:
  - Val Paliy
Keywords: [visual studio code, vscode, editor, IDE, theme]
Tags:
  - visual studio code
  - vscode
  - editor
  - IDE
  - theme
---
## How To Change Your VSCode Theme Depending On The Time Of Day

Eye comfort is very important, especially to programmers, who spend most of their day looking at code in their favorite editor.

I've already mentioned a few [themes](https://valticus.netlify.app/tags/theme/) I like, and today I am going to teach you how to set your editor up in such away that the theme changes automatically depending on what time of day it is.

Take a look at the three screenshots above:

<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/theme-morning.png' loading='lazy' alt='Night Owl Light' title='Night Owl Light' class="align_center"><a href="https://marketplace.visualstudio.com/items?itemName=sdras.night-owl"><br />Night Owl Light</a>.</div>

<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/theme-afternoon.png' loading='lazy' alt='Cobalt2' title='Cobalt2' class="align_center"><a href="https://marketplace.visualstudio.com/items?itemName=wesbos.theme-cobalt2"><br />Cobalt2</a>.</div>

<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/theme-night.png' loading='lazy' alt='Night Owl' title='Night Owl' class="align_center"><a href="https://marketplace.visualstudio.com/items?itemName=sdras.night-owl"><br />Night Owl</a>.</div>

The above are the three wonderful editor themes I use throughout the day (***Night Owl Light*** is in effect from 6am to noon, ***Cobalt2*** is noon to 6pm and ***Night Owl*** is my go to theme from 6pm to 6am, because it's, well, perfect for us night owls out there).

To achieve the same you will need to install the two themes plus two additional extensions ([Theme Switcher](https://marketplace.visualstudio.com/items?itemName=savioserra.theme-switcher) by *Sávio Santos Serra* & [Theme switcher](https://marketplace.visualstudio.com/items?itemName=JanBn.vscode-theme-switcher) by *JanBn*), as well as add a couple of lines to your vscode configuration file:

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
*Note: I am using a 24h clock format in this example.*

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
One other tweak I've added to the config file is something to make the sidebar stand out when using ***Night Owl Light***:
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

*I'd like to thank ***Sarah Drasner*** and ***Wes Boss*** for the themes, as well as ***Sávio Santos Serra*** and ***JanBn*** for their theme switching extensions. And I'd like to thank you, ***dear reader***, for taking your time to read this article.* ***Thank you!***