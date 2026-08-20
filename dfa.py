"""
GenoCheck — Stage 1 (DFA) Implementation
TECH315 — Models of Computation

Validates DNA sequences for:
1. Valid alphabet (A, C, G, T only)
2. Length is a multiple of 3 (codon constraint)

Formal Definition: (Q, Σ, δ, q0, F)
- Q = {q0, q1, q2, reject}
- Σ = {A, C, G, T}
- q0 = initial state (length mod 3 = 0)
- F = {q0} (accepting state)
- States track: (1) invalid symbol seen, (2) current length mod 3
"""

def validate(sequence: str) -> dict:
    """
    Validates a DNA sequence using a DFA.
    
    Args:
        sequence: DNA string over alphabet {A, C, G, T}
    
    Returns:
        {
            "accepted": bool,
            "trace": list[str],
            "states_visited": list[str],
            "final_state": str,
            "current_state_at_step": list[str]  # For UI highlighting
        }
    """
    
    VALID_ALPHABET = {'A', 'C', 'G', 'T'}
    trace = []
    states_visited = ["q0"]  # Start at q0
    current_state_at_step = []
    
    # Initial state
    current_state = "q0"
    length_mod_3 = 0
    trace.append(f"[q0] Start state. Input: '{sequence}' (length {len(sequence)})")
    current_state_at_step.append(current_state)
    
    # Process each symbol
    for i, char in enumerate(sequence):
        if char not in VALID_ALPHABET:
            current_state = "reject"
            trace.append(f"[reject] Invalid symbol '{char}' at position {i}")
            current_state_at_step.append(current_state)
            return {
                "accepted": False,
                "trace": trace,
                "states_visited": states_visited,
                "final_state": current_state,
                "current_state_at_step": current_state_at_step
            }
        
        # Update length mod 3
        length_mod_3 = (length_mod_3 + 1) % 3
        next_state = f"q{length_mod_3}"
        states_visited.append(next_state)
        current_state_at_step.append(next_state)
        
        remaining = sequence[i+1:]
        trace.append(f"[{next_state}] Read '{char}' at position {i} | Length mod 3 = {length_mod_3} | Remaining: '{remaining}'")
        current_state = next_state
    
    # Check if we end in accepting state (q0, meaning length mod 3 == 0)
    accepted = current_state == "q0"
    if accepted:
        trace.append(f"[ACCEPT] Sequence length ({len(sequence)}) is a multiple of 3")
    else:
        trace.append(f"[REJECT] Sequence length ({len(sequence)}) mod 3 = {length_mod_3}")
    
    return {
        "accepted": accepted,
        "trace": trace,
        "states_visited": states_visited,
        "final_state": current_state,
        "current_state_at_step": current_state_at_step
    }


if __name__ == "__main__":
    # Quick test
    test_cases = [
        ("ATG", True),
        ("ATGCAT", True),
        ("AT", False),
        ("ATGC", False),
        ("ATX", False),
    ]
    
    for seq, expected in test_cases:
        result = validate(seq)
        status = "PASS" if result["accepted"] == expected else "FAIL"
        print(f"[{status}] '{seq}' -> {result['accepted']} (expected {expected})")
