import rapidsms

class App (rapidsms.app.App):
    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        self.arabic = false
        parts = message.split(" ")
        for part in parts:
            if not is_english(part):
                self.arabic = true
                break
        if self.arabic:
            t = Translator()
            translated_text = t.translate(parts)
        
        message.text = translated_text

    def handle (self, message):
        """Add your main application logic in the handle phase."""
        pass

    def cleanup (self, message):
        """Perform any clean up after all handlers have run in the
           cleanup phase."""
        pass

    def outgoing (self, message):
        """Handle outgoing message notifications."""
        pass

    def stop (self):
        """Perform global app cleanup when the application is stopped."""
        pass
