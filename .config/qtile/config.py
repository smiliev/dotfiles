# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess

from libqtile.core.manager import Qtile

mod = "mod4"
terminal = guess_terminal()
wallpaper_path = '~/.config/qtile/wallpapers/world-of-warcraft-classic-raid-uhd-4k-wallpaper.jpg'

def spawn_dmenu(qtile):
    qtile.spawn(f"j4-dmenu-desktop --dmenu='dmenu -m {qtile.current_screen.index} -i -fn \"TerminessTTF Nerd Font:size=16\" -nb \"#000000\" -nf \"#ffffff\" -sf \"#ffffff\"'")

def swap_screens(qtile):
    if len(qtile.screens) < 2:
        return
    
    s1 = qtile.screens[0]
    s2 = qtile.screens[1]
    g1 = s1.group
    g2 = s2.group
    
    # Perform the swap
    s1.set_group(g2)
    s2.set_group(g1)

    focus_current_screen(qtile)

def focus_current_screen(qtile):
    # Get the index of the currently focused screen
    current_index = qtile.current_screen.index
    other_index = 1 - current_index

    qtile.to_screen(other_index)
    qtile.to_screen(current_index)

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "e", lazy.spawn("thunar"), desc="Launch Thunar file manager"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.function(spawn_dmenu), desc="Launch dmenu on current screen"),
    # Volume control keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%"), desc="Increase volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%"), desc="Decrease volume"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Toggle mute"),
    # Media control keys
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next track"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous track"),
    # Focus screens
    Key([mod], "z", lazy.to_screen(1), lazy.function(focus_current_screen), desc="Focus left screen"),
    Key([mod], "x", lazy.to_screen(0), lazy.function(focus_current_screen), desc="Focus right screen"),
    Key([mod], "s", lazy.function(swap_screens), desc="Swap workspaces between screens"),

    Key(["shift"], "Alt_L", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(), lazy.function(focus_current_screen),
            desc="Switch to group {}".format(i.name)),
	
        # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(border_focus="#225377", border_width=2),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
]

widget_defaults = dict(
    font="TerminessTTF Nerd Font",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper=wallpaper_path,
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Spacer(),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.KeyboardLayout(
                    configured_keyboards=['us', 'bg bas_phonetic'],
                    display_map={'us': 'EN', 'bg bas_phonetic':'BG'},
                    padding=5,
                ),
                widget.Systray(),
                
                widget.TextBox("cpu:", padding=5),
                widget.CPUGraph(
                    graph_color='#18BAEB',
                    fill_color='#1667EB.3',
                    border_width=1,
                    border_color='#18BAEB',
                    width=80,
                ),
                widget.TextBox("mem:", padding=5),
                widget.MemoryGraph(
                    graph_color='#00FE00',
                    fill_color='#00FE00.3',
                    border_width=1,
                    border_color='#00FE00',
                    width=80,
                ),
                widget.Clock(format="%a %b %d"),
                widget.Clock(format="%I:%M %p"),
                widget.QuickExit(),
            ],
            26,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        wallpaper=wallpaper_path,
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Spacer(),
                widget.Clock(format="%a %b %d"),
                widget.Clock(format="%I:%M %p"),
            ],
            26,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# 1. Fix the focus_screen order
def fixed_focus_screen(self, n, warp=True):
    if n >= len(self.screens):
        return
    old = self.current_screen
    self.current_screen = self.screens[n]
    if old != self.current_screen:
        hook.fire("current_screen_change")
        hook.fire("setgroup")
        # Change: focus NEW group first, then re-layout OLD group
        self.current_group.focus(self.current_window, warp)
        old.group.layout_all()
        if self.current_window is None and warp:
            self.warp_to_screen()

Qtile.focus_screen = fixed_focus_screen

# 2. Fix the Screen.set_group swap logic
def fixed_set_group(self, new_group, save_prev=True, warp=True):
    if new_group is None:
        return
    if new_group.screen == self:
        return
    if save_prev and new_group is not self.group:
        self.previous_group = self.group

    if new_group.screen:
        g1, s1 = self.group, self
        g2, s2 = new_group, new_group.screen
        with self.qtile.core.masked():
            s2.group, s1.group = g1, g2
            # Swap order based on which screen is currently focused
            if s1 == self.qtile.current_screen:
                g2.set_screen(s1, warp)
                g1.set_screen(s2, warp)
            else:
                g1.set_screen(s2, warp)
                g2.set_screen(s1, warp)
    else:
        # Standard non-swap logic
        old_group = self.group
        self.group = new_group
        with self.qtile.core.masked():
            new_group.set_screen(self, warp)
            if old_group is not new_group:
                old_group.set_screen(None, warp)
    
    hook.fire("setgroup")
    hook.fire("focus_change")
    hook.fire("layout_change", self.group.layouts[self.group.current_layout], self.group)

Screen.set_group = fixed_set_group
