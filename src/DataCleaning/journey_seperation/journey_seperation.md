# Explanation on Journey seperation

For each ````mapped_veh_id````  we will split up the given data in seperate train journeys. 

**Definition of train journey**:
- Data for each ````mapped_veh_id```` is given in some parts that are continuous and some time jumps
- A train journey is a continuous (with relation to time) subset of the data


**Why useful to split up in train journeys?**:
- An added parameter ````running_time```` can be added, intuitively the longer a train has been running the greater the chance of a failure
- etc.

