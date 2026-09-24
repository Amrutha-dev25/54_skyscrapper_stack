# Skyscraper Stack Repair Lab

This project is a precision timing and balance tower stacking game using **Pygame**. It introduces students to 1D bounding-box intersection math, dynamic geometry slicing, vertical camera offset scrolling, and escalating difficulty curves within an object-oriented codebase.
---

## What's Provided

A working Skyscraper Stack game with:

- A foundation block positioned at the base of the arena
- Horizontally oscillating active blocks that bounce between screen boundaries at escalating speeds
- Precision placement triggered via `Space` key or left mouse click
- Automatic dynamic width trimming based on overlap alignment against the previous tier
- Downward camera scrolling when the stack exceeds the vertical threshold
- A Game Over collapse screen displaying total tower height with instant restart functionality

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Press Space or Left-Click to drop the active block. Press Space or R to restart after Game Over.


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the inverted overlap placement bug

Landing a block directly on top of the tower results in an immediate game over, whereas dropping a block completely off into thin air allows the tower to build upward. In game_engine.drop_block(), the placement check evaluates is_successful_drop = overlap <= 0. A positive overlap represents a successful collision, while an overlap of zero or less means the block completely missed the tower beneath it. Invert this condition so that overlap > 0 registers as a valid placement and overlap <= 0 triggers the tower collapse.

### Task 2: Implement "Perfect Placement" bonus & width restoration

Currently, any overlap trims the active block to the exact overlapping width. In game_engine.drop_block(), implement a precision reward: if the alignment error between the active block and the top stack block is within a tiny margin (e.g., abs(act.x - top_block.x) <= 3), snap the block directly into alignment without trimming its width, display a golden "PERFECT!" popup label, and reward extra bonus score points. If the player lands 3 perfect placements in a row, slightly expand the block width back outward.
 
### Task 3: Implement falling off-cut debris animation

When a block is trimmed, the overhang portion simply disappears from the scene instantly. Create an off-cut debris object representing the sliced-off excess rectangle that retains gravity velocity, rotating and falling off the screen to give satisfying visual weight to block trims.

### Task 4: Implement combo streak background color shifting

The background currently stays a flat dark grey throughout the entire climb. Enhance game_engine.render() so the sky background gradually transitions through atmospheric gradients (e.g., twilight blue, dusk purple, night starfield, stratosphere black) as the player stacks the skyscraper higher and higher into the sky.
---

## Expected Behavior

- Dropping a block while aligned over the stack trims the edges, places the block, and increases the tower height score.
- Dropping a block outside the stack triggers the TOWER COLLAPSED! game over screen.
- As the stack grows taller, the camera smoothly scrolls downward so the top of the tower remains visible.
- Pressing Space or R on the collapse screen resets the tower and restores base dimensions.

## Folder Structure

```
word_scramble/
├── game/
│   ├── game_engine.py
│   └── text_box.py
├── main.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
