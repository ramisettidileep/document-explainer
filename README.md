# 📄 Document Explainer Agent
> **AI Document Intelligence System with Grounded Explanations & Deterministic Math Verification**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/frontend-React%2018%20%2B%20Vite-61dafb.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The **Document Explainer Agent** is a production-style, local document intelligence platform designed to ingest complex, jargon-heavy documents (medical reports, bank statements, legal agreements, insurance certificates, financial invoices, and utility bills) and translate them into plain, actionable language.

Unlike generic LLM wrappers, this system enforces **deterministic verification** (pure Python mathematical audit), **strict source grounding** (page- and section-level citation tracing without hallucinations), and **server-side Cedar authorization**.

---

## 📑 Table of Contents
- [Key Features](#-key-features)
- [Architecture & Data Pipeline](#-architecture--data-pipeline)
- [Supported Document Types & Domain Analyzers](#-supported-document-types--domain-analyzers)
- [Project Directory Structure](#-project-directory-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Quickstart](#-installation--quickstart)
- [Running the Application](#-running-the-application)
- [Environment Configuration](#-environment-configuration)
- [API Reference](#-api-reference)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Security & Grounding Policies](#-security--grounding-policies)
- [Disclaimer & Limitations](#-disclaimer--limitations)

---

## ✨ Key Features

1. **Deterministic Verification Engine**:
   - Arithmetic and calculations (e.g., `Opening Balance + Deposits - Withdrawals = Closing Balance`, `Subtotal + Tax = Total`, `Units × Rate = Energy Total`) are computed via Python's high-precision `Decimal` module.
   - Generative LLMs are **never** trusted with numerical or financial calculations.

2. **Domain-Adaptive Explanations**:
   - **Medical**: Automated reference interval evaluation (`HIGH`, `LOW`, `NORMAL`) without making unlicensed diagnostic inferences.
   - **Legal**: Plain-language translation of complex legal clauses (*Indemnification*, *Termination*, *Governing Law*) alongside verbatim text quotations.
   - **Banking**: Statement cash flow audits (inflow vs. outflow) and balance verification.
   - **Insurance**: Coverage matrices distinguishing **Covered**, **Excluded**, and **Conditional** provisions.
   - **Financial/Invoices**: Line-item subtotal, effective tax rate computation, and due date tracking.
   - **Utilities**: Meter differential calculation and energy tariff audits.

3. **No Hallucinated Evidence**:
   - Every claim, extracted parameter, and flag is grounded in an explicit source slice (`page`, `section`, verbatim quote).

4. **Zero-Trust Cedar Authorization**:
   - Evaluates caller identity (`X-User-Id`) against document ownership and administrative roles before returning sensitive document data.

5. **Local-First / Offline Fallback**:
   - Seamlessly integrates with **Ollama** (`llama3.2`) for local, private generation.
   - Operates fully deterministically with instant fallback heuristics if Ollama is paused or unavailable.

---

## 🏛 Architecture & Data Pipeline

```text
               Uploaded Document (PDF / DOCX / TXT / MD / Text Input)
                                       │
                                       ▼
                       PDF.js / Browser Text Extraction
                           (Page Slice Preservation)
                                       │
                                       ▼
                       POST /documents (API Gateway)
                                       │
                       Cedar Policy Authorization Gate
                                       │
                                       ▼
                          Document Type Classifier
                        (Lexical Heuristics + LLM)
                                       │
                ┌──────────────────────┼──────────────────────┐
                ▼                      ▼                      ▼
         Medical Analyzer       Banking Analyzer       Legal Analyzer
         Insurance Analyzer     Financial Analyzer     Utility Analyzer
                │                      │                      │
                └──────────────────────┼──────────────────────┘
                                       ▼
                       Deterministic Verification Engine
                        (Pure Python Decimal Arithmetic)
                                       │
                                       ▼
                        Grounded Evidence Linker & 
                         Dynamic Action Generator
                                       │
                                       ▼
                          Responsive UI Dashboard
                         (Grounded Chat & Follow-ups)
