"""
Keystone Legal Data — US Statutory & Citation Graph Sample Showcase Quickstart
Website & Full 57-Jurisdiction Catalog: https://keystonelegaldata.com
"""

import duckdb

# 1. Count sample sections, subsections, and citation edges by jurisdiction
print("=== Top 10 Sample Slices by Statutory Section Count ===")
df_summary = duckdb.sql("""
    SELECT
        jurisdiction,
        container_type,
        container_id,
        container_name,
        COUNT(*) AS sample_sections,
        SUM(paragraph_count) AS total_paragraphs
    FROM 'hf://datasets/keystone-legal-data/us-statutes-medallion-samples/data/sections/train-00000-of-00001.parquet'
    GROUP BY jurisdiction, container_type, container_id, container_name
    ORDER BY sample_sections DESC
    LIMIT 10
""").df()
print(df_summary.to_string(index=False))

# 2. Reconstruct hierarchical subsections for a sample section
print("\n=== Hierarchical Subsections Specimen ===")
df_subs = duckdb.sql("""
    SELECT
        jurisdiction,
        doc_id,
        paragraph_seq,
        enum_label,
        indent_level,
        LEFT(text, 100) AS text_preview
    FROM 'hf://datasets/keystone-legal-data/us-statutes-medallion-samples/data/subsections/train-00000-of-00001.parquet'
    WHERE enum_label != ''
    LIMIT 8
""").df()
print(df_subs.to_string(index=False))

# 3. Traverse directed intra-jurisdiction statutory citation graph edges
print("\n=== Sample Resolved Directed Citation Graph Edges ===")
df_edges = duckdb.sql("""
    SELECT
        jurisdiction,
        source_doc_id,
        source_section,
        target_doc_id,
        target_section,
        citation_count
    FROM 'hf://datasets/keystone-legal-data/us-statutes-medallion-samples/data/edges/train-00000-of-00001.parquet'
    ORDER BY citation_count DESC
    LIMIT 10
""").df()
print(df_edges.to_string(index=False))
