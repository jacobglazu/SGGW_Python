import requests
import csv
import time
import functools
import logging



class ConnectionError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class NotFoundError(ConnectionError):
    def __init__(self, status):
        self.status = status
        super().__init__(f"Nie znaleziono strony, status: {status}")
class AccessDenied(ConnectionError):
    def __init__(self, status):
        self.status = status
        super().__init__(f"Brak dostępu do strony, status: {status}")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# dekorator
def log_execution_time(func):
    @functools.wraps(func)

    def wrapper(*args, **kwrgs):
        func_display_name = func.__name__
        logging.info(f"Rozpoczęto wykonanie funkcji: {func_display_name}")
        
        start = time.perf_counter()
        result = func(*args, **kwrgs)
        elapsed =time.perf_counter() - start
        
        logging.info(f"Zakonczono wykonanie funkcji: {func_display_name}")
        logging.info(f"Funkcja {func_display_name} wykonała się w: {elapsed:,.4f} sekund")
        return result
    return wrapper


class GeneratorETL():
    def __init__(self, filename : str):
        self.filename = filename
        
    def _read_csv(self):
        with open(self.filename, newline = '', encoding = 'utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                yield row
        
    
    @log_execution_time
    def _load(self):
       
        rows = [ value for  value in list(self._read_csv())]

        num_value = [[(i,float(value)) for i, value in enumerate(row) if value != '-' and i != 0] for row in rows]

        
        missing_id = [[col_id for col_id, value in enumerate(row) if value == '-'] for row in rows]
        miss_join = [",".join(str(value) for value in row) for row in missing_id]
        
        missing_values = [(i, x) for i, x in enumerate(miss_join, start=1)]
        
        
    
        total = [round(sum(value for _, value in row),3) for row in num_value]
                          
        lengths = [len(row) for row in num_value]
        
        avg = [round(x / y, 3) for x, y in zip(total, lengths)]
        
        values = [(i, x, y) for i, (x, y) in enumerate(zip(total, avg), start=1)]
        
            

        

        self._save_values(values)
        self._save_missing_values(missing_values)

    def _save_values(self, values):
        with open('values.csv', mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Nr porządkowy', 'Suma', 'Średnia'])
            writer.writerows(values)

    def _save_missing_values(self, missing_values):
        with open('misssing_values.csv', mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Nr porządkowy', 'Indeksy brakujących wartości'])
            writer.writerows(missing_values)




def download_file(url, name):
    try:
        # Pobranie pliku
        
        response = requests.get(url)
        #response.raise_for_status()
        if response.status_code == 404:  
            
        
            raise NotFoundError(f"404 dla    url: {url}")
        elif response.status_code == 403:
            
            raise AccessDenied(f"403 dla url: {url}")
        elif response.status_code == 503:
            print(f"Strona nie dostępna status: 503 dla url: {url}")
            return
        """elif response.status_code == 200:
            print(f"Plik {name} został pobrany dla url: {url}")
            return
        else:
            #raise ConnectionError(f"Wystąpił błąd dla url: {url}")"""
            #response.raise_for_status()  # Sprawdza, czy zapytanie zakończyło się błędem
        # Zapisanie pliku na dysku
        
        
        with open(f"sample.csv", 'wb') as file:
            if response.status_code == 200:
                file.write(response.content)

           
        with open(f"latest.txt", 'wb') as file_2:
            if response.status_code == 404:     
                file_2.write(response.content)
                    #if(response.status_code == '403'):           
                     #   raise AccessDenied('403')            
                
           
        if(name != 'sample.csv'):
            name = 'Latest.txt'
        print(f"Plik zapisano jako: {name}, status : {response.status_code}")
     

    
    except requests.ConnectionError:
        print(f"Wystąpił problem z połączeniem. URL: {url}")
    except NotFoundError as e:
        print(e)
    except AccessDenied as e:
        print(e)
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
    
    


url_1 = 'https://oleksandr-fedoruk.com/wp-content/uploads/2025/10/sample.csv'
url_2 = 'https://httpbin.org/status/403'
url_3 = 'https://oleksandr-fedoruk.com/wp-content/uploads/20225/10/sample.csv'
download_file(url_1, 'sample.csv')
download_file(url_2, 'new.csv')

download_file(url_3, 'text.csv')
        
    
if __name__ == "__main__":
    elt = GeneratorETL('sample.csv')
    result = elt._load()

#@log_execution_time
#def demo():
 #   time.sleep(0.02)

#demo()