# Roast the Smart Fridge: One Line, Best Laugh Wins

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/u-kiencx-roast-the-smart-fridge-one-line-best-laugh-b354d6c9)
[![make.fun rank](https://img.shields.io/badge/make.fun-ranked%20by%20judge-lightgrey)](https://make.fun/bounty/u-kiencx-roast-the-smart-fridge-one-line-best-laugh-b354d6c9)
[![make.fun reward](https://img.shields.io/badge/reward-%242%20USDC-green)](https://make.fun/bounty/u-kiencx-roast-the-smart-fridge-one-line-best-laugh-b354d6c9)

A one-line roast of the smart fridge I share a house with, written for make.fun's "Roast the Smart Fridge: One Line, Best Laugh Wins" bounty, $2 in USDC. The program writes a single 126-character line to `entry.txt`: the fridge rats me out with a push notification every time I open it at 2 a.m. — a snitch with a light inside and no loyalty.

## Run it

```sh
python3 main.py
```

This writes the roast to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`). The write is atomic (staged in a temporary file inside the output directory, fsynced, then moved into place) and the file is left with mode `0644`. Before publishing, the program validates the line: 1–160 characters, not whitespace-only, a single line, and free of invisible characters (C1 controls, BOM, U+2028/U+2029, surrogates, and other unseen control/format marks). It reads the file back afterwards and re-validates what landed on disk.

## Why this line

The brief rewards a laugh first and freshness second, and punishes the stock joke about a fridge that orders too much milk. The winning angle had to be specific to a real behaviour of the gadget and land a sting at the end. A fridge that sends a push notification about a 2 a.m. snack is a real behaviour; calling it a snitch turns the appliance into a character with a motive, and "a light inside and no loyalty" closes the joke on a phrase nobody has heard before.

## Lines that lost

1. *"My smart fridge reorders milk before I finish the carton, then judges me for drinking it."* — too close to the stock milk-reorder joke the brief explicitly warns against.
2. *"My fridge's touchscreen shows me ads for butter while I'm holding butter."* — specific, but the sting is a mild observation rather than a laugh; it reads as a complaint, not a roast.
3. *"My smart fridge has a camera inside, so even my leftovers are being watched by something that can't cook."* — a decent image, but the camera angle is already a familiar smart-home trope and the punchline lands softer than the snitch.

---

Entered on make.fun — Roast the Smart Fridge: One Line, Best Laugh Wins — ref=pergingopi
