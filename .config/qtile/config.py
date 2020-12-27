#Andrea Locatelli

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import subprocess

from os.path import expanduser  

mod = "mod4"
terminal = "alacritty"

colors = [
    "#472C25",  # panel background
    "#91371B",  # panel background for current screen
    "#F7EFD4",  # font color for active group name
    "#6E6B60",  # font color for inactive group name
    "#FADDAF",  # border line color for current tab
    "#EB712F"   # Selected and active item
]

keys = [
    ## Window 
    Key([mod],  "Left",             lazy.layout.down()),
    Key([mod],  "Right",            lazy.layout.up()),
    Key([mod],  "Up",               lazy.layout.left()),
    Key([mod],  "Down",             lazy.layout.right()),   
    Key([mod,   "shift"], "space",  lazy.layout.rotate()),
    Key([mod,   "shift"], "Return", lazy.layout.toggle_split(),),
    Key([mod],  "q",                lazy.window.kill()),

    Key([mod],  "Left",     lazy.layout.left()),
    Key([mod],  "Right",    lazy.layout.right()),
    Key([mod],  "Up",       lazy.layout.down()),
    Key([mod],  "Down",     lazy.layout.up()),
    Key([mod,   "shift"],   "Left", lazy.layout.swap_left()),
    Key([mod,   "shift"],   "Right", lazy.layout.swap_right()),
    Key([mod,   "shift"],   "Up", lazy.layout.shuffle_up()),
    Key([mod,   "shift"],   "Down", lazy.layout.shuffle_down()),
    
    Key([mod,   "control"], "Left", lazy.layout.grow()),
    Key([mod,   "control"], "Up", lazy.layout.normalize()),
    Key([mod,   "control"], "Right", lazy.layout.shrink()),
    Key([mod,   "control"], "Down", lazy.layout.maximize()),
    Key([mod,   "shift"],   "space", lazy.layout.flip()),
    
    # Menu launcher
    Key([mod], "r",             lazy.spawn("rofi -show drun")),

    # Change keyboard layout
    Key([mod], "space",         lazy.spawn(expanduser("~/.config/myscript/kbdtoggle.sh"))),
    
    Key([mod], "Return",        lazy.spawn(terminal)),
    Key([mod], "Tab",           lazy.next_layout()),
    Key([mod, "control"], "r",  lazy.restart()),
    Key([mod, "control"], "q",  lazy.shutdown()),
]

groups = [
    Group("Home",   layout="MonadTall"),
    Group("Dev",    layout="MonadTall"),
    Group("Web",    layout="MonadTall"),
    Group("Tty",    layout="MonadTall"),
    Group("Spoty",  layout="MonadTall")
]

for index, grp in enumerate(groups):
    keys.extend([
        Key([mod], str(index+1), lazy.group[grp.name].toscreen()),
        Key([mod, "shift"], str(index+1), lazy.window.togroup(grp.name)),
    ])

layout_settings = {
    'border_focus':     colors[5],
    'border_normal':    colors[1],
    'margin':           8,
    'border':           2
}

layouts = [
    layout.MonadTall(**layout_settings),
    layout.MonadWide(**layout_settings),
    layout.Max(**layout_settings),
]

widget_defaults = dict(
    font="UbuntuMono Nerd Font Mono",
    fontsize = 15,
    padding = 4,

)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    background = colors[4],
                    foreground = colors[0],
                    text = "  ",
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('rofi rofi -show drun -theme .config/rofi/left_menu.rasi')},
                ),
                widget.GroupBox(
                    background = colors[0],
                    foreground = colors[2],
                    active = colors[2],
                    inactive = colors[3],
                    this_current_screen_border = colors[5],
                    rounded = False
                ),
                widget.Prompt(),
                widget.WindowName(
                    background = colors[4],
                    foreground = colors[0],
                ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#e3a24d", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.CurrentLayoutIcon(
                    background = colors[0],
                    foreground = colors[2],
                    custom_icon_paths = [expanduser("~/.config/qtile/icon")],
                    scale = 0.6
                ),
                widget.Systray(),
                #widget.CPU(
                #    background = colors[0],
                #    foreground = colors[2],
                #    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' htop')},
                #),
                widget.KeyboardLayout(
                    background = colors[0],
                    foreground = colors[2],
                    configured_keyboard = ['it','us'],

                ),
                #widget.Battery(
                #    background = colors[0],
                #    foreground = colors[2],
                #),
                widget.Clock(
                    background = colors[0],
                    foreground = colors[2],
                    format='%a %H:%M %Y/%m/%d'),
            ],
            26,
        ),
    ),  
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def autostart():
    autostart = expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([autostart])

wmname = "LG3D"
