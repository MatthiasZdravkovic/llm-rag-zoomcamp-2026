from opentelemetry import trace
from rag_helper import RAGBase

tracer = trace.get_tracer("llm-zoomcamp")

class RAGTraced(RAGBase):

    def llm(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            result = super().llm(prompt)
            usage = result.usage
            span.set_attribute("input_tokens", usage.input_tokens)
            span.set_attribute("output_tokens", usage.output_tokens)
            return result
        

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search") as span:
            result = super().search(query, num_results=5)
            # span.set_attribute("my_key", "my_value")
            return result
    
    # def rag(self, query):
    #     with tracer.start_as_current_span("rag") as span:
    #         result = super().rag(query)
    #         return result
