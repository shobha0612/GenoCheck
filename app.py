#!/usr/bin/env python3
"""
GenoCheck — Complete Interactive Web Application
TECH315 — Models of Computation

A full-stack Flask web application with HTML/CSS/JavaScript frontend
and Python backend implementing DFA, PDA, and Turing Machine validators.

Usage:
    pip install flask flask-cors
    python app.py

Then open http://localhost:5000 in your browser.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys

# Import the three validation stages
import dfa
import pda
import tm

app = Flask(__name__)
CORS(app)

# Configure template folder
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    """Serve the main interactive simulator page."""
    return render_template('index.html')


@app.route('/api/validate', methods=['POST'])
def validate_sequence():
    """
    API Endpoint: POST /api/validate
    Input JSON: {"sequence": "ATGCGATAA"}
    Output JSON: Complete validation result with all three stages
    """
    try:
        data = request.get_json()
        sequence = data.get('sequence', '').upper().strip()
        
        if not sequence:
            return jsonify({"error": "Empty sequence"}), 400
        
        result = {
            "sequence": sequence,
            "length": len(sequence),
            "stages": {}
        }
        
        # Stage 1: DFA Validation
        dfa_result = dfa.validate(sequence)
        result["stages"]["stage1_dfa"] = {
            "name": "Stage 1: DFA (Regular Language)",
            "accepted": dfa_result["accepted"],
            "trace": dfa_result["trace"],
            "states_visited": dfa_result["states_visited"],
            "final_state": dfa_result["final_state"],
            "current_state_at_step": dfa_result["current_state_at_step"],
            "valid_alphabet": dfa_result.get("valid_alphabet", True),
            "final_rem": dfa_result.get("final_rem", 0)
        }
        
        # Stage 2: PDA Validation (only if Stage 1 passed)
        if dfa_result["accepted"]:
            pda_result = pda.validate(sequence)
            result["stages"]["stage2_pda"] = {
                "name": "Stage 2: PDA (Context-Free Language)",
                "accepted": pda_result["accepted"],
                "trace": pda_result["trace"],
                "stack_operations": pda_result["stack_operations"],
                "stem1": pda_result["stem1"],
                "stem2": pda_result["stem2"],
                "loop": pda_result["loop"],
                "final_stack": pda_result.get("final_stack", [])
            }
            
            # Stage 3: Turing Machine Validation (only if Stage 2 passed)
            if pda_result["accepted"]:
                tm_result = tm.validate(sequence)
                result["stages"]["stage3_tm"] = {
                    "name": "Stage 3: Turing Machine (Decidable Language)",
                    "accepted": tm_result["accepted"],
                    "trace": tm_result["trace"],
                    "tape_history": tm_result["tape_history"],
                    "passes": tm_result["passes"],
                    "counts": tm_result["counts"]
                }
            else:
                result["stages"]["stage3_tm"] = {
                    "name": "Stage 3: Turing Machine (Decidable Language)",
                    "accepted": False,
                    "trace": ["Skipped: Stage 2 (PDA) did not accept."],
                    "tape_history": [],
                    "passes": [],
                    "counts": {"G": 0, "C": 0}
                }
        else:
            result["stages"]["stage2_pda"] = {
                "name": "Stage 2: PDA (Context-Free Language)",
                "accepted": False,
                "trace": ["Skipped: Stage 1 (DFA) did not accept."],
                "stack_operations": [],
                "stem1": None,
                "stem2": None,
                "loop": None,
                "final_stack": []
            }
            result["stages"]["stage3_tm"] = {
                "name": "Stage 3: Turing Machine (Decidable Language)",
                "accepted": False,
                "trace": ["Skipped: Stage 1 (DFA) did not accept."],
                "tape_history": [],
                "passes": [],
                "counts": {"G": 0, "C": 0}
            }
        
        # Overall result
        result["overall_accepted"] = (
            result["stages"]["stage1_dfa"]["accepted"] and
            result["stages"]["stage2_pda"]["accepted"] and
            result["stages"]["stage3_tm"]["accepted"]
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\n" + "="*80)
    print("GenoCheck — Interactive DNA Sequence Validator")
    print("TECH315 — Models of Computation")
    print("="*80)
    print("\nFlask development server starting...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress CTRL+C to stop the server.\n")
    
    app.run(debug=True, port=5000, host='127.0.0.1')
