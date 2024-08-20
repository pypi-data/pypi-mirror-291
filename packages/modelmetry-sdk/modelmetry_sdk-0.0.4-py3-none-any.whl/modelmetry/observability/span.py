from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import uuid

from modelmetry.observability.finding import Finding
from modelmetry.observability.event import Event
from modelmetry.openapi import CreateSpanParams
from modelmetry import (
    EmbeddingsPayload,
    CompletionPayload,
    RetrievalPayload,
    Options,
)
from modelmetry.openapi.models.completion_payload_context import (
    CompletionPayloadContext,
)
from modelmetry.openapi.models.input import Input
from modelmetry.openapi.models.options import Options
from modelmetry.openapi.models.output import Output
from modelmetry.openapi.models.retrieval_query import RetrievalQuery
from modelmetry.openapi.models.retrieved_item import RetrievedItem


class BaseSpan:

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        family: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.xid: str = str(uuid.uuid4())
        self.tenant_id: str = tenant_id
        self.trace_id: str = trace_id
        self.parent_id: Optional[str] = parent_id
        self.name: str = name
        self.message: str = message
        self.started_at: datetime = datetime.now(timezone.utc)
        self.ended_at: Optional[datetime] = None
        self.severity: str = severity
        self.metadata: Dict[str, Any] = metadata or {}
        self.family: str = family
        self.family_data: Dict[str, Any] = {}

        self.spans: List[
            Union["CompletionSpan", "RetrievalSpan", "EmbeddingsSpan", "OtherSpan"]
        ] = []
        self.findings: List[Finding] = []
        self.events: List[Event] = []

    def finding(
        self,
        name: str,
        value: Union[int, bool, str],
        comment: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
    ) -> Finding:
        finding = Finding(
            name=name,
            value=value,
            tenant_id=self.tenant_id,
            trace_id=self.trace_id,
            span_id=self.xid,
            comment=comment,
            description=description,
            metadata=metadata,
            source=source,
        )
        self.findings.append(finding)
        return finding

    def event(self, name: str) -> Event:
        event = Event(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            span_id=self.xid,
        )
        self.events.append(event)
        return event

    def get_events(self) -> List[Event]:
        return self.events

    def get_findings(self) -> List[Finding]:
        return self.findings

    def errored(self, error: Exception) -> None:
        self.event("errored")
        self.severity = "error"
        self.message = str(error)
        self.metadata["error"] = str(error)
        self.ended_at = datetime.now(timezone.utc)

    def completion(self, name: str) -> "CompletionSpan":
        span = CompletionSpan(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            parent_id=self.xid,
        )
        self.spans.append(span)
        return span

    def retrieval(self, name: str) -> "RetrievalSpan":
        span = RetrievalSpan(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            parent_id=self.xid,
        )
        self.spans.append(span)
        return span

    def embeddings(self, name: str) -> "EmbeddingsSpan":
        span = EmbeddingsSpan(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            parent_id=self.xid,
        )
        self.spans.append(span)
        return span

    def other_span(self, name: str) -> "OtherSpan":
        span = OtherSpan(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            parent_id=self.xid,
        )
        self.spans.append(span)
        return span

    def get_children_spans(self) -> List["BaseSpan"]:
        return self.spans

    def get_descendant_spans(self) -> List["BaseSpan"]:
        descendants = []
        for span in self.get_children_spans():
            descendants.append(span)
            descendants.extend(span.get_descendant_spans())
        return descendants

    def get_descendant_spans_count(self) -> int:
        return len(self.get_descendant_spans())

    def maybe_set_ended_at_to_now(self) -> None:
        if not self.ended_at:
            self.ended_at = datetime.now(timezone.utc)

    def set_ended_at_automatically(self):
        for span in self.get_children_spans():
            span.set_ended_at_automatically()

        if not self.ended_at:
            children_ended_at = [
                span.ended_at for span in self.get_children_spans() if span.ended_at
            ]
            if not children_ended_at:
                self.ended_at = datetime.now(timezone.utc)
                return self

            max_children_ended_at = max(children_ended_at)
            self.ended_at = max_children_ended_at

        if self.ended_at:
            children_ended_at = [
                span.ended_at for span in self.get_children_spans() if span.ended_at
            ]
            if not children_ended_at:
                return self

            max_children_ended_at = max(children_ended_at)
            if max_children_ended_at > self.ended_at:
                self.ended_at = max_children_ended_at

        return self

    def to_ingest_params(self) -> CreateSpanParams:
        return CreateSpanParams(
            xid=self.xid,
            name=self.name,
            start=self.started_at,
            end=self.ended_at or None,
            message=self.message,
            trace_id=self.trace_id,
            metadata=self.metadata,
            family=self.family,
            family_data=self.family_data,
            parent_id=self.parent_id,
            severity=self.severity,
        )

    def __eq__(self, other):
        if not isinstance(other, BaseSpan):
            return False
        return self.xid == other.xid

    def __hash__(self):
        return hash(self.xid)


class OtherSpan(BaseSpan):

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        family: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            name=name,
            trace_id=trace_id,
            tenant_id=tenant_id,
            parent_id=parent_id,
            message=message,
            severity=severity,
            family=family,
            metadata=metadata,
        )

    def end(self) -> "OtherSpan":
        self.maybe_set_ended_at_to_now()
        return self


class EmbeddingsSpan(BaseSpan):

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        family: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        inputs: List[str] = None,
        options: Options = None,
    ):
        super().__init__(
            name=name,
            trace_id=trace_id,
            tenant_id=tenant_id,
            parent_id=parent_id,
            message=message,
            severity=severity,
            family=family,
            metadata=metadata,
        )

        self.family_data = EmbeddingsPayload(
            inputs=inputs or [],
            options=options or Options(),
        )

    def end(self) -> "EmbeddingsSpan":
        self.maybe_set_ended_at_to_now()
        return self


class CompletionSpan(BaseSpan):

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        model: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        family: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        input: Input = None,
        context: CompletionPayloadContext = None,
        options: Options = None,
        output: Output = None,
    ):
        super().__init__(
            name=name,
            trace_id=trace_id,
            tenant_id=tenant_id,
            parent_id=parent_id,
            message=message,
            severity=severity,
            family=family,
            metadata=metadata,
        )

        self.family_data = CompletionPayload(
            Model=model or "unknown/unknown",
            Options=options or Options(),
            # optional
            Context=context or None,
            Input=input or None,
            Output=output or None,
        )

    def end(self) -> "CompletionSpan":
        self.maybe_set_ended_at_to_now()
        return self


class RetrievalSpan(BaseSpan):

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        family: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        queries: List[RetrievalQuery] = None,
        retrieved: List[RetrievedItem] = None,
    ):
        super().__init__(
            name=name,
            trace_id=trace_id,
            tenant_id=tenant_id,
            parent_id=parent_id,
            message=message,
            severity=severity,
            family=family,
            metadata=metadata,
        )

        self.family_data = RetrievalPayload(
            Queries=queries or [],
            Retrieved=retrieved or [],
        )

    def end(self) -> "RetrievalSpan":
        self.maybe_set_ended_at_to_now()
        return self
