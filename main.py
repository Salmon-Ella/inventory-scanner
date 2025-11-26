import threading
import requests
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

# --- KivyMD App Class ---

class MissingInventoryApp(MDApp):
    
    confirmation_dialog = None 
    _current_product_data = None
    
    def build(self):
        # Initialize storage and load UI from the KV file
        self.store = JsonStore('inventory_data.json')
        # Kivy looks for the .kv file matching the app name
        self.root = Builder.load_file('missinginventoryapp.kv')
        return self.root

    def on_start(self):
        # Initial population of the list when the app opens
        self.load_inventory()

    # --- Navigation and UI Helpers ---
    
    def go_to_main_screen(self):
        # Transition back to the main list screen
        self.root.current = 'main_list_screen'
        self.load_inventory()

    def go_to_scanner_screen(self):
        # Transition to the scanner screen
        self.root.current = 'scanner_screen'

    def close_dialog(self, instance):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

    # --- 1. Load Inventory Logic (Function 1) ---
    
    def load_inventory(self):
        """Reads data from JsonStore and prepares it for the RecycleView."""
        data = []
        for barcode_id in self.store.get_storage_keys():
            item = self.store.get(barcode_id)
            data.append({
                'viewclass': 'MissingItem',          
                'text': item['name'],                
                'secondary_text': f"{item['brand']} | {item['size']}", 
                'source': item['image_path'],        
                'barcode_id': barcode_id,           
            })
        
        # Update the RecycleView with the loaded data
        if self.root and 'missing_list_rv' in self.root.ids:
            self.root.ids.missing_list_rv.data = data

    # --- 2. Add Item Logic (Function 2) ---

    def add_missing_item(self, barcode_id, data):
        """Saves a new item to storage."""
        if barcode_id in self.store.get_storage_keys():
            self.show_error_dialog("Error", "Item is already on the list.")
            return
            
        self.store.put(barcode_id, **data)
        self.load_inventory() 

    # --- 3. Remove Item Logic (Function 3 / Swipe Gesture) ---

    def remove_found_item(self, barcode_id):
        """Deletes item from storage and updates the UI (triggered by swipe)."""
        self.store.delete(barcode_id)
        self.load_inventory()

    # --- 4. Clear All Logic (Function 4) ---

    def show_clear_dialog(self):
        """Displays the 'Are you sure?' confirmation dialog."""
        self.dialog = MDDialog(
            title="Confirm Clear All",
            text="Are you sure you want to clear the entire missing list?",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                MDFlatButton(text="CLEAR", on_release=self.confirm_clear),
            ],
        )
        self.dialog.open()

    def confirm_clear(self, instance):
        """Called after user confirms CLEAR."""
        self.store.clear()
        self.close_dialog(instance)
        self.load_inventory() 

    # --- 5. Scanner and Asynchronous Network Logic ---

    def handle_barcode_scan(self, barcode_data):
        """Receives the barcode data string and starts the network lookup."""
        self.root.current = 'loading_screen' 
        threading.Thread(
            target=self._fetch_product_details_worker, 
            args=(barcode_data,)
        ).start()

    def _fetch_product_details_worker(self, barcode_id):
        """Worker function: Performs the blocking web request safely."""
        try:
            # --- REPLACE THIS MOCK API WITH YOUR REAL ONLINE CATALOG ENDPOINT ---
            api_url = f"https://your-online-catalog-api.com/product/{barcode_id}"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            product_data = response.json()
            product_data['barcode_id'] = barcode_id

            # Safely call back to main thread to show confirmation
            Clock.schedule_once(lambda dt: self.show_confirmation_dialog(product_data), 0)

        except Exception as e:
            # Safely handle error on the main thread
            print(f"Network or Lookup Error: {e}")
            Clock.schedule_once(lambda dt: self.show_error_dialog("Network Error", f"Failed to fetch: {e}"), 0)
            Clock.schedule_once(lambda dt: self.go_to_scanner_screen(), 0)
            
    def show_error_dialog(self, title, text):
        MDDialog(title=title, text=text, buttons=[MDFlatButton(text="OK")]).open()

    # --- 6. Confirmation Dialog Logic (Option B) ---

    def _build_confirmation_content(self, data):
        """Builds the custom content for the pop-up dialog."""
        content = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing="10dp", padding="10dp")
        content.add_widget(MDLabel(text=f"Product: **{data.get('name', 'N/A')}**", markup=True))
        content.add_widget(MDLabel(text=f"Brand: {data.get('brand', 'N/A')}"))
        content.add_widget(MDLabel(text=f"Size: {data.get('size', 'N/A')}"))
        return content

    def show_confirmation_dialog(self, product_data):
        """Displays the Pop-up Confirmation Screen."""
        self._current_product_data = product_data 
        
        self.confirmation_dialog = MDDialog(
            title="Confirm Product",
            type="custom",
            content_cls=self._build_confirmation_content(product_data),
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_confirmation_dialog),
                MDFlatButton(text="ADD TO LIST", on_release=self.confirm_add_to_list),
            ],
        )
        self.confirmation_dialog.open()
        
    def close_confirmation_dialog(self, instance=None):
        if self.confirmation_dialog:
            self.confirmation_dialog.dismiss()
            # Return to scanner screen to allow continuous scanning
            self.go_to_scanner_screen() 

    def confirm_add_to_list(self, instance):
        """Final call to the core logic function."""
        barcode_id = self._current_product_data['barcode_id']
        # Prepare data for saving (remove ID key)
        data_to_save = {k: v for k, v in self._current_product_data.items() if k != 'barcode_id'}
        
        self.add_missing_item(barcode_id, data_to_save)
        
        self.confirmation_dialog.dismiss()
        self.go_to_main_screen() 

if __name__ == '__main__':
    MissingInventoryApp().run()
