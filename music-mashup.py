#!/usr/bin/env python2
#    Music MashUp    -    a program to generate fading audio files of song intros, usefull in music quizzes
#    Copyright (C) 2018  Michael Connor Buchan
#
#    Music MashUp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Music MashUp is distributed in the hope that it will be useful, 
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Music MashUp.  If not, see <http://www.gnu.org/licenses/>.

#Import the require_version function to check that we have at least gtk+3.0
from gi import require_version
require_version("Gtk", "3.0")
#at this point, we know we've got at least gtk 2.

#import the AudioSegment class from pydub
from pydub import AudioSegment

#import the gtk modual
from gi.repository import Gtk, Gio

#create the mashup_ui class to house the user interface
class mashup_ui(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Music MashUp")
        self.set_default_size(480, 560)
        self.set_size_request(480, 560)
        self.main_container = Gtk.VBox(spacing=5)
        self.add(self.main_container)
        self.header = self.create_headerbar()
        self.set_titlebar(self.header)
        self.file_tree = self.create_list()
        self.main_container.pack_start(self.file_tree, True, True, 0)
        #some default variables
        self.default_fade_duration = 1.0
        self.cleanup()
    
    def cleanup(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()
    
    
    def start_process(self):
        pass
    
    def add_audio_file(self,widget):
        open_dialog = Gtk.FileChooseropen_dialog("Please choose an audio file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = open_dialog.run()
        if response == Gtk.ResponseType.OK:
            print("File selected: " + open_dialog.get_filename())
            path = open_dialog.get_filename().split("")
            folder = path[:-1]
            folder_path = "/"
            for item in folder:
                folder_path += item + "/"
            file = path[-1]
            filename = file.split(".")[:-1]
            print(folder_path)
            print(file)
            print(filename)
        open_dialog.destroy()
    
    def remove_audio_file(self,widget):
        model, iter = self.current_selection.get_selected()
        if iter is not None:
            model.remove(iter)
    
    def create_headerbar(self):
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title(self.get_title())
        self.export_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-export")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.export_button.set_image(image)
        self.export_button.set_label("Export")
        self.export_button.set_tooltip_text("Export the final audio file.")
        self.export_button.connect("clicked", self.start_process)
        hb.pack_end(self.export_button)
        self.add_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="list-add")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.add_button.set_image(image)
        self.add_button.set_label("add")
        self.add_button.set_tooltip_text("add an audio file to the project.")
        self.add_button.connect("clicked", self.add_audio_file)
        hb.pack_start(self.add_button)
        self.remove_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="list-remove")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.remove_button.set_image(image)
        self.remove_button.set_label("remove")
        self.remove_button.set_tooltip_text("remove an audio file from the project.")
        self.remove_button.connect("clicked", self.remove_audio_file)
        hb.pack_start(self.remove_button)
        return hb
    
    def update_fade_duration(self, widget, path, value):
        self.file_store[path][-1] = float(value)
        #print("value is now", self.file_store[path][-1])
    
    def create_list(self):
        self.file_store = Gtk.ListStore(str, str, float)
        #adds test items to the store
        for i in range(0, 10):
            self.file_store.append(["Invinsible", "/home/mikey/Music", 3.0])
            self.file_store.append(["Blank", "/home/mikey/Documents/great-songs", 5.0])
        self.file_column = Gtk.TreeViewColumn("Track name")
        title = Gtk.CellRendererText()
        self.file_column.pack_start(title, True)
        self.file_column.add_attribute(title, "text", 0)
        self.file_column.set_sort_column_id(0)
        self.path_column = Gtk.TreeViewColumn("Path")
        path = Gtk.CellRendererText()
        self.path_column.pack_start(path, True)
        self.path_column.add_attribute(path, "text", 1)
        self.path_column.set_sort_column_id(1)
        self.fade_duration_column = Gtk.TreeViewColumn("Fade Duration")
        fade_duration = Gtk.CellRendererSpin()
        fade_duration.connect("edited", self.update_fade_duration)
        fade_duration.set_property("editable", True)
        adjustment = Gtk.Adjustment(0, 0, 100, 0.5, 5, 1)
        fade_duration.set_property("adjustment", adjustment)
        self.fade_duration_column.pack_start(fade_duration, True)
        self.fade_duration_column.add_attribute(fade_duration, "text", 2)
        self.fade_duration_column.set_sort_column_id(2)
        list = Gtk.TreeView(self.file_store)
        list.append_column(self.file_column)
        list.append_column(self.path_column)
        list.append_column(self.fade_duration_column)
        self.current_selection = list.get_selection()
        return list

window = mashup_ui()