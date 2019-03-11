#!/usr/bin/env python3

# usage: path to _code_browser.tcd (in your home directory)

import os
import json
import sys
from xml.dom import minidom


def set_color(xmldoc, category, name, color):
    for category_tag in xmldoc.getElementsByTagName("CATEGORY"):
        if category_tag.getAttribute("NAME") == category:
            break

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

    icon = xmldoc.getElementsByTagName("ICON")[0]
    icon.setAttribute("LOCATION", "red-dragon.gif")

    d = os.path.dirname(sys.argv[1])

    filename_out = "%s/_code_browser_dark_night.tcd" % d
    open(filename_out, "w+").write(xmldoc.toprettyxml(indent="    ", newl="\n"))

    print("-> %s" % filename_out)
    print("now open ghidra and select the red dragon")
