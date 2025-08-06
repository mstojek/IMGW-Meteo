# -*- coding: utf-8 -*-
#
# IMGW Stacja Pogodowa Plugin
# Author: Gemini, 2025
# Version: 1.7.4 - Simplified data type labels.
#
"""
<plugin key="IMGWMeteo" name="IMGW Stacja Pogodowa" author="Gemini" version="1.7.4" wikilink="https://danepubliczne.imgw.pl/apiinfo" externallink="https://danepubliczne.imgw.pl/api/data/">
    <description>
        <h2>IMGW Stacja Pogodowa v1.7.4</h2>
        <p>Plugin pobiera dane z publicznego API IMGW. Każda stacja (Meteo lub Synop) powinna być dodana jako osobny sprzęt.</p>
        <p>W polu <b> 'Nazwa' </b> dla tego sprzętu wpisz nazwę lokalizacji (np. 'Kraków' lub 'Warszawa-Okęcie'). Będzie ona prefiksem dla wszystkich urządzeń.</p>
        <hr/>
        <h3>Jak znaleźć ID stacji?</h3>
        <ul style="list-style-type:square; margin-left:20px;">
            <li>
                <b>Stacje METEOROLOGICZNE (opady 10-min, temp. gruntu):</b><br/>
                <a href="https://danepubliczne.imgw.pl/api/data/meteo/" target="_blank" style="color: white;">https://danepubliczne.imgw.pl/api/data/meteo/</a> (szukaj: <code>"kod_stacji"</code>)
            </li>
            <br/>
            <li>
                <b>Stacje SYNOPTYCZNE (ciśnienie, temp. powietrza):</b><br/>
                <a href="https://danepubliczne.imgw.pl/api/data/synop/" target="_blank" style="color: white;">https://danepubliczne.imgw.pl/api/data/synop/</a> (szukaj: <code>"id_stacji"</code>)
            </li>
        </ul>
    </description>
    <params>
        <param field="Mode1" label="Typ danych" width="200px">
            <options>
                <option label="Synoptyczne" value="synop" default="true"/>
                <option label="Meteorologiczne" value="meteo"/>
            </options>
        </param>
        <param field="Address" label="ID stacji" width="150px" required="true" default="12566"/>
        <param field="Mode6" label="Tryb debugowania" width="150px">
            <options>
                <option label="Tak" value="Debug"/>
                <option label="Nie" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import json

class BasePlugin:
    # Definicje jednostek
    # Jednostki 1-4 dla Meteo, 5-8 dla Synop
    UNIT_METEO_RAIN, UNIT_METEO_TEMP_GROUND, UNIT_METEO_HUMIDITY, UNIT_METEO_WIND = 1, 2, 3, 4
    UNIT_SYNOP_TEMP_HUM, UNIT_SYNOP_BAROMETER, UNIT_SYNOP_RAIN_DAILY, UNIT_SYNOP_WIND = 5, 6, 7, 8

    def __init__(self):
        self.poll_interval = 60
        self.poll_count = 0
        self.data_type = ""
        self.station_id = ""
        self.api_connection = None

    def onStart(self):
        Domoticz.Log(f"Plugin IMGW Stacja Pogodowa (v1.7.4) wystartował dla '{Parameters['Name']}'.")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            Domoticz.Log("Tryb debugowania włączony.")

        self.data_type = Parameters["Mode1"]
        self.station_id = Parameters["Address"].strip()
        
        Domoticz.Log(f"Konfiguracja: Typ danych='{self.data_type}', ID stacji='{self.station_id}'")

        if self.data_type == "meteo":
            if self.UNIT_METEO_RAIN not in Devices: Domoticz.Device(Name="Deszcz", Unit=self.UNIT_METEO_RAIN, TypeName="Rain", Used=1).Create()
            if self.UNIT_METEO_TEMP_GROUND not in Devices: Domoticz.Device(Name="Temperatura gruntu", Unit=self.UNIT_METEO_TEMP_GROUND, TypeName="Temperature", Used=1).Create()
            if self.UNIT_METEO_HUMIDITY not in Devices: Domoticz.Device(Name="Wilgotność", Unit=self.UNIT_METEO_HUMIDITY, TypeName="Humidity", Used=1).Create()
            if self.UNIT_METEO_WIND not in Devices: Domoticz.Device(Name="Wiatr", Unit=self.UNIT_METEO_WIND, TypeName="Wind", Used=1).Create()
        elif self.data_type == "synop":
            if self.UNIT_SYNOP_TEMP_HUM not in Devices: Domoticz.Device(Name="Temp/Wilg", Unit=self.UNIT_SYNOP_TEMP_HUM, TypeName="Temp+Hum", Used=1).Create()
            if self.UNIT_SYNOP_BAROMETER not in Devices: Domoticz.Device(Name="Ciśnienie", Unit=self.UNIT_SYNOP_BAROMETER, TypeName="Barometer", Used=1).Create()
            if self.UNIT_SYNOP_RAIN_DAILY not in Devices: Domoticz.Device(Name="Deszcz", Unit=self.UNIT_SYNOP_RAIN_DAILY, TypeName="Rain", Used=1).Create()
            if self.UNIT_SYNOP_WIND not in Devices: Domoticz.Device(Name="Wiatr", Unit=self.UNIT_SYNOP_WIND, TypeName="Wind", Used=1).Create()
        
        self.poll_count = self.poll_interval - 1

    def onHeartbeat(self):
        self.poll_count += 1
        if self.poll_count >= self.poll_interval:
            self.poll_count = 0
            Domoticz.Log(f"Rozpoczynanie pobierania danych {self.data_type.upper()} dla stacji: {self.station_id}")
            self.api_connection = Domoticz.Connection(Name=f"IMGW {self.data_type.upper()}", Transport="TCP/IP", Protocol="HTTPS", Address="danepubliczne.imgw.pl", Port="443")
            self.api_connection.Connect()

    def onConnect(self, Connection, Status, Description):
        if Status == 0:
            Domoticz.Debug("Połączono z serwerem IMGW.")
            api_path = f"/api/data/{self.data_type}/id/{self.station_id}"
            sendData = {'Verb':'GET', 'URL': api_path, 'Headers': {'Host': 'danepubliczne.imgw.pl', 'User-Agent': 'Domoticz-IMGW-Plugin', 'Accept': 'application/json'}}
            Connection.Send(sendData)
        else:
            Domoticz.Error(f"Połączenie z serwerem IMGW nie powiodło się: {Description}")

    def onMessage(self, Connection, Data):
        try:
            if str(Data["Status"]) == '200':
                api_data_raw = Data["Data"].decode("utf-8", "ignore")
                Domoticz.Debug(f"Otrzymano dane: {api_data_raw}")
                api_data = json.loads(api_data_raw)
                
                if not api_data: 
                    Domoticz.Error(f"Otrzymano pustą odpowiedź z API dla {self.data_type}.")
                    return
                
                Domoticz.Log(f"Pomyślnie pobrano i przetworzono dane {self.data_type.upper()}.")
                if self.data_type == "meteo":
                    self.update_meteo_devices(api_data[0])
                elif self.data_type == "synop":
                    self.update_synop_devices(api_data)
            else:
                Domoticz.Error(f"API IMGW zwróciło błąd HTTP {Data['Status']}.")
        except Exception as e:
            Domoticz.Error(f"Wystąpił błąd w onMessage: {str(e)}")

    def update_meteo_devices(self, data):
        Domoticz.Debug("Aktualizowanie urządzeń Meteo...")
        if data.get("opad_10min") is not None:
            rain_10min = float(data["opad_10min"])
            rain_rate = rain_10min * 6
            current_total = float(Devices[self.UNIT_METEO_RAIN].sValue.split(';')[1]) if ';' in Devices[self.UNIT_METEO_RAIN].sValue else 0.0
            UpdateDevice(self.UNIT_METEO_RAIN, 0, f"{rain_rate:.1f};{current_total + rain_10min:.2f}")
        if data.get("temperatura_gruntu") is not None:
            UpdateDevice(self.UNIT_METEO_TEMP_GROUND, 0, str(data["temperatura_gruntu"]))
        if data.get("wilgotnosc_wzgledna") is not None:
            humidity = float(data["wilgotnosc_wzgledna"])
            UpdateDevice(self.UNIT_METEO_HUMIDITY, int(humidity), "0" if humidity < 40 else ("2" if humidity > 70 else "1"))
        if data.get("wiatr_kierunek") is not None and data.get("wiatr_srednia_predkosc") is not None:
            bearing = int(data["wiatr_kierunek"])
            direction_str = self.get_wind_direction_str(bearing)
            speed_ms = float(data["wiatr_srednia_predkosc"])
            gust_ms = float(data.get("wiatr_predkosc_maksymalna", speed_ms))
            UpdateDevice(self.UNIT_METEO_WIND, 0, f"{bearing};{direction_str};{int(speed_ms * 10)};{int(gust_ms * 10)};0;0")

    def update_synop_devices(self, data):
        Domoticz.Debug("Aktualizowanie urządzeń Synop...")
        temp = float(data["temperatura"]) if data.get("temperatura") is not None else 0.0
        
        if data.get("temperatura") is not None and data.get("wilgotnosc_wzgledna") is not None:
            hum = float(data["wilgotnosc_wzgledna"])
            hum_stat = 0 if hum < 40 else (2 if hum > 70 else 1)
            UpdateDevice(self.UNIT_SYNOP_TEMP_HUM, 0, f"{temp:.1f};{hum:.1f};{hum_stat}")
        
        if data.get("cisnienie") is not None:
            pressure = float(data["cisnienie"])
            forecast = "2" if 990 <= pressure <= 1010 else ("3" if pressure < 990 else ("4" if pressure < 1010 else ("0" if pressure > 1030 else "1")))
            UpdateDevice(self.UNIT_SYNOP_BAROMETER, 0, f"{pressure:.1f};{forecast}")
        
        if data.get("suma_opadu") is not None:
            UpdateDevice(self.UNIT_SYNOP_RAIN_DAILY, 0, f"0;{float(data['suma_opadu']):.2f}")
        
        if data.get("kierunek_wiatru") is not None and data.get("predkosc_wiatru") is not None:
            bearing = int(data["kierunek_wiatru"])
            direction_str = self.get_wind_direction_str(bearing)
            speed_kmh = float(data["predkosc_wiatru"])
            speed_ms = speed_kmh / 3.6
            UpdateDevice(self.UNIT_SYNOP_WIND, 0, f"{bearing};{direction_str};{int(speed_ms * 10)};{int(speed_ms * 10)};{temp:.1f};0")

    def get_wind_direction_str(self, degrees):
        dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        return dirs[round(degrees / (360. / len(dirs))) % len(dirs)]

    def onStop(self):
        Domoticz.Log("Plugin IMGW Stacja Pogodowa zatrzymany.")

    def onError(self, Connection, Status, Description):
        Domoticz.Error(f"Błąd połączenia {Connection.Name}: {Description}")

    def onDisconnect(self, Connection):
        Domoticz.Debug(f"Rozłączono z {Connection.Name}")

_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onStop():
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    _plugin.onMessage(Connection, Data)

def onHeartbeat():
    _plugin.onHeartbeat()

def onError(Connection, Status, Description):
    _plugin.onError(Connection, Status, Description)

def onDisconnect(Connection):
    _plugin.onDisconnect(Connection)

def UpdateDevice(Unit, nValue, sValue):
    if Unit in Devices and (Devices[Unit].nValue != nValue or Devices[Unit].sValue != str(sValue)):
        Devices[Unit].Update(nValue=nValue, sValue=str(sValue))
        Domoticz.Log(f"Aktualizacja urządzenia (Unit: {Unit}): nValue={nValue}, sValue='{sValue}'")
