#!/usr/bin/env python3

import os
import signal
from subprocess import call
from gi.repository import Gtk
from gi.repository import AppIndicator3 as AppIndicator

APPINDICATOR_ID = "screenrotator"
orientation = "normal"

def main():
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/home/dom/Git/ScreenRotator/icon.svg'), AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    Gtk.main()

def build_menu():
    menu = Gtk.Menu()
    #Tablet Mode
    item_flip = Gtk.MenuItem('Tablet Mode')
    item_flip.connect('activate', flip_screen)
    menu.append(item_flip)
    #brightness
    item_brightness_up = Gtk.MenuItem('Increase Brightness')
    item_brightness_up.connect('activate', increase_brightness)
    menu.append(item_brightness_up)
    item_brightness_down = Gtk.MenuItem("Decrease Brightness")
    item_brightness_down.connect('activate', decrease_brightness)
    menu.append(item_brightness_down)
    #rotate
    item_rotate = Gtk.MenuItem('Rotate')
    item_rotate.connect('activate', rotate_screen)
    menu.append(item_rotate)
    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)
    #quit
    item_quit = Gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def rotate_screen(source):
    global orientation
    if orientation == "normal":
        direction = "left"
    elif orientation == "left":
        direction ="normal"
    call(["xrandr", "-o", direction])
    orientation = direction

def flip_screen(source):
    global orientation
    if orientation == "normal":
        direction = "inverted"
        call(["xinput", "disable", "SynPS/2 Synaptics TouchPad"])
        call(["xinput", "disable", "AT Translated Set 2 keyboard"])
        call(["gsettings", "set", "org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/", "launcher-hide-mode", "0"])
        call(["xrandr", "-o", direction])
        #call(["onboard"])
    elif orientation == "inverted":
        direction ="normal"
        call(["xinput", "enable", "SynPS/2 Synaptics TouchPad"])
        call(["xinput", "enable", "AT Translated Set 2 keyboard"])
        call(["gsettings", "set", "org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/", "launcher-hide-mode", "1"])
        call(["xrandr", "-o", direction])
        #call(["killall", "onboard"])
    orientation = direction


def increase_brightness(source):
    call(["xbacklight", "-inc", "20"])

def decrease_brightness(source):
    call(["xbacklight", "-dec", "20"])

def quit(source):
    Gtk.main_quit()

if __name__ == "__main__":
    #make sure the screen is in normal orientation when the script starts
    call(["xrandr", "-o", orientation])
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
