# Plugin IMGW dla Domoticz

Plugin dla platformy Domoticz umożliwiający pobieranie aktualnych danych pogodowych z publicznego API Instytutu Meteorologii i Gospodarki Wodnej (IMGW).

Plugin pozwala na integrację dwóch typów danych:
* **Synoptycznych**, zawierających m.in. temperaturę powietrza, ciśnienie i sumę opadów.
* **Meteorologicznych**, zawierających m.in. intensywność opadów, porywy wiatru i temperaturę powietrza.

Dzięki prostej konfiguracji możesz monitorować wiele różnych stacji i lokalizacji jednocześnie.

**Zakładka "Temperatura":**
<img width="1189" height="138" alt="IMGW-Meteo-plugin-temperatura" src="https://github.com/user-attachments/assets/1c6d1261-b720-4af3-a0d1-cd197b8d0319" />

**Zakładka "Pogoda":**
<img width="1184" height="272" alt="IMGW-Meteo-plugin-Pogoda" src="https://github.com/user-attachments/assets/3f7a9b2c-e9cd-4b22-88ba-44954cc8473b" />

## Kluczowe Funkcje

* ✅ **Pełna integracja z API IMGW**.
* ✅ Obsługa dwóch typów danych: **Synoptycznych** i **Meteorologicznych**.
* ✅ **Automatyczne tworzenie** odpowiednich czujników w Domoticz.
* ✅ Prosta i elastyczna konfiguracja oparta o zasadę: **jedna stacja = jeden wpis na liście sprzętu**.
* ✅ Możliwość monitorowania wielu lokalizacji jednocześnie.
* ✅ W pełni spolszczony interfejs i opisy.
* ✅ **Konfigurowalny interwał** odświeżania danych.
* ✅ Odporność na brakujące dane z niektórych stacji.

## Instalacja

Instalacja pluginu wymaga wykonania kilku prostych kroków na serwerze, na którym działa Domoticz.

1.  Przejdź do folderu z pluginami Domoticz:
    ```bash
    cd domoticz/plugins
    ```

2.  Sklonuj repozytorium za pomocą `git` (metoda zalecana):
    ```bash
    git clone https://github.com/mstojek/IMGW-Meteo.git
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

* **Nazwa:** `IMGW Kraków` *(Ta nazwa będzie prefiksem dla urządzeń, np. "IMGW Kraków - Ciśnienie")*
* **Typ danych:** `Synoptyczne`
* **ID stacji:** `12566`
* **Interwał odpytywania (minuty):** `10` *(Domyślnie 10 minut. Zmień według potrzeb. Wartość większa niż 10 minut może spowodowac że dane Meteorologiczne o opadach będą niepoprawne)*

<img width="974" height="733" alt="IMGW-plugin-konfiguracja" src="https://github.com/user-attachments/assets/5d094c02-39dd-46a1-beac-c5ff0d9878e6" />

---

#### **Przykład 2: Dodanie stacji meteorologicznej dla Krakowa**

1.  Ponownie kliknij `Dodaj` dla typu `IMGW Stacja Pogodowa`.
2.  Wypełnij formularz:
    * **Nazwa:** `Kraków Wola (Meteo)`
    * **Typ danych:** `Meteorologiczne`
    * **ID stacji:** `250190470`
    * **Interwał odpytywania (minuty):** `10`

Dzięki takiemu podejściu możesz dodać dowolną liczbę stacji z różnych miast Polski.

### Jak znaleźć ID Stacji?

To kluczowy element konfiguracji. Listy stacji wraz z ich ID znajdziesz pod poniższymi linkami:

* <b>Stacje METEOROLOGICZNE (opady 10-min, temp. powietrza):</b>
    * Otwórz link: [https://danepubliczne.imgw.pl/api/data/meteo/](https://danepubliczne.imgw.pl/api/data/meteo/)
    * Naciśnij `Ctrl+F` i wyszukaj nazwę stacji.
    * Skopiuj wartość z pola `"kod_stacji"`.

* <b>Stacje SYNOPTYCZNE (ciśnienie, opady, temp. powietrza):</b>
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
* `Temp/Wilg` (Temperatura i wilgotność powietrza)
* `Deszcz` (Intensywność i suma opadów z 10 min)
* `Wiatr` (Kierunek, prędkość i porywy)

## Autor

Plugin został stworzony przez **Gemini (Google AI)**.
