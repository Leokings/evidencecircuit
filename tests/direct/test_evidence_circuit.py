import json


LABELS = json.dumps(["HAS_SIGNED_APPROVAL", "HAS_CURRENT_DATE", "HAS_REFERENCE"])
PROGRAM = json.dumps([
    {"op": "AND", "a": 0, "b": 1},
    {"op": "AND", "a": 3, "b": 2},
])
EVIDENCE = "The packet has signed approval, today's current date, and a traceable reference number."


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
    direct_vm.mock_llm(r".*Evaluate public evidence against a closed Boolean input vocabulary.*", json.dumps({"true_inputs": ["HAS_SIGNED_APPROVAL", "HAS_CURRENT_DATE", "HAS_REFERENCE"]}))
    run_id = contract.evaluate_circuit(circuit_id, "case_1", EVIDENCE)
    assert contract.output_is(run_id, True) is True
    assert contract.get_run(run_id)["truth_mask"] == 7


def test_missing_input_changes_output(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    circuit_id = contract.publish_circuit("packet_gate", LABELS, PROGRAM)
    direct_vm.mock_llm(r".*Evaluate public evidence against a closed Boolean input vocabulary.*", json.dumps({"true_inputs": ["HAS_SIGNED_APPROVAL", "HAS_CURRENT_DATE"]}))
    run_id = contract.evaluate_circuit(circuit_id, "case_2", EVIDENCE)
    assert contract.output_is(run_id, False) is True


def test_model_cannot_invent_input(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    circuit_id = contract.publish_circuit("packet_gate", LABELS, PROGRAM)
    direct_vm.mock_llm(r".*Evaluate public evidence against a closed Boolean input vocabulary.*", json.dumps({"true_inputs": ["INVENTED"]}))
    with direct_vm.expect_revert("[LLM_ERROR] unknown_or_duplicate_truth_label"):
        contract.evaluate_circuit(circuit_id, "case_3", EVIDENCE)
