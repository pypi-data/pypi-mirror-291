import openai
import requests
import json
import uuid
from datetime import datetime
import functools
from fastapi import FastAPI, Request
import uvicorn
import inspect
import importlib
from fastapi.middleware.cors import CORSMiddleware
import ast
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

BACKPROXY_URL = "http://127.0.0.1:8000"
session_id = str(uuid.uuid4())
call_sequence = []

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the call graph
call_graph = nx.DiGraph()

def push_to_fastapi(data, endpoint):
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BACKPROXY_URL}/{endpoint}", json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Data log failed: {response.text}")

def calculate_cost(model, usage):
    pricing = {
        "gpt-3.5-turbo": 0.002 / 1000,
        "gpt-4": 0.03 / 1000,
    }
    base_price = pricing.get(model, 0.002 / 1000)
    return (usage["prompt_tokens"] + usage["completion_tokens"]) * base_price

def traced_function(func=None, *, name=None, inputs=None, type=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            caller = inspect.currentframe().f_back.f_code.co_name
            func_name = name or f.__name__
            
            trace_id = str(uuid.uuid4())
            trace_oai_instance.trace_id_map[func_name] = trace_id
            
            # Log the function call
            trace_oai_instance.log_execution(caller, trace_id, 'function')
            
            start_time = datetime.now()
            result = f(*args, **kwargs)
            end_time = datetime.now()

            trace_data = {
                "id": trace_id,
                "type": type or "custom_function",
                "agentId": func_name,
                "metadata": json.dumps(
                    {
                        "function_name": func_name,
                        "args": inputs or args,
                        "kwargs": kwargs,
                        "result": result,
                        "duration": (end_time - start_time).total_seconds(),
                    }
                ),
                "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "tags": json.dumps(["custom_function"]),
                "prompt": json.dumps({"args": inputs or args, "kwargs": kwargs}),
                "response": json.dumps({"result": result}),
                "session_id": session_id,
                "cost": 0,
                "sequence_number": len(call_sequence),
            }
            call_sequence.append(trace_id)
            push_to_fastapi(trace_data, "push-data")
            return result

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)

class TracedChatCompletions:
    def __init__(self, client):
        self.client = client

    def create(self, *args, **kwargs):
        agent_id = kwargs.pop("agent_id", "default_agent")
        metadata = kwargs.pop("metadata", {})
        tags = kwargs.pop("tags", [])

        start_time = datetime.now()
        response = self.client.chat.completions.create(*args, **kwargs)
        end_time = datetime.now()

        trace_id = str(uuid.uuid4())
        llm_node = f"LLM_{agent_id}"
        trace_oai_instance.trace_id_map[llm_node] = trace_id

        usage = response.usage.model_dump()
        cost = calculate_cost(response.model, usage)

        # Add node and edge to call graph
        call_graph.add_node(llm_node, type='llm')
        if call_sequence:
            call_graph.add_edge(call_sequence[-1], llm_node)

        metadata.update(
            {
                "model": response.model,
                "usage": usage,
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "duration": (end_time - start_time).total_seconds(),
            }
        )

        trace_data = {
            "id": trace_id,
            "type": "llm_call",
            "agentId": llm_node,
            "metadata": json.dumps(metadata),
            "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "tags": json.dumps(tags),
            "prompt": json.dumps(kwargs),
            "response": json.dumps(response.model_dump()),
            "session_id": session_id,
            "cost": cost,
            "sequence_number": len(call_sequence),
        }
        call_sequence.append(trace_id)
        push_to_fastapi(trace_data, "push-data")
        
        # Log the LLM call
        caller = inspect.currentframe().f_back.f_code.co_name
        trace_oai_instance.log_execution(caller, trace_id, 'llm')

        return response

class TracedChat:
    def __init__(self, client):
        self.completions = TracedChatCompletions(client)

class TracedOpenAI:
    def __init__(self, client):
        self.chat = TracedChat(client)
        self.session_start = datetime.now()
        self.create_session()
        self.execution_sequence = []
        self.function_calls = defaultdict(list)
        self.edges = {}
        self.trace_id_map = {}  # New dictionary to map function names to trace IDs

    def log_execution(self, caller, callee, call_type):
        caller_trace_id = self.trace_id_map.get(caller, caller)
        callee_trace_id = self.trace_id_map.get(callee, callee)
        self.execution_sequence.append((caller_trace_id, callee_trace_id, call_type))
        self.function_calls[caller_trace_id].append(callee_trace_id)

    def create_session(self):
        session_data = {
            "id": session_id,
            "session_start": self.session_start.strftime("%Y-%m-%d %H:%M:%S"),
            "trace_ids": json.dumps([]),
        }
        push_to_fastapi(session_data, "create-session")

    def generate_call_graph(self):
        G = nx.DiGraph()
        
        # Add nodes and edges based on execution sequence
        for caller, callee, call_type in self.execution_sequence:
            G.add_edge(caller, callee)
            if call_type == 'llm':
                G.nodes[callee]['color'] = 'lightgreen'
            else:
                G.nodes[callee]['color'] = 'lightblue'

        # Add 'main' node as the root if it doesn't exist
        if 'main' not in G:
            main_trace_id = str(uuid.uuid4())
            self.trace_id_map['main'] = main_trace_id
            G.add_node(main_trace_id, color='yellow')
            # Connect 'main' to all nodes without incoming edges
            for node in G.nodes():
                if G.in_degree(node) == 0 and node != main_trace_id:
                    G.add_edge(main_trace_id, node)

        # Generate edges dictionary
        self.edges = {node: {"inbound": [], "outbound": []} for node in G.nodes()}
        for edge in G.edges():
            self.edges[edge[0]]["outbound"].append(edge[1])
            self.edges[edge[1]]["inbound"].append(edge[0])

        # Generate layout
        pos = nx.spring_layout(G, k=0.9, iterations=50)

        # Draw the graph
        plt.figure(figsize=(20, 12))
        node_colors = [G.nodes[node].get('color', 'lightgray') for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=8, arrows=True)
        nx.draw_networkx_labels(G, pos)
        edge_labels = nx.get_edge_attributes(G, 'type')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Holistic Function and LLM Call Graph")
        plt.savefig(f"holistic_call_graph_{session_id}.png", dpi=300, bbox_inches='tight')
        plt.close()

    def end_session(self):
        self.generate_call_graph()
        session_data = {
            "id": session_id,
            "call_sequence": json.dumps(call_sequence),
            "edges": json.dumps(self.edges)
        }
        push_to_fastapi(session_data, "end-session")

def trace_oai(api_key):
    openai.api_key = api_key
    global trace_oai_instance
    trace_oai_instance = TracedOpenAI(openai)
    return trace_oai_instance

def analyze_ast(source_code):
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            call_graph.add_node(node.name, type='function')
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == 'trace_oai':
                call_graph.add_node("LLM_call", type='llm')

def start_server():
    module = importlib.import_module("test_sdk")
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and hasattr(obj, "__wrapped__"):
            globals()[name] = obj

    # Analyze AST of the test_sdk module
    with open("test_sdk.py", "r") as file:
        source_code = file.read()
    analyze_ast(source_code)

    uvicorn.run(app, host="0.0.0.0", port=5001)

@app.post("/call-function")
async def call_function(request: Request):
    data = await request.json()
    function_name = data["function_name"]
    args = data.get("args", [])
    kwargs = data.get("kwargs", {})

    func = globals().get(function_name)
    if not func:
        return {"error": f"Function {function_name} not found"}

    print(f"Calling function {function_name} with args {args} and kwargs {kwargs}")
    result = func(*args, **kwargs)
    print(f"Function {function_name} returned {result}")
    return {"result": result}

if __name__ == "__main__":
    start_server()