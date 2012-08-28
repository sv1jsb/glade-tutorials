#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk                                                                # Τα αναγκαία imports για την λειτουργία
pygtk.require('2.0')                                                        # του προγράμματος. 
import gtk
from datetime import datetime

class BackgroundXML(object):     

    DIALOG_TYPE_ERROR = 0                                                   # Δύο σταθερές, χρησιμοποιούνται στην εμφάνιση
    DIALOG_TYPE_INFO = 1                                                    # του σωστού dialog

    CHOOSER_CANCEL = 0                                                      # Οι τιμές επιστροφής από τα παράθυρα επιλογής αρχείων
    CHOOSER_OK = 1

    def close_window(self, widget, data=None):                              # Καλείται όταν ο χρήστης πατήσει "Έξοδος" ή
        gtk.main_quit()                                                     # το Χ του παραθύρου

    def delete_chooser(self, widget, data=None):                           # Καλείται όταν χρήστης πατήσει Χ στο παράθυρο επιλογής αρχείων.
        return True                                                         # Επιστρέφει True για να ΜΗΝ γίνει καταστροφή του παραθύρου.

    def xmlbutton_click(self,widget,data=None):                             # Καλείται όταν ο χρήστης πατήσει το κουμπί επιλογής αρχείου XML,
        response=self.xmlchooser.run()                                      # δείχνουμε το αντίστοιχο παράθυρο και περιμένουμε επιστροφή.
        if response == self.CHOOSER_OK:                                     # Αν έχει πατήσει "Έντάξει" αποθηκεύουμε το όνομα του αρχείου στο πεδίο
            self.xmlfile.set_text(self.xmlchooser.get_filename())           # Κρύβουμε το παράθυρο για όλες τις επιλογές του χρήστη.
        self.xmlchooser.hide()

    def picbutton_click(self,widget,data=None):                             # Καλείται όταν ο χρήστης πατήσει το κουμπί επιλογής εικόνων.
        response = self.picchooser.run()                                    # εικόνων.
        if response == self.CHOOSER_OK:
            buffer1=self.picbuffer.get_text(self.picbuffer.get_start_iter(), self.picbuffer.get_end_iter())
            for fn in self.picchooser.get_filenames():                      # Όταν ο χρήστης πατήσει "Εντάξει" στο παράθυρο επιλογής 
                buffer1=buffer1+fn+'\n'                                     # εικόνων, διαβάζουμε τα αρχεία από το παράθυρο και τα προσθέτουμε
            self.picbuffer.set_text(buffer1)                                # στο buffer που είναι υπεύθυνο για το περιεχόμενο της λίστας.
        self.picchooser.hide()                                              # Κρύβουμε το παράθυρο σε όλες τις περιπτώσεις.
            
    def clearbutton_click(self,widget,data=None):                           # Καλείται όταν ο χρήστης πατήσει το κουμπί καθαρισμού
        self.picbuffer.set_text(u'')                                        # της λίστας των εικόνων

    def picchooser_cancel_clicked(self, widget, data=None):                 # Καλείται όταν ο χρήστης πατήσει "Ακύρωση" στο παράθυρο
        self.picchooser.response(self.CHOOSER_CANCEL)                       # επιλογής εικόνων. Επιστρέφουμε CHOOSER_CANCEL

    def picchooser_ok_clicked(self, widget, data=None):                     # Καλείται όταν ο χρήστης πατήσει "Εντάξει" στο παράθυρο επιλογής εικόνων
        self.picchooser.response(self.CHOOSER_OK)                           # Επιστρέφουμε CHOOSER_OK

    def xmlchooser_ok_clicked(self,widget,data=None):                       # Καλείται όταν ο χρήστης πατήσει "Εντάξει". 
        self.xmlchooser.response(self.CHOOSER_OK)                           # Επιστρέφουμε CHOOSER_OK

    def xmlchooser_cancel_clicked(self,widget,date=None):                   # Καλείται όταν ο χρήστης πατήσει "Ακύρωση" στο παράθυρο επιλογής
        self.xmlchooser.response(self.CHOOSER_CANCEL)                       # XML. Επιστρέφουμε CHOOSER_CANCEL

    def dialog(self, text, dialogtype):                                     # Μέθοδος βοηθός για να δείχνουμε το σωστό παράθυρο διαλόγου ανάλογα
        if dialogtype == self.DIALOG_TYPE_ERROR:                            # με την περίσταση. 
            dialog=gtk.MessageDialog(parent=None,flags=gtk.DIALOG_MODAL & \
             gtk.DIALOG_DESTROY_WITH_PARENT, \
             type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
            dialog.set_title(u"Σφάλμα")                                     # Δημιουργία του διαλόγου από το πρόγραμμα και όχι από το αρχείο Glade
            dialog.format_secondary_text(u"Διορθώστε τα παραπάνω προβλήματα.")
        elif dialogtype == self.DIALOG_TYPE_INFO:
            dialog=gtk.MessageDialog(parent=None,flags=gtk.DIALOG_MODAL & \
            gtk.DIALOG_DESTROY_WITH_PARENT, \
            type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
            dialog.set_title(u"Ενημέρωση")
        dialog.set_markup(u"<b>"+text+"</b>")                               # Στο μήνυμα προστίθεται markup για να είναι πιο εμφανές,
        response=dialog.run()
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_OK:
            dialog.destroy()                                                # Έλεγχος της επιστροφής από τον διάλογο, γίνεται καταστροφή του διαλόγου.            

    def clicked_ok(self, widget, data=None):
        picfiles = self.picbuffer.get_text(self.picbuffer.get_start_iter(), self.picbuffer.get_end_iter())
        filelist=picfiles.split("\n")                                               # Η βασική μέθοδος του προγράμματος καλείται όταν ο χρήστης πατήσει
        filelist.remove('')                                                         # "Εφαρμογή". Βάζουμε το περιεχόμενο του buffer σε έναν πίνακα και
        errortxt=''                                                                 # σβήνουμε από τον πίνακα άδειες θέσεις αν υπάρχουν.
        now = datetime.now()                                                        # Απόκτηση της τρέχουσας ώρας και ημερομηνίας
        if not self.xmlfile.get_text().endswith('.xml'):                            # Έλεγχος αν έχει επιλέξει αρχείο XML.
            errortxt+=u'Το όνομα του XML αρχείου πρέπει να τελειώνει σε .xml\n'
        if not filelist :
            errortxt+=u'Πρέπει να διαλέξετε φωτογραφίες\n'                          # Έλεγχος αν έχει επιλέξει εικόνες.
        if not self.duration.get_text().isdigit() :
            errortxt+=u'Πρέπει να δώσετε την διάρκεια εμφάνισης (αριθμητικά)\n'     # Έλεγχος αν έχει γράψει διάρκεια και είναι αριθμός.
        if not self.change.get_text().isdigit() :
            errortxt+=u'Πρέπει να δώσετε την διάρκεια εναλλαγής (αριθμητικά)\n'     # Έλεγχος αν έχει γράψει διάρκεια και είναι αριθμός.
        if errortxt:
            self.dialog(errortxt, self.DIALOG_TYPE_ERROR)                           # Αν υπάρχει λάθος δείχνουμε το αντίστοιχο λεκτικό σε διάλογο λάθους.
        else:
            with open(self.xmlfile.get_text(),'w') as f:
                try:
                    f.write("<background>\n")                                       # Ο βασικός βρόγχος δημιουργίας του αρχείου XML.
                    f.write("  <starttime>\n")
                    f.write("    <year>"+str(now.year)+"</year>\n")
                    f.write("    <month>"+str(now.month)+"</month>\n")
                    f.write("    <day>"+str(now.day)+"</day>\n")
                    f.write("    <hour>"+str(now.hour)+"</hour>\n")
                    f.write("    <minute>"+str(now.minute)+"</minute>\n")
                    f.write("    <second>"+str(now.second)+"</second>\n")
                    f.write("  </starttime>\n")
                    first=filelist[0]
                    for ln in range(len(filelist)):
                        f.write("  <static>\n")
                        f.write("    <duration>"+self.duration.get_text()+"</duration>\n")
                        f.write("    <file>"+filelist[ln]+"</file>\n")
                        f.write("  </static>\n")
                        f.write("  <transition>\n")
                        f.write("    <duration>"+self.change.get_text()+"</duration>\n")
                        f.write("    <from>"+filelist[ln]+"</from>\n")
                        if ln == len(filelist)-1:
                            f.write("    <to>"+first+"</to>\n")
                        else:
                            f.write("    <to>"+filelist[ln+1]+"</to>\n")
                        f.write("  </transition>\n")
                        f.write("</background>\n")
                    self.dialog(u"Επιτυχής δημιουργία αρχείου XML",self.DIALOG_TYPE_INFO) # Επιτυχία και ανάλογος διάλογος.
                except:
                    self.dialog(u"Πρόβλημα στην δημιουργία του αρχείου XML",self.DIALOG_TYPE_ERROR) # Αποτυχία και μήνυμα λάθους.

    def __init__(self):
        builder = gtk.Builder()                                                     # Η μέθοδος όπου κατασκευάζεται το παράθυρο από
        builder.add_from_file("backgroundxml.glade")                                # το αρχείο Glade.
        builder.connect_signals(self)
        self.backgroundxml = builder.get_object("backgroundxml")                    # Δήλωση όλων τον τοπικών μεταβλητών που χρειαζόμαστε
        self.picchooser = builder.get_object("picchooser")                          # στο πρόγραμμα από τα αντίστοιχα αντικείμενα του Glade.
        self.picbuffer = builder.get_object("picbuffer") 
        self.xmlchooser = builder.get_object("xmlchooser")
        self.xmlfile = builder.get_object("xmlfile")
        self.duration = builder.get_object("duration")
        self.change = builder.get_object("change")
        self.xmlfilter = builder.get_object("xmlfilter")                            # Προσθήκη φίλτρων για τα παράθυρα επιλογής αρχείων.
        self.xmlfilter.add_pattern('*.xml')
        self.picfilter = builder.get_object("picfilter")
        self.picfilter.add_pattern('*.jpg')
        self.picfilter.add_pattern('*.png')
        self.picfilter.add_pattern('*.JPG')
        self.picfilter.add_pattern('*.PNG')

    def main(self):                                                                 # Εμφάνιση του κεντρικού παραθύρου και εκτέλεση της
        self.backgroundxml.show()                                                   # main ρουτίνας του GTK που είναι υπεύθυνη για το
        gtk.main()                                                                  # "τρέξιμο" του παραθύρου
        
if __name__ == "__main__":
    app = BackgroundXML()                                                           # Δημιουργία του βασικού αντικείμενου μας και κάλεσμα
    app.main()                                                                      # της main ρουτίνας του.

