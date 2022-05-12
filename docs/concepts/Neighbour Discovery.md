# Neighbour discovery concept

We have an arbitrary amount of devices which will be able to send messages to each other.
Thus each of them has to know if and how to reach the target device.


# Network topology

All of our devices are fully connected

# Initialization

How do we know that a new device has connected?
- The new device has to send a *hello message* to all the other devices

From where does the new device know to which addresses it has to send a *hello messages*
- The new device is capable to search after other devices in the same network and to look if they have the respective PIME-port open.
  Then it will send the *home message' to them.

# Scenarios

1. New device connects
2. Device loses connection
3. Connection recovery

## Solutions

### 1. New device connects

Three approaches: (Paper: A lightweight messaging engine for decentralized data processing in
the Internet of Things)
1. Publishing the information of the new device through a central component (not wished)
2. Publishing *hello messages* from the newly added device to other devices
3. Sending a multicast message from the newly added device to all other devices

-> A combination of 2. and 3. could be good

#### Possible Problems through these approaches:

1. We want a decentralized messaging engine, why we can't use this approach
2. If one device loses connection, the message can't be forwarded and will be lost
3. Direct connection to the receiver could be lost. The message will never reach the receiver

#### Problem solving
To solve problems 2 and 3 we can combine the approaches 2 and 3. So even if one Approach fails the other one could have success if the receiver stays in the network.


### 2. Device loses connection

We have to distinguish between planned and unplanned connection losses.

- planned: The device which wants to disconnect has to inform all other devices of it's unavailability in the future.
This can be done by sending a *goodbye message* by combining the above approaches 2 and 3
- unplanned: When devices are unable consistently to deliver a message, they then will recognize that the receiver has some problems. Or the devices could periodically check their health status.

### 3. Connection recovery
Assume that all devices are connected well. But what happens if one device gets disconnected planned or unplanned and connects back after that?
Do we have to recognize this device as a known one? Or can we just assume that it's a new device?


- planned disconnect:
Every device that disconnects planned will be recognized as a new device. They won't have any unfinished tasks to perform from the previous connection.
Since they have sent a goodbye message to the other devices they will have marked this device as unavailable.

- unplanned disconnection:
two ways <br>
1. timed reconnection: the disconnected device has to reconnect until a specific deadline. After the deadline it will be recognized as a new device
2. independently of the disconnected time, the device will be recognized as a known one


#### Note:
The lost devices will have to search in their database for their own *uuid*. If there is none they have to generate a new one. But the consequence of this will be, that they can't be recognized as a known device.
If there exists an *uuid* they will send it with a hello message and since it was connected with the other devices in the past, they will have saved this *uuid* and change it's status to available. 
If a message was sent previously and none answer was received, then the sender could send the same message again to the receiver. 


##IDEAS

hello message:
- ip adresse
- uuid of the device: new generated if none exists in database of the device itself
- sensors
- actuators

Caches:
- Destination Cache: Consists all targets to which it sent a message. Every entry has the next hop to the respective target.

Router advertisements: Every device sends a hello message after a specific time to notify all the other devices about its present 
