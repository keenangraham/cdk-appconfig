import json

from aws_cdk import App
from aws_cdk import Stack
from aws_cdk import RemovalPolicy

from aws_cdk.aws_appconfig import CfnApplication
from aws_cdk.aws_appconfig import CfnEnvironment
from aws_cdk.aws_appconfig import CfnConfigurationProfile
from aws_cdk.aws_appconfig import CfnDeploymentStrategy
from aws_cdk.aws_appconfig import CfnHostedConfigurationVersion
from aws_cdk.aws_appconfig import CfnDeployment

from constructs import Construct

from shared_infrastructure.cherry_lab.environments import US_WEST_2


app = App()

'''
AWS AppConfig requires that you create resources and deploy a configuration in the following order:

Create an application

Create an environment

Create a configuration profile

Create a deployment strategy

Deploy the configuration
'''


class AppConfigStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        application = CfnApplication(
            self,
            'AppConfigApplication',
            name='some-branch',
        )

        application.apply_removal_policy(
            policy=RemovalPolicy.DESTROY
        )

        environment = CfnEnvironment(
            self,
            'AppConfigEnvironment',
            application_id=application.ref,
            name='some-env'
        )

        environment.apply_removal_policy(
            policy=RemovalPolicy.DESTROY
        )

        configuration_profile = CfnConfigurationProfile(
            self,
            'AppConfigConfigurationProfile',
            application_id=application.ref,
            location_uri='hosted',
            name='some-configuration-profile-feature-flags',
            type='AWS.AppConfig.FeatureFlags',
        )

        configuration_profile.apply_removal_policy(
            policy=RemovalPolicy.DESTROY
        )

        deployment_strategy = CfnDeploymentStrategy(
            self,
            'AppConfigDeploymentStrategy',
            name='some-deployment-strategy',
            deployment_duration_in_minutes=0,
            growth_factor=100,
            replicate_to='NONE',
        )

        deployment_strategy.apply_removal_policy(
            policy=RemovalPolicy.DESTROY
        )

        configuration_version = CfnHostedConfigurationVersion(
            self,
            'AppConfigHostedConfigurationVersion',
            application_id=application.ref,
            configuration_profile_id=configuration_profile.ref,
            latest_version_number=0.1,
            content_type='application/json',
            content=json.dumps(
                {
                    'version': '0.1',
                    'flags': {
                        'BLOCK_DATABASE_WRITES': {
                            'name': 'BLOCK_DATABASE_WRITES',
                        }
                    },
                    'values': {
                        'BLOCK_DATABASE_WRITES': {
                            'enabled': False
                        }
                    }
                }
            )
        )

        configuration_version.apply_removal_policy(
            policy=RemovalPolicy.DESTROY
        )

        deployment = CfnDeployment(
            self,
            'AppConfigDeployment',
            application_id=application.ref,
            configuration_profile_id=configuration_profile.ref,
            configuration_version='0.1',
            deployment_strategy_id=deployment_strategy.ref,
            environment_id=environment.ref,
        )


appconfig_stack = AppConfigStack(
    app,
    'AppConfigStack',
    env=US_WEST_2,
)


app.synth()
