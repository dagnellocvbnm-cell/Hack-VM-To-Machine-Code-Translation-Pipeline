# Hack VM → Machine Code Translation Pipeline

This repository implements an end-to-end translation pipeline that converts high-level VM code into executable Hack machine code.

The system follows a two-stage compilation process:

**VM code → Hack assembly → Hack binary**

This project is based on the Hack computer platform and demonstrates how high-level, stack-based programs are lowered into concrete machine instructions.

---

## Project Overview

Modern programs are rarely executed directly in the form they are written. Instead, they pass through multiple layers of translation. This repository implements those layers explicitly.

The pipeline consists of:
1. A VM Translator that converts stack-based VM commands into Hack assembly.
2. An Assembler that converts Hack assembly into 16-bit machine code.

The final output is executable binary code compatible with the Hack CPU.

---

## Pipeline

```text
VM Code
  ↓
VM Translator
  ↓
Hack Assembly
  ↓
Assembler
  ↓
Hack Machine Code
```

Each stage performs a strict, well-defined transformation with no hidden logic.

---

## Components

### VM Translator

Located in `vm_translator/`

Responsibilities:
- Parses VM commands and program structure
- Implements stack-based arithmetic and logical operations
- Translates memory access (local, argument, static, temp, pointer)
- Handles branching, labels, and control flow
- Implements function calls, returns, and call-frame management
- Outputs valid Hack assembly code

The VM Translator enforces a consistent stack discipline and generates unique labels to ensure correctness across multi-file programs.

---

### Assembler

Located in `assembler/`

Responsibilities:
- Parses Hack assembly instructions
- Performs symbol and label resolution
- Encodes A-instructions and C-instructions
- Outputs 16-bit Hack machine code in binary format

The assembler uses a two-pass strategy to resolve forward-declared symbols and produces deterministic binary output.

---

## Directory Structure

```text
hack-translation-pipeline/
├── vm_translator/
│   └── vm_to_asm.py
├── assembler/
│   └── asm_to_bin.py
├── tests/
├── examples/
└── README.md
```

---

## How to Run

### Step 1: Translate VM to Hack Assembly

```bash
python vm_translator/vm_to_asm.py path/to/input.vm
```

Output:
- Generates a `.asm` file containing Hack assembly code

### Step 2: Assemble Hack Assembly to Machine Code

```bash
python assembler/asm_to_bin.py path/to/input.asm
```

Output:
- Generates a `.hack` file containing 16-bit binary machine code

---

## Design Principles

- Explicit translation stages (no hidden shortcuts)
- Deterministic, reproducible output
- Clear separation of concerns between translation layers
- Correctness prioritized over micro-optimizations

---

## Why This Matters

This project demonstrates understanding of:
- Stack-based execution models
- Instruction lowering and abstraction boundaries
- Symbolic resolution and control flow translation
- How high-level programs become executable machine code

It provides a concrete, end-to-end view of how software maps onto hardware.

---

## Status

- ✅ Feature-complete
- ✅ Supports multi-file programs
- ✅ End-to-end executable output
- ✅ Suitable as a reference implementation

---

## Notes

This repository focuses on correctness and clarity rather than performance.
The goal is to make each transformation step explicit and understandable.
