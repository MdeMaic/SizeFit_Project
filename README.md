# Fit-size Recommender | Project


## Objective
The current size guide used in Zara Kids is a table not very user-friendly. The objective of this project is create a size recommendator using a picture of the user and a Machine Learning model that validate the picture and recommend the best size according to the main measures.

![proposal](presentation/images/proposal.png)


## Instructions

####### MAKE CHANGES #######

Two datasets are given in a [kaggle competition](https://www.kaggle.com/c/avila-bible-datamad0120)

- Train Set: with the following columns. 

| Feature | Description |
| --- | --- |
|`id` | only for test & sample submission files, id for prediction sample identification |
|`carat`| weight of the diamond |
|`cut`| quality of the cut (Fair, Good, Very Good, Premium, Ideal) |
|`color`| diamond colour, from J (worst) to D (best) |
|`clarity`| a measurement of how clear the diamond is (I1 (worst), SI2, SI1, VS2, VS1, VVS2, VVS1, IF (best)) |
|`x`| length in mm |
|`y`| width in mm |
|`z`| depth in mm |
|`depth`| total depth percentage = z / mean(x, y) = 2 * z / (x + y) (43--79) |
|`table`| width of top of diamond relative to widest point (43--95) |

| Independent variable | Description |
| --- | --- |
|`price` | price in USD |

- Test Set: With the same features of the training set but in this case without the price, that has to be predicted using the ML model. 

- Submit Set: Id the test set with the only columns of “id” and “price”. This set has to be submitted to Kaggle competition that will return a score based on the MRSE. The lower this score, the better model you are delivering. 


## Resources and libraries
- Sklearn | Machine Learning Library with regression models
- CV2 | Image treatment for python
- Tkinter | GUI for python


## Inputs
- train_human_dataset_images | Shape 565
- train_not_human_dataset_images | Shape 590
- test_kids_dataset_images | Shape 50
- Updated size dataset 


## Outputs
- Models trained
- Code to recommendation


## Methodology
1. Generate the strategy

2. Cleaning and create all datasets
The following decision has to be done 
    - Ensure not Null values
    - Avoid not numeric values
    - Drop the high correlated features
    - Standardize or normalize high-value range features
    - Get all images path

3. Identify the best model
Different models apport different results. Some of them are analysed in the project.
    - LinearClassification
    - RandomForestClassification
    - HistGradientBoostingClassification

4. Analyse the result
There are metrics from sklearn that help you to choose the best model
    - Accuracy score
    - MRSE…

![model_result](presentation/images/result_table.jpg)


5. Generate the cv2 image treatment
    - Get measures in the picture
    - Ensure pixel per metric transformation
    - Save this measures

6. Recommend using query to the size Dataset



## Results
![Result table](/outputs/img/results.png)

As it can be appreciated, the best solution addressed is the Polynomic Random Forest Regressor.
These are the plots that demmonstrate the relationship between the true and the predicted values




## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Project status
Learning and enjoying every day.
Next steps:
- Test new models and explore better neural networks
- Use h2O to learn the AutoML function
