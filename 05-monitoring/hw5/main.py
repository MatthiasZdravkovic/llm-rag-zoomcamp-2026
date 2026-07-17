from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

import pandas as pd

provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)
trace.set_tracer_provider(provider)

from starter import index, client
from rag_traced import RAGTraced

rag = RAGTraced(index=index, llm_client=client)

# Question 1 et 2

# query = "How does the agentic loop keep calling the model until it stops?"
# answer = rag.rag(query)
# print(answer)

import sqlite3
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


class SQLiteSpanExporter(SpanExporter):

    def __init__(self, db_path="traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spans (
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
        """)
        self.conn.commit()

    def export(self, spans):
        for span in spans:
            attrs = dict(span.attributes or {})
            self.conn.execute(
                "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
                (
                    span.name,
                    span.start_time,
                    span.end_time,
                    attrs.get("input_tokens"),
                    attrs.get("output_tokens"),
                    attrs.get("cost"),
                ),
            )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self):
        self.conn.close()

    def force_flush(self):
        return True


provider.add_span_processor(
    SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
)

# Question 4

# query = "How does the agentic loop keep calling the model until it stops?"
# answer = rag.rag(query)
# print(answer)

from sqlalchemy import create_engine, text

db = create_engine("sqlite:///traces.db")

df = pd.read_sql_table("spans", db)
df['duration_sec'] = (df['end_time'] - df['start_time']) / 1_000_000
print(df[df['name'] == 'llm'])