![Version](https://img.shields.io/github/v/release/remmob/itho_amber 'Release')
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg 'Default Home Assistant community store')](https://github.com/custom-components/hacs)
![Latest Release Downloads](https://img.shields.io/github/downloads/remmob/itho_amber/latest/total 'Downloads for the latest release')
![Total Downloads](https://img.shields.io/github/downloads/remmob/itho_amber/total 'Total downloads across all releases')
[![total issues](https://img.shields.io/github/issues/remmob/itho_amber 'Total issues')](https://github.com/remmob/itho_amber/issues)
![Stars](https://img.shields.io/github/stars/remmob/itho_amber)

# Itho Daalderop Amber Heat pump integration
Home Assistant integration for Itho Daalderop Amber heat pump.<br> 
The Amber heat pump family contains 3 models.
- 65 (6,5Kw)
- 95 (9,5Kw)
- 120 (12Kw)

Although only tested with the Amber 95. It should work fine with the other two models.

The Itho Daalderop Amber is produced in Asia for the West European market.<br>
Using a WIN CE as a controller with a custom version of the Heatstar software.

Although there are models/brands using the same controller it is not advisible
to use this integration with other than the three Itho Amber models.
Because of the custom version of the Heatstar software.<br>And
doing so can cause damage to your heat pump.
### <u>Sensor Updates&nbsp;</u>
After changing a sensor value, it can take up sometime (poling time) before it updates.
### <u>Modbus&nbsp;</u>
This integration uses the external Modbus connection on the back of the LCD controller.<br>Connections 1 (RS485B) & 2 (RS485A). 
![Modbus connections](images/Amber%20Modbus%20connection.png)
### <u>Hardware&nbsp;</u>
For this Home Assistant integration, the RS485 serial Modbus connection must be converted to Modbus TCP/IP.<br>
This can be done with standard of shelf modbus RTU RS485 to TCP/IP gateways.<br>
[Waveshare](https://www.waveshare.com) as example, has afordable gateways.<br>
Please make sure you order the right one that supports Modbus TCP, because not all do!<br>
It is possible to use a Raspberry Pi 2 or higer as gateway with 
[this](https://github.com/3cky/mbusd) software.

# Installation
### HACS Custom Repository
On the HACS main page, hit the triple dots menu upper right corner.
click on custom repositories and add https://github.com/remmob/itho_amber as URL
the category must be integration. Click add to save.

### Manual 
Copy the `itho_amber` folder in the `custom_components` folder into your Home Assistant `config/custom_components` folder.<br>
After rebooting Home Assistant, this integration can be configured through the integration setup UI.

## Settings
### Modbus settings
#### Serial: \[\<waveshare\>gateway\]
- Baudrate: 19200 k/bits
- Databits: 8
- stopbit: 1
- flow control: none
- parity: none
#### TCP/IP: \[\<waveshare\>gateway\]
- Device IP: \<IP-address of your (Waveshare) gateway\>
- Subnet mask: \<depends on your network settings (default: 255.255.255.0)>
- Device & destination port: \<default-port: 502\>
- workmode: \<TCP server\>
- device web port: \<80\>
- gateway: \<IP-address-your-router\>
- multihost settings protocol: \<Modbus TCP to RTU\>
### Integration:
- prefix: used for the entity names. (default: amber)<br>
    <i>example: sensor.amber_ambient_temperture_ta</i>
- IP-address: \<IP-address of your gateway\>
- port: \<default-port: 502\> 
- polling time: \<default: 10 seconds\>

## Wiki
Visit the [wiki](https://github.com/remmob/itho_amber/wiki) for more information.

## Known issues
-   The first V2.29 software, released in 5-2024 contains a bug.<br>
    When a Modbus value is written, the days when the legionella program 
    runs, get altered.<br>
    This is known tot Itho and will be resolved in the next update.<br>
    Please contact your installer for information about and how to get the software updates.
-   Settings M1.01, M1.20 and M9.05 have different bandwidth in the Modbus 
    than through the LCD controller.<br>
    For example: M1.01 can be set in the LCD between 1-5°C, in the Modbus
    between 1-3°C. When set above 3°C in the LCD, will display correctly in the integration<br>
    When you set it to 5 in the integration, it reverts back to max 3°C.
-   Some values are read-only. I do not understand why this choice was made by 
    Itho, I have asked them<br> to make all settings writeable... To be continued... 

## Roadmap
- Adding Modbus RTU support
  


