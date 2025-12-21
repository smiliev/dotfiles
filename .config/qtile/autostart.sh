#!/bin/sh

xinput set-prop 'Xtrfy Xtrfy Wireless Receiver' "libinput Accel Profile Enabled" 0, 1
xinput set-prop 'Xtrfy Xtrfy Wireless Receiver' "libinput Accel Speed" 0

xinput set-prop 'Xtrfy Xtrfy Wireless Mouse' "libinput Accel Profile Enabled" 0, 1
xinput set-prop 'Xtrfy Xtrfy Wireless Mouse' "libinput Accel Speed" 0

xrandr --auto --output HDMI-A-0 --mode 1280x1024 --left-of DisplayPort-0
xrandr --output DisplayPort-0 --primary --mode 1920x1080 --rate 144 --right-of HDMI-A-0

pactl set-default-sink alsa_output.usb-Logitech_Logitech_G430_Gaming_Headset-00.analog-stereo
pactl set-default-source alsa_input.usb-Logitech_Logitech_G430_Gaming_Headset-00.mono-fallback

xset s off
xset -dpms

redshift &
parcellite &
#~/.fehbg &
#nm-applet &
#mictray &
#pasystray &
# picom &
