from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool

def add(a: float, b: float) -> float:
  """Add two numbers and returns the result"""
  return a + b
add_tool = FunctionTool.from_defaults(fn=add)

def multiply(a: float, b: float) -> float:
  """Multiply two numbers and returns the result"""
  return a * b
multiply_tool = FunctionTool.from_defaults(fn=multiply)

def subtract(a: float, b: float) -> float:
  """Subtract two numbers and returns the result"""
  return a - b
subtract_tool = FunctionTool.from_defaults(fn=subtract)

def divide(a: float, b: float) -> float:
  """Divide two numbers and returns the result. Handles division by zero error"""
  if b == 0:
    raise ZeroDivisionError("Division by zero is not allowed")
  return a / b
divide_tool = FunctionTool.from_defaults(fn=divide)




tools = [multiply_tool, add_tool, subtract_tool, divide_tool]

llm = OpenAI(model="gpt-3.5-turbo")
agent = ReActAgent.from_tools(tools, llm=llm,verbose=True)

response = agent.chat("5 + 5")
print(response)



