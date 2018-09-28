# Entity_Classify
In search engine area, when a user inputs a query "Big Bang", what actually it is? Physical terminology? Or Sheldon's show? A general way is to calculate the probability distribution of "Big Bang" and return the results concerning with most likely intention. That is if 83% of "Big Bang" actually mean the TV show, then this search engine will find more information about show rather than physics.  However, this probability is **static**, the **primary** intention will change dramatically as time went by, an events like new cosmic physics theory is discovered will dramatically change that probability! The "Big Bang" may not be a TV series any more, what "Apple" is today is not what it is tomorrow. Thus, to **update** this probability distribution is crucial for providing an high precision and high recall searching results.


## OverView
This integrated module automatically provides the **newest** probability distribution of an entity which can be used in **user intension identify**, **real-time ambiguous entity classifying**, **Query-Answer system log analysis** and so forth. It automatically catches up with **newest** data collected from mainstream search engine, cleans data, extracts feature, trains probability model, calculate probability distribution and analyze result.

To ensure a satisfying classification result, this module is designed to be highly **flexible**, users are able to customize quite a few parameters and pipeline features, from training parameters, training features to document representation parameters.

> Example input:
> Pocahontas

> Example output:

> | Movie| Music|Person|Location|Restaurant|Dish|
> | ---- |:----:| ----:| ------:| --------:| --:|
> | 32%  | 22%  |31%   |10%     |4%        |1%  |

## Implementaion

## Evaluation

## Command
