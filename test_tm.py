"""
GenoCheck — Stage 3 (Turing Machine) Test Cases
TECH315 — Models of Computation
"""

import tm

STOP_CODONS = {"TAA", "TAG", "TGA"}

TEST_CASES = [
    # (id, input, expected_accept, category, reasoning)
    (1, "ATGCGATAA",              True,  "happy_path",         "start=ATG, mid=CGA, stop=TAA, G=2, C=2"),
    (2, "GGCATGTAA",              False, "boundary",           "no start codon at position 0"),
    (3, "ATGGGCGGG",              False, "boundary",           "valid start, no in-frame stop codon before end"),
    (4, "ATGTAAGGC",              False, "boundary",           "len 10, not a multiple of 3 -- frame itself broken"),
    (5, "ATGATATAA",              False, "hierarchy_proving",  "valid start/stop, but count(G)=1 != count(C)=0"),
    (6, "ATGTAG",                 True,  "boundary",           "minimal valid: start=ATG, stop=TAG, G=0, C=0"),
]


def run_all():
    print("\n" + "="*80)
    print("STAGE 3 (TURING MACHINE) TEST SUITE")
    print("="*80 + "\n")
    
    passed = 0
    for case_id, seq, expected, category, reasoning in TEST_CASES:
        result = tm.validate(seq)
        ok = result["accepted"] == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] Case {case_id} ({category}): input='{seq}'")
        print(f"        expected={expected}, got={result['accepted']}  -- {reasoning}")
        print(f"        G={result['counts']['G']}, C={result['counts']['C']}")
        if not ok:
            for line in result["trace"][:4]:
                print(f"          {line}")
        print()
    
    print(f"\n{'='*80}")
    print(f"RESULT: {passed}/{len(TEST_CASES)} passed")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    run_all()
