from . import variant4

class DataCrypt:
    def __init__(self, config):
        if(config.VARIANT):
            self.variant = config.VARIANT
        else: self.variant=4 # default
        if(self.variant == 3):
            print("VARIANT:", 3, " ", "Multiple File Run")
        elif(self.variant == 4):
            print("VARIANT:", 4, " ", "Single Folder Run")
            variant4.runCommand(config)

