"""
GenoCheck — Stage 2 (PDA) Test Cases
TECH315 — Models of Computation
"""

import pda

def revcomp(s):
    """Helper: reverse complement."""
    complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(complement[c] for c in reversed(s))


def make_hairpin(stem_len, loop="TTT"):
    """Programmatically build a valid hairpin."""
    import random
    random.seed(stem_len)  # deterministic
    stem1 = "".join(random.choice("ACGT") for _ in range(stem_len))
    return stem1 + loop + revcomp(stem1)


TEST_CASES = [
    # (id, input, expected_accept, category, reasoning)
    (1, "GAATTC",             True,  "happy_path",        "classic palindrome (EcoRI site); loop length 0"),
    (2, "GCATTTTGC",          True,  "happy_path",         "stem='GCA', loop='TTT', stem2=revcomp(stem); loop length 3"),
    (3, "GAATTG",             False, "boundary",           "one symbol off from case 1 -- exact match required"),
    (4, "AAAAAAAAAA",         False, "happy_path_negative","no valid split; revcomp('A')='T' never matches 'A'"),
    (5, "A",                  False, "edge_case",          "too short for any stem/stem2 pairing"),
    (6, "AT",                 True,  "edge_case",          "smallest possible palindrome, loop length 0"),
]


def hierarchy_proving_cases():
    """Scale stem length to prove PDA with fixed states, unbounded stack depth."""
    cases = []
    for stem_len in (5, 10, 20):
        valid = make_hairpin(stem_len)
        cases.append((f"7-scale-{stem_len}", valid, True,
                       f"valid hairpin, stem_len={stem_len}"))
        # Flip last symbol
        flipped = valid[:-1] + ("A" if valid[-1] != "A" else "T")
        cases.append((f"8-flip-{stem_len}", flipped, False,
                       f"same hairpin, last symbol flipped, stem_len={stem_len}"))
    return cases


def run_all():
    print("\n" + "="*80)
    print("STAGE 2 (PDA) TEST SUITE")
    print("="*80 + "\n")
    
    passed, total = 0, 0
    for case_id, seq, expected, category, reasoning in TEST_CASES:
        total += 1
        result = pda.validate(seq)
        ok = result["accepted"] == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] Case {case_id} ({category}): input='{seq}'")
        print(f"        expected={expected}, got={result['accepted']}  -- {reasoning}")
        if not ok:
            for line in result["trace"][:3]:
                print(f"          {line}")
        print()

    print("\n" + "-"*80)
    print("Hierarchy-proving: scaling stem length")
    print("-"*80 + "\n")
    
    for case_id, seq, expected, reasoning in hierarchy_proving_cases():
        total += 1
        result = pda.validate(seq)
        ok = result["accepted"] == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] Case {case_id}: len={len(seq):3d}  expected={expected}, got={result['accepted']}  -- {reasoning}")
    
    print(f"\n{'='*80}")
    print(f"RESULT: {passed}/{total} passed")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    run_all()
