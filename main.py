from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
# REMOVED: requests, threading, and scanner logic for Safe Mode test

class MissingInventoryApp(MDApp):
    
    confirmation_dialog = None 
    
    def build(self):
        self.store = JsonStore('inventory_data.json')
        self.root = Builder.load_file('missinginventoryapp.kv')
        return self.root

    def on_start(self):
        self.load_inventory()

    def go_to_main_screen(self):
        self.root.current = 'main_list_screen'
        self.load_inventory()

    def go_to_scanner_screen(self):
        self.root.current = 'scanner_screen'

    def close_dialog(self, instance):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

    # --- 1. Load Inventory Logic ---
    def load_inventory(self):
        data = []
        for barcode_id in self.store.get_storage_keys():
            item = self.store.get(barcode_id)
            data.append({
                'viewclass': 'MissingItem',          
                'text': item['name'],                
                'secondary_text': f"{item['brand']} | {item['size']}", 
                'barcode_id': barcode_id,           
            })
        if self.root:
            self.root.ids.missing_list_rv.data = data

    # --- 2. Add Item Logic ---
    def add_missing_item(self, barcode_id, data):
        if barcode_id in self.store.get_storage_keys():
            return
        self.store.put(barcode_id, **data)
        self.load_inventory() 

    # --- 3. Remove Item Logic ---
    def remove_found_item(self, barcode_id):
        self.store.delete(barcode_id)
        self.load_inventory()

    # --- 4. Clear All Logic ---
    def show_clear_dialog(self):
        self.dialog = MDDialog(
            title="Confirm Clear All",
            text="Are you sure?",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                MDFlatButton(text="CLEAR", on_release=self.confirm_clear),
            ],
        )
        self.dialog.open()

    def confirm_clear(self, instance):
        self.store.clear()
        self.close_dialog(instance)
        self.load_inventory() 

    # --- SAFE MODE: Simulated Scan ---
    def simulate_scan(self):
        # Fake a successful scan of a "Test Product"
        fake_data = {
            'barcode_id': '123456789',
            'name': 'Test Cola',
            'brand': 'Generic',
            'size': '12oz'
        }
        self.add_missing_item('123456789', fake_data)
        self.go_to_main_screen()

if __name__ == '__main__':
    MissingInventoryApp().run()
    
