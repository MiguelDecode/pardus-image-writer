import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from USBDeviceManager import USBDeviceManager
from ImageWriter import ImageWriter

class MainWindow:
    def __init__(self, application):
        # Gtk Builder
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../ui/MainWindow.glade")
        self.builder.connect_signals(self)

        # Window
        self.window = self.builder.get_object("window")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_application(application)
        self.window.connect("destroy", self.onDestroy)
        self.defineComponents()

        # Define Image Writer
        self.imageWriter = ImageWriter()

        # Get inserted USB devices
        self.usbManager = USBDeviceManager()
        self.listUSBDevices()

        # Show Screen:
        self.window.show_all()
    
    # Window methods:
    def onDestroy(self, action):
        self.window.get_application().quit()
    
    def defineComponents(self):
        self.list_devices = self.builder.get_object("list_devices")
        self.cmb_devices = self.builder.get_object("cmb_devices")
        self.btn_selectISOFile = self.builder.get_object("btn_selectISOFile")
    

    # USB Methods
    def listUSBDevices(self):
        deviceList = self.usbManager.getUSBDevices()
        for device in deviceList:
            self.list_devices.append(device)

        if len(deviceList) > 0:
            self.cmb_devices.set_active(0)
        pass




    # UI Signals:
    def btn_selectISOFile_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select File",
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        fileFilter = Gtk.FileFilter()
        fileFilter.set_name("ISO Files")
        fileFilter.add_pattern("*.iso")
        dialog.add_filter(fileFilter)

        dialog.show()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filepath = dialog.get_filename()

            self.imageWriter.setFilepath(filepath)
            print(filepath)
            print(filepath.split('/'))
            print(filepath.split('/')[-1])
            self.btn_selectISOFile.set_label(filepath.split('/')[-1])
        
        dialog.destroy()

    def cmb_devices_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        model = combobox.get_model()
        deviceInfo = model[tree_iter][:3]
        print(f"{deviceInfo[0]} {deviceInfo[1]} {deviceInfo[2]}")
        self.imageWriter.setDevice(deviceInfo)

    def btn_start_clicked(self, button):
        print("START CLICKED")
        print(self.imageWriter.device)
        print(self.imageWriter.filepath)
