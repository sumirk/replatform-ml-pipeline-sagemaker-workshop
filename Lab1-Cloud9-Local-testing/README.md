# (Optional) Lab1 Cloud9 Local testing 
------------------------------------------------  

the idea of this local testing lab is to do debugging faster and verify if your code integrates with Sagemaker API's. If you start porting your code to Sagemaker Studio directly then you have to debug using Cloudwatch logs and wait for yuur jobs to complete on Sgemaker jobs.


If you are opting to do this Lab then please ensure to not the below considerations:-

    - Sagemaker Local testing currently does not support checkpointing in training job.
    - Give the Cloud9 role (AWSCloud9SSMAccessRole) full s3 permissions (This is a role assigned to the EC2 instance for Cloud9)
    - The admin role which used to login to Cloud9 and assumed by Cloud9 instance should have additional IAM trust relationship as below: (arn:aws:iam::AcountNumber:role/admin)
    
          {
            "Effect": "Allow",
            "Principal": {
                "Service": "sagemaker.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }

    - Docker compose is needed for local testing which downloads the sagemaker docker images and runs them locally. This has been already installed by the starter bash script.
    - Validate Docker compose installation by running - "docker-compose version" , in the shell terminal.
    - Python library "sagemaker[local]" is required locally and has been already installed by the starter bash script.
    


In this our goal is to first modularize the steps in their own separate projects BY RUNNING THEM LOCALLY ON CLOUD9. We Will start by first seperating out the pre-processing step.

-  Directories for modularizing the steps in their own jobs have been created with some placeholder files with some hints. 

-  If you are unable to progress then use the hints directory to see the hints in sequential manner. Try not to look at all of them but rather look at them if you have spent 10-15 minutes on a task without any progress. 

- If you look at the hints too often then the task will be too easy to complete and you will not get the kick of doing it yourself. If its too hard then you will lose interest, so make sure to look at the hints and get back with some more effort.



Look at these examples to refer and build your scripts as a standard example for all the steps. These are not an exacts solution but you can understand the process defined in below notebook and use in your own way here:-

https://github.com/aws/amazon-sagemaker-examples/blob/main/sagemaker-pipelines/tabular/train-register-deploy-pipeline-model/train%20register%20and%20deploy%20a%20pipeline%20model.ipynb

https://github.com/aws/amazon-sagemaker-examples/blob/89c54681b7e0f83ce137b34b879388cf5960af93/sagemaker-pipelines/tabular/abalone_build_train_deploy/sagemaker-pipelines-preprocess-train-evaluate-batch-transform.ipynb 


# Lab1 - Section1 - (Pre-processing)
-----------------------------------------------------------------------------------------------------------------------------------------------------------


If you check the evaluation.py in your Cloud9 or UI where you have opened the other repo (ml-replatform-pipeline-workshop) 

There is a main function which executes all the steps in sequence , starting with downloading the raw data from S3 and then calls the preprocess_data function as below:-

```
def main():
    # local_folder = "data"  # Local folder to save downloaded data
    # bucket_name = "your-s3-bucket-name"
    print("Data DpownloadStarted")
    download_data_from_s3(bucket_name, remote_folder, local_folder)
    print("Data Dpownload Complete")
    print("Data Preprocessing Started")
    X_train, X_val, y_train, y_val, X_test, y_test = preprocess_data(local_folder)

```


As you can see we are dealing with a pre-processing job. The best way to run this job seperately is to run the pre-processing.py script on Sagemaker Processing.

Read the first two paragraph's of the documentation to understand SageMaker processing job

https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html



Notice the flow from the image in doc - You have to pass the s3 bucket location with the input data which maps to the processing-containers input path - /opt/ml/processing/input and vice versa.

When the container completes its task, the processing script would to write the output to /opt/ml/processing/output 

So, as long as you have the below the input and output definitions for processor with Sagemaker SDK, the job would work as expected. You can have multiple inputs and outputs. Specially multiple outpus allows us to reference these outputs paths on S3 in our pipeline for training and evaluation steps. (More on this later)

```
from sagemaker.sklearn.processing import SKLearnProcessor

source_data = 's3://bucket/path/to/input_data'

sklearn_processor.run(
    code='processing-script.py',
    source_dir='scripts',
    inputs=[
        ProcessingInput(input_name='source_data',source=source_data, destination="/opt/ml/processing/input")
    ],
    outputs=[
        ProcessingOutput(output_name="output", source="/opt/ml/processing/output", destination=f's3://path/to/output_data')
    ])
```



You can run Sagemaker processing job with different pre-built containers for Apache Spark, Scikit-learn , or Framework Processors with different machine learning libraries like Tensorflow, Huggingface, MXNet, PyTorch etc.

We will be using the Tensorflow Framework processor just as a demonstration, however the current task at hand can be done by sci-kit processor as well.

https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job-frameworks-tensorflow.html - Read this page to be familiar with Tensorflow processor.

The documentation above shows how to use the Amazon SageMaker Python SDK.


-  A notebook script named pre-processing-Local-Notebook-SG-SDK.py is available in the Lab1-Cloud9-Local-testing directory.

-  In the notebook, change the framework_version, py_version to the tensorflow version being used in the ECS-project requirements.txt file. 


Now lets understand what should be the input and output for the processing job. In the original ECS-Pipeline the input to the job is the raw data but there is no such output being saved back to S3 as all the rest of the steps are being done within the container itself. 

    The processed raw_data which is split into X_train, y_train for training data and lablel respectively. 
    The X_val and y_val data is used for validating the model gening trained and generate the training metrics.
    The X_test and y_test is used later in the evaluation step to generate evaluation metrics.

But all of these are being kept locally within the container as its a single compute and the data can be shared between tasks from local storage.

However, we want to run these jobs as individual steps with different processors, and hence all the datasets being generated should be stored back to S3 to be fetched by the next steps.

So, the each of the above data should be stored in seperate directories locally in the /opt/ml/processing/ path. 


Estimated time for each task - 10 minutes, if it takes more time then look at hints and move forward. The idea is to learn and move forward and not being stuck, it takes time do do these things sometimes.

Estimated time for this section :- 20 minutes , if it takes more ethan this then use the final data directory as refernece to complete your section.


Note:- Run the python notebook files as a typical python file as in Cloud9 we are not using notebooks. For example - # python pre-processing-Notebook-Final.py


Tasks:-

     - Add the inputs to the notebook script for the TensorFlowProcessor to have the s3 raw_data source which maps to /opt/ml/processing/source_data path in the processing job.
     - Add outputs to the notebook script TensorFlowProcessor to take the source data from different directories in /opt/ml/processing/ , for example /opt/ml/processing/train to copy the training data (data + label) back to S3.
     - Modify the preprocessing.py inside script_processing to map the 'local_folder' variabble being passed to the preprocess_data function with the path for source data.
     - Make this preprocessing.py script executable like its executed in the evauation.py in ecs-fargate project.
     - Save the outputs datasets using np.save to the different directories inside /opt/ml/processing/, for eg - /opt/ml/processing/train/X_train/X_train.npy
     - This would push the data automatically to S3.
     - validate that you see the processed datasets in S3 in the DataProcessed directory of your S3 bucket.
     - You should also copy the requirements.txt file from the ecs-fargate project to ensure the pre-processing job install the libraries required, although we would not need particulary here but its a good practice.
     

Look at hints when you need them in the hints directory sequentially. There is a final directory as well in the directory which has the finished project. Try not to look at the final unless its needed to move to LAB2.



# Lab1 - Section2 (Training)
-----------------------------------------------------------------------------------------------------------------------------------------------------------


Its a similar task in this section. We would be using the Sagemaker Training API which is dedicated for runnign training jobs as it provides many features and integrations with Sagemaker Experiments / HPO optimization , Distributed training etc which makes it very useful to use with the Sagenaker SDK for larger teams and projects 

Take a look at the Sagemaker Training job model storage paths so that you understand the default paths.

Pay attention to how input channel (in simple words a S3 path for input data like cleaned Training data or Label data) is defined and the fact that it create a folder in /opt/ml/input/data/{channelName}

You can have many input channels.

Other areas to check are /opt/ml/model , /opt/ml/output , /opt/ml/checkpoints (this can be defined as to which local directory is for checkpoint) 

Understand how the environment variables are automatically created for all these paths in the training container and you can fetch them using python argparse. or just extract from os library.

## https://docs.aws.amazon.com/sagemaker/latest/dg/model-train-storage.html


Points to note:-

    - The ecs-argate python pipelines training.py step is executed by the evaluation.py file as its the main entry point script.
    - From evaluation.py, the mdoel definition to create a cnn model and the train_model function passes the inputs and ececutes training.py
    - The checkpoints are being uploaded to S3 during training and a best checkpoint model is stored seperately in the root of S3 bucket.
    - Training metric is being logged in SystemOut in the script, which is collected by CLoudwatch Logs
   

Estimated time for each task: ~ 10 minutes, if it takes more time then look at hints and move forward. The idea is to learn and move forward and not being stuck, it takes time do do these things sometimes.

Estimated time for this section : ~ 20 minutes , if it takes more ethan this then use the final data directory as refernece to complete your section.




Tasks:-

    - A directory script_train is already present in Lab1 along with a notebook script training-Local-Notebook-SG-SDK.py
    - The training.py in the script_train is not the main file and the fact that we have to parse a lot of parameters to the training job, we should create a seperate main.py file in the script_train directory which will import the training.py module functions.
    - You should use python argparse.ArgumentParser() to parse the parameters bieng passed and refer to the two example notebooks liked above as reference.
    - In your main function yoou should be able to load the data passed as input channel paths and run the train_model(model, X_train, y_train, X_val, y_val, output_dir, bucket_name) function.
    - The training.py also owuld need to be modified to save the files to the respective local directories for checkpoint, best_model checkpoint, other checkpoints and you will have to remove the S3 uppload/download functions as Sagemaker automatically does it for you when you use input channels or when you save files to /opt/ml/model or /opt/ml/checkpoint or /opt/ml/output
    - You should have the training artifacts in S3 bucket after successfull training.




Look at hints when you need them in the hints directory sequentially. There is a final directory as well in the directory which has the finished project. Try not to look at the final unless its needed to move to LAB2.



# Lab1 - Section3 (Evaluation)
-----------------------------------------------------------------------------------------------------------------------------------------------------------


You know the drill now. This job is very similar to pre-processing and almost similar from the Pipeline notebook perspective. However, the evaluation.py script in the script_evaluation needs some changes.

Tasks

    - You will have to be able to pass the model.tar.gz from the training job (uoloaded to s3) to an input diretory in the Sagemaker processing job here. 
    - Load the best_checkpoint model using tensorflow.keras load_model function 
    - You will need to remove the reference to pre-processing, training jobs and upload/download s3 functions.
    - Change the metrics_file_path to an output path directory which should be synced with S3 by the Tensorflow processor.
    

Look at hints when you need them in the hints directory sequentially. There are final files as well in the directory which has the finished project. Try not to look at the final unless its needed to move to LAB3.


Note:- Run the python notebook files as a typical python file as in Cloud9 we are not using notebooks.


Estimated time for each task: ~ 10 minutes, if it takes more time then look at hints and move forward. The idea is to learn and move forward and not being stuck, it takes time do do these things sometimes.

Estimated time for this section : ~ 20 minutes , if it takes more ethan this then use the final data directory as refernece to complete your section.
