import rapidsms

class App (rapidsms.app.App):
    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        """Parse and annotate messages in the parse phase."""
        pass

    def handle (self, message):
        if message.text.lower().find("bulk") > -1:
            message_processor = BulkMessageProcessor(message.text)
            answers = message_processor.parse_and_create_user(message.connection, message.text)
            response = message_processor.save_user_and_responses(answers)
            message.respond(response)
            return True

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
