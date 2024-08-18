from typing import Dict, Final, Optional, Set

from botocore.exceptions import ClientError

from moto.stepfunctions.parser.api import HistoryEventType, TaskFailedEventDetails
from moto.stepfunctions.parser.asl.component.common.error_name.custom_error_name import (
    CustomErrorName,
)
from moto.stepfunctions.parser.asl.component.common.error_name.failure_event import (
    FailureEvent,
)
from moto.stepfunctions.parser.asl.component.state.exec.state_task.service.resource import (
    ResourceRuntimePart,
)
from moto.stepfunctions.parser.asl.component.state.exec.state_task.service.state_task_service_callback import (
    StateTaskServiceCallback,
)
from moto.stepfunctions.parser.asl.eval.environment import Environment
from moto.stepfunctions.parser.asl.eval.event.event_detail import EventDetails
from moto.stepfunctions.parser.asl.utils.boto_client import boto_client_for
from moto.stepfunctions.parser.asl.utils.encoding import to_json_str


class StateTaskServiceSns(StateTaskServiceCallback):
    _SUPPORTED_API_PARAM_BINDINGS: Final[Dict[str, Set[str]]] = {
        "publish": {
            "Message",
            "MessageAttributes",
            "MessageStructure",
            "PhoneNumber",
            "Subject",
            "TargetArn",
            "TopicArn",
        }
    }

    def _get_supported_parameters(self) -> Optional[Set[str]]:
        return self._SUPPORTED_API_PARAM_BINDINGS.get(self.resource.api_action.lower())

    def _from_error(self, env: Environment, ex: Exception) -> FailureEvent:
        if isinstance(ex, ClientError):
            error_code = ex.response["Error"]["Code"]

            exception_name = error_code
            if not exception_name.endswith("Exception"):
                exception_name += "Exception"
            error_name = f"SNS.{exception_name}"

            error_message = ex.response["Error"]["Message"]
            status_code = ex.response["ResponseMetadata"]["HTTPStatusCode"]
            request_id = ex.response["ResponseMetadata"]["RequestId"]
            error_cause = (
                f"{error_message} "
                f"(Service: AmazonSNS; "
                f"Status Code: {status_code}; "
                f"Error Code: {error_code}; "
                f"Request ID: {request_id}; "
                f"Proxy: null)"
            )

            return FailureEvent(
                error_name=CustomErrorName(error_name=error_name),
                event_type=HistoryEventType.TaskFailed,
                event_details=EventDetails(
                    taskFailedEventDetails=TaskFailedEventDetails(
                        error=error_name,
                        cause=error_cause,
                        resource=self._get_sfn_resource(),
                        resourceType=self._get_sfn_resource_type(),
                    )
                ),
            )
        return super()._from_error(env=env, ex=ex)

    def _eval_service_task(
        self,
        env: Environment,
        resource_runtime_part: ResourceRuntimePart,
        normalised_parameters: dict,
    ):
        service_name = self._get_boto_service_name()
        api_action = self._get_boto_service_action()
        sns_client = boto_client_for(
            region=resource_runtime_part.region,
            account=resource_runtime_part.account,
            service=service_name,
        )

        # Optimised integration automatically stringifies
        if "Message" in normalised_parameters and not isinstance(
            message := normalised_parameters["Message"], str
        ):
            normalised_parameters["Message"] = to_json_str(message)

        response = getattr(sns_client, api_action)(**normalised_parameters)
        response.pop("ResponseMetadata", None)
        env.stack.append(response)
