class DataProcessor:
    def __init__(self, llm_client, data_dir):
        self.llm = llm_client
        self.data_dir = data_dir

    def extract_image_amount(self, image_id, diagnostic_mode=False):
        """Extracts the amount from an image using the LLM client."""
        # Stub implementation
        return 0.0

    def is_message_potentially_relevant(self, message_text, req_date, sent_at):
        """Determines if a message is potentially relevant to the request."""
        # Stub implementation
        return True

    def parse_message(self, message_text, req_date, sent_at, diagnostic_mode=False, msg_id=None):
        """Parses a message into a structured format using the LLM client."""
        # Stub implementation
        return {
            "is_relevant": True,
            "event_id": msg_id,
            "extracted_data": {}
        }