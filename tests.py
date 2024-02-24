operation = "runInstances"
action = "create_instances" if any(word.lower() in operation.lower() for word in ["runinstances", "terminateinstances"]) else "terminate_instances"
print(action)