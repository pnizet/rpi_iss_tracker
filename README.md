# rpi_iss_tracker
a raspberry pi ISS tracker displaying map on a Pimoroni Phat e-ink display

This python script 
* fetch the position of the ISS with the [International Space Station Current Location API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/)
* find the closest city to the ISS position
* display a worlmap with the current position and the last 60 position
* display the name of the closest city and the distance to it

Display is made on a Pimoroni Phat
