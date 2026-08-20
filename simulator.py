#!/usr/bin/env python3
"""
GenoCheck — Interactive CLI Simulator
TECH315 — Models of Computation

A beautiful, interactive terminal-based simulator demonstrating
the three stages of DNA sequence validation through the Chomsky hierarchy.

Usage:
    python simulator.py

The simulator will prompt for DNA sequences and display:
- Stage 1: DFA with state diagram and current state highlighting
- Stage 2: PDA with live stack visualization
- Stage 3: Turing Machine with individual tape cells and head position
"""

import sys
import time
from typing import List, Dict, Any
import dfa
import pda
import tm

# Color codes for terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[46m'
    
    @staticmethod
    def success(text):
        return f"{Colors.GREEN}✓ {text}{Colors.RESET}"
    
    @staticmethod
    def error(text):
        return f"{Colors.RED}✗ {text}{Colors.RESET}"
    
    @staticmethod
    def info(text):
        return f"{Colors.CYAN}ℹ {text}{Colors.RESET}"
    
    @staticmethod
    def stage_header(stage_num, name, model):
        return f"{Colors.BOLD}{Colors.YELLOW}{'='*80}{Colors.RESET}\n{Colors.BOLD}{Colors.BLUE}STAGE {stage_num}: {name}{Colors.RESET} ({Colors.MAGENTA}{model}{Colors.RESET})\n{Colors.BOLD}{Colors.YELLOW}{'='*80}{Colors.RESET}"


def print_separator(char="-", length=80):
    """Print a separator line."""
    print(f"{Colors.DIM}{char * length}{Colors.RESET}")


def print_dfa_diagram(current_state: str, sequence: str, states_at_step: List[str] = None):
    """
    Display a simplified DFA state diagram with current state highlighted.
    
    The DFA for Stage 1 has states: q0, q1, q2 (tracking length mod 3)
    All transitions accept A, T, C, G
    """
    print(f"\n{Colors.BOLD}DFA State Diagram:{Colors.RESET}")
    print()
    
    # Simplified diagram
    diagram = """
                  A,T,C,G          A,T,C,G          A,T,C,G
              q0 ---------> q1 ---------> q2 ---------> q0
             [START]        |             |          [ACCEPT]
              EVEN           ODD+1         ODD+2
           (len%3=0)      (len%3=1)      (len%3=2)
    """
    print(diagram)
    
    # Highlight current state
    if current_state == "q0":
        highlight = f"Current state: {Colors.BG_GREEN}{Colors.BOLD} q0 (ACCEPTING) {Colors.RESET}"
    elif current_state == "q1":
        highlight = f"Current state: {Colors.BG_YELLOW}{Colors.BOLD} q1 (ODD+1) {Colors.RESET}"
    elif current_state == "q2":
        highlight = f"Current state: {Colors.BG_YELLOW}{Colors.BOLD} q2 (ODD+2) {Colors.RESET}"
    else:
        highlight = f"Current state: {Colors.BG_RED}{Colors.BOLD} {current_state} (REJECT) {Colors.RESET}"
    
    print(highlight)
    print()


def print_pda_stack_visualization(stack_operations: List[Dict], current_step: int = None):
    """
    Display a detailed visualization of PDA stack operations.
    """
    print(f"\n{Colors.BOLD}PDA Stack Visualization:{Colors.RESET}")
    print()
    
    if not stack_operations:
        print(f"  {Colors.DIM}[No stack operations]{Colors.RESET}")
        return
    
    # Show stack at each step
    for i, op in enumerate(stack_operations):
        stack = op.get('stack', [])
        operation = op.get('operation', '')
        value = op.get('value', '')
        
        # Determine if this is the current step
        is_current = (current_step == i) if current_step is not None else False
        
        # Visual stack representation
        if not stack:
            stack_vis = "[empty]"
        else:
            stack_vis = f"[{' | '.join(stack)}]"
        
        if operation == "push":
            op_symbol = f"{Colors.GREEN}↑ PUSH{Colors.RESET}"
        else:
            matched = op.get('matched_with', '')
            op_symbol = f"{Colors.RED}↓ POP{Colors.RESET} (matched {value}↔{matched})"
        
        current_marker = f"{Colors.BG_CYAN}{Colors.BOLD} CURRENT {Colors.RESET} " if is_current else ""
        print(f"  Step {i+1:2d}: {op_symbol} {value:5s}  →  {stack_vis:20s} {current_marker}")
    
    print()


def print_tm_tape_visualization(sequence: str, tape_history: List[Dict] = None, current_step: int = None):
    """
    Display a Turing Machine tape with individual cells and head position.
    """
    print(f"\n{Colors.BOLD}Turing Machine Tape Visualization:{Colors.RESET}")
    print()
    
    # Show tape cells
    tape = list(sequence)
    n = len(sequence)
    
    # Display tape cells
    print("  Tape: ", end="")
    for i, base in enumerate(tape):
        if tape_history and current_step is not None:
            # Check if this position is relevant to current step
            current_history = tape_history[min(current_step, len(tape_history)-1)]
            if current_history['position'] == i:
                print(f"{Colors.BG_CYAN}{Colors.BOLD}[ {base} ]{Colors.RESET}", end="")
            else:
                print(f"[ {base} ]", end="")
        else:
            print(f"[ {base} ]", end="")
    
    # Add blank cells
    print(f"[ {Colors.DIM}□{Colors.RESET} ][ {Colors.DIM}□{Colors.RESET} ][ {Colors.DIM}□{Colors.RESET} ]", end="")
    print()
    
    # Display head position
    print("  Head: ", end="")
    for i in range(n):
        if tape_history and current_step is not None:
            current_history = tape_history[min(current_step, len(tape_history)-1)]
            if current_history['position'] == i:
                print(f"  ↑   ", end="")
            else:
                print(f"      ", end="")
        else:
            print(f"      ", end="")
    print()
    print()


def display_dfa_stage(sequence: str):
    """
    Display and execute Stage 1: DFA validation.
    """
    print(f"\n{Colors.stage_header(1, 'DFA — Regular Language', 'Deterministic Finite Automaton')}\n")
    
    result = dfa.validate(sequence)
    
    print(f"Input sequence: {Colors.BOLD}{sequence}{Colors.RESET} (length: {len(sequence)})")
    print()
    
    # Show DFA diagram
    print_dfa_diagram(result['final_state'], sequence, result['current_state_at_step'])
    
    # Show trace with step-by-step state progression
    print(f"{Colors.BOLD}Trace:{Colors.RESET}")
    print_separator("-")
    
    for i, trace_line in enumerate(result['trace']):
        print(f"  {trace_line}")
        if i < len(result['trace']) - 2:
            time.sleep(0.1)  # Slight delay for readability
    
    print_separator("-")
    print()
    
    # Result
    if result['accepted']:
        print(Colors.success(f"ACCEPTED: Sequence passes Stage 1 (DFA)\n  ✓ Valid alphabet (A,T,C,G only)\n  ✓ Length is a multiple of 3"))
    else:
        print(Colors.error(f"REJECTED: Sequence fails Stage 1 (DFA)\n  ✗ Invalid alphabet OR length not a multiple of 3"))
    
    print()
    return result['accepted']


def display_pda_stage(sequence: str):
    """
    Display and execute Stage 2: PDA validation.
    """
    print(f"\n{Colors.stage_header(2, 'PDA — Context-Free Language', 'Pushdown Automaton with Stack')}\n")
    
    result = pda.validate(sequence)
    
    print(f"Input sequence: {Colors.BOLD}{sequence}{Colors.RESET} (length: {len(sequence)})")
    print()
    
    # Show PDA stack operations
    print_pda_stack_visualization(result['stack_operations'])
    
    # Show trace
    print(f"{Colors.BOLD}Trace:{Colors.RESET}")
    print_separator("-")
    
    for trace_line in result['trace']:
        print(f"  {trace_line}")
        time.sleep(0.1)
    
    print_separator("-")
    print()
    
    # Result with structure details
    if result['accepted']:
        print(Colors.success(f"ACCEPTED: Sequence passes Stage 2 (PDA)"))
        print(f"  ✓ Hairpin structure found:")
        print(f"    - Stem 1 (left):  {Colors.CYAN}{result['stem1']}{Colors.RESET}")
        print(f"    - Loop (middle):  {Colors.YELLOW}{result['loop']}{Colors.RESET}")
        print(f"    - Stem 2 (right): {Colors.CYAN}{result['stem2']}{Colors.RESET}")
        print(f"    - Stem 2 = reverse complement of Stem 1: {Colors.GREEN}✓{Colors.RESET}")
    else:
        print(Colors.error(f"REJECTED: Sequence fails Stage 2 (PDA)"))
        print(f"  ✗ No valid hairpin structure spanning entire sequence")
    
    print()
    return result['accepted']


def display_tm_stage(sequence: str):
    """
    Display and execute Stage 3: Turing Machine validation.
    """
    print(f"\n{Colors.stage_header(3, 'Turing Machine — Decidable Language', 'Turing Machine with Read/Write Head')}\n")
    
    result = tm.validate(sequence)
    
    print(f"Input sequence: {Colors.BOLD}{sequence}{Colors.RESET} (length: {len(sequence)})")
    print()
    
    # Show tape visualization
    print_tm_tape_visualization(sequence, result['tape_history'])
    
    # Show validation passes
    print(f"{Colors.BOLD}Validation Passes:{Colors.RESET}")
    print_separator("-")
    
    for pass_desc in result['passes']:
        if "PASSED" in pass_desc:
            print(f"  {Colors.success(pass_desc)}")
        elif "FAILED" in pass_desc:
            print(f"  {Colors.error(pass_desc)}")
        else:
            print(f"  {pass_desc}")
        time.sleep(0.15)
    
    print_separator("-")
    print()
    
    # Show trace
    print(f"{Colors.BOLD}Tape Head Movement Trace:{Colors.RESET}")
    print_separator("-")
    
    for i, trace_line in enumerate(result['trace']):
        if i < 5 or "PASS" in trace_line or "REJECT" in trace_line or "ACCEPT" in trace_line:
            print(f"  {trace_line}")
        elif i == 5:
            print(f"  {Colors.DIM}... (detailed trace omitted for brevity) ...{Colors.RESET}")
    
    print_separator("-")
    print()
    
    # Result with detailed validation info
    if result['accepted']:
        print(Colors.success(f"ACCEPTED: Sequence passes Stage 3 (TM)"))
        print(f"  ✓ Valid start codon (ATG) at position 0")
        print(f"  ✓ Valid stop codon at sequence terminus")
        print(f"  ✓ Base-count constraint satisfied:")
        print(f"    - Count(G) = {result['counts']['G']}")
        print(f"    - Count(C) = {result['counts']['C']}")
        print(f"    - Equal: {Colors.GREEN}✓{Colors.RESET}")
    else:
        print(Colors.error(f"REJECTED: Sequence fails Stage 3 (TM)"))
        print(f"  ✗ One or more validation criteria failed")
        print(f"  Base counts: G={result['counts']['G']}, C={result['counts']['C']}")
    
    print()
    return result['accepted']


def display_final_result(sequence: str, stage1_pass: bool, stage2_pass: bool, stage3_pass: bool):
    """
    Display final overall result.
    """
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}OVERALL VALIDATION RESULT{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*80}{Colors.RESET}\n")
    
    print(f"Sequence: {Colors.BOLD}{sequence}{Colors.RESET}\n")
    
    # Summary table
    stages = [
        ("Stage 1", "DFA (Regular Language)", stage1_pass),
        ("Stage 2", "PDA (Context-Free Language)", stage2_pass),
        ("Stage 3", "TM (Decidable Language)", stage3_pass),
    ]
    
    print(f"{Colors.BOLD}Stage Results:{Colors.RESET}")
    print_separator("-")
    
    for stage, model, passed in stages:
        status = Colors.success("PASS") if passed else Colors.error("FAIL")
        print(f"  {stage:8s} | {model:35s} | {status}")
    
    print_separator("-")
    print()
    
    # Overall status
    overall_pass = stage1_pass and stage2_pass and stage3_pass
    
    if overall_pass:
        print(f"{Colors.BG_GREEN}{Colors.BOLD}{Colors.WHITE} ✓✓✓ FULL ACCEPTANCE ✓✓✓ {Colors.RESET}")
        print()
        print(f"{Colors.GREEN}{Colors.BOLD}The sequence successfully passes through all three stages of the Chomsky hierarchy!{Colors.RESET}")
    else:
        print(f"{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE} ✗ REJECTION ✗ {Colors.RESET}")
        print()
        if not stage1_pass:
            print(f"{Colors.YELLOW}Sequence rejected at Stage 1 (DFA).{Colors.RESET}")
            print(f"  Reason: Invalid alphabet or length not a multiple of 3.")
        elif not stage2_pass:
            print(f"{Colors.YELLOW}Sequence rejected at Stage 2 (PDA).{Colors.RESET}")
            print(f"  Reason: No valid hairpin structure found.")
        else:
            print(f"{Colors.YELLOW}Sequence rejected at Stage 3 (TM).{Colors.RESET}")
            print(f"  Reason: Start/stop codon or base-count constraint failed.")
    
    print()
    print_separator("=")
    print()


def print_welcome():
    """
    Print welcome message and instructions.
    """
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}╔{'='*78}╗{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║  {Colors.YELLOW}GenoCheck: DNA Sequence Validator{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║  {Colors.MAGENTA}Mapping Validation Complexity to the Chomsky Hierarchy{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║  {Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║  Team: Rajesh & Abhinav | TECH315 — Models of Computation{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚{'='*78}╝{Colors.RESET}")
    print()
    print(f"{Colors.BOLD}How it works:{Colors.RESET}")
    print(f"  1. {Colors.MAGENTA}Stage 1 (DFA){Colors.RESET}: Regular language — validates alphabet and length mod 3")
    print(f"  2. {Colors.MAGENTA}Stage 2 (PDA){Colors.RESET}: Context-free language — checks for hairpin structure")
    print(f"  3. {Colors.MAGENTA}Stage 3 (TM){Colors.RESET}: Decidable language — validates codons and base counts")
    print()
    print(f"{Colors.BOLD}Example sequences:{Colors.RESET}")
    print(f"  • {Colors.CYAN}GAATTC{Colors.RESET}                  (6 bp, classic EcoRI palindrome)")
    print(f"  • {Colors.CYAN}GCATTTTGC{Colors.RESET}              (9 bp, stem='GCA', loop='TTT')")
    print(f"  • {Colors.CYAN}ATGCGATAA{Colors.RESET}              (9 bp, complete gene)")
    print(f"  • {Colors.CYAN}ATGCGATTAG{Colors.RESET}             (10 bp, invalid — not multiple of 3)")
    print()


def get_sequence_input() -> str:
    """
    Prompt user for a DNA sequence.
    """
    while True:
        try:
            seq = input(f"{Colors.BOLD}Enter DNA sequence (A,T,C,G) or 'quit' to exit: {Colors.RESET}").upper().strip()
            
            if seq.lower() == 'quit':
                return None
            
            if not seq:
                print(f"{Colors.error('Empty sequence. Please enter a valid DNA sequence.')}")
                continue
            
            # Validate characters
            if not all(c in 'ACTG' for c in seq):
                invalid_chars = set(seq) - set('ACTG')
                print(f"{Colors.error(f'Invalid characters: {invalid_chars}')}")
                continue
            
            return seq
        
        except KeyboardInterrupt:
            return None
        except Exception as e:
            print(f"{Colors.error(f'Error: {e}')}")


def main():
    """
    Main interactive simulator loop.
    """
    print_welcome()
    
    while True:
        # Get sequence from user
        sequence = get_sequence_input()
        if sequence is None:
            print(f"\n{Colors.BOLD}Thank you for using GenoCheck!{Colors.RESET}")
            print(f"{Colors.DIM}Questions? Check the project documentation or review the trace details above.{Colors.RESET}")
            break
        
        # Run all three stages
        print(f"\n{Colors.BOLD}{Colors.YELLOW}Processing: {Colors.CYAN}{sequence}{Colors.RESET}\n")
        time.sleep(0.5)
        
        stage1_pass = display_dfa_stage(sequence)
        
        if not stage1_pass:
            print(f"{Colors.YELLOW}Stopping after Stage 1: Sequence did not pass DFA validation.{Colors.RESET}")
            display_final_result(sequence, False, False, False)
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            continue
        
        time.sleep(0.5)
        stage2_pass = display_pda_stage(sequence)
        
        if not stage2_pass:
            print(f"{Colors.YELLOW}Stopping after Stage 2: Sequence did not pass PDA validation.{Colors.RESET}")
            display_final_result(sequence, True, False, False)
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            continue
        
        time.sleep(0.5)
        stage3_pass = display_tm_stage(sequence)
        
        # Display final result
        display_final_result(sequence, True, True, stage3_pass)
        
        input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.error(f'Unexpected error: {e}')}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
