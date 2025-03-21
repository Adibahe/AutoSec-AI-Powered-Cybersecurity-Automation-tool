from langchain.memory import ConversationBufferWindowMemory

import threading

class MemorySingleton:
    """Singleton class for managing conversation memory."""
    
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, k=5):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MemorySingleton, cls).__new__(cls)
                cls._instance.memory = ConversationBufferWindowMemory(k=k)
        return cls._instance

    def add_message(self, user_input, bot_response):
        """Stores user input and bot response in memory."""
        self.memory.save_context({"input": user_input}, {"output": bot_response})

    def get_history(self):
        """Retrieves stored conversation history as text."""
        return self.memory.load_memory_variables({})["history"]

