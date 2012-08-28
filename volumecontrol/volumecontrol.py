#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    import alsaaudio
    HAVEALSA=True
except:
    import subprocess
    import commands
    HAVEALSA=False
import pygtk
pygtk.require('2.0')
import gtk

class VolumeControl():

    def __init__(self):
        builder=gtk.Builder()
        builder.add_from_file("volumecontrol.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("volumewindow")
        self.window_position = (0, 0)
        self.staticon = builder.get_object("staticon")
        self.menu = builder.get_object("menu")
        self.masterslider = builder.get_object("masterslider")

    def close_window(self, widget, data=None):
        gtk.main_quit()

    def button_clicked(self, widget):
        os.system('gnome-alsamixer')

    def window_show(self, widget, data=None):
        if self.window.get_property('visible'):
            self.window.hide()
        else:
            self.masterslider.set_value(self.get_master_volume())
            self.set_window_position()
            self.window.move(self.window_position[0], self.window_position[1])
            self.window.show_all()
            self.window.present()
            
    def menu_popup(self, widget, button, time, data = None):
        if button == 3:
            self.menu.show_all()
            self.menu.popup(None, None, None, 3, time)

    def masterslider_change(self, widget):
        volume = int(widget.get_value())
        if HAVEALSA:
            mix = alsaaudio.Mixer()
            mix.setvolume(volume)
        else:
            proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(volume) + '%', shell=True, stdout=subprocess.PIPE)
            proc.wait()

    def set_window_position(self):
        staticon_geometry = self.staticon.get_geometry()[1]
        if staticon_geometry.y <= 200:
            y_coords = staticon_geometry.y
        else:
            y_coords = staticon_geometry.y-180
        self.window_position = (staticon_geometry.x+20, y_coords+10)

    def get_master_volume(self):
        if HAVEALSA:
            mix = alsaaudio.Mixer()
            return mix.getvolume()[0]
        else:
            output = commands.getoutput('/usr/bin/amixer sget Master | grep "%"')
            master = output.split('\n')[0]
            start = master.find('[') + 1
            end = master.find('%]', start)
            return float(master[start:end])

    def aboutdialog(self, widget, data=None):
        about = gtk.AboutDialog()
        about.set_program_name('Volume Control')
        about.set_version('1.0')
        about.set_comments(u'Πρόγραμμα ελέγχου της στάθμης του ήχου.')
        about.run()
        about.destroy()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    app=VolumeControl()
    app.main()
