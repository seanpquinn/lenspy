# Building an Auger themed kiosk

Here you'll find all the necessary code and instructions to install your own visitor kiosk. This kiosk uses a variety of publicly available resources and also records statistics about which pages user visit. These instructions assume the user is working on a Linux based desktop. Moderate Linux/command line skill also assumed. Let's get started.

The finished product should resemble something like this

![](http://headisplay.student.cwru.edu/display/img/display_scrnshot.png)

And the statistics page, which has a plot that corresponds to each tile on the display page, will look like this

![](http://headisplay.student.cwru.edu/display/img/page_stats.png)

## Hardware 

 * Large computer monitor or television
 * Small desktop machine
   * 1 GHz single core processor should be fine (or better)
   * 2 GB system memory
   * 80 GB hard disk
   * Ethernet network adapter
   * Preferably HDMI video output
   * OFC audio jacks
 * 4GB USB thumb drive
 * Trackwheel or keyboard with touchpad: a device whose right click can be disabled is essential to prevent tampering with the web browser.
 
## Installing the operating system

Our kiosk uses Ubuntu Server available at http://www.ubuntu.com/download/server

To create a bootable install image on your thumb drive first insert it into your machine.  Next you want to identify the device ID. A nice tool for this is ```lsblk```

```bash
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0 465.8G  0 disk 
└─sda1   8:1    0 465.8G  0 part /
sdb      8:16   0 3.8G  0 disk 
└─sdb1   8:17   0 3.8G  0 part /media/user
```

