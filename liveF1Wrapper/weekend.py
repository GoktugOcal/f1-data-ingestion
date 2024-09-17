from typing import List, Dict
import liveF1Wrapper

class Meeting: # Weekend
    def __init__(
        self,
        **kwargs
        ):
        # Iterate over the kwargs and set them as attributes of the instance
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)

        if hasattr(self, "sessions"):
            self.sessions_json = self.sessions
            self.sessions = []
            for session_data in self.sessions_json:
                self.sessions.append(liveF1Wrapper.Session(meeting = self, **session_data))