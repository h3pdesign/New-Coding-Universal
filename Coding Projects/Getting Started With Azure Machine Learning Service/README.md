## Welcome Azure Machine Learning service through Azure Notebooks

If you haven't created Azure Machine Learning Workspace yet, first run [configuration](configuration.ipynb)
notebook. If you created a Workspace from Azure portal and launched notebooks from there, your workspace 
is configured already, and you can proceed to examples.

Try the example [01.run-experiment](01.run-experiment.ipynb) to connect to your workspace 
and run a basic experiment using Azure Machine Learning Python SDK, 
and then [02.deploy-web-service](02.deploy-web-service.ipynb) to deploy a model as a web service.

Then move to more comprehensive examples in **tutorials** folder, or explore different features 
in **how-to-use-azureml** folder.

See also:
 * [Azure/MachineLearningNotebooks GitHub site](https://github.com/Azure/MachineLearningNotebooks)
 * [Azure Machine Learning service documentation](https://docs.microsoft.com/en-us/azure/machine-learning/service)

 **Important:** You must select Python 3.6 as the kernel for your notebooks to use the SDK.

 **Note:**
 The config.json file in this folder was created for you with details of your Azure Machine 
 Learning service workspace. Both these notebooks use this file to connect to your workspace. 
 You can also copy this file into other places where you have code that needs this connection.