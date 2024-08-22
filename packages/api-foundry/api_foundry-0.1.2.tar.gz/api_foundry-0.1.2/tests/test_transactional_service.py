from datetime import datetime
import json

from api_foundry.utils.app_exception import ApplicationException
from api_foundry.utils.logger import logger
from api_foundry.operation import Operation
from api_foundry.services.transactional_service import TransactionalService

from test_fixtures import load_model, db_secrets

log = logger(__name__)


class TestTransactionalService:
    def test_crud_service(self, load_model, db_secrets):
        """
        Integration test to check insert
        """
        # test insert/create
        result = TransactionalService().execute(
            Operation(
                operation_id="media_type",
                action="create",
                store_params={"name": "X-Ray"},
            )
        )
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert result[0]["name"] == "X-Ray"
        media_type_id = result[0]["media_type_id"]

        # test select/read
        operation = Operation(
            operation_id="media_type",
            action="read",
            query_params={"media_type_id": media_type_id},
        )
        result = TransactionalService().execute(operation)

        log.info(f"result: {result}")
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert result[0]["media_type_id"] == media_type_id
        assert result[0]["name"] == "X-Ray"

        # test update
        operation = Operation(
            operation_id="media_type",
            action="update",
            query_params={"media_type_id": media_type_id},
            store_params={"name": "Ray gun"},
        )

        result = TransactionalService().execute(operation)

        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 1
        assert result[0]["name"] == "Ray gun"

        # test delete
        operation = Operation(
            operation_id="media_type",
            action="delete",
            query_params={"media_type_id": media_type_id},
        )

        result = TransactionalService().execute(operation)

        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 1
        assert result[0]["media_type_id"] == media_type_id
        assert result[0]["name"] == "Ray gun"

        # test select/read
        operation = Operation(
            operation_id="media_type",
            action="read",
            query_params={"media_type_id": media_type_id},
        )
        result = TransactionalService().execute(operation)

        log.info(f"result: {result}")
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 0

    def test_crud_with_timestamp_service(self, load_model, db_secrets):
        """
        Integration test to check insert
        """
        # test insert/create
        operation = Operation(
            operation_id="invoice",
            action="create",
            store_params={
                "invoice_date": datetime.now().isoformat(),
                "customer_id": 2,
                "billing_address": "address",
                "billing_city": "billing_city",
                "billing_state": "billing_state",
                "billing_country": "billing_country",
                "billing_postal_code": "code",
                "total": "3.1459",
            },
        )

        result = TransactionalService().execute(operation)
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert result[0]["billing_address"] == "address"

        invoice_id = result[0]["invoice_id"]

        # test select/read
        operation = Operation(
            operation_id="invoice",
            action="read",
            query_params={"invoice_id": invoice_id},
            metadata_params={"properties": ".* customer:.* invoice_line_items:.*"},
        )
        result = TransactionalService().execute(operation)

        log.info(f"result: {result}")
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert result[0]["invoice_id"] == invoice_id
        assert result[0]["customer"]["customer_id"] == 2

        invoice_id = result[0]["invoice_id"]

        # try update without concurrency value. should fail
        try:
            operation = Operation(
                operation_id="invoice",
                action="update",
                query_params={"invoice_id": invoice_id},
            )

            result = TransactionalService().execute(operation)
            assert len(result) == 1
        except ApplicationException as e:
            assert (
                e.message
                == "Missing required concurrency management property.  schema_object: invoice, property: last_updated"
            )

        # test update
        operation = Operation(
            operation_id="invoice",
            action="update",
            query_params={
                "invoice_id": invoice_id,
                "last_updated": result[0]["last_updated"],
            },
            store_params={"billing_address": "updated address"},
        )

        result = TransactionalService().execute(operation)

        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 1
        assert result[0]["billing_address"] == "updated address"

        # delete without concurrency value. should fail
        try:
            operation = Operation(
                operation_id="invoice",
                action="delete",
                query_params={"invoice_id": invoice_id},
            )

            result = TransactionalService().execute(operation)
            assert False, "Exception not thrown"
        except ApplicationException as e:
            assert (
                e.message
                == "Missing required concurrency management property.  schema_object: invoice, property: last_updated"
            )

        # test delete
        operation = Operation(
            operation_id="invoice",
            action="delete",
            query_params={
                "invoice_id": invoice_id,
                "last_updated": result[0]["last_updated"],
            },
        )

        result = TransactionalService().execute(operation)

        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 1
        assert result[0]["invoice_id"] == invoice_id
        assert result[0]["customer_id"] == 2

        # test select/read
        operation = Operation(
            operation_id="invoice",
            action="read",
            query_params={"invoice_id": invoice_id},
        )
        result = TransactionalService().execute(operation)

        log.info(f"result: {result}")
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 0

    def test_crud_with_uuid_service(self, load_model, db_secrets):
        """
        Integration test to check insert
        """
        # test insert/create
        operation = Operation(
            operation_id="customer",
            action="create",
            store_params={
                "first_name": "John",
                "last_name": "Doe",
                "company": "Acme Inc.",
                "address": "123 Main St",
                "city": "Anytown",
                "state": "California",
                "country": "United States",
                "postal_code": "12345",
                "phone": "123-456-7890",
                "fax": "123-456-7890",
                "email": "john.doe@example.com",
                "support_rep_id": 3,
            },
        )

        result = TransactionalService().execute(operation)
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert result[0]["address"] == "123 Main St"

        customer_id = result[0]["customer_id"]

        # test select/read
        operation = Operation(
            operation_id="customer",
            action="read",
            query_params={"customer_id": customer_id},
        )
        result = TransactionalService().execute(operation)

        log.info(f"result: {result}")
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert result[0]["customer_id"] == customer_id
        assert result[0]["support_rep_id"] == 3

        # try update without concurrency value. should fail
        try:
            operation = Operation(
                operation_id="customer",
                action="update",
                query_params={"customer_id": customer_id},
                store_params={"address": "321 Broad St"},
            )

            result = TransactionalService().execute(operation)
            assert False, "Expecting exception"
        except ApplicationException as e:
            assert (
                e.message
                == "Missing required concurrency management property.  schema_object: customer, property: version_stamp"
            )

        # test update
        operation = Operation(
            operation_id="customer",
            action="update",
            query_params={
                "customer_id": customer_id,
                "version_stamp": result[0]["version_stamp"],
            },
            store_params={"address": "321 Broad St"},
        )

        result = TransactionalService().execute(operation)

        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 1
        assert result[0]["address"] == "321 Broad St"

        try:
            # test delete without version stamp
            operation = Operation(
                operation_id="customer",
                action="delete",
                query_params={"customer_id": customer_id},
            )

            result = TransactionalService().execute(operation)
            assert False, "Expecting exception"
        except ApplicationException as e:
            assert (
                e.message
                == "Missing required concurrency management property.  "
                + "schema_object: customer, property: version_stamp"
            )

        # test delete
        operation = Operation(
            operation_id="customer",
            action="delete",
            query_params={
                "customer_id": customer_id,
                "version_stamp": result[0]["version_stamp"],
            },
        )

        result = TransactionalService().execute(operation)

        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 1
        assert result[0]["customer_id"] == customer_id

        # test select/read
        operation = Operation(
            operation_id="customer",
            action="read",
            query_params={"customer_id": customer_id},
        )
        result = TransactionalService().execute(operation)

        log.info(f"result: {result}")
        log.info(f"result: {json.dumps(result, indent=4)}")
        assert len(result) == 0
