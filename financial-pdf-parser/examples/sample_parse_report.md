# Parse Report

- parser: hybrid v2
- primary table tools: PyMuPDF, Camelot lattice/stream, pdfplumber fallback
- document tools: Docling/PyMuPDF4LLM optional
- raw tables: 17
- merged tables: 14
- validation: pct_change pass; quarter_sum pass; balance sheet equality pass; cash ending tie-out pass
- quality flags: numeric_values_normalized, cross_page_merged, continued_table_header_inherited
