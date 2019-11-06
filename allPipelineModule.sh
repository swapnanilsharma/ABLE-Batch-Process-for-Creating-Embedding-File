# Running all the pipeline module for generating Embedding file
python getRawDataFromES.py
python readRawDataAddIntoDataframe.py
python getSummarizeData.py
python getVectorizedData.py
python finalTouchDataFrame.py

