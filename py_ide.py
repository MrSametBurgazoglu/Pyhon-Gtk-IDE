#-*-coding:utf-8-*-

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GtkSource
from gi.repository import Gdk
from gi.repository import Vte
from gi.repository import GLib
import sys


class Notepad2(Gtk.HBox):
    def __init__(self, *args, **kwargs):
        super(Notepad2, self).__init__(*args, **kwargs)

        self.label = Gtk.Label(label="Yeni sayfa")

        self.close_image = Gtk.Image()
        self.close_image.set_from_file("close.png")
        self.close_button = Gtk.Button()
        self.close_button.set_image(self.close_image)

        self.add(self.label)
        self.add(self.close_button)
        self.show_all()

class Notepad(Gtk.VBox):
    def __init__(self, *args, **kwargs):
        super(Notepad, self).__init__(*args, **kwargs)

        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_hexpand(True)
        self.scrolled.set_vexpand(True)
        self.sourceview = GtkSource.View()
        self.sourcebuffer = self.sourceview.get_buffer()
        self.sourceview.set_show_line_numbers(True)
        self.sourceview.set_smart_home_end(0)
        self.sourceview.set_auto_indent(True)
        self.scrolled.add(self.sourceview)
        self.sourcebuffer.set_highlight_syntax(True)
        self.sourcebuffer.set_highlight_matching_brackets(True)
        start, end = self.sourcebuffer.get_bounds()
        self.sourcebuffer.ensure_highlight(start, end)
        self.sourcelanguagemanager = GtkSource.LanguageManager()
        lang = self.sourcelanguagemanager.get_default()
        abc = self.sourcelanguagemanager.get_language("python")
        self.sourcebuffer.set_language(abc)
        self.sourcestyle = GtkSource.Style()
        self.sourcestylescheme = GtkSource.StyleScheme()
        self.sourcestyleschememanager = GtkSource.StyleSchemeManager()
        style = self.sourcestyleschememanager.get_scheme("oblivion")
        self.sourcebuffer.set_style_scheme(style)
        self.sourcesearch = GtkSource.SearchContext.new(self.sourcebuffer)
        self.sourcesearchsettings = GtkSource.SearchSettings()
        self.sourcesearchsettings.set_search_text("deneme")
        self.sourcesearch.set_settings(self.sourcesearchsettings)
        self.sourcesearch.set_highlight(True)
        self.textiter = Gtk.TextIter() 

        self.searchtoolbar = Gtk.Toolbar()

        self.toolitem = Gtk.ToolItem()
        self.search_bar = Gtk.Entry()
        self.search_bar.set_width_chars(30)
        self.search_bar.connect("activate", self.search)
        self.toolitem.add(self.search_bar)
        self.searchtoolbar.insert(self.toolitem, 0)

        self.replacetoolbar = Gtk.Toolbar()

        self.toolitem2 = Gtk.ToolItem()
        self.search_bar2 = Gtk.Entry()
        self.search_bar2.set_width_chars(30)
        self.search_bar2.connect("activate", self.search)
        self.toolitem2.add(self.search_bar2)
        self.replacetoolbar.insert(self.toolitem2, 0)

        self.toolitem3 = Gtk.ToolItem()
        self.search_bar3 = Gtk.Entry()
        self.search_bar3.set_width_chars(30)
        self.search_bar3.connect("activate", self.search)
        self.toolitem3.add(self.search_bar3)
        self.replacetoolbar.insert(self.toolitem3, 0)

        self.pack_start(self.scrolled, True, True, 0)
        self.pack_start(self.searchtoolbar, False, True, 0)
        self.pack_start(self.replacetoolbar, False, True, 0)

        self.show()
        self.scrolled.show_all()

    def search(self, widget):
        a = self.search_bar.get_text()
        self.sourcesearchsettings.set_search_text(a)


class Interface(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super(Interface, self).__init__(*args, **kwargs)
        Gtk.Window.__init__(self)
        self.set_title("Notebook")
        self.set_name('interface')
        self.maximize()
        style_provider = Gtk.CssProvider()

        style_provider.load_from_path("style2.css")

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.connect("delete-event", Gtk.main_quit)
        self.connect("destroy", Gtk.main_quit)
	
 	self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(False)

        self.new_page_button = Gtk.ToolButton()
        self.new_page_button.set_label("Yeni sayfa")
        self.new_page_button.connect("clicked", self.new_page)
        self.new_page_button.set_tooltip_text("Boş bir sayfa aç")
        self.header_bar.add(self.new_page_button)

        self.open_page_button = Gtk.ToolButton()
        self.open_page_button.set_label("Oku")
        self.open_page_button.connect("clicked", self.open_page)
        self.open_page_button.set_tooltip_text("Bir dosyayı içe aktar")
        self.header_bar.add(self.open_page_button)

        self.save_page_button = Gtk.ToolButton()
        self.save_page_button.set_label("Kaydet")
        self.save_page_button.connect("clicked", self.save_page)
        self.save_page_button.set_tooltip_text("Dosyayı kaydet")
        self.header_bar.add(self.save_page_button)

        self.undo_page_button = Gtk.ToolButton()
        self.undo_page_button.set_label("Geri al")
        self.undo_page_button.connect("clicked", self.undo_page)
        self.undo_page_button.set_tooltip_text("Yapılan işlemi geri al")
        self.header_bar.add(self.undo_page_button)

        self.redo_page_button = Gtk.ToolButton()
        self.redo_page_button.set_label("Tekrar yap")
        self.redo_page_button.connect("clicked", self.redo_page)
        self.redo_page_button.set_tooltip_text("Geri alınan işlemi tekrarla")
        self.header_bar.add(self.redo_page_button)

        self.separator = Gtk.SeparatorToolItem()
        self.header_bar.add(self.separator)

        self.search_page_button = Gtk.ToolButton()
        self.search_page_button.set_label("Arama")
        self.search_page_button.connect("clicked", self.search_page)
        self.search_page_button.set_tooltip_text("Sayfada arama yap")
        self.header_bar.add(self.search_page_button)

        self.search_page_button2 = Gtk.ToolButton()
        self.search_page_button2.set_label("Arama")
        self.search_page_button2.connect("clicked", self.search_page2)
        self.search_page_button2.set_tooltip_text("Sayfada arama yap")
        self.header_bar.add(self.search_page_button2)

        self.header_bar.show_all()
        self.search_page_button2.hide()

        self.notebook = Gtk.Notebook()
	
        self.notebook.set_scrollable(True)
        self.notebook.set_show_tabs(True)
        self.notebook.set_show_border(True)

        self.tabs = []

        self.tabs.append((self.create_page(), self.create_title()))

        self.notebook.append_page(*self.tabs[0])
 
        self.show()
 
        self.vbox = Gtk.VBox()
        self.vbox.pack_start(self.header_bar, False, True, 0)
        self.vbox.pack_start(self.notebook, True, True, 0)
        self.notebook.show()
        
        self.vbox.show()        

        self.add(self.vbox)

    def create_page(self):
        notepad = Notepad()
        global notepad
        return notepad
        notepad.searchtoolbar.hide()

    def create_title(self):
        notepad2 = Notepad2()
        notepad2.close_button.connect("clicked", self.close_page)
        return notepad2

    def new_page(self, widget):
        current_page = self.notebook.get_current_page()
        page_tuple = (self.create_page(), self.create_title())
        self.tabs.insert(current_page+1, page_tuple)
        self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page+1)
        self.notebook.set_current_page(current_page+1)   

    def close_page(self, widget):
        a = self.notebook.get_n_pages()
        if a == 1:
           Gtk.main_quit() 
        else:
           current_page = self.notebook.get_current_page()
           self.notebook.remove_page(current_page) 	

    def open_page(self, widget):
        self.new_page(self)
	filechooserdialog = Gtk.FileChooserDialog(title="FileChooserDialog")

        filechooserdialog.add_button("İptal", Gtk.ResponseType.CANCEL)
        filechooserdialog.add_button("Aç", Gtk.ResponseType.OK)

	response = filechooserdialog.run()

	if response == Gtk.ResponseType.OK:
    	   file_chooser_path = filechooserdialog.get_filename()
           global file_chooser_path
           self.set_title(file_chooser_path)
           dosya = open(file_chooser_path)
           b = dosya.read()
           current_page = self.notebook.get_current_page()
           self.tabs[current_page][0].sourcebuffer.set_text(b) 
           self.notebook.set_current_page(current_page+1)   

	filechooserdialog.destroy()

    def save_page(self, widget):
        current_page = self.notebook.get_current_page()
        start, end = self.tabs[current_page][0].sourcebuffer.get_bounds()
        text = self.tabs[current_page][0].sourcebuffer.get_text(start, end, False)
        try:
          dosya = open(file_chooser_path, "w")
          dosya.write(text)
        except:
	  filechooserdialog = Gtk.FileChooserDialog(title="FileChooserDialog")
          filechooserdialog.add_button("İptal", Gtk.ResponseType.CANCEL)
          filechooserdialog.add_button("Aç", Gtk.ResponseType.OK)
	  response = filechooserdialog.run()
	  if response == Gtk.ResponseType.OK:
    	     file_chooser_path = filechooserdialog.get_filename()
             dosya = open(file_chooser_path, "w")
             dosya.write(text) 
	  filechooserdialog.destroy()

    def undo_page(self, widget):
        current_page = self.notebook.get_current_page()
        a = self.tabs[current_page][0].sourcebuffer.can_undo()
        if a == True:
           self.tabs[current_page][0].sourcebuffer.undo()
        else:
           pass 

    def redo_page(self, widget):
        current_page = self.notebook.get_current_page()
        a = self.tabs[current_page][0].sourcebuffer.can_redo()
        if a == True:
           self.tabs[current_page][0].sourcebuffer.redo()
        else:    
           pass

    def search_page(self, widget):
        current_page = self.notebook.get_current_page()
        self.tabs[current_page][0].searchtoolbar.show_all()
        self.search_page_button.hide()
        self.search_page_button2.show()

    def search_page2(self, widget):
        current_page = self.notebook.get_current_page()
        self.tabs[current_page][0].searchtoolbar.hide()
        self.search_page_button2.hide()
        self.search_page_button.show()
        

window = Interface()
Gtk.main()
