# Written by Aaron Barge
# Copyright 2022


class LoadingBar:
    def __init__(
            self,
            max_iterations: int,
            width: int = 20,
            empty_char: str = ' ',
            filled_char: str = '█',
            show_percent: bool = True
        ):
        self.max_iterations = max_iterations
        self.width = width
        self.empty_char = empty_char
        self.filled_char = filled_char
        self.show_percent = show_percent

    def loading(self, iteration: int = 0):
        progress = iteration / self.max_iterations
        filled_width = round(progress * self.width)
        bar = self.filled_char * filled_width + self.empty_char * (self.width - filled_width)
        percent = f" {round(progress * 100, 1)}%" if self.show_percent else ''
        print(f"{bar}{percent}", end='\r')
