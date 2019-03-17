#!/usr/bin/env python3

# usage: path to _code_browser.tcd (in your home directory)

import os
import json
import sys
from os.path import expanduser
from xml.dom import minidom
from shutil import copyfile


def set_color(xmldoc, category, name, color):
    found = False
    for category_tag in xmldoc.getElementsByTagName("CATEGORY"):
        if category_tag.getAttribute("NAME") == category:
            found = True
            break

    if not found:
        options_tag = xmldoc.getElementsByTagName("OPTIONS")[0]
        category_tag = xmldoc.createElement("CATEGORY")
        category_tag.setAttribute("NAME", category)
        options_tag.appendChild(category_tag)

    wrapper = xmldoc.createElement("WRAPPED_OPTION")
    wrapper.setAttribute("NAME", name)
    wrapper.setAttribute("CLASS", "ghidra.framework.options.WrappedColor")

    state = xmldoc.createElement("STATE")
    state.setAttribute("NAME", "color")
    state.setAttribute("TYPE", "int")
    state.setAttribute("VALUE", str(color))

    category_tag.appendChild(wrapper)
    wrapper.appendChild(state)


if __name__ == "__main__":
    code_browser_tcd = sys.argv[1]

    xmldoc = minidom.parse(sys.argv[1])

    """
    # debug
    for category in xmldoc.getElementsByTagName("CATEGORY"):
        print('"%s": {' % category.getAttribute("NAME"))
        for tag in category.getElementsByTagName("WRAPPED_OPTION"):
            if tag.getAttribute("CLASS") == "ghidra.framework.options.WrappedColor":
                state = tag.getElementsByTagName("STATE")[0]
                print('    "%s": %d,' % (tag.getAttribute("NAME"), int(state.getAttribute("VALUE"))))
        print("},")
    """

    all_colors = json.loads(open("darknight", "r").read())

    for tag in xmldoc.getElementsByTagName("WRAPPED_OPTION"):
        if tag.getAttribute("CLASS") == "ghidra.framework.options.WrappedColor":
            tag.parentNode.removeChild(tag)

    for category, colors in all_colors.items():
        for name, color in colors.items():
            set_color(xmldoc, category, name, color)

    tool = xmldoc.getElementsByTagName("TOOL")[0]
    tool.setAttribute("TOOL_NAME", "CodeBrowserDarkNight")

    dragon_path = expanduser("~") + "/.ghidra/.ghidra-9.0/tools/black_dragon.png"
    icon = xmldoc.getElementsByTagName("ICON")[0]
    icon.setAttribute("LOCATION", dragon_path)
    copyfile("black_dragon.png", dragon_path)
    print("-> black dragon icon to %s" % dragon_path)

    d = os.path.dirname(sys.argv[1])

    filename_out = "%s/_code_browser_dark_night.tcd" % d
    open(filename_out, "w+").write(xmldoc.toprettyxml(indent="    ", newl="\n"))

    print("-> %s" % filename_out)
    print("now open ghidra and select the black dragon")
