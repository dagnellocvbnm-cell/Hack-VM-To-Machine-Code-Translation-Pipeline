# Hack VM → Machine Code Translation Pipeline

This repository implements an end-to-end translation pipeline that converts
high-level VM code into executable Hack machine code.

The system is structured as two translation stages:
VM code → Hack assembly → Hack binary.

---

## What This Project Does

- Translates stack-based VM instructions into Hack assembly language
- Assembles Hack assembly into 16-bit Hack machine code
- Produces executable binaries compatible with the Hack CPU

---

## Pipeline Overview

