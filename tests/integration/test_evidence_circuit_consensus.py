"""Local five-validator simulation; mocked models are not live-network proof."""

import json
from pathlib import Path

import pytest
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


pytestmark = pytest.mark.integration
NOW = {"genvm_datetime": "2026-08-25T12:00:00Z"}
LABELS = ["CONDITION_ALPHA", "CONDITION_BETA", "CONDITION_GAMMA"]


def _ok(receipt):
    assert receipt["status_name"] == TransactionStatus.FINALIZED.value
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _rejected(receipt, code):
    assert receipt["status_name"] == TransactionStatus.FINALIZED.value
    assert not tx_execution_succeeded(receipt)
    assert code in json.dumps(receipt, default=str)


@pytest.fixture
def deployed():
    owner = create_accounts(1)[0]
    source = Path(__file__).resolve().parents[2] / "contracts" / "evidence_circuit.py"
    factory = get_contract_factory(contract_file_path=source)
    receipt = factory.deploy_contract_tx(args=[], account=owner, transaction_context=NOW,
                                         wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    return owner, factory.build_contract(extract_contract_address(receipt), account=owner)


@pytest.mark.parametrize("gate,statuses,expected", [
    ({"op": "AND", "a": 0, "b": 1}, ["SUPPORTED", "SUPPORTED", "SUPPORTED"], "TRUE"),
    ({"op": "AND", "a": 0, "b": 1}, ["CONTRADICTED", "INSUFFICIENT_EVIDENCE", "SUPPORTED"], "FALSE"),
    ({"op": "OR", "a": 0, "b": 1}, ["SUPPORTED", "INSUFFICIENT_EVIDENCE", "SUPPORTED"], "TRUE"),
    ({"op": "XOR", "a": 0, "b": 1}, ["SUPPORTED", "SUPPORTED", "SUPPORTED"], "FALSE"),
    ({"op": "ATLEAST2", "a": 0, "b": 1, "c": 2}, ["SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE"], "UNKNOWN"),
    ({"op": "ATLEAST2", "a": 0, "b": 1, "c": 2}, ["SUPPORTED", "SUPPORTED", "INSUFFICIENT_EVIDENCE"], "TRUE"),
    ({"op": "NOT", "a": 0}, ["INSUFFICIENT_EVIDENCE", "SUPPORTED", "SUPPORTED"], "UNKNOWN"),
    ({"op": "NOT", "a": 0}, ["CONTRADICTED", "SUPPORTED", "SUPPORTED"], "TRUE"),
])
def test_five_validator_three_valued_circuit_flow(deployed, gate, statuses, expected):
    owner, contract = deployed
    circuit_id = f"{str(owner.address).lower()}:PACKET_GATE"
    _ok(contract.publish_circuit(args=["packet_gate", json.dumps(LABELS), json.dumps([gate])]).transact(
        transaction_context=NOW, wait_transaction_status=TransactionStatus.FINALIZED))
    rows, sentences = [], []
    for label, status in zip(LABELS, statuses):
        sentence = f"{label} is {'present' if status == 'SUPPORTED' else 'explicitly absent'}."
        quote = sentence if status != "INSUFFICIENT_EVIDENCE" else ""
        if quote:
            sentences.append(quote)
        rows.append({"label": label, "status": status, "quote": quote})
    evidence = " ".join(sentences)
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={
        "nondet_exec_prompt": {"Evaluate public evidence against a closed Boolean input vocabulary":
                               json.dumps({"assessments": rows})}})
    context = {**NOW, "validators": [item.to_dict() for item in validators]}
    run_id = f"{circuit_id}:{str(owner.address).lower()}:CASE_1"
    _ok(contract.evaluate_circuit(args=[circuit_id, "case_1", evidence]).transact(
        transaction_context=context, wait_transaction_status=TransactionStatus.FINALIZED))
    state = contract.get_run(args=[run_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["schema"] == "evidencecircuit/run/v2"
    assert state["assessments"] == rows
    assert state["output_status"] == expected
    assert state["output"] is (None if expected == "UNKNOWN" else expected == "TRUE")
    for value in (True, False):
        assert contract.output_is(args=[run_id, value]).call() is (expected == ("TRUE" if value else "FALSE"))
    assert state["circuit_digest"] == contract.get_circuit(args=[circuit_id]).call()["circuit_digest"]
    assert len(state["evidence_digest"]) == 64
    _rejected(contract.evaluate_circuit(args=[circuit_id, "case_1", evidence]).transact(
        transaction_context=NOW, wait_transaction_status=TransactionStatus.FINALIZED), "run_exists")
    assert contract.get_run(args=[run_id]).call() == state


def test_program_validation_and_circuit_replay(deployed):
    _, contract = deployed
    _rejected(contract.publish_circuit(args=["bad", json.dumps(LABELS),
        json.dumps([{"op": "NOT", "a": 3}])]).transact(transaction_context=NOW,
        wait_transaction_status=TransactionStatus.FINALIZED), "invalid_gate_reference")
    args = ["frozen", json.dumps(LABELS), json.dumps([{"op": "NOT", "a": 0}])]
    _ok(contract.publish_circuit(args=args).transact(transaction_context=NOW,
        wait_transaction_status=TransactionStatus.FINALIZED))
    _rejected(contract.publish_circuit(args=args).transact(transaction_context=NOW,
        wait_transaction_status=TransactionStatus.FINALIZED), "circuit_exists")
