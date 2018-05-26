#!/usr/bin/env python3
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
        Gtk.ApplicationWindow.__init__(self, title="Music MashUp")
        self.set_default_size(480, 560)
        self.set_size_request(480, 560)
        self.main_container = Gtk.VBox(spacing=12)
        self.add(self.main_container)
        self.header = self.create_headerbar()
        self.set_titlebar(self.header)
        self.file_tree = self.create_list()
        self.main_container.pack_start(self.file_tree, True, True, 0)
        self.no_items_widget = self.create_no_items_widget()
        self.main_container.pack_start(self.no_items_widget, True, True, 0)
        #call a function to set some default variables and create some objects
        self.create_misc()
        self.cleanup()
    
    def cleanup(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        # hide the file_tree until the user adds an item.
        self.file_tree.hide()
        Gtk.main()
    
    def create_misc(self):
        # This is a list of all supported mime types for any audio file that is imported. This list may be incomplete and there may be unusible formats here, so feel free to change it if you find ffmpeg and/or pydub doesn't suport one of these, or supports something else.
        self.supported_mimetypes = ["audio/aiff",
        "audio/aiff",
"audio/basic",
"audio/it",
"audio/make",
"audio/make.my.funk",
"audio/mid",
"audio/midi",
"audio/mod",
"audio/mpeg",
"audio/mpeg3",
"audio/nspaudio",
"audio/s3m",
"audio/tsp-audio",
"audio/tsplayer",
"audio/vnd.qcelp",
"audio/voc",
"audio/voxware",
"audio/wav",
"audio/x-adpcm",
"audio/x-aiff",
"audio/x-au",
"audio/x-gsm",
"audio/x-jam",
"audio/x-liveaudio",
"audio/xm"
"audio/x-mid",
"audio/x-midi",
"audio/x-mod",
"audio/x-mpeg",
"audio/x-mpeg-3",
"audio/x-mpequrl",
"audio/x-nspaudio",
"audio/x-pn-realaudio",
"audio/x-pn-realaudio",
"audio/x-pn-realaudio-plugin",
"audio/x-psid",
"audio/x-realaudio",
"audio/x-twinvq",
"audio/x-twinvq-plugin",
"audio/x-vnd.audioexplosion.mjuicemediafile",
"audio/x-voc",
"audio/x-wav"]
        # Print the list of supported mime types.
        #print self.supported_mimetypes
        self.default_fade_duration = 1.0        #the default amount of time taken to fade from one track to another.
        self.default_length = 10.0        #the length of the track, starting from the beginning
        # Create the "all files" filter
        self.file_filter_all = Gtk.FileFilter()
        self.file_filter_all.set_name("All Files")
        self.file_filter_all.add_pattern("*")
        # Create the "Audio Files" filter
        self.file_filter_audio = Gtk.FileFilter()
        self.file_filter_audio.set_name("Audio Files ")
        for mimetype in self.supported_mimetypes:
            self.file_filter_audio.add_mime_type(mimetype)
        
    # This function creates a Gtk widget that displays the no items message and allows the user to add some files. It is only shown when the list of files is empty.
    def create_no_items_widget(self):
        self.no_items_label = Gtk.Label()
        self.no_items_label.set_markup("<big>Looks like you have no audio files yet.</big>")
        self.no_items_add_button = Gtk.Button("Why not add some?")
        self.no_items_add_button.connect("clicked",self.add_audio_file)
        no_items_box = Gtk.VBox()
        no_items_box.pack_start(self.no_items_label, False, False, 0)
        no_items_box.pack_start(self.no_items_add_button, False, True, 0)
        return no_items_box
    
    # This function starts to process the audio files and generate a final result.
    # It is empty in this branch of the code for now, as I'm working on the interface first.
    def start_process(self):
        pass
    
    # This function handles adding of an audio file to the current project, including the file chooser dialog.
    def add_audio_file(self,widget):
        open_dialog = Gtk.FileChooserDialog("Please choose an audio file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        open_dialog.add_filter(self.file_filter_audio)
        open_dialog.add_filter(self.file_filter_all)
        response = open_dialog.run()
        if response == Gtk.ResponseType.OK:
            # Print the selected file to the console for debugging.
            #print("File selected: " + open_dialog.get_filename())
            # Split the fine path into a list.
            path = open_dialog.get_filename().split("/")
            folder = path[:-1]        # The enclosing folder's path.
            folder_path = ""        # Stores a textual representation of the folder path instead of a list
            for item in folder:
                folder_path += item + "/"
            file = path[-1]        # The selected file's name, with extension.
            filename_list = list(file.split(".")[:-1])        # A list containing the name and extension of the file.
            filename = ""       # Stores the file name withoug extension
            for part in filename_list:
                filename += "." + part
            filename = filename[1:]        # Get rid of the first '.'
            extention = file.split(".")[-1]        # Stores the file extension
            # Print out some of these variables for debugging
            #print(folder_path)
            #print(file)
            #print(filename)
            model, selection = self.current_selection.get_selected()
            self.file_store.insert_after(selection,[filename, folder_path, self.default_fade_duration, self.default_length, extention])        # Add the item to the list
            self.export_button.set_sensitive(True)        # Now that we've added an item, we should allow the user to export their project.
            self.file_tree.set_visible(True)
            self.no_items_widget.hide()        # We've added an item, so we don't need the no items message.
        open_dialog.destroy()
    
    # This function is run when the user removes an audio file from the project
    def remove_audio_file(self,widget):
        model, iter = self.current_selection.get_selected()
        if iter is not None:
            model.remove(iter)
        if len(model) == 0:
            self.export_button.set_sensitive(False)        # There are no audio files, so the user can't export nothing.
            self.file_tree.hide()
            self.no_items_widget.show()
    
    # This function generates the main headerbar with all of the buttons to add, remove and manipulate files in the project, as well as exporting it
    def create_headerbar(self):
        hb = Gtk.HeaderBar(spacing=6)
        hb.set_show_close_button(True)
        hb.set_title(self.get_title())
        self.export_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-export")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.export_button.set_image(image)
        self.export_button.set_label("Export")
        self.export_button.set_tooltip_text("Export the final audio file.")
        self.export_button.connect("clicked", self.start_process)
        self.export_button.set_sensitive(False)
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
        self.remove_button.set_sensitive(False)        # By default, you can't remove a file, because there isn't one to remove.
        hb.pack_start(self.remove_button)
        return hb
    
    # This function updates the Gtk.ListStore data when the user manipulates the fade duration value.
    def update_fade_duration(self, widget, path, value):
        self.file_store[path][2] = float(value)
        # Print what we've just stored for debugging
        #print("value is now", self.file_store[path][-1])
    
    # This function updates the Gtk.ListStore data when the user manipulates the length value.
    def update_length(self, widget, path, value):
        self.file_store[path][3] = float(value)
        # Print what we've just stored for debugging
        #print("value is now", self.file_store[path][-1])
    
    # This function is ran whenever the user selects an item in the list
    def on_list_selection_changed(self,selection):
        model, selected = selection.get_selected()
        if selected == None:
            self.remove_button.set_sensitive(False)
        else:
            self.remove_button.set_sensitive(True)
    
    # This function creates both the Gtk.ListStore for storing the data on the backend, but also creates the Gtk.TreeView widget for the frontend.
    def create_list(self):
        self.file_store = Gtk.ListStore(str, str, float, float, str)
        #adds test items to the store for debugging
        #for i in range(0, 10):
            #self.file_store.append(["Invinsible", "/home/mikey/Music", 3.0, "wav"])
            #self.file_store.append(["Blank", "/home/mikey/Documents/great-songs", 5.0, "mp3"])
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
        self.length_column = Gtk.TreeViewColumn("Length")
        length = Gtk.CellRendererSpin()
        length.connect("edited", self.update_length)
        length.set_property("editable", True)
        length.set_property("adjustment", adjustment)
        self.length_column.pack_start(length, True)
        self.length_column.add_attribute(length, "text", 3)
        self.length_column.set_sort_column_id(3)
        list = Gtk.TreeView(self.file_store)
        list.append_column(self.file_column)
        list.append_column(self.path_column)
        list.append_column(self.fade_duration_column)
        list.append_column(self.length_column)
        self.current_selection = list.get_selection()
        self.current_selection.connect("changed",self.on_list_selection_changed)
        return list

# Create the main object
window = mashup_ui()
