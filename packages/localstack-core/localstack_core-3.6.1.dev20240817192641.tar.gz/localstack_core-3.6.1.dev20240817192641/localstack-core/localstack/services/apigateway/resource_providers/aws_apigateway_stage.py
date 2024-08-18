# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

import copy
from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)
from localstack.utils.objects import keys_to_lower


class ApiGatewayStageProperties(TypedDict):
    RestApiId: Optional[str]
    AccessLogSetting: Optional[AccessLogSetting]
    CacheClusterEnabled: Optional[bool]
    CacheClusterSize: Optional[str]
    CanarySetting: Optional[CanarySetting]
    ClientCertificateId: Optional[str]
    DeploymentId: Optional[str]
    Description: Optional[str]
    DocumentationVersion: Optional[str]
    MethodSettings: Optional[list[MethodSetting]]
    StageName: Optional[str]
    Tags: Optional[list[Tag]]
    TracingEnabled: Optional[bool]
    Variables: Optional[dict]


class AccessLogSetting(TypedDict):
    DestinationArn: Optional[str]
    Format: Optional[str]


class CanarySetting(TypedDict):
    DeploymentId: Optional[str]
    PercentTraffic: Optional[float]
    StageVariableOverrides: Optional[dict]
    UseStageCache: Optional[bool]


class MethodSetting(TypedDict):
    CacheDataEncrypted: Optional[bool]
    CacheTtlInSeconds: Optional[int]
    CachingEnabled: Optional[bool]
    DataTraceEnabled: Optional[bool]
    HttpMethod: Optional[str]
    LoggingLevel: Optional[str]
    MetricsEnabled: Optional[bool]
    ResourcePath: Optional[str]
    ThrottlingBurstLimit: Optional[int]
    ThrottlingRateLimit: Optional[float]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class ApiGatewayStageProvider(ResourceProvider[ApiGatewayStageProperties]):
    TYPE = "AWS::ApiGateway::Stage"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[ApiGatewayStageProperties],
    ) -> ProgressEvent[ApiGatewayStageProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/RestApiId
          - /properties/StageName

        Required properties:
          - RestApiId

        Create-only properties:
          - /properties/RestApiId
          - /properties/StageName



        IAM permissions required:
          - apigateway:POST
          - apigateway:PATCH
          - apigateway:GET

        """
        model = request.desired_state
        apigw = request.aws_client_factory.apigateway

        stage_name = model.get("StageName", "default")
        stage_variables = model.get("Variables")
        # we need to deep copy as several fields are nested dict and arrays
        params = keys_to_lower(copy.deepcopy(model))
        # TODO: add methodSettings
        # TODO: add custom CfN tags
        param_names = [
            "restApiId",
            "deploymentId",
            "description",
            "cacheClusterEnabled",
            "cacheClusterSize",
            "documentationVersion",
            "canarySettings",
            "tracingEnabled",
            "tags",
        ]
        params = util.select_attributes(params, param_names)
        params["tags"] = {t["key"]: t["value"] for t in params.get("tags", [])}
        params["stageName"] = stage_name
        if stage_variables:
            params["variables"] = stage_variables

        result = apigw.create_stage(**params)
        model["StageName"] = result["stageName"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[ApiGatewayStageProperties],
    ) -> ProgressEvent[ApiGatewayStageProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - apigateway:GET
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[ApiGatewayStageProperties],
    ) -> ProgressEvent[ApiGatewayStageProperties]:
        """
        Delete a resource

        IAM permissions required:
          - apigateway:DELETE
        """
        model = request.desired_state
        apigw = request.aws_client_factory.apigateway
        try:
            # we are checking if stage api has already been deleted before calling delete
            apigw.get_stage(restApiId=model["RestApiId"], stageName=model["StageName"])
            apigw.delete_stage(restApiId=model["RestApiId"], stageName=model["StageName"])
        except apigw.exceptions.NotFoundException:
            pass

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[ApiGatewayStageProperties],
    ) -> ProgressEvent[ApiGatewayStageProperties]:
        """
        Update a resource

        IAM permissions required:
          - apigateway:GET
          - apigateway:PATCH
          - apigateway:PUT
          - apigateway:DELETE
        """
        raise NotImplementedError
