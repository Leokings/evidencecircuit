import json
import os
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address

from tests.studionet_support import emit_record, ok, source_schema_proof, wallet_accounts


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("RUN_STUDIONET") != "1", reason="opt-in live StudioNet test"),
]


def test_studionet_boolean_evidence_circuit():
    accounts = wallet_accounts("evidencecircuit", 1)
    owner = accounts[0]
    source = Path(__file__).resolve().parents[2] / "contracts" / "evidence_circuit.py"
    factory = get_contract_factory(contract_file_path=source)
    deployed = ok(factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=owner)
    labels = json.dumps(["HAS_SIGNED_APPROVAL", "HAS_CURRENT_DATE", "HAS_REFERENCE"])
    program = json.dumps([{"op": "AND", "a": 0, "b": 1}, {"op": "AND", "a": 3, "b": 2}])
    setup = ok(contract.publish_circuit(args=["packet_gate", labels, program]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    circuit_id = f"{str(owner.address).lower()}:PACKET_GATE"
    run_id = f"{circuit_id}:{str(owner.address).lower()}:CASE_1"
    intelligent = ok(contract.evaluate_circuit(args=[circuit_id, "case_1", "The public packet has signed approval, a current date, and a traceable reference number." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = contract.get_run(args=[run_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["schema"] == "evidencecircuit/run/v1" and isinstance(state["output"], bool)
    proof = source_schema_proof(address, source, {"publish_circuit", "evaluate_circuit", "get_run"})
    emit_record("evidencecircuit", "A", address, deployed, [setup], intelligent, accounts, proof, {"output": state["output"], "true_input_count": len(state["true_inputs"])})
