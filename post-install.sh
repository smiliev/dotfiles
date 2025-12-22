#!/bin/bash

# Installing all necessery packages

read -p "Install packages?(y/n)" pcg
if [ $pcg = "y" ] 
then
	sudo zypper install git ueberzugpp alacritty alacarte parcellite qutebrowser xviewer discord steam mpv htop neofetch ranger wine lutris picom redshift opi 7zip libreoffice xrandr xset xinput sensors pavucontrol playerctl python311-adblock cpu-x dmenu noto-coloremoji-fonts yazi
	git config --global credential.helper store
	opi xarchiver
	opi j4-dmenu-desktop
	opi qt5-webengine-widevinie

	read -p "Install qtile?(y/n)" qtile
	if [ $qtile = "y" ]
	then
		opi qtile
		opi python311-psutil
fi

read -p "Install spotify? (y/n)" spotify
if [ $spotify = "y" ]
then
	opi spotify-easyrpm
	spotify-easyrpm --set-channel edge
	spotify-easyrpm
	opi spotify-adblock
fi

# Moving config files

read -p "Replace config files?(y/n)" rplc

if [ $rplc = "y" ]
then
	cp -r .config ~/

	cp -r .fonts ~/ 
fi
