from typing import List, Dict


class Session:
    def __init__(
        self,
        **kwargs
        ):
        print(kwargs)
        # Iterate over the kwargs and set them as attributes of the instance
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)
