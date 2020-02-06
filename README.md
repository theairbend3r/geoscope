# GeoScope

You can find the video demo [here](https://www.youtube.com/watch?v=xW_Yzzs3_ys&feature=youtu.be).

A natural disaster is a devastating event caused by rain, wind, fire, and even earth that endangers people's lives and property. Natural disasters claim thousands of lives every year. One of the most important aspects of managing a natural disaster is to identify the people affected by it. Our app will create a centralised database that will enable the relatives as well as relief teams dispatched by the government to conduct a crowd sourced, real time census of people affected by a natural disaster. The rescue teams will upload facial photos of the people rescued along with any personal information they can obtain like name, mobile number, date of birth, age, and address. They will then append information like the coordinates of where the said person was rescued from, the status of his injury, and the relief camp/hospital he was taken to. Now, there is a high possibility that the person is either unconcious, dead, or unable to respod to questions. This is where the facial recognition part will step in. The friends, neighbours, and relatives of that person can upload a single picture on our server. We will then match that information with the available pitcures in our database (using One Shot Learning). If a match is found, the information about that person will be returned. People who have been taken to the relief camps can further provide information about their neighbours and the people that they know. All the information will aggregated and duplications merged. This way, an accurate estimate of the affected population can be identified using crowd sourced information which will greatly help the relief teams in planning out their rescue operations. People who are stranded can also mark their locations on a map along with their essential information like picture, name, age etc. This information will be made available to the relief teams(volunteers, army, navy), who can then take better decisions based on the population density in different regions made available on a map using the GoogleMaps API.

The application will have three views. One for the admin team who are coordinating this operation, one for the rescue personnel (army, navy, voluneers) who will upload photos and information to the server, and one for the relatives and friends to look up people using the facial recognition(and other personal information) feature.

For this project, Flask and SQL database is used in the backend. HTML, CSS, and JavaScript is used to develop the front end. Google Maps API is used to plot the location of hospitals, relief camps, and the place survivors are found. OpenCV is used to handle the facial recognition part.