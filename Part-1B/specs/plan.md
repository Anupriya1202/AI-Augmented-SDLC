# Technical Plan

Define a provider interface returning structured JSON, isolate parsing from evaluation, and keep the evaluator independent of the provider. The offline fixture provider supplies outputs for reproducible harness testing. The single evaluation runner validates schema, invariants, and case-specific semantic expectations, then applies the predeclared conjunctive threshold and writes JSON evidence.
