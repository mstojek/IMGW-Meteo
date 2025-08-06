# Plugin IMGW dla Domoticz

Plugin dla platformy Domoticz umożliwiający pobieranie aktualnych danych pogodowych z publicznego API Instytutu Meteorologii i Gospodarki Wodnej (IMGW).

Plugin pozwala na integrację dwóch typów danych:
* **Synoptycznych**, zawierających m.in. temperaturę powietrza, ciśnienie i sumę opadów.
* **Meteorologicznych**, zawierających m.in. intensywność opadów, porywy wiatru i temperaturę gruntu.

Dzięki prostej konfiguracji możesz monitorować wiele różnych stacji i lokalizacji jednocześnie.

**Zakładka "Temperatura":**
<img width="1199" height="146" alt="IMGW-Meteo-plugin-temperatura" src="https://github.com/user-attachments/assets/111ec2ea-1815-430d-bf67-9a1c4acf6f94" />
**Zakładka "Pogoda":**
<img width="1202" height="291" alt="IMGW-Meteo-plugin-Pogoda" src="https://github.com/user-attachments/assets/f5cae73e-4cca-400f-979f-18ae1bb1bd02" />


## Kluczowe Funkcje

* ✅ **Pełna integracja z API IMGW**.
* ✅ Obsługa dwóch typów danych: **Synoptycznych** i **Meteorologicznych**.
* ✅ **Automatyczne tworzenie** odpowiednich czujników w Domoticz.
* ✅ Prosta i elastyczna konfiguracja oparta o zasadę: **jedna stacja = jeden wpis na liście sprzętu**.
* ✅ Możliwość monitorowania wielu lokalizacji jednocześnie.
* ✅ W pełni spolszczony interfejs i opisy.

## Instalacja

Instalacja pluginu wymaga wykonania kilku prostych kroków na serwerze, na którym działa Domoticz.

1.  Przejdź do folderu z pluginami Domoticz:
    ```bash
    cd domoticz/plugins
    ```

2.  Sklonuj repozytorium za pomocą `git` (metoda zalecana):
    ```bash
    git clone [https://github.com/mstojek/IMGW-Meteo.git](https://github.com/mstojek/IMGW-Meteo.git) IMGW-Meteo
    ```
    > **Alternatywnie**, jeśli nie używasz gita, możesz pobrać pliki `.zip` z GitHub, rozpakować je i umieścić folder `IMGW-Meteo` w katalogu `domoticz/plugins`.

3.  Nadaj uprawnienia do wykonywania dla głównego pliku pluginu:
    ```bash
    chmod +x IMGW-Meteo/plugin.py
    ```

4.  Zrestartuj usługę Domoticz:
    ```bash
    sudo systemctl restart domoticz.service
    ```

## Konfiguracja

Konfiguracja pluginu jest bardzo prosta i elastyczna. Opiera się na zasadzie: **jeden dodany sprzęt = jedna monitorowana stacja**. Jeśli chcesz monitorować dane synoptyczne i meteorologiczne (nawet dla tej samej lokalizacji), musisz dodać plugin dwa razy.

1.  W interfejsie webowym Domoticz przejdź do `Ustawienia` -> `Sprzęt`.
2.  Wybierz z listy `IMGW Stacja Pogodowa` i kliknij `Dodaj`.
3.  Wypełnij formularz konfiguracyjny.

---

#### **Przykład 1: Dodanie stacji synoptycznej dla Krakowa**

* **Nazwa:** `Kraków (Synop)` *(Ta nazwa będzie prefiksem dla urządzeń, np. "Kraków (Synop) - Ciśnienie")*
* **Typ danych:** `Synoptyczne`
* **ID stacji:** `12566`

![konfiguracja-synop](https://i.imgur.com/f8p8n1O.png)

---

#### **Przykład 2: Dodanie stacji meteorologicznej dla Krakowa**

1.  Ponownie kliknij `Dodaj` dla typu `IMGW Stacja Pogodowa`.
2.  Wypełnij formularz:
    * **Nazwa:** `Kraków Wola (Meteo)`
    * **Typ danych:** `Meteorologiczne`
    * **ID stacji:** `250190470`

Dzięki takiemu podejściu możesz dodać dowolną liczbę stacji z różnych miast Polski.

### Jak znaleźć ID Stacji?

To kluczowy element konfiguracji. Listy stacji wraz z ich ID znajdziesz pod poniższymi linkami:

* <b>Stacje METEOROLOGICZNE (opady 10-min, temp. gruntu):</b>
    * Otwórz link: [https://danepubliczne.imgw.pl/api/data/meteo/](https://danepubliczne.imgw.pl/api/data/meteo/)
    * Naciśnij `Ctrl+F` i wyszukaj nazwę stacji.
    * Skopiuj wartość z pola `"kod_stacji"`.

* <b>Stacje SYNOPTYCZNE (ciśnienie, temp. powietrza):</b>
    * Otwórz link: [https://danepubliczne.imgw.pl/api/data/synop/](https://danepubliczne.imgw.pl/api/data/synop/)
    * Naciśnij `Ctrl+F` i wyszukaj nazwę miasta.
    * Skopiuj wartość z pola `"id_stacji"`.

## Tworzone Urządzenia

W zależności od wybranego typu danych, plugin automatycznie utworzy następujące urządzenia:

#### Po wybraniu typu `Synoptyczne`:
* `Ciśnienie` (Barometr)
* `Temp/Wilg` (Połączony czujnik temperatury i wilgotności powietrza)
* `Deszcz` (Suma dobowa opadów)
* `Wiatr` (Kierunek, prędkość i temperatura powietrza)

#### Po wybraniu typu `Meteorologiczne`:
* `Temperatura gruntu`
* `Wilgotność`
* `Deszcz` (Intensywność i suma opadów z 10 min)
* `Wiatr` (Kierunek, prędkość i porywy)

## Autor

Plugin został stworzony przez **Gemini (Google AI)**.
