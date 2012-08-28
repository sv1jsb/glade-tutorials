#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import gtk
import os
import codecs

CODEPAGES = ['utf_16','utf_8','cp1253','iso8859_7']
EOL = ['Windows','Unix','Mac']
DICT_EOL = {'Windows':'\r\n','Unix':'\n','Mac':'\r'}

class FileToConvert(object):

    def __init__(self,fn = None, cp = None, eol=None):
        self.fn = fn
        self.cp = cp
        self.eol = eol
        self.to_cp = ''
        self.to_eol = ''

    def checkfile(self,codefrom=None):
        encodings=CODEPAGES
        if codefrom:
            encodings=[codefrom]
        for enc in encodings:
            t1=codecs.open(self.fn,'r',enc)
            try:
                line=t1.readline()
                if '\r\n' in line:
                    self.eol = EOL[0]
                elif '\n' in line:
                    self.eol = EOL[1]
                elif '\r' in line:
                    self.eol = EOL[2]
                self.cp=enc
                t1.close()
                ret=True
                break
            except:
                ret=False
        return ret       

class ConvertFiles(object):

    def close_window(self, widget, data=None):
        gtk.main_quit()

    def delete_chooser(self, widget, data=None):
        return True

    def aboutmenu_clicked(self, widget, data=None):
        self.aboutdialog.run()
        self.aboutdialog.hide()

    def helpmenu_clicked(self, widget, data=None):
        import webbrowser
        webbrowser.open("help.html")

    def openmenu_clicked(self, widget, data=None):
        self.filechooser.show()

    def filterbox_changed(self, widget, data=None):
        if widget.get_active() == 0:
            self.filechooser.set_filter(self.txtfilter)
        if widget.get_active() == 1:
            self.filechooser.set_filter(self.srtfilter)
        if widget.get_active() == 2:
            self.filechooser.set_filter(self.allfilter)                

    def filelistview_key(self, widget, data=None):
        treeviewmodel, treeviewindex = widget.get_selection().get_selected()
        if (gtk.gdk.keyval_name(data.keyval) == 'Delete') and treeviewindex:
            treeviewmodel.remove(treeviewindex)

    def filelist_row_deleted(self,widget,data=None):
        del self.files[data[0]]
        self.statusbar.push(0,"Αφαίρεση αρχείου")

    def filechooser_cancel(self, widget, data=None):
        self.filechooser.hide()

    def filechooser_ok(self, widget, data=None):
        filenames=[]
        if self.files:
            for fi in self.files:
                filenames.append(fi.fn)
        errortxt=''
        i=0
        for fi in self.filechooser.get_filenames():
            if fi not in filenames:
                newfile = FileToConvert(fi)
                if newfile.checkfile():
                    self.files.append(newfile)
                    self.filelist.append([newfile.fn,newfile.cp,newfile.eol])
                    i+=1
                else:
                    errortxt+=u"Πρόβλημα στην ανάγνωση του αρχείου: %s.\n" % cf.fn
                    self.errordialog(errortxt)
        self.filechooser.hide()  
        if i>0:
            self.statusbar.push(0,u"Επιτυχής αναγνωση %d αρχείων" % i)
        else:
            self.statusbar.push(0,"")

    def errordialog(self, errortxt):
        dialog=gtk.MessageDialog(parent=None,flags=gtk.DIALOG_MODAL & gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
        dialog.set_title(u"Σφάλμα")
        dialog.set_markup(u"<b>"+errortxt+"</b>")
        response=dialog.run()
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_OK:
           dialog.destroy() 

    def savemenu_clicked(self, widget, data=None):
        errortxt=''
        if not self.files:
            self.errordialog(u"Δεν έχετε επιλέξει αρχεία.\n")
            return
        for fi in self.files:
            if self.codefrombox.get_active()>0:
                if not fi.checkfile(CODEPAGES[self.codefrombox.get_active()-1]):
                    errortxt+=u"Πρόβλημα στην ανάγνωση του αρχείου: %s.\n" % fi.fn
        if errortxt:
            self.errordialog(errortxt)
            self.statusbar.push(0,u"Δεν ήταν σωστή η κωδικοποίηση που ορίσατε.")
            return
        for i in range(len(self.files)):
            self.files[i].to_cp=CODEPAGES[self.codetobox.get_active()]
            self.files[i].to_eol=EOL[self.eolbox.get_active()]
        treeiter=self.filelist.get_iter_first()
        for fi in self.files:
            try:
                t1=codecs.open(fi.fn,'r',fi.cp)
                t2=codecs.open('tmp','w',fi.to_cp)
                for line in t1:
                    line=line.replace(DICT_EOL[fi.eol],DICT_EOL[fi.to_eol])
                    t2.write(line)
                t2.close()
                t1.close()
                os.rename('tmp',fi.fn)
            except:
                self.errordialog(u"Πρόβλημα στην μετατροπή του %s.\n" % fi.fn)
                success=False
            else:
                if fi.checkfile():
                    self.filelist.set_value(treeiter,1,fi.cp)
                    self.filelist.set_value(treeiter,2,fi.eol)
                    fi.to_cp = ''
                    fi.to_eol = ''
                    success=True
                else:
                    self.errordialog(u"Πρόβλημα στην τελική ανάγνωση του %s.\n" % fi.fn)
                    success=False
            treeiter=self.filelist.iter_next(treeiter)
        if success:
            self.statusbar.push(0,u"Επιτυχής μετατροπή")
        else:
            self.statusbar.push(0,u"Προβλήματα στην μετατροπή")
        
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("convert.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("convertwindow")
        self.codefrombox = builder.get_object("codefrombox")
        self.codetobox = builder.get_object("codetobox")
        self.eolbox = builder.get_object("eolbox")
        self.codefromlist = builder.get_object("codefromlist")
        self.codetolist = builder.get_object("codetolist")
        self.eollist = builder.get_object("eollist")
        self.filelist = builder.get_object("filelist")
        self.codefromlist.append([u"Μαντεψιά"])
        for item in CODEPAGES:
            self.codefromlist.append([item])
            self.codetolist.append([item])
        for item in EOL:
            self.eollist.append([item])
        self.codefrombox.set_active(0)
        self.codetobox.set_active(0)
        self.eolbox.set_active(0)
        self.filechooser = builder.get_object("filechooser")
        self.aboutdialog = builder.get_object("aboutdialog")
        self.txtfilter = builder.get_object("txtfilter")
        self.srtfilter = builder.get_object("srtfilter")
        self.allfilter = builder.get_object("allfilter")
        self.filterbox = builder.get_object("filterbox")
        self.txtfilter.add_pattern('*.txt')
        self.txtfilter.add_pattern('*.TXT')
        self.srtfilter.add_pattern('*.srt')
        self.srtfilter.add_pattern('*.SRT')
        self.allfilter.add_pattern('*.*')
        self.filterbox_changed(self.filterbox)
        self.statusbar=builder.get_object("statusbar")
        self.files=[]
        
    def main(self):
        self.window.show()
        gtk.main()
  
if __name__== "__main__":
    app=ConvertFiles()
    app.main()    



