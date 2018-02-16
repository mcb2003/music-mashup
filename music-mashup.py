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

#Import the require_version function to check that we have at least gtk+2.0
from gi import require_version
require_version("Gtk","2.0")
#at this point, we know we've got at least gtk 2.

#import the AudioSegment class from pydub
from pydub import AudioSegment


