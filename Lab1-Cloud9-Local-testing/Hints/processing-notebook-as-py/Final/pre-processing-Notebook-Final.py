#!/usr/bin/env python
# coding: utf-8

# In[2]:


import boto3
import sagemaker
from sagemaker import get_execution_role
region = boto3.session.Session().region_name

role = get_execution_role()


# In[5]:


source_data = "s3://XXXX/raw_data/"


# In[7]:


from sagemaker.tensorflow import TensorFlowProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker import get_execution_role

region = boto3.session.Session().region_name

from sagemaker.local import LocalSession
sagemaker_session = LocalSession()
sagemaker_session.config = {'local': {'local_code': True}}

role = get_execution_role()
BUCKET = 'XXXXXXX'
train_path = 'DataProcessed/train'
val_path = 'DataProcessed/val'
test_path = 'DataProcessed/test'

#Initialize the TensorFlowProcessor
tp = TensorFlowProcessor(
    framework_version='2.11.0',
    role=get_execution_role(),
    instance_type='local',
    instance_count=1,
    base_job_name='frameworkprocessor-TF',
    py_version='py39'
)

# there is a limit to the number of outputs to 10

#Run the processing job
tp.run(
    code='preprocessing.py',
    source_dir='script_processing',
    inputs=[
        ProcessingInput(input_name='source_data',source=source_data, destination="/opt/ml/processing/source_data")
    ],
    outputs=[
        ProcessingOutput(output_name="train_output_data", source="/opt/ml/processing/train/X_train", destination=f's3://{BUCKET}/{train_path}/X_train'),
        ProcessingOutput(output_name="train_output_label", source="/opt/ml/processing/train/y_train", destination=f's3://{BUCKET}/{train_path}/y_train'),
        ProcessingOutput(output_name="val_output_data", source="/opt/ml/processing/val/X_val", destination=f's3://{BUCKET}/{val_path}/X_val'),
        ProcessingOutput(output_name="val_output_label", source="/opt/ml/processing/val/y_val", destination=f's3://{BUCKET}/{val_path}/y_val'),
        ProcessingOutput(output_name="test_data_eval", source="/opt/ml/processing/test", destination=f's3://{BUCKET}/{test_path}')
    ]
)


# In[ ]:





# In[ ]:




