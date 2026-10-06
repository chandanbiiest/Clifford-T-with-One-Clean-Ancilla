#!/usr/bin/env python3
"""List provider targets in an Azure Quantum workspace.

Set AZURE_QUANTUM_CONNECTION_STRING or use the authentication method configured
for your QDK installation.
"""
import os
from qdk.azure import Workspace

connection = os.environ.get("AZURE_QUANTUM_CONNECTION_STRING")
if not connection:
    raise SystemExit("Set AZURE_QUANTUM_CONNECTION_STRING before running this script.")
workspace = Workspace.from_connection_string(connection)
for target in workspace.get_targets():
    print(target.name)
