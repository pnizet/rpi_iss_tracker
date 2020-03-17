# rpi_iss_tracker
a raspberry pi ISS tracker displaying map on a [Pimoroni Inky pHAT display](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)

This python script 
* fetch the position of the ISS with the [International Space Station Current Location API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/)
* find the closest city to the ISS position
* display a worlmap with the current position and the last 60 position
* display the name of the closest city and the distance to it


Deeply inspired by [this project](https://www.raspberryconnect.com/projects/39-programming/179-python-project-with-e-ink-display-iss-global-tracker) and adapted to a Pimoroni Inky pHAT
