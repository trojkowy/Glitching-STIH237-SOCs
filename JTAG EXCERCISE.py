#!/usr/bin/env python
# coding: utf-8

# In[ ]:

1. ZAINSTALUJ stm-st40.530-5.3.0-mswin32-x86 + stm-stmc.160-1.6.0-MSWin32-x86
2. POLACZ PROCESOR JTAGIEM FT4232H
3. POLACZ LINIE RST_IN PROCESORA Z NTRST CWLITE
4. ODPAL SKRYPT I WYKONAJ POLECENIE URUCHAMIAJACE DANY TARGETPACK W PRZYKLADZIE ZASTOSOWANO TARGETPACK STIH205/207 (STI7108):
   sh4tp STMCLT1000A:b2067stxh205:host,no_reset=1,no_pokes=1 resettype=none

st40300tp STMCLT1000A:b2067stxh205:host (NIEKTORE NOWSZE PROCKI TO ARCH ST40 300)
        


# In[ ]:

        
SKRYPT WYSYLA GLITCH PO ODEBRANIU STANU WYSOKIEGO Z JTAGA NA TIO4 JEDNAK PETLA KTORA ZMIENIA DELAY I WIDTH OPIERA SIE TYLKO
NA ZASADZIE PETLI GDYBY BYLO COS NIE TAK MOZNA SPROBOWAC WPROWADZIC WERYFIKACJE CZY TRIGGER ZOSTAL ODEBRANY:
def WERYIKUJ():
    if
    scope.io.tio4 = 'gpio_high'
    #time.sleep(delay_sec) 
    scope.io.tio4 = 'gpio_low'
JEZELI STAN WYSOKI ZOSTAL USTAWIONY KONTYNUUJ WYKONYWANIE PETLI


# In[ ]:


UWAGA ! 24.01.2025
W SKRYPCIE NTRST ZOSTAL DOSTOSOWANY DO STEROWANIA PRZEKAZNIKIEM SSR LUB TRANZYSTOREM OD ZASILANIA 12V LUB LINIA RESET IN
W PRZYPADKU GLITCHOWANIA JTAGA STEROWAC LINIA RESET IN DEKODERA , W PRZYPADKU SYGNATURY MOZNA STEROWAC KAZDA INNA 


# In[ ]:


UWAGA ! 28.01.2025 ZWEZONO CZAS OCZEKIWANIA PO WYSLANIU GLITCHA time.sleep(2) # ODCZEKAJ JAKIS CZAS AZ WYZWOLI GLITCH
JESLI COS BEDZIE NIE TAK ZWIEKSZYC TEN CZAS


# In[ ]:


UWAGA ! 31.01.2025 KOMPLETNA PRZEBUDOWA SKRYPTOW - TYM RAZEM WERYFIKOWANE SA ODPOWIEDZI WYPISYWANY JEST AKTUALNY STATUS
I NA ZAKONCZENIE MAMY PELNE PODSUMOWANIE PRZEBIEGU GLITCHOWANIA


# In[ ]:


UWAGA ! 05.02.2025 DODANO STATUS RESETÓW PROCESORA


# In[ ]:


UWAGA ! 15.02.2025 OGRANICZONO SKRYPT DO SKANOWANIA JEDNYM KODEM TZW. BRUTEFORCE DODANA JEST ROWNIEZ WERYFIKACJA RESETOW 
PROCESORA


# In[ ]:


SCOPETYPE = 'OPENADC'
import chipwhisperer as cw
scope = cw.scope()
print("INFO: Found ChipWhisperer😍") 

import time 
import os 
import subprocess 
import matplotlib.pyplot as plt
from tqdm import tqdm


# In[ ]:



scope.clock.clkgen_freq = 160e6

scope.glitch.resetDCMs()
scope.glitch.clk_src = "clkgen"
scope.glitch.output = "enable_only"
scope.glitch.trigger_src = "ext_continuous"

scope.glitch.ext_offset = 39388440 # AKTYWOWAC JESLI UZYWANY JEST KOD Z (BRUTEFORCE)

scope.io.glitch_hp = True
scope.io.glitch_lp = False
scope.trigger.triggers = "tio4"
#scope.arm()
scope.io.nrst = 'high' 


# In[ ]:

gdb_path = r'D:\STM\ST40R5.4.0\bin\sh4gdb'

#gdb_path = '/usr/local/gdb/gdb'


# In[ ]:


def stb_power():
    scope.io.nrst = 'low'
    scope.arm()
    #time.sleep(1) 
    scope.io.nrst = 'high'


# In[ ]:


get_ipython().system('pip show chipwhisperer')


# In[ ]:


W poniższym kodzie width (repeat) i delay glitcha (ext_offset) są inkrementowane co każdy kolejny skok (BRUTEFORCE) OPROCZ TEGO
SKRYPT POSIADA DODANA WERYFIKACJE RESETOW PROCESORA , MOZNA SKANOWAC JEDNA WARTOSCIA GLITCHA GENERALNIE TEN SKRYPT JEST JEDNYM
Z NAJSENSOWNIEJSZYCH DO SKANOWANIA: W CELU BRUTEFORCE USTAW DELAY OD DO I SZER. SZPILKI OD DO (WIEKSZY ZAKRES) SKRYPT ZACZNIE 
WYSYLAC GLITCHE ZMIENIAJAC WIDTH I DELAY JAK JUZ COS ZNAJDZIE POZOSTAWA ZADANA SZER. GLITCHA I SKANUJ DELAY OD DO Z TAKA SZER.


# In[ ]:



# delay od 16160000 do 39410000 wykonuje caly init jtaga , gdzies pomiedzy 38450000 a 39410000 lub 38730000 zmienia sie fr i zaczyna 
# odczytywac sentinela i cala reszte rejestrow. skanowac 16160000 do 39410000 skok co 70000 - 150000 , 
# dla 38450000 a 39410000 skok co 1 - 2 (przyklad 38450000,39410000,2)

# Oczekiwana linia do porównania tu wpisz pierwsza linie oczekiwana
expected_line = "SDI [ERROR] :: [SERVER] serviceASEMode: Sentinel not found (0xffffffff != 0xbeefface)"
expected_line2 = "SDI [ERROR] :: [SERVER] host_UDI_SDDR_FIFO_NOPOLL: Missing data transfer handshake in SDSR register (0)"

# Liczniki
correct_answers = 0
incorrect_answers = 0
total_answers = 0
reset_answers = 0

# Zbiory do przechowywania zakresów odpowiedzi poprawnych i niepoprawnych
correct_ranges = []
incorrect_ranges = []
reset_ranges = []


# Funkcja do kolorowania tekstu
def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

start=True
while start:

# Pętla z zapytaniami
    for i in range(290,291):
        scope.glitch.ext_offset = scope.glitch.ext_offset+5
        # Wyświetlanie statusu
        print(f"GLITCH STATUS: width = {i}, delay = {scope.glitch.ext_offset}")
        scope.glitch.repeat = i
        
        time.sleep(0.5)
        
        stb_power()

        # Uruchomienie procesu GDB
        process = subprocess.Popen(
            [gdb_path, '--batch', '-ex', 'sh4tp STMCLT1000A:b2067stxh205:host,no_reset=1,no_pokes=1 resettype=none'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Odbiór danych z procesu
        stdout, stderr = process.communicate()
        time.sleep(2)

        # Przekonwertuj odebrane dane na string (UTF-8) i usuń zbędne białe znaki
        output_str = stdout.decode('utf-8').strip()
        
        # Debug: wyświetlamy otrzymane dane odhaszuj jezeli glitch znaleziony celem podgladu odpowiedzi! zahaszuj by zaoszcz?dzi? woln? pami??
        print(f"Otrzymane dane:\n{output_str}")
        
        # Zliczanie całkowitej liczby odpowiedzi
        total_answers += 1

        # Sprawdzenie, czy oczekiwana linia jest w odebranych danych
        if expected_line in output_str:
            correct_answers += 1
            print(color_text("Odpowiedź poprawna", "32"))  # Zielony dla poprawnej odpowiedzi
            # Dodaj zakres do listy odpowiedzi poprawnych
            correct_ranges.append(f"width {i}, delay {scope.glitch.ext_offset}")
        elif expected_line2 in output_str:
            reset_answers += 1
            print(color_text("CPU_RESET", "33"))  # Zielony dla poprawnej odpowiedzi
            # Dodaj zakres do listy odpowiedzi poprawnych
            reset_ranges.append(f"width {i}, delay {scope.glitch.ext_offset}")
        else:
            incorrect_answers += 1
            print(color_text("Odpowiedź niepoprawna", "31"))  # Czerwony dla niepoprawnej odpowiedzi
            # Dodaj zakres do listy odpowiedzi niepoprawnych
            incorrect_ranges.append(f"width {i}, delay {scope.glitch.ext_offset}")
        if scope.glitch.ext_offset > 39410000: # JEZELI DOLECI DO 190000 DELAY WYSWIETL NO SUCCESS I PRZERWIJ OPERACJE
            print("KONIEC")
            start=False
            break
# Po zakończeniu wszystkich iteracji, wyświetlenie podsumowania
print(f"\nPodsumowanie:")
print(f"Liczba wyslanych glitchy: {total_answers}")
print(f"Liczba poprawnych odpowiedzi: {correct_answers}")
print(f"Liczba niepoprawnych odpowiedzi: {incorrect_answers}")
print(f"Liczba resetów procesora: {reset_answers}")


# Wyświetlanie szczegółowych zakresów odpowiedzi
#if correct_ranges:
    #print("\nZakresy odpowiedzi poprawnych:")
    #for range_item in correct_ranges:
        #print(range_item)

if incorrect_ranges:
    print("\nZakresy odpowiedzi niepoprawnych:")
    for range_item in incorrect_ranges:
        print(range_item)
        
#if reset_ranges:
    #print("\nZakresy odpowiedzi niepoprawnych:")
    #for range_item in reset_ranges:
        #print(range_item)


# In[ ]:




