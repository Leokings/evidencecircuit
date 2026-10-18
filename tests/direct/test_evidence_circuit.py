import json


LABELS = json.dumps(["HAS_SIGNED_APPROVAL", "HAS_CURRENT_DATE", "HAS_REFERENCE"])
PROGRAM = json.dumps([
    {"op": "AND", "a": 0, "b": 1},
    {"op": "AND", "a": 3, "b": 2},
])
EVIDENCE = "Signed approval is present. The date is current. A reference is present."


def _assessment(statuses, quotes):
    return json.dumps({"assessments": [
        {"label": label, "status": status, "quote": quote}
        for label, status, quote in zip(json.loads(LABELS), statuses, quotes)
    ]})


def test_publishes_acyclic_circuit(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    circuit_id = contract.publish_circuit("packet_gate", LABELS, PROGRAM)
    assert contract.get_circuit(circuit_id)["node_count"] == 5


def test_rejects_forward_gate_reference(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    bad = json.dumps([{"op": "AND", "a": 0, "b": 9}])
    with direct_vm.expect_revert("invalid_gate_reference"):
        contract.publish_circuit("bad", LABELS, bad)


def test_consensus_truth_executes_program(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    circuit_id = contract.publish_circuit("packet_gate", LABELS, PROGRAM)
    direct_vm.mock_llm(r".*Evaluate public evidence against a closed Boolean input vocabulary.*", _assessment(["SUPPORTED"] * 3, ["Signed approval is present.", "The date is current.", "A reference is present."]))
    run_id = contract.evaluate_circuit(circuit_id, "case_1", EVIDENCE)
    assert contract.output_is(run_id, True) is True
    assert contract.get_run(run_id)["truth_mask"] == 7


def test_missing_input_changes_output(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    circuit_id = contract.publish_circuit("packet_gate", LABELS, PROGRAM)
    direct_vm.mock_llm(r".*Evaluate public evidence against a closed Boolean input vocabulary.*", _assessment(["SUPPORTED", "SUPPORTED", "INSUFFICIENT_EVIDENCE"], ["Signed approval is present.", "The date is current.", ""]))
    run_id = contract.evaluate_circuit(circuit_id, "case_2", "Signed approval is present. The date is current.")
    assert contract.get_run(run_id)["output_status"] == "UNKNOWN"
    assert contract.output_is(run_id, True) is False
    assert contract.output_is(run_id, False) is False


def test_model_cannot_invent_input(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    circuit_id = contract.publish_circuit("packet_gate", LABELS, PROGRAM)
    direct_vm.mock_llm(r".*Evaluate public evidence against a closed Boolean input vocabulary.*", json.dumps({"assessments": [
        {"label": "INVENTED", "status": "SUPPORTED", "quote": "Signed approval is present."},
        {"label": "HAS_CURRENT_DATE", "status": "SUPPORTED", "quote": "The date is current."},
        {"label": "HAS_REFERENCE", "status": "SUPPORTED", "quote": "A reference is present."},
    ]}))
    with direct_vm.expect_revert("[LLM_ERROR] unknown_or_duplicate_truth_label"):
        contract.evaluate_circuit(circuit_id, "case_3", EVIDENCE)
