"""
Minimal Consciousness Simulator
A simple demonstration of the four-stage cognitive model.
"""

import numpy as np
import random
import time

class MinimalConsciousnessSimulator:
    def __init__(self):
        self.stage = "UNKNOWN"
        self.traces = []
        self.understanding_modules = []
        self.time_step = 0
        
    def run_demo(self, steps=50):
        print("Starting Minimal Consciousness Simulator")
        print("This system will go through the four stages: Unknown, Chaos, Inverted, Unified.")
        print("-" * 60)
        
        for i in range(steps):
            self.time_step += 1
            self._update_stage()
            self._process_experience()
            
            if i % 10 == 0:
                print(f"Step {i}: Stage = {self.stage}")
                
        print("-" * 60)
        print("Simulation complete.")
        print(f"Final stage: {self.stage}")
        print(f"Total traces: {len(self.traces)}")
        
    def _update_stage(self):
        # Simulate stage transitions based on traces and randomness
        if len(self.traces) < 5:
            self.stage = "UNKNOWN"
        elif len(self.traces) < 15:
            # Randomly choose between Chaos and Inverted
            if random.random() < 0.7:
                self.stage = "CHAOS"
            else:
                self.stage = "INVERTED"
        else:
            # Eventually reach Unified
            self.stage = "UNIFIED"
            
    def _process_experience(self):
        # Simulate having an experience
        experience = {
            'id': self.time_step,
            'content': f"Experience {self.time_step}",
            'significance': random.random()
        }
        
        # Create a trace
        trace = {
            'experience': experience,
            'stage': self.stage,
            'interpretation': self._interpret_experience(experience)
        }
        
        self.traces.append(trace)
        
        # Occasionally create an understanding module
        if random.random() < 0.2:
            module = {
                'id': len(self.understanding_modules),
                'pattern': f"Pattern from experiences {max(0, self.time_step-3)}-{self.time_step}",
                'strength': random.random()
            }
            self.understanding_modules.append(module)
            
    def _interpret_experience(self, experience):
        # Simulate interpretation based on stage
        if self.stage == "UNKNOWN":
            return "I don't understand."
        elif self.stage == "CHAOS":
            interpretations = ["Maybe this means X.", "Could be Y.", "Perhaps Z."]
            return random.choice(interpretations)
        elif self.stage == "INVERTED":
            return "This clearly means A."
        else:  # UNIFIED
            return "This fits with my understanding of B."

if __name__ == "__main__":
    sim = MinimalConsciousnessSimulator()
    sim.run_demo()
