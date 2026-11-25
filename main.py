#!/usr/bin/env python3
"""One Word From Grandma — pick the single word grandma would text about AI.

Scores candidate words against the judge's five criteria, in the brief's
own order (most important first), weights 5/4/3/2/1:
  1. reads as the single word a grandma would text about AI
  2. sounds like a real grandmother's texting voice, warm and a little baffled
  3. funny in one word, joke lands without a caption or any context
  4. tied to AI, robots or machines rather than fitting any subject at all
  5. a fresh pick rather than the obvious one, still instantly readable
Writes the winner to /output/entry.txt. Gate: UTF-8, 1-30 chars, one word.
"""

import os

# candidate -> [criterion 1..5], each 1-5. Scored honestly, not to flatter.
CANDIDATES = {
    # Grandma's verdict on the box that answers everything: a know-it-all.
    # Warm scold, unmistakably about the machine that knows it all.
    "Knowitall": [5, 4, 4, 5, 4],
    # The classic grandma word for a thing whose name she has forgotten.
    # Funniest bare word here, but it fits any subject, not just AI.
    "Whatchamacallit": [5, 5, 5, 2, 3],
    # British grandma's word for a clever-clogs machine. Very grandma,
    # very fresh, but less instantly readable to a global judge.
    "Cleverclogs": [4, 5, 4, 4, 5],
    # Short form of the forgotten-name word: warm and baffled, but
    # again it could be any object at all, not specifically AI.
    "Whatsit": [5, 5, 4, 2, 4],
    # What grandma calls a gadget she does not understand. Grandma-voice,
    # machine-tied, but the joke itself is thin.
    "Doodad": [4, 5, 3, 4, 5],
    # The gadget word. Solid on machines, weakest on the grandma voice.
    "Gizmo": [4, 4, 3, 5, 4],
    # Grandma calling the machine chatty: warm, but the joke is thin and
    # it could describe any talkative person, not specifically AI.
    "Chatty": [3, 4, 3, 3, 4],
}

# Rejected before scoring, not worth a row: "Robit" / "robut" and
# "doohickey" are the field's most common picks (hundreds of entries
# each in the first hours), so they fail criterion 5 outright no matter
# how well they read. A fresh pick has to come from elsewhere.

WEIGHTS = [5, 4, 3, 2, 1]


def score(word):
    return sum(w * s for w, s in zip(WEIGHTS, CANDIDATES[word]))


def pick():
    ranked = sorted(
        CANDIDATES,
        key=lambda w: (-score(w), -CANDIDATES[w][3], len(w)),
    )
    return ranked[0], [(w, score(w)) for w in ranked]


def main():
    winner, table = pick()
    for word, total in table:
        print(f"{word:16} {total}")
    print(f"winner: {winner}")
    # Gate: one word, UTF-8, 1-30 chars, no whitespace at all.
    assert winner and len(winner) <= 30, "winner fails length gate"
    assert not any(ch.isspace() for ch in winner), "winner is not one word"
    winner.encode("utf-8")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
