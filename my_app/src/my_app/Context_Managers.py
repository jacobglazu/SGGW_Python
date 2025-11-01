import time

class Logger:
    def __enter__(self):
        self.start_time = time.time()
        print(f"Start logowania")
        return self
    
    def __exit__(self, ecx_type, exc_val, exc_tb):
        end_time = time.time()
        print(f"Zakonczenie logowania")

with Logger() as logger:
    print(f"Logowanie w trakcie")
    time.sleep(5)

class FileWriter:
    def __init__(self, path):
        self.path = path
        self.file = open(path, "w", encoding= "utf-8")
                
    
    def __enter__(self):
        print(f"Otwieram zasób")
        return self.file
    
    def __exit__(self,ecx_type, exc_val, exc_tb):
        print(f"Zamykam zasób")
        if self.file:
            self.file.close()
        
            



"""text = FileWriter('text.txt')
obj = text.__enter__()
try:
    print(obj)
finally:
    text.__exit__(ecx_type=None, exc_val=None, exc_tb=None)"""

with FileWriter('text.txt') as resource: 
    resource.write('Tu LastPass, ')