define  renamer     = Renamer()
default save_name   = ""

label after_load:
    $ save_name = renamer.savename_temp

init offset = -1

## Renamer #####################################################################
##
## Screens used to name saves and pages

screen renamer_file_slots(title):

    $ pager = Pager()

    use game_menu(title):

        fixed:

            ## The page name, which can be edited by clicking on a button.
            hbox:
                style_prefix "renamer"
                xsize ((config.thumbnail_width + gui.slot_spacing) * 3)
                xpos 84
                ypos 0
                spacing gui.slot_spacing * 3
                hbox:
                    if pager.int > 0:
                        button:
                            text renamer.pagename.get_text()
                            style style.button["renamer_edit"]
                            selected True
                            action Show("renamer_popup", None, "page")
                    else:
                        text renamer.pagename.get_text():
                            xalign 0.0
                            color gui.interface_text_color
                hbox:
                    text _("Current save name:"):
                        xalign 1.0
                        color gui.idle_color
                hbox:
                    button:
                        if save_name == "":
                            text _("(choose a name)") color gui.idle_color
                        else:
                            text save_name
                        style style.button["renamer_edit"]
                        selected True
                        action Show("renamer_popup", None, "save")

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:

                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action [Function(renamer.set_savename_temp, pager, slot), FileAction(slot)]

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:

                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                if pager.int > 10:
                    textbutton _("«") action FilePage(pager.int - 10)
                else:
                    textbutton "" action NullAction()

                if pager.int > 1:
                    textbutton _("<") action FilePagePrevious()
                else:
                    textbutton "" action NullAction()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                for page in pager.rng:
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()

                textbutton _("»"):
                    action FilePage(pager.int + 10)

screen renamer_popup(what):

    default title   = _("How do you want to name your saves?") if (what == "save") else _("How do you want to rename this page?")
    default name    = save_name if (what == "save") else renamer.pagename.get_text()

    modal True
    zorder 1
    style_prefix "renamerpopup"

    frame:
        vbox:
            ## This ensures the input will get the enter event before any of the buttons do.
            order_reverse   False
            text title
            input:
                value ScreenVariableInputValue("name", True, False)
            hbox:
                button:
                    text _("Save")
                    style style.button["renamer_save"]
                    selected True
                    action [Function(renamer.rename, what, name), Hide("renamer_popup")]
                button:
                    text _("Undo")
                    style style.button["renamer_return"]  xpos 0
                    selected True
                    action Hide("renamer_popup")

style renamer_text:
    font                    gui.interface_text_font
    selected_color          gui.interface_text_color
    idle_color              gui.idle_color
    hover_color             gui.hover_color
    selected_hover_color    gui.hover_color

style renamer_hbox:
    xsize                   config.thumbnail_width
    ysize                   50

style renamerpopup_frame:
    xsize                   1000
    ysize                   225
    xpos                    670
    ypos                    200
    xpadding                25
    ypadding                25

style renamerpopup_vbox:
    spacing                 25
    
style renamerpopup_hbox:
    spacing                 250

style renamerpopup_button:
    xsize                   250

style renamerpopup_text is renamer_text

## Code ########################################################################
##
## Classes used to name saves and pages, and to browse pages

init -2 python:

    class Renamer(object):
        """
        A class used to name saves and pages

        Attributes
        ----------
        savename_temp : str
            A temporary save name. Used to temporarily store the name of a save the player is inspecting
        pagename : FilePageNameInputValue
            A renpy object storing the page names

        Methods
        -------
        rename(what, name) : None
            Sets either the name of the page or the name of the save.
        set_savename_temp(pager, slot) : None
            When a player inspects a save, this method assigns its name to savename_temp
        """

        def __init__(self):
            self.savename_temp  = ""
            self.pagename = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"), default=False)

        def rename(self, what, name):
            if what == "save":
                store.save_name = name
            else:
                self.pagename.set_text(name)

        def set_savename_temp(self, pager, slot):
            if (renpy.current_screen().screen_name[0] == "load") and (pager.int > 0):
                full_slot = "{0}-{1}".format(pager.str, slot)
                self.savename_temp = str(renpy.slot_json(full_slot)["_save_name"]).strip()

    class Pager(object):
        """
        A class used to browse regular saves

        Attributes
        ----------
        str : str
            The page number (it's "auto" for the automatic saves page; it's "quick" for the quick saves page)
        int : int
            The page number (it's zero for the automatic saves and quick saves pages)
        rng : [int]
            A list of nine page numbers to be displayed
        """

        def __init__(self):
            self.str    = FileCurrentPage()
            self.int    = 0 if (self.str in ["auto", "quick"]) else int(self.str)
            self.rng    = range(1,10) if (self.int < 6) else range(self.int - 4, self.int + 5)

    for i in ("renamer_edit", "renamer_return", "renamer_save"):
        j = i[8:]
        style.button[i].idle_background             = "images/renamer/idle/{0}.webp".format(j)
        style.button[i].hover_background            = "images/renamer/hover/{0}.webp".format(j)
        style.button[i].selected_background         = "images/renamer/selected/{0}.webp".format(j)
        style.button[i].selected_idle_background    = "images/renamer/selected/{0}.webp".format(j)
        style.button[i].selected_hover_background   = "images/renamer/hover/{0}.webp".format(j)
        style.button[i].padding                     = (50, 0, 0, 0)
