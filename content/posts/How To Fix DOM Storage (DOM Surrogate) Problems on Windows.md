---
title: How To Fix DOM Storage (DOM Surrogate) Problems on Windows
description: If you ever run into a "DOM Surrogate has stopped working" problem, like I did recently, here is a solution that worked (for me).
published: 2022-11-21
author:
  - Val Paliy
keywords:
  - Windows
  - drivers
  - COM Surrogate error
  - fix
  - works
tags:
  - Windows
  - drivers
  - COM Surrogate error
  - fix
  - works
---

So, today, I ran into a problem. Well, it has been bugging me for the last few days, actually. I started
getting the "**COM Surrogate has stopped working**" error.

While Googling did help, not every solution worked for me. What did work is reverting the video card driver
(I have a built-in **Intel HD graphics card**). So this is the first thing I'd suggest you try.

1. To uninstall your current video card driver, first open the **Run** dialog by pressing **Win+R**:

{{< figure src="/images/COMSurrogateRunDialog.webp" title="Windows Run Dialog" alt="Windows Run Dialog" width="75%" height="75%" >}}

2. Type **devmgmt.msc** and hit **Enter**

{{< figure src="/images/COMSurrogatedevmgmt.msc.webp" title="devmgmt.msc" alt="devmgmt.msc" width="75%" height="75%" >}}

3. In the window that opens, find your **display adapter**, right-click, and select **Properties**:

{{< figure src="/images/COMSurrogateDeviceProperties.webp" title="Device Properties" alt="Device Properties" width="75%" height="75%" >}}

4. When the **Properties** window opens, click **Uninstall** to remove the driver. Please note: if you
   have the Roll Back option (it was grayed-out for me at the time), you can try and roll the driver back
   to an earlier version, restart the system and see if the **COM Surrogate has stopped working** error is
   fixed. Otherwise, just uninstall the driver.

{{< figure src="/images/COMSurrogateUninstall.webp" title="Uninstall Driver" alt="Uninstall Driver" width="75%" height="75%" >}}

**Please note:** there is no need to remove the driver, just uninstall it, and reboot your PC.

5. The next step is to install the driver back. The easiest step would be to go and fetch a driver from
   the company that manufactured your graphics card, Or use a driver updater software,
   like [Driver Easy](https://www.drivereasy.com/), for example.

6. After the driver has finished installing, restart your PC and the problem should be fixed. If
   not, let me know - I might be able to help you.

Hope the article was helpful. Have an awesome day!
