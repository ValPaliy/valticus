---
Title: How To Get macOS Font Rendering In Windows
Description: Let's Talk About Fonts (Part 2) or how to get macOS style font rendering in Windows.
Published: 2021-06-08
Author:
  - Val Paliy
Keywords: [Windows, macOS, Fonts, MacType, GDIPP]
Tags:
  - Windows
  - macOS
  - Fonts
  - MacType
  - GDIPP
---

## How To Get macOS Font Rendering In Windows

Tell me something - are you happy with how ClearType, the default font renderer in <a href="https://valticus.netlify.app/tags/windows">Windows</a> does its job? If you are like me and have to look at your computer screen for the most part of your day, you might prefer something better.

Let me show you something really quick. This is how the fonts are rendered on my Windows machine:

<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/mactype-0.png' loading='lazy' alt='MacType Font Rendering Example' title='MacType Font Rendering Example' class="align_center"></div>

If you would like to achieve similar results, there are only a couple of steps you have to do, and they don't require any tweaking.

First, download and install a free program called MacType <a href="https://www.mactype.net/">from here</a>. Your browser may state that the file you are trying to download is unsafe. This is due to MacType changing the way your fonts look. The file does not contain any suspicious or harmful code.

After you download the file, double click it and follow the setup steps. At some point you will be presented with a few options to chose from:

<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/mactype-1.png' loading='lazy' alt='MacType Font Rendering Example' title='MacType Font Rendering Example' class="align_center"></div></br>
<div class="align_center" style="height:auto; max-width: 100%; border:none; display:block;">
<img src='/img/mactype-2.png' loading='lazy' alt='MacType Font Rendering Example' title='MacType Font Rendering Example' class="align_center"></div>

Chose your favorite startup method and the way you would like the fonts on the screen to be rendered, click <i>Finish</i>.

Don't restart your computer just yet, there is one more little step we have to take to complete the font rendering transformation process on Windows, and that is install GDIPP, to make your Mac fonts even more beautiful. Visit <a href="https://code.google.com/archive/p/gdipp/downloads">GDIPP's Google Code page and chose an installer for either 32 or 64 bit operating systems, depending on what architecture your system is using.

After installing GDIPP, restart your system and enjoy the beautiful macOS fonts in your Windows OS. Should you ever decide to get the old Windows font rendering back, just uninstall MacType and GDIPP like you would any other program on your PC.

<i><b>Note:</b> while I followed the same steps and everything is working fine for me, your mileage may vary. I am not to be held responsible should anything go wrong.</i>

<i>See a related article about fonts <a href="https://valticus.netlify.app/posts/lets-talk-about-fonts">here</a></i>.

Thank you for your time!