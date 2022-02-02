# PerfSONAR

PerfSONAR (https://www.perfsonar.net/) is a network measurement toolkit that monitors and stores network performance data between pairs of endpoints (links).
There are thousands of PerfSONAR endpoints all over the world, organized in different meshes. 
We are specially interested in a mesh that covers around 250 of them. 
Since each endpoint measures perfomance to each other endpoint total number of links monitored is 250^2.
<img src="images/perfsonarmap.png" width="400" >
There are four main types of measurement that describe link characteristics:

* packet loss rate - percentage of lost packets over the total transferred packets in 1 minute intervals (actually measured at 10Hz)
* one way delay - measures delay (in ms) separately for each direction of a path
* throughput - measures the amount of data that can be transferred over a period of time (25 seconds)
* traceroute - finds the path between the source and destination and the transition time

All the data is stored and can be easily accessed from Elasticsearch cluster at University of Chicago.
Here an example of first free data types for one link:
<img src="images/perfsonarplot.png" width="800" >


  
