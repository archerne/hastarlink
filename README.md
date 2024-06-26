# Please use the offical integration

This integration has beem replaced with the offical HomeAssistant integration: https://www.home-assistant.io/integrations/starlink


# Starlink Statistics and Alerts Integration

This integration will provide sensors for Starlink Statistics and Alerts information from the Starlink Dish.
Please make sure that you can get to <a target="_blank" href="http://192.168.100.1/">this site<a> (http://192.168.100.1) on your home assistant instance.

####  Stat Sensors:
- Downlink Throughput
- Ping Drop Rate
- Ping Latency
- Software Version
- State
- Uplink Throughput
- Uptime
- Latitude
- Longitude
- Altitude

####  Alert Sensors:
- Install Pending
- Is Heating
- Mast Not Near Vertical
- Motors Stuck
- Obstructed
- Roaming
- Slow Ethernet Speeds
- Thermal Shutdown
- Thermal Throttle
- Unexpected Location

####  Buttons:
- Reboot
- Stow
- Unstow

## (Optional) Enable Location

This step is only required if you want to see the latitude, longitude, and altitude in homeassistant (otherwise those sensors will just be blank).

Access to location data must be enabled per dish and currently (2022-Sep), this can only be done using the Starlink mobile app, version 2022.09.0 or later. It cannot be done using the browser app. To enable access, you must be logged in to your Starlink account. You can log in by pressing the user icon in the upper left corner of the main screen of the app. Once logged in, from the main screen, select SETTINGS, then select ADVANCED, then select DEBUG DATA. Scroll down and you should see a toggle switch for "allow access on local network" in a section labelled STARLINK LOCATION, which should be off by default. Turn that switch on to enable access or off to disable it. This may move in the future, and there is no guarantee the ability to enable this feature will remain in the app.

Note that the Starlink mobile app can be pretty finicky and painfully slow. It's best to wait for the screens to load completely before going on to the next one.

## Install

Install from the custom HACS repository or by copying the contents of the starlink folder into your custom_components/starlink folder and rebooting your Home Assistant, go to Configuration -> Integrations and click the + to add a new integration.

Search for Starlink and you will see the integration available.

Click add, confirm you want to install

<a target="_blank" href="https://www.buymeacoffee.com/archerne"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy me a coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;"></a>

## Thanks
A large thanks to Sparky8512 for providing the kick start to all of this, this uses modified versions of scripts from https://github.com/sparky8512/starlink-grpc-tools
