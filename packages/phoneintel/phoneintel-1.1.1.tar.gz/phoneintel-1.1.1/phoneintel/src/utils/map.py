#!/usr/bin/env python3
##########################################
#                                        #
#      CREATED BY THE PHONEINTEL TEAM    #
#                                        #
##########################################
#                                        #
# ALL INFORMATION IS SOURCED EXCLUSIVELY #
#      FROM OPEN SOURCE AND PUBLIC       #
#               RESOURCES                #
#                                        #
#   THIS SOFTWARE IS PROVIDED "AS IS",   #
#   WITHOUT WARRANTY OF ANY KIND,        #
#   EXPRESS OR IMPLIED, INCLUDING BUT    #
#   NOT LIMITED TO THE WARRANTIES OF     #
#   MERCHANTABILITY, FITNESS FOR A       #
#   PARTICULAR PURPOSE AND               #
#   NONINFRINGEMENT.                     #
#                                        #
#   IN NO EVENT SHALL THE AUTHORS OR     #
#   COPYRIGHT HOLDERS BE LIABLE FOR ANY  #
#   CLAIM, DAMAGES OR OTHER LIABILITY,   #
#   WHETHER IN AN ACTION OF CONTRACT,    #
#   TORT OR OTHERWISE, ARISING FROM,     #
#   OUT OF OR IN CONNECTION WITH THE     #
#   SOFTWARE OR THE USE OR OTHER         #
#   DEALINGS IN THE SOFTWARE.            #
#                                        #
#     THIS NOTICE MUST REMAIN INTACT     #
#   FOR CODE REDISTRIBUTION UNDER THE    #
#           GPL-3.0 license              #
#                                        #
##########################################

import requests
import webbrowser
import json
from phoneintel.src.utils.const import separator, COUNTRY_COORDINATES_JSON

class PhoneIntelMap:
    
    def __init__(self, country: str, state: str = None, lat:str='', lon:str='' ) -> None:
        self.__country = country
        self.__state = state
        self.__api = None
        self.__lon = None
        self.__lat = None
        self.coordinates_json_path = COUNTRY_COORDINATES_JSON 
        self.__req_coordinates()
        if lat == '' or lon == '':
            try:
                self.__make_req()
                if self.__lon:
                    self.open_map()
            except Exception as e:
                print(f"An error occurred: {e}")

        else:
            self.__lon = lon
            self.__lat = lat
            try:
                self.open_map()
            except Exception as e:
                print(f"An error occurred: {e}")
            
    def __req_coordinates(self):
        
        self.__load_coordinates_from_json()
            
            
    def __load_coordinates_from_json(self):
        try:
            with open(self.coordinates_json_path, 'r') as f:
                data = json.load(f)
                for entry in data["country_info"]:
                    if entry["country"].lower() == self.__country.lower():
                        self.__lat = str(entry["latitude"])
                        self.__lon = str(entry["longitude"])
                        break
                if self.__lat is None or self.__lon is None:
                    raise ValueError(f"No coordinates found for country: {self.__country}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Coordinates JSON file not found at {self.coordinates_json_path}")
        except json.JSONDecodeError:
            raise ValueError("Error decoding the JSON file")
    
    def __make_req(self):
        if not self.__api and (self.__lat is None or self.__lon is None):
            raise ValueError("API URL is not set and coordinates are not found in the JSON. Call req_coordinates() first.")

        if self.__api:
            try:
                response = requests.get(self.__api, timeout=5)
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                separator()
                print(f"[!] Error in map request {e}")
            except requests.exceptions.RequestException as e:
                separator()
                print(f"[!] Error in map request {e}")

            if response.status_code == 200:
                response_data = response.json()
                if 'latitude' in response_data and 'longitude' in response_data:
                    self.__lon = response_data['longitude']
                    self.__lat = response_data['latitude']
                else:
                    raise ValueError("No coordinates found for the provided location.")
            else:
                separator()
                print(f"[!] Error in map request")
            
    def open_map(self):
        
        if self.__lon and self.__lat:
            map_url = f"https://www.openstreetmap.org/?mlat={self.__lat}&mlon={self.__lon}#map=12/{self.__lat}/{self.__lon}"
            webbrowser.open(map_url)
        else:
            raise ValueError("Coordinates are not set. Ensure the API request was successful.")

