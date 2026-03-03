import warnings
from typing import Optional

from opentelemetry import trace
from phoenix.otel import register
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from pathlib import Path



def instrument_adk_with_phoenix() -> Optional[trace.Tracer]:
    """
    Instrument the Google ADK with Phoenix (local OpenInference tracing).

    This sets up:
    - An OpenTelemetry TracerProvider
    - A Phoenix exporter (local UI)
    - Google ADK auto-instrumentation
    """

    try:
        # Register with Phoenix / OpenInference
        parent_name = Path(__file__).resolve().parent.name
        tracer_provider = register(project_name=parent_name, batch=True)
    except Exception as e:
        warnings.warn(f"Failed to initialize Phoenix tracing: {e}")
        return None

    # Instrument Google ADK so agent + tool calls emit OpenInference spans
    GoogleADKInstrumentor().instrument(
        tracer_provider=tracer_provider
    )

    return tracer_provider.get_tracer(__name__)
