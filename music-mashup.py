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
require_version("Gtk","3.0")
#at this point, we know we've got at least gtk 2.

#import the AudioSegment class from pydub
from pydub import AudioSegment

#import the gtk modual
from gi.repository import Gtk, Gio
#create the mashup_ui class to house the user interface
class mashup_ui(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Music MashUp")
        self.set_default_size(480,560)
        self.set_size_request(480,560)
        self.main_container = Gtk.VBox(spacing=5)
        self.add(self.main_container)
        self.header = self.create_headerbar()
        self.set_titlebar(self.header)
        self.cleanup()
    
    def cleanup(self):
        self.connect("delete-event",Gtk.main_quit)
        self.show_all()
        Gtk.main()
    
    
    def start_process(self):
        pass
    
    def add_audio_file(self):
        pass
    
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
        self.export_button.connect("clicked",self.start_process)
        hb.pack_end(self.export_button)
        self.add_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="list-add")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.add_button.set_image(image)
        self.add_button.set_label("add")
        self.add_button.set_tooltip_text("add an audio file to the project.")
        self.add_button.connect("clicked",self.add_audio_file)
        hb.pack_start(self.add_button)
        return hb

window = mashup_ui()