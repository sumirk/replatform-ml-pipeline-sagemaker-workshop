# Lab0 Cloud9 docker pipeline 
------------------------------------------------ 

For Lab0 and Lab1 we will be using the Cloud9 environment:


- Clone this repository in Cloud9 environment - git clone https://github.com/sumirk/ml-replatform-pipeline-sagemaker-workshop.git
  
- Change the current directory to "Lab0-cloud9-docker-pipeline/"

- Use the below commands to resize the EBS volume:-
    - chmod +x resize.sh
    - ./resize.sh 20
  - https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html


- Run the command "chmod +x deploy-cfn-run-task.sh" in the root diretory
  
- Run the bash script './deploy-cfn-run-task.sh' and then run pass the s3-bucket name, the stack-name and your AWS account number to this command. for eg - ./deploy-cfn-run-task techsummit2023mlops cfn-test-summit-cli-01 9707709xxxx
  
- The above step will create a cloudformation template and build the docker container from the DockerFile locally and tag and push the image to ECR.
  
- A Fargate ECS cluster will also be created which will run a task to run the ML pipeline project as a standlone task in your accounts default VPC, Default Subnet with Default security group.
  
- So, please validate if they provide network connectivity to connect to public resources.
  
- The trained model and the checkpoints will be saved to your S3 bucket by the container task and then the task will be stopped.
  
- The training metrics are being logged to Cloudwatch by the Fargate task. If you want to take a look check the tasks logging in ECS console.
  
- If you want to run the task again you can do so by running the "aws ecs run-task ...." command from the shell script.
  
- You should spend the initial 10-15 mins to understand this project and have taken note of the steps and resources being created.

- The below two diagrams/screenshots show the structure of the project.

![image](https://github.com/sumirk/ml-replatform-pipeline-workshop/assets/53355338/07ef5076-1ea8-45ab-a68e-a86a7555095e)


![image](https://github.com/sumirk/ml-replatform-pipeline-workshop/assets/53355338/c028f47a-4e45-4f24-9687-f2511275bbb9)


- After this step open Sagemaker Studio in other browser window if you already have Studio deployed and then use the system terminal to clone the below repository in your Sagemaker studio system terminal.

  - To open in browser - https://github.com/sumirk/ml-replatform-pipeline-sagemaker-workshop
  - Clone link - https://github.com/sumirk/ml-replatform-pipeline-sagemaker-workshop.git

- If you have completed the above steps - Congratulations !! you have completed the first section of this workshop. The fun begins now :)
  

Stay in Cloud9 if you want to do the Optional Local testing and move to directory - Lab1-Cloud9-Local-testing/

Open the README.md file in Lab1-Cloud9-Local-testing/ to follow the next steps.

If you do not want to do local testing step then you can move to Sagemaker Studio and open the README.md in Lab2-Unit-testing/ in Sagemaker studio

