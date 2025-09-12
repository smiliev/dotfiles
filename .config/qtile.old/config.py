import os
import subprocess
from typing import Callable, List  # noqa: F401

from libqtile import hook

from libqtile.extension.dmenu import DmenuRun
from libqtile.extension.window_list import WindowList
from libqtile.extension.command_set import CommandSet

# import layout objects
from libqtile.layout.max import Max
from libqtile.layout.xmonad import MonadTall, MonadWide
from libqtile.layout.floating import Floating

# import widgets and bar

from libqtile.config import Click, Drag, DropDown, Group, Key, Match, ScratchPad, Screen
from libqtile.lazy import lazy
# from libqtile.utils import guess_terminal

from colors import gruvbox

from bar1 import bar
from bar1s import bar_small

mod = "mod4"
terminal = "alacritty"
myfont = "TerminessTTF Nerd Font"
# wallpaper = "1651314815321.jpg"
wallpaper = "VwnKIERszZC2_16536x0_Dey4K3h6.jpg"
# terminal = guess_terminal()

keys = [
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod], "x", lazy.to_screen(0)),
    Key([mod], "z", lazy.to_screen(1)),

    # Launch applications
    Key([mod], "w", lazy.spawn('qutebrowser'), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(f'{terminal} -T "ranger" -e ranger'),
        desc="Launch ranger in home directory"),
    Key([mod], "d", lazy.spawn('discord'), desc="Launch discord"),
    Key([mod], "s", lazy.spawn('f{terminal} -T "htop" -e htop'), desc="Launch htop"),
    # Key([mod], "s", lazy.spawn('lutris'), desc="Launch lutris"),
    Key([mod], "a", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Return", lazy.spawn(f'{terminal} sudo yast2')),    

    Key(["shift"], "Alt_L", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
    Key([], "Print", lazy.spawn('xfce4-screenshooter'), desc="Launch xfce4-screenshooter"),
    
    # Command prompt
    # Key([mod], "p", lazy.spawncmd(),
    #     desc="Spawn a command using a prompt widget"),

    # DmenuRun
    # Key([mod], 'r', lazy.run_extension(DmenuRun(
        # font=myfont,
        # fontsize="13",
        # dmenu_command="j4-dmenu-desktop",
        # dmenu_prompt=" ",
        # dmenu_height=10,
        # dmenu_lines=15,
        # background=gruvbox['bg'],
        # foreground=gruvbox['fg'],
        # selected_foreground=gruvbox['dark-blue'],
        # selected_background=gruvbox['bg'],
    # ))),q

    Key([mod], "r", lazy.spawn(f"j4-dmenu-desktop --dmenu=\"dmenu -l 15 -i -fn \'{myfont}-12\' -nb \'{gruvbox['bg']}\' -nf \'{gruvbox['fg']}\' -sb \'{gruvbox['bg']}\' -sf \'{gruvbox['dark-blue']}\'\" --term=\"kitty\"")),

    Key([mod, "shift"], 'w', lazy.run_extension(WindowList(
        all_groups=True,
        font=myfont,
        fontsize="13",
        dmenu_prompt=" ",
        # dmenu_height=10,
        dmenu_lines=15,
        background=gruvbox['bg'],
        foreground=gruvbox['fg'],
        selected_foreground=gruvbox['dark-blue'],
        selected_background=gruvbox['bg'],
    ))),

    Key([mod, "control"], 'n', lazy.run_extension(CommandSet(
        commands={
            'Thesis notes': f'{terminal} nvim Neorg/Notes/Thesis/index.norg',
            'Dev notes': f'{terminal} nvim Neorg/Notes/Dev/index.norg',
            'JWL notes': f'{terminal} nvim Neorg/Notes/JWL/index.norg',
            'YouTube notes': f'{terminal} nvim Neorg/YT/index.norg',
        },
        background=gruvbox['bg'],
        foreground=gruvbox['fg'],
        dmenu_prompt=' ',
        dmenu_lines=10,
        # dmenu_height=10,
        selected_foreground=gruvbox['blue'],
        selected_background=gruvbox['bg'],
    ))),

    # Toggle floating and fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen mode"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(),
        desc="Toggle floating mode"),

    # Keybindings for resizing windows in MonadTall layout
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "control"], "space", lazy.layout.flip()),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),
        desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts as defined below
    Key([mod, "shift"], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    
    # Media keys
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),

    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),

    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),

    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),

    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
]

groups = [
    Group('1', label="一", matches=[
          Match(wm_class='firefox'), Match(wm_class='brave'), Match(wm_class='qutebrowser')], layout="max"),
    Group('2', label="二", layout="monadtall"),
    Group('3', label="三", matches=[Match(title="htop"), Match(title="ranger")], layout="max"),
    Group('4', label="四", matches=[
          Match(wm_class='discord'), Match(wm_class='zoom'), Match(wm_class="teams-for-linux")], layout="max"),
    Group('5', label="五", matches=[Match(wm_class="Spotify")], layout="max"),
    Group('6', label="六", layout="monadtall"),
    Group('7', label="七", layout="monadtall"),
    Group('8', label="八", layout="max"),
    Group('9', label="九", layout="monadtall", screen_affinity="0"),
]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(0),
            desc="Switch to group {}".format(i.name)),
	
        Key([mod, "control"], i.name, lazy.group[i.name].toscreen(1)),  
	
        # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)),
    ])

# Append scratchpad with dropdowns to groups
groups.append(ScratchPad('scratchpad', [
    DropDown('term', terminal, width=0.4, height=0.5, x=0.3, y=0.1, opacity=1),
    DropDown('ranger', f'{terminal} -e ranger', width=0.4, height=0.5, x=0.3, y=0.1, opacity=1),
    DropDown('htop', f'{terminal} -e htop', width=0.4, height=0.5, x=0.3, y=0.1, opacity=1),
    DropDown('mixer', 'pavucontrol', width=0.4,
             height=0.6, x=0.3, y=0.1, opacity=1),
]))

# extend keys list with keybinding for scratchpad
keys.extend([
    Key(["mod1"], "a", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key(["mod1"], "e", lazy.group['scratchpad'].dropdown_toggle('ranger')),
    Key(["mod1"], "s", lazy.group['scratchpad'].dropdown_toggle('htop')),
    Key(["mod1"], "m", lazy.group['scratchpad'].dropdown_toggle('mixer')),
])

layouts = [
    Max(
        border_normal=gruvbox['dark-gray'],
        border_focus=gruvbox['cyan'],
        border_width=1,
        margin=8,
    ),
    MonadTall(
        border_normal=gruvbox['dark-gray'],
        border_focus=gruvbox['cyan'],
        margin=8,
        border_width=2,
        single_border_width=1,
        single_margin=8,
        new_client_position='bottom',
        ratio=0.65,
    ),
]

floating_layout = Floating(
    border_normal=gruvbox['bg0'],
    border_focus=gruvbox['magenta'],
    border_width=2,
    float_rules=[
        *Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry

        Match(title="Android Emulator - pixel5:5554"),
        Match(wm_class="Genymotion Player"),
        Match(title="AICOMS"),
        Match(wm_class="blueman-manager"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="zoom "),
        Match(wm_class="bitwarden"),
        Match(wm_class="nemo"),
        Match(wm_class="xarchiver"),
    ])

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]
widget_defaults = dict(
    font=myfont,
    fontsize=13,
    padding=10,
    foreground=gruvbox['bg'],
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(top=bar,
    wallpaper=f'~/.config/qtile/{wallpaper}',
    wallpaper_mode='stretch'),
    Screen(top=bar_small,
    wallpaper=f'~/.config/qtile/{wallpaper}',
    wallpaper_mode='fill')
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = 'floating_only'
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"


@ hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])

follow_mouse_focus = False

# Icons only
# groups = [
#     Group(""),
#     Group(""),
#     Group(""),
#     Group(""),
#     Group(""),
#     Group(""),
#     Group(""),
#     Group("λ"),
#     Group(""),
#     Group(""),
# ]

# browser, terminal, ranger-monadtall, discord/spotify, vim-stack, steam/lutris-stack/league-stack, home, imageviewer/documentviewer
# binds to open discord, lutris, steam, vim, ranger

