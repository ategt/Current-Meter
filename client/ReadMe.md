## Current Monitor With Temperature

This uses three inputs.  An analog thermistor from a Pioneer Seed branded digital thermometer wired with two resistors.  Green/White goes from positive five volts (+5V) to a lead on the thermistor and the other lead is joined with two resistors and a green wire under a wire nut.  The green wire goes to A3 analog input on the Arduino development board.  Finally, Orange/White goes from the unwirenutted end of the resistor pair to negative ground on the development board (GND).

In Summary:
* Orange/White&nbsp;&nbsp;&nbsp; Ground
* Green&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Analog 3
* Green/White&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 5V

#

### Quickstart
This project is meant to be used with a server running, launchable from a batch file in the project root.  And also, a python script, which may need to be launched after the server starts, for streaming the readings from a connected Arduino to the server.  This script is also launchable from a batch file in project root.  Once both services are running, the project client user interface can be accessed from a web browser, usually by way of [http://127.0.0.1:5000](http://127.0.0.1:5000).

Right now two versions of the client app can be seen by visiting [http://127.0.0.1:5000/?temperature](http://127.0.0.1:5000/?temperature) for temperature data and [http://127.0.0.1:5000/?watts](http://127.0.0.1:5000/?watts) for power data.  The app defaults to temperature at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

#

To install javascript dependencies the NPM clean-install command is recommended

```
npm ci
```


To build the project 
```
npm run build
```
will put shippable files into the 'distribution' folder.