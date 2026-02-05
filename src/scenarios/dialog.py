from src.entities.character import player

class DialogMixin():

    def add_message(self, text):
        self.message_queue.append(text)

    def next_message(self):
        if self.message_queue:
            self.message_queue.pop(0)

    def has_messages(self):
        return len(self.message_queue) > 0
