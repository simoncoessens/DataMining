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
  - Assign weather data from closest weather station?
        - Is weather data always pulled from closest weather station?
        - Would it be more accurate to assign a temperature based on trip partitions?
  - Choose a time interval and update weather data only after every time interval



TODO: 2 November
  - Narmina: Anomaly detection techniques ✅
  - Konok: Data Cleaning ✅, Anomaly detection techniques ✅
  - Pepe: Weather data ✅
  - Simon: Visualizations ✅, Seperate journeys ✅

**NEXT MEETING**: thursday 9 november 10:00 

TODO: 9 November:
  - Simon: MobilityDB setup ✅
  - Narmina: Anomaly detection techniques ✅
  - Konok: Local notebook (jupyter) ✅
  - Pepe: other work ✅

for  everyone: 
  - Refresh on Data Mining concepts ✅
  - How to build Data Mining workflows? ✅

WEATHER DATA: 
What weather data are we going to incorporate in the analyis. 
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
- Connect kaggle to local postgres (Simon)
- Adding extra features to the DB (Pepe)
- Correlation, heat map, feature extraction (Konok)
- preprocessing (Narmina)


**NEXT MEETING**: Sunday 19 november 10:00 


**NEXT MEETING:** Thursday 23, November (after going to Data Mining lab)

Classification will be important for the stream outlier detection part of the project

Feature extraction:
- Difference between two sensors
- Temperature categorization

Type portability:
- Numerical to categorical (temperature values)

Descriptive Analytics:
- Narmina has performed sampling rate (it varies)
- Simon has looked into segment speed
- Pepe has looked into bounding box (values not contained in the Belgium geom)

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
- Absolute number of times the temperatures are outside the boundaries for each vehicle_id (maybe there are more for one -> problem with a veh_id). (look at abs_occ_temp.csv in exports)
- Locations of the places where the temperatures are outside of the boundaries.
- Look at the rpm values for when the temperatures are outside the boundaries.
- Are there specific times of day, days of the week, or months where temperature anomalies are more frequent?
- How do external weather conditions correlate with the anomalies in the cooling systems?
- How long do temperature anomalies last, and how severe are they?
- Has the frequency or nature of anomalies changed over the observed period (January 2023 to September 2023)?
- 
