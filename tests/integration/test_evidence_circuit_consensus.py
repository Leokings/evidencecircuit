import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def test_five_validator_boolean_circuit_flow():
    owner = create_accounts(1)[0]
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "evidence_circuit.py")
    receipt = factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    contract = factory.build_contract(extract_contract_address(receipt), account=owner)
    labels = json.dumps(["HAS_SIGNED_APPROVAL", "HAS_CURRENT_DATE", "HAS_REFERENCE"])
    program = json.dumps([{"op": "AND", "a": 0, "b": 1}, {"op": "AND", "a": 3, "b": 2}])
    circuit_id = f"{str(owner.address).lower()}:PACKET_GATE"
    receipt = contract.publish_circuit(args=["packet_gate", labels, program]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {"Evaluate public evidence against a closed Boolean input vocabulary": json.dumps({"true_inputs": ["HAS_SIGNED_APPROVAL", "HAS_CURRENT_DATE", "HAS_REFERENCE"]})}})
    context = {"validators": [item.to_dict() for item in validators], "genvm_datetime": "2026-08-25T12:00:00Z"}
    run_id = f"{circuit_id}:{str(owner.address).lower()}:CASE_1"
    receipt = contract.evaluate_circuit(args=[circuit_id, "case_1", "The packet has signed approval, a current date, and a traceable reference number."]).transact(transaction_context=context, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    assert contract.output_is(args=[run_id, True]).call() is True
