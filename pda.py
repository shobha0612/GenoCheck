"""
GenoCheck — Stage 2 (PDA) Implementation
TECH315 — Models of Computation

Validates DNA sequences for reverse-complement hairpin (stem-loop) structure.
A hairpin must span the ENTIRE sequence:
  - First half: stem1
  - Second half: stem2 = reverse_complement(stem1)
  - Loop length: 0 (pure palindrome)

Example: "GAATTC" has stem1="GA", loop="", stem2="TC" (revcomp of "GA")

Formal Definition: PDA uses a stack to match stem1 against revcomp(stem2)
- Push: read first half of sequence
- Pop: read second half and compare with stack top
"""

def complement(base: str) -> str:
    """Return the Watson-Crick complement of a DNA base."""
    comp = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return comp.get(base, None)


def reverse_complement(seq: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    if not all(c in 'ACGT' for c in seq):
        return None
    return ''.join(complement(c) for c in reversed(seq))


def validate(sequence: str) -> dict:
    """
    Validates a DNA sequence for hairpin structure using a PDA.
    
    The hairpin must span the ENTIRE sequence:
    - stem1 (first part) must be the reverse complement of stem2 (last part)
    - The middle section (if any) is the loop
    - For a pure palindrome (loop length 0), stem1 directly matches revcomp(stem2)
    
    Args:
        sequence: DNA string
    
    Returns:
        {
            "accepted": bool,
            "trace": list[str],
            "stack_operations": list[dict],  # {"operation": "push"|"pop", "value": char, "stack": [...]}
            "stem1": str or None,
            "stem2": str or None,
            "loop": str or None,
            "final_stack": list[str]
        }
    """
    
    trace = []
    stack_operations = []
    n = len(sequence)
    
    trace.append(f"[PDA] Start state. Input: '{sequence}' (length {n})")
    trace.append(f"[PDA] Attempting to find hairpin spanning entire sequence...")
    
    # Try all possible stem lengths (nondeterministic guess of midpoint)
    # Hairpin spans entire sequence, so:
    # stem1 = sequence[0:stem_len]
    # loop = sequence[stem_len:n-stem_len]
    # stem2 = sequence[n-stem_len:n]
    
    for stem_len in range(1, n // 2 + 1):
        stem1 = sequence[:stem_len]
        loop = sequence[stem_len:n - stem_len]
        stem2 = sequence[n - stem_len:]
        
        # Check if stem2 is reverse complement of stem1
        expected_stem2 = reverse_complement(stem1)
        
        if expected_stem2 and stem2 == expected_stem2:
            # Found valid hairpin!
            trace.append(f"[PDA] Guessed midpoint: stem_len={stem_len}")
            trace.append(f"[PDA] stem1='{stem1}', loop='{loop}', stem2='{stem2}'")
            trace.append(f"[PDA] stem2 == reverse_complement(stem1) ✓")
            
            # Simulate stack operations for trace
            trace.append(f"[PDA] PUSH phase: processing stem1='{stem1}'")
            stack = []
            for i, c in enumerate(stem1):
                stack.append(c)
                stack_operations.append({
                    "operation": "push",
                    "value": c,
                    "stack": stack.copy()
                })
                trace.append(f"[PDA] PUSH '{c}' | stack={stack}")
            
            trace.append(f"[PDA] LOOP phase: skipping loop='{loop}'")
            
            trace.append(f"[PDA] POP phase: processing stem2='{stem2}'")
            for i, c in enumerate(stem2):
                if not stack:
                    trace.append(f"[PDA] ERROR: stack empty when trying to pop for '{c}'")
                    return {
                        "accepted": False,
                        "trace": trace,
                        "stack_operations": stack_operations,
                        "stem1": None,
                        "stem2": None,
                        "loop": None,
                        "final_stack": stack
                    }
                
                popped = stack.pop()
                expected_popped = complement(c)  # stem2[i] should match complement of stem1[n-1-i]
                
                if popped == expected_popped:
                    stack_operations.append({
                        "operation": "pop",
                        "value": popped,
                        "matched_with": c,
                        "stack": stack.copy()
                    })
                    trace.append(f"[PDA] POP '{popped}' (matches complement of '{c}') | stack={stack}")
                else:
                    trace.append(f"[PDA] ERROR: popped '{popped}', expected '{expected_popped}' (complement of '{c}')")
                    return {
                        "accepted": False,
                        "trace": trace,
                        "stack_operations": stack_operations,
                        "stem1": None,
                        "stem2": None,
                        "loop": None,
                        "final_stack": stack
                    }
            
            if not stack:
                trace.append(f"[ACCEPT] Stack empty after processing - valid hairpin found!")
                return {
                    "accepted": True,
                    "trace": trace,
                    "stack_operations": stack_operations,
                    "stem1": stem1,
                    "stem2": stem2,
                    "loop": loop,
                    "final_stack": stack
                }
            else:
                trace.append(f"[PDA] Stack not empty at end: {stack} - continuing search")
    
    trace.append(f"[REJECT] No valid hairpin spanning entire sequence found")
    return {
        "accepted": False,
        "trace": trace,
        "stack_operations": stack_operations,
        "stem1": None,
        "stem2": None,
        "loop": None,
        "final_stack": []
    }


if __name__ == "__main__":
    test_cases = [
        ("GAATTC", True),          # Classic palindrome
        ("GCATTTTGC", True),       # stem='GCA', loop='TTT'
        ("AT", True),              # Smallest palindrome
        ("AAAAAAAAAA", False),     # No valid split
        ("GAATTG", False),         # Almost palindrome
    ]
    
    for seq, expected in test_cases:
        result = validate(seq)
        status = "PASS" if result["accepted"] == expected else "FAIL"
        print(f"[{status}] '{seq}' -> {result['accepted']} (expected {expected})")
