"""
GenoCheck — Stage 1 (DFA) Test Cases
TECH315 — Models of Computation
"""

import dfa

TEST_CASES = [
    # (id, input, expected_accept, category, reasoning)
    (1,  "ATG",                 True,  "happy_path",         "len 3, valid alphabet"),
    (2,  "ATGCAT",              True,  "happy_path",         "len 6, two codons"),
    (3,  "AT",                  False, "boundary",           "len 2, 2 mod 3 != 0"),
    (4,  "ATGC",                False, "boundary",           "len 4, 1 mod 3 != 0"),
    (5,  "ATX",                 False, "alphabet",           "X not in sigma"),
    (6,  "ATGNTAG",             False, "alphabet",           "invalid symbol mid-string"),
    (7,  "",                    True,  "edge_case",          "POLICY: 0 mod 3 == 0; empty string accepted"),
    (8,  "atgcat",              False, "edge_case",          "lowercase; case-sensitive alphabet"),
    (9,  "ACGT" * 75,           True,  "hierarchy_proving",  "300bp, constant state count"),
    (10, "AAAAAAAAAA",          False, "boundary",           "len 10, 10 mod 3 = 1"),
]


def run_all():
    print("\n" + "="*80)
    print("STAGE 1 (DFA) TEST SUITE")
    print("="*80 + "\n")
    
    passed = 0
    for case_id, seq, expected, category, reasoning in TEST_CASES:
        result = dfa.validate(seq)
        ok = result["accepted"] == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        display_seq = seq if len(seq) <= 40 else f"{seq[:20]}...{seq[-10:]} (len={len(seq)})"
        print(f"[{status}] Case {case_id} ({category}): input='{display_seq}'")
        print(f"        expected={expected}, got={result['accepted']}  -- {reasoning}")
        if not ok or category == "hierarchy_proving":
            for i, line in enumerate(result["trace"]):
                if i < 3 or i >= len(result["trace"]) - 2:
                    print(f"          {line}")
                elif i == 3:
                    print(f"          ... (trace omitted) ...")
        print()
    
    print(f"\n{'='*80}")
    print(f"RESULT: {passed}/{len(TEST_CASES)} passed")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    run_all()
