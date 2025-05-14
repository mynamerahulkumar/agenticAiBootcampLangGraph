🧪 Example:
Let's say the user sends:
“What’s 3 plus 4?”

The model sees that this is a math task and returns a message like:


{
  "tool_calls": [
    {
      "name": "add",
      "arguments": {"a": 3, "b": 4}
    }
  ]
}
should_continue sees tool_calls is present → goes to "tools"

"tools" executes add(3, 4) and adds a message back with result 7

Then it loops back to agent for final response

