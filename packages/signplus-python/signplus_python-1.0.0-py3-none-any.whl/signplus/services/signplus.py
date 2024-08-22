from typing import List
from typing import Any
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.webhook import Webhook
from ..models.utils.cast_models import cast_models
from ..models.template import Template
from ..models.set_template_comment_request import SetTemplateCommentRequest
from ..models.set_envelope_legality_level_request import SetEnvelopeLegalityLevelRequest
from ..models.set_envelope_expiration_request import SetEnvelopeExpirationRequest
from ..models.set_envelope_dynamic_fields_request import SetEnvelopeDynamicFieldsRequest
from ..models.set_envelope_comment_request import SetEnvelopeCommentRequest
from ..models.rename_template_request import RenameTemplateRequest
from ..models.rename_envelope_request import RenameEnvelopeRequest
from ..models.list_webhooks_response import ListWebhooksResponse
from ..models.list_webhooks_request import ListWebhooksRequest
from ..models.list_templates_response import ListTemplatesResponse
from ..models.list_templates_request import ListTemplatesRequest
from ..models.list_template_documents_response import ListTemplateDocumentsResponse
from ..models.list_template_document_annotations_response import (
    ListTemplateDocumentAnnotationsResponse,
)
from ..models.list_template_annotations_response import ListTemplateAnnotationsResponse
from ..models.list_envelopes_response import ListEnvelopesResponse
from ..models.list_envelopes_request import ListEnvelopesRequest
from ..models.list_envelope_documents_response import ListEnvelopeDocumentsResponse
from ..models.list_envelope_document_annotations_response import (
    ListEnvelopeDocumentAnnotationsResponse,
)
from ..models.envelope_notification import EnvelopeNotification
from ..models.envelope import Envelope
from ..models.document import Document
from ..models.create_webhook_request import CreateWebhookRequest
from ..models.create_template_request import CreateTemplateRequest
from ..models.create_envelope_request import CreateEnvelopeRequest
from ..models.create_envelope_from_template_request import (
    CreateEnvelopeFromTemplateRequest,
)
from ..models.annotation import Annotation
from ..models.add_template_signing_steps_request import AddTemplateSigningStepsRequest
from ..models.add_template_document_request import AddTemplateDocumentRequest
from ..models.add_envelope_signing_steps_request import AddEnvelopeSigningStepsRequest
from ..models.add_envelope_document_request import AddEnvelopeDocumentRequest
from ..models.add_annotation_request import AddAnnotationRequest


class SignplusService(BaseService):

    @cast_models
    def create_envelope(self, request_body: CreateEnvelopeRequest) -> Envelope:
        """Create new envelope

        :param request_body: The request body.
        :type request_body: CreateEnvelopeRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope created successfully
        :rtype: Envelope
        """

        Validator(CreateEnvelopeRequest).validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/envelope", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def create_envelope_from_template(
        self, request_body: CreateEnvelopeFromTemplateRequest, template_id: str
    ) -> Envelope:
        """Create new envelope from template

        :param request_body: The request body.
        :type request_body: CreateEnvelopeFromTemplateRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope created successfully
        :rtype: Envelope
        """

        Validator(CreateEnvelopeFromTemplateRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/from_template/{{template_id}}",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def list_envelopes(
        self, request_body: ListEnvelopesRequest = None
    ) -> ListEnvelopesResponse:
        """List envelopes

        :param request_body: The request body., defaults to None
        :type request_body: ListEnvelopesRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of envelopes retrieved successfully
        :rtype: ListEnvelopesResponse
        """

        Validator(ListEnvelopesRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/envelopes", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return ListEnvelopesResponse._unmap(response)

    @cast_models
    def get_envelope(self, envelope_id: str) -> Envelope:
        """Get envelope

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope details retrieved successfully
        :rtype: Envelope
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}", self.get_default_headers()
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def delete_envelope(self, envelope_id: str) -> Any:
        """Delete envelope

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}", self.get_default_headers()
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)
        return response

    @cast_models
    def get_envelope_document(self, envelope_id: str, document_id: str) -> Document:
        """Get envelope document

        :param envelope_id: envelope_id
        :type envelope_id: str
        :param document_id: document_id
        :type document_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Document details retrieved successfully
        :rtype: Document
        """

        Validator(str).validate(envelope_id)
        Validator(str).validate(document_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/document/{{document_id}}",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .add_path("document_id", document_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return Document._unmap(response)

    @cast_models
    def get_envelope_documents(self, envelope_id: str) -> ListEnvelopeDocumentsResponse:
        """Get envelope documents

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Documents of envelope retrieved successfully
        :rtype: ListEnvelopeDocumentsResponse
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/documents",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return ListEnvelopeDocumentsResponse._unmap(response)

    @cast_models
    def add_envelope_document(
        self, request_body: AddEnvelopeDocumentRequest, envelope_id: str
    ) -> Document:
        """Add envelope document

        :param request_body: The request body.
        :type request_body: AddEnvelopeDocumentRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Document added to envelope successfully
        :rtype: Document
        """

        Validator(AddEnvelopeDocumentRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/document",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body, "multipart/form-data")
        )

        response = self.send_request(serialized_request)
        return Document._unmap(response)

    @cast_models
    def set_envelope_dynamic_fields(
        self, request_body: SetEnvelopeDynamicFieldsRequest, envelope_id: str
    ) -> Envelope:
        """Set envelope dynamic fields

        :param request_body: The request body.
        :type request_body: SetEnvelopeDynamicFieldsRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Dynamic fields added successfully
        :rtype: Envelope
        """

        Validator(SetEnvelopeDynamicFieldsRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/dynamic_fields",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def add_envelope_signing_steps(
        self, request_body: AddEnvelopeSigningStepsRequest, envelope_id: str
    ) -> Envelope:
        """Add envelope signing steps

        :param request_body: The request body.
        :type request_body: AddEnvelopeSigningStepsRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Signing steps added successfully
        :rtype: Envelope
        """

        Validator(AddEnvelopeSigningStepsRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/signing_steps",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def send_envelope(self, envelope_id: str) -> Envelope:
        """Send envelope for signature

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope sent successfully
        :rtype: Envelope
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/send",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def duplicate_envelope(self, envelope_id: str) -> Envelope:
        """Duplicate envelope

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope duplicated successfully
        :rtype: Envelope
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/duplicate",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def void_envelope(self, envelope_id: str) -> Envelope:
        """Void envelope

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope voided successfully
        :rtype: Envelope
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/void",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def rename_envelope(
        self, request_body: RenameEnvelopeRequest, envelope_id: str
    ) -> Envelope:
        """Rename envelope

        :param request_body: The request body.
        :type request_body: RenameEnvelopeRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope renamed successfully
        :rtype: Envelope
        """

        Validator(RenameEnvelopeRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/rename",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def set_envelope_comment(
        self, request_body: SetEnvelopeCommentRequest, envelope_id: str
    ) -> Envelope:
        """Set envelope comment

        :param request_body: The request body.
        :type request_body: SetEnvelopeCommentRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope comment changed successfully
        :rtype: Envelope
        """

        Validator(SetEnvelopeCommentRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/set_comment",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def set_envelope_notification(
        self, request_body: EnvelopeNotification, envelope_id: str
    ) -> Envelope:
        """Set envelope notification

        :param request_body: The request body.
        :type request_body: EnvelopeNotification
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope notification changed successfully
        :rtype: Envelope
        """

        Validator(EnvelopeNotification).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/set_notification",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def set_envelope_expiration_date(
        self, request_body: SetEnvelopeExpirationRequest, envelope_id: str
    ) -> Envelope:
        """Set envelope expiration date

        :param request_body: The request body.
        :type request_body: SetEnvelopeExpirationRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope expiration date changed successfully
        :rtype: Envelope
        """

        Validator(SetEnvelopeExpirationRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/set_expiration_date",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def set_envelope_legality_level(
        self, request_body: SetEnvelopeLegalityLevelRequest, envelope_id: str
    ) -> Envelope:
        """Set envelope legality level

        :param request_body: The request body.
        :type request_body: SetEnvelopeLegalityLevelRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope legality level changed successfully
        :rtype: Envelope
        """

        Validator(SetEnvelopeLegalityLevelRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/set_legality_level",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def get_envelope_annotations(self, envelope_id: str) -> List[Annotation]:
        """Get envelope annotations

        :param envelope_id: ID of the envelope
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of annotations retrieved successfully
        :rtype: List[Annotation]
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/annotations",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return [Annotation._unmap(item) for item in response]

    @cast_models
    def get_envelope_document_annotations(
        self, envelope_id: str, document_id: str
    ) -> ListEnvelopeDocumentAnnotationsResponse:
        """Get envelope document annotations

        :param envelope_id: ID of the envelope
        :type envelope_id: str
        :param document_id: ID of document
        :type document_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of document annotations retrieved successfully
        :rtype: ListEnvelopeDocumentAnnotationsResponse
        """

        Validator(str).validate(envelope_id)
        Validator(str).validate(document_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/annotations/{{document_id}}",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .add_path("document_id", document_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return ListEnvelopeDocumentAnnotationsResponse._unmap(response)

    @cast_models
    def add_envelope_annotation(
        self, request_body: AddAnnotationRequest, envelope_id: str
    ) -> Annotation:
        """Add envelope annotation

        :param request_body: The request body.
        :type request_body: AddAnnotationRequest
        :param envelope_id: ID of the envelope
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Annotation added successfully
        :rtype: Annotation
        """

        Validator(AddAnnotationRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/annotation",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Annotation._unmap(response)

    @cast_models
    def delete_envelope_annotation(self, envelope_id: str, annotation_id: str) -> Any:
        """Delete envelope annotation

        :param envelope_id: ID of the envelope
        :type envelope_id: str
        :param annotation_id: ID of the annotation to delete
        :type annotation_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(envelope_id)
        Validator(str).validate(annotation_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/envelope/{{envelope_id}}/annotation/{{annotation_id}}",
                self.get_default_headers(),
            )
            .add_path("envelope_id", envelope_id)
            .add_path("annotation_id", annotation_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)
        return response

    @cast_models
    def create_template(self, request_body: CreateTemplateRequest) -> Template:
        """Create new template

        :param request_body: The request body.
        :type request_body: CreateTemplateRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Envelope created successfully
        :rtype: Template
        """

        Validator(CreateTemplateRequest).validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/template", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def list_templates(
        self, request_body: ListTemplatesRequest = None
    ) -> ListTemplatesResponse:
        """List templates

        :param request_body: The request body., defaults to None
        :type request_body: ListTemplatesRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of templates retrieved successfully
        :rtype: ListTemplatesResponse
        """

        Validator(ListTemplatesRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/templates", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return ListTemplatesResponse._unmap(response)

    @cast_models
    def get_template(self, template_id: str) -> Template:
        """Get template

        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Template details retrieved successfully
        :rtype: Template
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}", self.get_default_headers()
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def delete_template(self, template_id: str) -> Any:
        """Delete template

        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}", self.get_default_headers()
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)
        return response

    @cast_models
    def duplicate_template(self, template_id: str) -> Template:
        """Duplicate template

        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Template duplicated successfully
        :rtype: Template
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/duplicate",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def add_template_document(
        self, request_body: AddTemplateDocumentRequest, template_id: str
    ) -> Document:
        """Add template document

        :param request_body: The request body.
        :type request_body: AddTemplateDocumentRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Document added to envelope successfully
        :rtype: Document
        """

        Validator(AddTemplateDocumentRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/document",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body, "multipart/form-data")
        )

        response = self.send_request(serialized_request)
        return Document._unmap(response)

    @cast_models
    def get_template_document(self, template_id: str, document_id: str) -> Document:
        """Get template document

        :param template_id: template_id
        :type template_id: str
        :param document_id: document_id
        :type document_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Document details retrieved successfully
        :rtype: Document
        """

        Validator(str).validate(template_id)
        Validator(str).validate(document_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/document/{{document_id}}",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .add_path("document_id", document_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return Document._unmap(response)

    @cast_models
    def get_template_documents(self, template_id: str) -> ListTemplateDocumentsResponse:
        """Get template documents

        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Documents of template retrieved successfully
        :rtype: ListTemplateDocumentsResponse
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/documents",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return ListTemplateDocumentsResponse._unmap(response)

    @cast_models
    def add_template_signing_steps(
        self, request_body: AddTemplateSigningStepsRequest, template_id: str
    ) -> Template:
        """Add template signing steps

        :param request_body: The request body.
        :type request_body: AddTemplateSigningStepsRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Signing steps added successfully
        :rtype: Template
        """

        Validator(AddTemplateSigningStepsRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/signing_steps",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def rename_template(
        self, request_body: RenameTemplateRequest, template_id: str
    ) -> Template:
        """Rename template

        :param request_body: The request body.
        :type request_body: RenameTemplateRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Template renamed successfully
        :rtype: Template
        """

        Validator(RenameTemplateRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/rename",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def set_template_comment(
        self, request_body: SetTemplateCommentRequest, template_id: str
    ) -> Template:
        """Set template comment

        :param request_body: The request body.
        :type request_body: SetTemplateCommentRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Template comment changed successfully
        :rtype: Template
        """

        Validator(SetTemplateCommentRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/set_comment",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def set_template_notification(
        self, request_body: EnvelopeNotification, template_id: str
    ) -> Template:
        """Set template notification

        :param request_body: The request body.
        :type request_body: EnvelopeNotification
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Template notification changed successfully
        :rtype: Template
        """

        Validator(EnvelopeNotification).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/set_notification",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def get_template_annotations(
        self, template_id: str
    ) -> ListTemplateAnnotationsResponse:
        """Get template annotations

        :param template_id: ID of the template
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of annotations retrieved successfully
        :rtype: ListTemplateAnnotationsResponse
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/annotations",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return ListTemplateAnnotationsResponse._unmap(response)

    @cast_models
    def get_document_template_annotations(
        self, template_id: str, document_id: str
    ) -> ListTemplateDocumentAnnotationsResponse:
        """Get document template annotations

        :param template_id: ID of the template
        :type template_id: str
        :param document_id: ID of document
        :type document_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of document annotations retrieved successfully
        :rtype: ListTemplateDocumentAnnotationsResponse
        """

        Validator(str).validate(template_id)
        Validator(str).validate(document_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/annotations/{{document_id}}",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .add_path("document_id", document_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return ListTemplateDocumentAnnotationsResponse._unmap(response)

    @cast_models
    def add_template_annotation(
        self, request_body: AddAnnotationRequest, template_id: str
    ) -> Annotation:
        """Add template annotation

        :param request_body: The request body.
        :type request_body: AddAnnotationRequest
        :param template_id: ID of the template
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Annotation added successfully
        :rtype: Annotation
        """

        Validator(AddAnnotationRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/annotation",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Annotation._unmap(response)

    @cast_models
    def delete_template_annotation(self, template_id: str, annotation_id: str) -> Any:
        """Delete template annotation

        :param template_id: ID of the template
        :type template_id: str
        :param annotation_id: ID of the annotation to delete
        :type annotation_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(template_id)
        Validator(str).validate(annotation_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/template/{{template_id}}/annotation/{{annotation_id}}",
                self.get_default_headers(),
            )
            .add_path("template_id", template_id)
            .add_path("annotation_id", annotation_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)
        return response

    @cast_models
    def create_webhook(self, request_body: CreateWebhookRequest) -> Webhook:
        """Create webhook

        :param request_body: The request body.
        :type request_body: CreateWebhookRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Webhook event received successfully
        :rtype: Webhook
        """

        Validator(CreateWebhookRequest).validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/webhook", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return Webhook._unmap(response)

    @cast_models
    def list_webhooks(
        self, request_body: ListWebhooksRequest = None
    ) -> ListWebhooksResponse:
        """List webhooks

        :param request_body: The request body., defaults to None
        :type request_body: ListWebhooksRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of webhooks retrieved successfully
        :rtype: ListWebhooksResponse
        """

        Validator(ListWebhooksRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/webhooks", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return ListWebhooksResponse._unmap(response)

    @cast_models
    def delete_webhook(self, webhook_id: str) -> Any:
        """Delete webhook

        :param webhook_id: webhook_id
        :type webhook_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(webhook_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/webhook/{{webhook_id}}", self.get_default_headers()
            )
            .add_path("webhook_id", webhook_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)
        return response
