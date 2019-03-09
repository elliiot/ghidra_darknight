DarkNight theme for [Ghidra](https://github.com/NationalSecurityAgency/ghidra)
==============================================================================

There are still some "bugs" in the display, because actually we can't
configure colors for everything :
 * colors in the Symbol Tree window (function names are hard to read)
 * when the cursor is in code but in an undefined function, the background of the decompilation window turns to white-gray
 * selection in decompilation mode

![ghidra_darknight](/screenshot.png?raw=true)

---

To install the theme, run the script :

    ./set_colors.py ~/.ghidra/.ghidra-9.0/tools/_code_browser.tcd
