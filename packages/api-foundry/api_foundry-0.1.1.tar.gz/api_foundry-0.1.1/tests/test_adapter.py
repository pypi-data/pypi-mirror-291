from api_foundry.services.service import Service
from api_foundry.adapters.adapter import Adapter
from api_foundry.operation import Operation


class MockService(Service):
    def execute(self, operation):
        # Simulating service execution and returning dummy result
        assert operation.operation_id == "entity"
        assert operation.action == "action"
        assert operation.query_params == {"query": "query"}
        return [{"key": "value"}]


# Mock adapter provides provides abstract functions for Adapter class
class MockAdapter(Adapter):
    def marshal(self, result: list[dict]):
        return result

    def unmarshal(self, event):
        return Operation(
            operation_id="entity",
            action="action",
            store_params={"store": "store"},
            query_params={"query": "query"},
            metadata_params={"metadata": "metadata"},
        )


class TestAdapter:
    def test_stub(self):
        assert True

    def test_adapter(self):
        mock_service = MockService()
        mock_adapter = MockAdapter(mock_service)

        # Calling the process_event method
        result = mock_adapter.process_event(event={})

        # Asserting the result
        assert result == [{"key": "value"}]
