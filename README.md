# Project: Microservice that creates a bag of words by combining all files on an EFS mount 

For NLP tasks, bag of words is generally needed to determine the way forward for a given use case, be it for EDA, determining the choice of algorithm, weeding out stop words in a naive approach or even to implement a solution that wont be computationally expensive.

In this project I have made use of the EFS (Elastic File System) and AWS lambda functions to further "save up" on costs. Both these components charge u for the usage rather than leveraging a fixed cost (when they are not actively being called or used, you dont get charge!). So if you are using a computationally inexpensive solution like bag of words and pairing it with these components, this project is a great place to start as a POC. This project returns a bag of words combining the contents of all the documents in a given mount.

Here I have mounted the EFS using cloud 9 on an EC2 instance and then connected the lambda functions to the EFS mount points.
I have also made use of step functions, so that all you have to do is start the execution using a set trigger word and it automatically calls all the microservices in the state machine. A rough architecture is as below and the setup details can be seen in the "References" section of this readme-
![image](https://user-images.githubusercontent.com/110474064/228689696-974acb61-8310-470f-9cf5-8e4e1ea374a5.png)

## Step function:

Sucessful invocation:

![image](https://user-images.githubusercontent.com/110474064/231635917-c24a3e0c-ab0a-40d0-98bd-afe94f794a06.png)

![image](https://user-images.githubusercontent.com/110474064/231635647-2d3b6798-2255-4c6d-8121-43fd2c57de0c.png)

![image](https://user-images.githubusercontent.com/110474064/231635803-5a1b0135-bfee-498e-bf89-eda9a31e810a.png)

![image](https://user-images.githubusercontent.com/110474064/231636075-5d96bdd7-4455-491c-b2ac-0dfbd1ed14fc.png)

![image](https://user-images.githubusercontent.com/110474064/231636180-bc08671f-b7b0-4ad5-97ce-9dd8bc466851.png)

## References:
1. Prof. Noah's class demo
2. https://github.com/NehaBardeDUKE/efs_integration 
3. https://docs.aws.amazon.com/lambda/latest/dg/services-efs.html
