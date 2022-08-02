# For more information, see https://github.com/platformdirs/platformdirs
import os
from platformdirs import *

class Path:
    
    def __init__(self):
        self.APP_NAME = "LibrarySystem"
        self.APP_AUTHOR = "Kim"
        
    def makedir(path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    
    @property
    def user_data_dir(self):
        path = user_data_dir(self.APP_NAME, self.APP_AUTHOR)
        return Path.makedir(path)
        # C:\Users\User\AppData\Local\Kim\LibrarySystem
    
    @property
    def user_data_roaming_dir(self):
        path = user_data_dir(self.APP_NAME, self.APP_AUTHOR, roaming = True)
        return Path.makedir(path)
        # C:\Users\User\AppData\Roaming\Kim\LibrarySystem
    
    @property
    def user_config_dir(self):
        path = user_config_dir(self.APP_NAME, self.APP_AUTHOR)
        return Path.makedir(path)
        # C:\Users\User\AppData\Local\Kim\LibrarySystem
    
    @property
    def user_cache_dir(self):
        path = user_cache_dir(self.APP_NAME, self.APP_AUTHOR)
        return Path.makedir(path)
        # C:\Users\User\AppData\Local\Kim\LibrarySystem\Cache
    
    @property
    def site_data_dir(self):
        path = site_data_dir(self.APP_NAME, self.APP_AUTHOR)
        return Path.makedir(path)
        # C:\ProgramData\Kim\LibrarySystem
    
    @property
    def site_config_dir(self):
        path = site_config_dir(self.APP_NAME, self.APP_AUTHOR)
        return Path.makedir(path)
        # C:\ProgramData\Kim\LibrarySystem
    
    @property
    def user_log_dir(self):
        path = user_log_dir(self.APP_NAME, self.APP_AUTHOR)
        return Path.makedir(path)
        # C:\Users\User\AppData\Local\Kim\LibrarySystem\Logs
    
    @property
    def user_documents_dir(self):
        path = user_documents_dir()
        return Path.makedir(path)
        # C:\Users\User\Documents
    
    @property
    def user_runtime_dir(self):
        path = user_runtime_dir(self.APP_NAME, self.APP_AUTHOR)
        return Path.makedir(path)
        # C:\Users\User\AppData\Local\Temp\Kim\LibrarySystem
