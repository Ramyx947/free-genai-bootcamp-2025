from aws_cdk import App
from cdk.cdk_stack import CdkStack

app = App()
CdkStack(app, "RomanianLearningApp")

app.synth()
