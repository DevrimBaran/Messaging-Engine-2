# Neighbour discovery concept

We have an arbitrary amount of devices which will be able to send messages to each other.
Thus each of them has to know if and how to reach the target device.


# Network topology
Description of all connected devices in the IoT environment:
Contains: names, addresses, available operations

Fully connected

# Scenarios

1. New device connects
2. Device loses connection
3. Same device connects after it lost connection
4. Recovery after power failure
5. Device is connected and reachable but doesn't response due to internal error
6. Sender kann verbindung an Empfänger verlieren-> Nachricht über einen Nachbar weiterleiten, der eine Verbindung zum Empfänger hat

### Solutions

#### 1. New device connects

Three approaches: (Paper: A lightweight messaging engine for decentralized data processing in
the Internet of Things)
1. Publishing the information of the new device through a central component (not wished)
2. Publishing *hello messages* from the newly added device to other devices
3. Sending a multicast message from the newly added device to all other devices

-> A combination of 2. and 3. could be good (TBD)

#### Possible Problems through these approaches:

TODO 

#### 2. Device loses connection

We have to distinguish between planned and unplanned connection losses.

- planned: The device which wants to disconnect has to inform all other devices of it's unavailability in the future.
This can be done by sending a *goodbye message*

#### 3. Same device connects after it lost connection

#### 4. Recovery after power failure

#### 5. Device is connected reachable but doesn't response due to internal error

# Initialization
Woher wissen wir, dass sich ein neues Gerät verbunden hat?
- Das neue Gerät muss an alle anderen Teilnehmer eine *hello messsage* schicken

Woher weiß das neue Gerät an welche Adressen es eine hello nachricht schicken muss?
- Das neue Gerät kann das Netzwerk nach anderen Geräten scannen und schauen, ob sie das entsprechende PIME-Port offen haben. An diese wird dann eine nachricht geschickt und auf eine antwort gewartet.

# Algorithms






# Implementation


##IDEAS

Caches:
1. Destination Cache: Beinhaltet alle Ziele, an die bereits eine Nachricht gesendet wurde. Jeder Enthält den nächsten Hop zum gewünschten Ziel.

Router advertisements: Jedes Gerät verschickt nach einer bestimmten Zeit Nachrichten um die anderen Geräte über ihre Anwesenheit in Kenntniss zu setzen (heartbeat?)



##Questions:

Wie ist die Netzwerktopologie?
- Fully Connected

Haben wir eine Management Komponente?
- Nein!