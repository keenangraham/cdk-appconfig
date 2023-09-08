from aws_cdk import App
from aws_cdk import Stack

from constructs import Construct

from shared_infrastructure.cherry_lab.environments import US_WEST_2


app = App()


class AppConfigStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


appconfig_stack = AppConfigStack(
    app,
    'AppConfigStack',
    env=US_WEST_2,
)


app.synth()
