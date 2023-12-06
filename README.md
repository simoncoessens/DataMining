README: 
Data Mining project for the Data Mining course at ULB.

```

 ______   ________   _________  ________       ___ __ __    ________  ___   __     ________  ___   __    _______     
/_____/\ /_______/\ /________/\/_______/\     /__//_//_/\  /_______/\/__/\ /__/\  /_______/\/__/\ /__/\ /______/\    
\:::_ \ \\::: _  \ \\__.::.__\/\::: _  \ \    \::\| \| \ \ \__.::._\/\::\_\\  \ \ \__.::._\/\::\_\\  \ \\::::__\/__  
 \:\ \ \ \\::(_)  \ \  \::\ \   \::(_)  \ \    \:.      \ \   \::\ \  \:. `-\  \ \   \::\ \  \:. `-\  \ \\:\ /____/\ 
  \:\ \ \ \\:: __  \ \  \::\ \   \:: __  \ \    \:.\-/\  \ \  _\::\ \__\:. _    \ \  _\::\ \__\:. _    \ \\:\\_  _\/ 
   \:\/.:| |\:.\ \  \ \  \::\ \   \:.\ \  \ \    \. \  \  \ \/__\::\__/\\. \`-\  \ \/__\::\__/\\. \`-\  \ \\:\_\ \ \ 
    \____/_/ \__\/\__\/   \__\/    \__\/\__\/     \__\/ \__\/\________\/ \__\/ \__\/\________\/ \__\/ \__\/ \_____\/ 

```

```
___________   _______________________________________^__
 ___   ___ |||  ___   ___   ___    ___ ___  |   __  ,----\                     Simon Coessens
|   | |   |||| |   | |   | |   |  |   |   | |  |  | |_____\                      Pepe Jose Carlos
|___| |___|||| |___| |___| |___|  | O | O | |  |  |        \                       MD Kamrul Islam
           |||                    |___|___| |  |__|         )                        Narmina Mahmudova
___________|||______________________________|______________/
           |||                                        /--------
-----------'''---------------------------------------'
```

How to import weather data: 
  - Assign weather data from the closest weather station.
        - Is weather data always pulled from the closest weather station?
        - Would it be more accurate to assign a temperature based on trip partitions?
  - Choose a time interval and update weather data only after every time interval



TODO: 2 November
  - Narmina: Anomaly detection techniques ✅
  - Konok: Data Cleaning ✅, Anomaly detection techniques ✅
  - Pepe: Weather data ✅
  - Simon: Visualizations ✅, Separate journeys ✅

**NEXT MEETING**: thursday 9 november 10:00 

TODO: 9 November:
  - Simon: MobilityDB setup ✅
  - Narmina: Anomaly detection techniques ✅
  - Konok: Local notebook (jupyter) ✅
  - Pepe: other work ✅

for  everyone: 
  - Refresh on Data Mining concepts ✅
  - How to build Data Mining workflows? ✅
  - ![image](https://github.com/simoncoessens/DataMining/assets/129620441/c3b7423b-24a5-4186-ad73-a1e03bacf0ac)



WEATHER DATA: 
What weather data are we going to incorporate in the analysis? 
- ``Temperature``
- ```Humidity```
- ````Snowfall````
- ```Rain```

**NEXT MEETING**: thursday 16 november 10:00 


NEXT STEPS: 

Feature extraction: 
- Labeling the anomalies


 1. Data cleaning ( output: .csv)
	2.	Database creation
	3.	Add features to the DB
	4.	Feature extraction
	5.	Data mining algorithms

TASKS: 
- Connect Kaggle to local postgres (Simon) ✅
- Adding extra features to the DB (Pepe) ✅
- Correlation, heat map, feature extraction (Konok) ✅
- preprocessing (Narmina) ✅


**NEXT MEETING**: Sunday 19 november 10:00 


**NEXT MEETING:** Thursday 23, November (after going to the Data Mining lab)

Classification will be important for the stream outlier detection part of the project

Feature extraction:
- Difference between two sensors
- Temperature categorization

Type portability:
- Numerical to categorical (temperature values)

Descriptive Analytics:
- Narmina has performed sampling rate (it varies)
- Simon has looked into segment speed
- Pepe has looked into the bounding box (values not contained in the Belgium geom)

Noisy entries:
- Konok mentioned binning to clean the noisy entries

Distance:
- Distance to weather pull sensors can be included in the outlier detection analysis

Clustering:
- Could be useful to clean data (if a data point doesn't end up in a cluster it could be considered an outlier)

Topics to be investigated:
- Narmina: Classification and model validation data preparation
- Konok: Clustering
- Simon: Frequent patterns and association rule mining
- Pepe: Outlier mining


**Basic research questions:**
1. Absolute number of times the temperatures are outside the boundaries for each vehicle_id (maybe there are more for one -> problem with a veh_id).\
	SIMON: ✅ Look at R1.ipynb in exports


2.  Locations of the places where the temperatures are outside of the boundaries.\
	SIMON: 🔄 


3.  Look at the rpm values for when the temperatures are outside the boundaries\
   	NARMINA: ✅ Look at R3.ipynb in exports


4. Are there specific times of day, days of the week, or months where temperature anomalies are more frequent?\
   	KONOK: ✅ Look at R4_R5.ipynb in exports


5. How do external weather conditions correlate with the anomalies in the cooling systems?\
   	KONOK: ✅ Look at R4_R5.ipynb in exports


6. How long do temperature anomalies last, and how severe are they?\
   	KONOK: 🔄  working on it


7.  Has the frequency or nature of anomalies changed over the observed period (January 2023 to September 2023)?\
   	NARMINA: ✅ Look at R7.ipynb in exports


8. Look at the speed and find anomalies\
   	SIMON: 🔄 working on it


9. Look at the internal temperature sensor values that exceed certain differences with the ambient temperature\
	PEPE: 🔄 working on it


10. Look at the differences between the pairs of sensors. Look at other attributes when they deviate from each other \
	PEPE: 🔄 working on it


**Ideas on things for the stream bonus task**
- Algorithm that checks incoming locations if the speed is within boundaries, it flags incorrect location
- Algorithm that checks incoming temperatures and checks the duration of occurrences when the temperature is outside of boundaries and then reports
