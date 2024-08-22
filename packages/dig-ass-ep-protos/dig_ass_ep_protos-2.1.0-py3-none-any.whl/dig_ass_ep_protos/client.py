from dig_ass_ep_protos.DigitalAssistantEntryPoint_pb2_grpc import (
    DigitalAssistantEntryPointStub,
)
from dig_ass_ep_protos.DigitalAssistantEntryPoint_pb2 import (
    DigitalAssistantEntryPointRequest,
    DigitalAssistantEntryPointResponse,
    OuterContextItem,
)

from agi_med_protos.abstract_client import AbstractClient


class EntryPointClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantEntryPointStub(self._channel)

    def __call__(self, text: str, outer_context: dict, image=None, pdf=None):
        # TODO REMOVE WHEN EVERYTHING IS SETTLED
        track_id = ''
        if 'TrackId' in outer_context.keys():
            track_id = outer_context['TrackId']

        request = DigitalAssistantEntryPointRequest(
            Text=text,
            OuterContext=OuterContextItem(
                Sex=outer_context['Sex'],
                Age=outer_context['Age'],
                UserId=outer_context['UserId'],
                SessionId=outer_context['SessionId'],
                ClientId=outer_context['ClientId'],
                TrackId=track_id,  # TODO CHANGE TO outer_context['TrackId'] WHEN EVERYTHING IS SETTLED
            ),
            Image=image,
            PDF=pdf,
        )
        response: DigitalAssistantEntryPointResponse = (
            self._stub.GetTextResponse(request)
        )
        return response.Text
