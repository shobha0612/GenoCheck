"""
GenoCheck — Stage 3 (Turing Machine) Implementation
TECH315 — Models of Computation

Validates DNA sequences for:
1. Valid start codon (ATG) at position 0
2. Valid in-frame stop codon (TAA, TAG, TGA) at the end
3. No premature stop codons
4. Base-count constraint: count(G) == count(C)

The Turing Machine can read/write tape symbols and move left/right,
allowing multiple passes and independent counters.
"""

STOP_CODONS = {"TAA", "TAG", "TGA"}
START_CODON = "ATG"


def validate(sequence: str) -> dict:
    """
    Validates a DNA sequence using a Turing Machine.
    
    The TM makes multiple passes over the tape:
    - Pass 1: Check start codon, scan for in-frame stop codon
    - Pass 2: Count G and C bases
    
    Args:
        sequence: DNA string
    
    Returns:
        {
            "accepted": bool,
            "trace": list[str],
            "tape_history": list[dict],  # {"position": int, "symbol": str, "step": int}
            "passes": list[str],  # Description of each pass
            "counts": {"G": int, "C": int}
        }
    """
    
    trace = []
    tape_history = []
    passes = []
    n = len(sequence)
    tape = list(sequence)  # Tape as list of symbols
    
    trace.append(f"[TM] Start state. Tape: '{sequence}' (length {n})")
    trace.append(f"[TM] Tape cells: {' | '.join(tape)} | □ | □ | □")
    
    # Sanity check: must have room for start + stop
    if n < 6 or n % 3 != 0:
        trace.append(f"[TM] REJECT: length {n} is not a positive multiple of 3")
        passes.append("Length check: FAILED (not a multiple of 3)")
        return {
            "accepted": False,
            "trace": trace,
            "tape_history": tape_history,
            "passes": passes,
            "counts": {"G": 0, "C": 0}
        }
    
    # PASS 1: Check start codon and scan for in-frame stop codon
    trace.append(f"[TM] === PASS 1: Start/Stop codon validation ===")
    trace.append(f"[TM] Head at position 0. Reading first codon...")
    
    # Record tape head position for visualization
    for i in range(3):
        tape_history.append({
            "position": i,
            "symbol": tape[i],
            "step": len(tape_history),
            "operation": "read_start"
        })
    
    start_codon = sequence[0:3]
    if start_codon != START_CODON:
        trace.append(f"[TM] Found '{start_codon}' at position 0, expected '{START_CODON}'")
        trace.append(f"[TM] REJECT: no valid start codon")
        passes.append(f"Start codon check: FAILED (found '{start_codon}', expected 'ATG')")
        return {
            "accepted": False,
            "trace": trace,
            "tape_history": tape_history,
            "passes": passes,
            "counts": {"G": 0, "C": 0}
        }
    
    trace.append(f"[TM] Found start codon '{start_codon}' at position 0 ✓")
    passes.append("Start codon check: PASSED (ATG found at position 0)")
    
    # Scan for in-frame stop codon
    stop_pos = None
    for i in range(3, n, 3):
        codon = sequence[i:i+3]
        # Record tape head movement
        for j in range(i, i+3):
            if j < n:
                tape_history.append({
                    "position": j,
                    "symbol": tape[j],
                    "step": len(tape_history),
                    "operation": "scan"
                })
        
        trace.append(f"[TM] Head at position {i}. Codon: '{codon}'")
        
        if codon in STOP_CODONS:
            stop_pos = i
            trace.append(f"[TM] Found in-frame stop codon '{codon}' at position {i}")
            passes.append(f"Stop codon scan: Found '{codon}' at position {i}")
            break
    
    if stop_pos is None:
        trace.append(f"[TM] REJECT: no in-frame stop codon found")
        passes.append("Stop codon scan: FAILED (no stop codon in frame)")
        return {
            "accepted": False,
            "trace": trace,
            "tape_history": tape_history,
            "passes": passes,
            "counts": {"G": 0, "C": 0}
        }
    
    # Check if stop codon is at the end (position n-3)
    if stop_pos != n - 3:
        trace.append(f"[TM] REJECT: stop codon at position {stop_pos}, but sequence ends at {n-3}")
        trace.append(f"[TM]         This indicates a premature stop (not at sequence terminus)")
        passes.append(f"Stop codon position check: FAILED (stop at {stop_pos}, not at end {n-3})")
        return {
            "accepted": False,
            "trace": trace,
            "tape_history": tape_history,
            "passes": passes,
            "counts": {"G": 0, "C": 0}
        }
    
    trace.append(f"[TM] Stop codon is at sequence terminus ✓")
    passes.append("Stop codon position check: PASSED (at sequence terminus)")
    
    # PASS 2: Count bases G and C
    trace.append(f"[TM] === PASS 2: Base-count validation ===")
    trace.append(f"[TM] Scanning entire tape to tally G and C counts...")
    
    count_g = 0
    count_c = 0
    for i, symbol in enumerate(tape):
        if symbol == 'G':
            count_g += 1
        elif symbol == 'C':
            count_c += 1
        
        # Record tape head movement
        tape_history.append({
            "position": i,
            "symbol": tape[i],
            "step": len(tape_history),
            "operation": "count"
        })
        trace.append(f"[TM] Position {i}: '{symbol}' | G_count={count_g}, C_count={count_c}")
    
    trace.append(f"[TM] Final tallies: G={count_g}, C={count_c}")
    passes.append(f"Base-count scan: G={count_g}, C={count_c}")
    
    if count_g != count_c:
        trace.append(f"[TM] REJECT: count(G)={count_g} != count(C)={count_c}")
        passes.append(f"Base-count constraint check: FAILED (G≠C)")
        return {
            "accepted": False,
            "trace": trace,
            "tape_history": tape_history,
            "passes": passes,
            "counts": {"G": count_g, "C": count_c}
        }
    
    trace.append(f"[TM] ACCEPT: All validations passed!")
    passes.append(f"Base-count constraint check: PASSED (G==C)")
    
    return {
        "accepted": True,
        "trace": trace,
        "tape_history": tape_history,
        "passes": passes,
        "counts": {"G": count_g, "C": count_c}
    }


if __name__ == "__main__":
    test_cases = [
        ("ATGCGATAA", True),       # start=ATG, mid=CGA, stop=TAA, G=2, C=2
        ("GGCATGTAA", False),      # no start codon
        ("ATGGGCGGG", False),      # no stop codon
    ]
    
    for seq, expected in test_cases:
        result = validate(seq)
        status = "PASS" if result["accepted"] == expected else "FAIL"
        print(f"[{status}] '{seq}' -> {result['accepted']} (expected {expected})")
        if not result["accepted"] == expected:
            print(f"  Counts: {result['counts']}")
