# Keystone Legal Data — US Statutory & Citation Graph Medallion Corpus (57-Jurisdiction Sample Showcase)

**Official Catalog & Commercial Licensing:** [**https://keystonelegaldata.com**](https://keystonelegaldata.com)  
**Corporate Profile & Engineering Methodology:** [**https://keystonelegaldata.com/about.html**](https://keystonelegaldata.com/about.html)  
**LLM & AI Agent Catalog Manifest (`/llms.txt`):** [**https://keystonelegaldata.com/llms.txt**](https://keystonelegaldata.com/llms.txt)  
**Publisher:** **Keystone Data Services LLC** (d/b/a **Keystone Legal Data**, Yuma, Arizona)  
**Interactive Sample Dataset (Hugging Face):** [**huggingface.co/datasets/keystone-legal-data/us-statutes-medallion-samples**](https://huggingface.co/datasets/keystone-legal-data/us-statutes-medallion-samples)  
**LinkedIn Company Page:** [**linkedin.com/company/keystone-legal-data**](https://www.linkedin.com/company/keystone-legal-data)  
**Direct Inquiries / Enterprise Quotes & Demos:** `info@keystonelegaldata.com` | `(928) 502-0228`

---

## Executive Summary

This repository contains the **official 57-jurisdiction free evaluation sample showcase & OASIS Akoma Ntoso 3.0 XSD verification suite** of the **Keystone Legal Data US Statutory & Citation Graph Medallion Corpus (`2026-10 Snapshot Edition`)**.

Across the complete 57-jurisdiction commercial master corpus (covering the **United States Code**, all **50 US States**, **Washington D.C.**, and all **5 inhabited US Territories**: American Samoa, Guam, Northern Mariana Islands, Puerto Rico, and the U.S. Virgin Islands), Keystone Legal Data delivers:

* **57 / 57 US Statutory Jurisdictions** (`100%` active container coverage across **4,048** titles, codes, and divisions)
* **2,129,709 Enacted Statutory Sections** (`sections.parquet` + **2,129,709** XSD-validated **OASIS Akoma Ntoso 3.0 XML** documents)
* **12,613,059 Hierarchically Shredded Subsections** (`subsections.parquet`, preserving exact `(a)(1)(A)` `enum_label` and `indent_level` 1–6)
* **2,556,423 Pre-Resolved Intra-Jurisdiction Directed Citation Graph Edges** (`edges.parquet`, with `100.00%` target node closure against `sections.parquet`)
* **End-to-End SHA-256 Cryptographic Provenance** linking every Gold Parquet row back to its Silver OASIS Akoma Ntoso 3.0 XML document and verbatim Bronze government source payload.
* **Zero-Trust IP & Editorial Hygiene**: Deterministically stripped of copyrighted third-party UCC Official Comments (`© by ALI and NCCUSL`), commercial publisher case notes (`West`, `LexisNexis`, `Matthew Bender`), and non-statutory Revisor commentaries.

---

## What Is Included in This Free Sample Repository

To allow legal data engineers, AI laboratories, and enterprise evaluation teams to inspect our schema, structural subsection shredding, XML validity, and citation graph fidelity before purchasing, this GitHub repository (together with our [companion Hugging Face dataset](https://huggingface.co/datasets/keystone-legal-data/us-statutes-medallion-samples)) provides:

1. **`silver_akn_xml_specimens/`**: **57** canonical **OASIS Akoma Ntoso 3.0 (LegalDocML)** XML specimen documents (one per jurisdiction).
2. **`schemas/akn30/akomantoso30.xsd` & `xml.xsd`**: Official W3C / OASIS Akoma Ntoso 3.0 XML Schema Definition files for local cryptographic and structural validation.
3. **`sample_manifests/sample_sha256_seals.json`**: Complete SHA-256 cryptographic checksum manifest across all 57 jurisdiction archives and sample packages.
4. **`scripts/verify_akn_specimens.py` & `scripts/quickstart_duckdb.py`**: Ready-to-run Python verification and DuckDB query scripts for validating the 57 XML specimens against `akomantoso30.xsd` and querying the 57-jurisdiction sample Parquet tables (**26,904** sections, **135,401** hierarchically shredded subsections, and **33,686** directed citation edges).

---

## Quickstart (Python / Hugging Face `datasets` / `duckdb`)

### Option 1: Load with Hugging Face `datasets`

```python
from datasets import load_dataset

# Load the 57-jurisdiction sample sections table
sections = load_dataset("keystone-legal-data/us-statutes-medallion-samples", "sections", split="train")
print(sections[0])

# Load the hierarchically shredded subsections table
subsections = load_dataset("keystone-legal-data/us-statutes-medallion-samples", "subsections", split="train")

# Load the directed statutory citation graph edges table
edges = load_dataset("keystone-legal-data/us-statutes-medallion-samples", "edges", split="train")
```

### Option 2: Query Directly with `duckdb`

```python
import duckdb

duckdb.sql("""
    SELECT
        s.jurisdiction,
        s.doc_id,
        s.heading,
        sub.enum_label,
        sub.indent_level,
        LEFT(sub.text, 120) AS clause_preview
    FROM 'hf://datasets/keystone-legal-data/us-statutes-medallion-samples/data/sections/train-00000-of-00001.parquet' s
    JOIN 'hf://datasets/keystone-legal-data/us-statutes-medallion-samples/data/subsections/train-00000-of-00001.parquet' sub
      ON s.doc_id = sub.doc_id
    WHERE s.jurisdiction = 'us_fed'
    ORDER BY s.doc_id, sub.paragraph_seq
    LIMIT 10;
""").show()
```

### Option 3: Validate Silver OASIS Akoma Ntoso 3.0 XML Specimens Locally

```bash
python3 scripts/verify_akn_specimens.py
```

---

## Standardized Gold Parquet Schema (Shared Identically Across All 57 Jurisdictions)

### 1. `sections.parquet`
| Column Name | Parquet Type | Description |
| :--- | :--- | :--- |
| `jurisdiction` | `VARCHAR` | Standardized jurisdiction identifier (e.g., `us_fed`, `US-CA`, `US-NY`, `US-TX`). |
| `doc_id` | `VARCHAR` | Collection-scoped primary key (e.g., `usc-1-7`, `CACODE-BPC-100`, `ALCODE-1-1-1`). |
| `universal_doc_id` | `VARCHAR` | Globally unique primary key across all 57 corpora (`<jurisdiction>-<doc_id>`). |
| `container_type` / `container_id` / `container_name` | `VARCHAR` | Top-level statutory container metadata (`title`, `code`, `chapter`, `division`). |
| `chapter_id` / `chapter_name` | `VARCHAR` | Intermediate chapter identifier and official chapter heading. |
| `subchapter_id` / `subchapter_name` | `VARCHAR` | Subchapter, article, or part identifier and heading where applicable. |
| `section_number` / `heading` | `VARCHAR` | Canonical section number and cleaned catchline heading. |
| `full_text` | `VARCHAR` | Complete, newline-delimited enacted statutory text of the section. |
| `history_note` | `VARCHAR` | Extracted legislative session-law enactment and amendment history citations. |
| `paragraph_count` | `INT32` | Number of child subsection paragraphs shredded into `subsections.parquet`. |
| `source_html_sha256` / `akn_sha256` | `VARCHAR` | 64-character SHA-256 digests linking the Gold row to its Silver XML and Bronze raw source payload. |

### 2. `subsections.parquet`
| Column Name | Parquet Type | Description |
| :--- | :--- | :--- |
| `jurisdiction` / `doc_id` | `VARCHAR` | Foreign key linking the paragraph to `sections.parquet`. |
| `paragraph_eid` / `paragraph_seq` | `VARCHAR` / `INT32` | OASIS AKN 3.0 element ID (`sec_1-1-1__para_2`) and deterministic 1-based sequence order. |
| `enum_label` / `indent_level` | `VARCHAR` / `INT32` | Structural enumerator (e.g., `(a)`, `(1)`, `(A)`) and hierarchical depth (`1`–`6`). |
| `text` | `VARCHAR` | Cleaned statutory text of the individual subsection or clause. |

### 3. `edges.parquet`
| Column Name | Parquet Type | Description |
| :--- | :--- | :--- |
| `jurisdiction` | `VARCHAR` | Jurisdiction identifier. |
| `source_doc_id` / `target_doc_id` | `VARCHAR` | Pre-resolved directed citation edge from citing section to cited target section (`100.00%` closure against `sections.parquet`). |
| `source_section` / `target_section` | `VARCHAR` | Canonical section numbers of the citing and cited sections. |
| `citation_count` | `INT32` | Frequency of references from `source_doc_id` to `target_doc_id`. |

---

## Complete 57-Jurisdiction Catalog & Commercial Acquisition

Every full dataset purchase includes **perpetual, worldwide commercial snapshot license rights** to all three Medallion tiers (**Bronze** raw source archive, **Silver OASIS Akoma Ntoso 3.0 XML** archive, and **Gold Apache Parquet + Citation Graph** archive) with zero recurring subscription fees or API lock-in:

* **Single-Jurisdiction Complete Medallion Snapshot (`2026-10 Edition`)**: **$500 USD** (Instant Stripe Checkout or Enterprise PO/Wire)
* **Complete 57-Jurisdiction Master Medallion Corpus (`2026-10 Edition`)**: **$10,000 USD** ([Acquire at keystonelegaldata.com](https://keystonelegaldata.com/#master-acquisition) or request an enterprise quote/demo at `info@keystonelegaldata.com`)

| Jurisdiction | Official Statutory Corpus | Active Containers | Enacted Sections | Shredded Subsections | Citation Edges | Catalog & Sample Page |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| **US Federal** (`US-FED`) | [United States Code (U.S.C.)](https://keystonelegaldata.com/statutes/USC.html) | 53 | 60,451 | 746,040 | 69,188 | [View Specs & Sample](https://keystonelegaldata.com/statutes/USC.html) |
| **Alabama** (`US-AL`) | [Code of Alabama 1975](https://keystonelegaldata.com/statutes/alabama.html) | 46 | 49,270 | 197,421 | 15,000 | [View Specs & Sample](https://keystonelegaldata.com/statutes/alabama.html) |
| **Alaska** (`US-AK`) | [Alaska Statutes](https://keystonelegaldata.com/statutes/alaska.html) | 45 | 20,217 | 110,088 | 23,068 | [View Specs & Sample](https://keystonelegaldata.com/statutes/alaska.html) |
| **American Samoa** (`US-AS`) | [American Samoa Code](https://keystonelegaldata.com/statutes/american-samoa.html) | 38 | 3,578 | 13,406 | 1,236 | [View Specs & Sample](https://keystonelegaldata.com/statutes/american-samoa.html) |
| **Arizona** (`US-AZ`) | [Arizona Revised Statutes](https://keystonelegaldata.com/statutes/arizona.html) | 47 | 25,156 | 199,389 | 30,080 | [View Specs & Sample](https://keystonelegaldata.com/statutes/arizona.html) |
| **Arkansas** (`US-AR`) | [Arkansas Code of 1987](https://keystonelegaldata.com/statutes/arkansas.html) | 28 | 37,488 | 240,754 | 22,945 | [View Specs & Sample](https://keystonelegaldata.com/statutes/arkansas.html) |
| **California** (`US-CA`) | [California Codes](https://keystonelegaldata.com/statutes/california.html) | 29 | 162,154 | 708,187 | 184,379 | [View Specs & Sample](https://keystonelegaldata.com/statutes/california.html) |
| **Colorado** (`US-CO`) | [Colorado Revised Statutes](https://keystonelegaldata.com/statutes/colorado.html) | 46 | 35,788 | 278,473 | 38,244 | [View Specs & Sample](https://keystonelegaldata.com/statutes/colorado.html) |
| **Connecticut** (`US-CT`) | [General Statutes of Connecticut](https://keystonelegaldata.com/statutes/connecticut.html) | 72 | 30,761 | 115,794 | 45,253 | [View Specs & Sample](https://keystonelegaldata.com/statutes/connecticut.html) |
| **Delaware** (`US-DE`) | [Delaware Code](https://keystonelegaldata.com/statutes/delaware.html) | 31 | 23,540 | 153,898 | 14,551 | [View Specs & Sample](https://keystonelegaldata.com/statutes/delaware.html) |
| **District of Columbia** (`US-DC`) | [Code of the District of Columbia](https://keystonelegaldata.com/statutes/district-of-columbia.html) | 52 | 23,395 | 153,113 | 20,587 | [View Specs & Sample](https://keystonelegaldata.com/statutes/district-of-columbia.html) |
| **Florida** (`US-FL`) | [Florida Statutes](https://keystonelegaldata.com/statutes/florida.html) | 49 | 24,993 | 248,576 | 62,939 | [View Specs & Sample](https://keystonelegaldata.com/statutes/florida.html) |
| **Georgia** (`US-GA`) | [Official Code of Georgia](https://keystonelegaldata.com/statutes/georgia.html) | 53 | 29,074 | 160,832 | 16,729 | [View Specs & Sample](https://keystonelegaldata.com/statutes/georgia.html) |
| **Guam** (`US-GU`) | [Guam Code](https://keystonelegaldata.com/statutes/guam.html) | 22 | 17,878 | 73,235 | 1,869 | [View Specs & Sample](https://keystonelegaldata.com/statutes/guam.html) |
| **Hawaii** (`US-HI`) | [Hawaii Revised Statutes](https://keystonelegaldata.com/statutes/hawaii.html) | 41 | 22,973 | 134,445 | 20,269 | [View Specs & Sample](https://keystonelegaldata.com/statutes/hawaii.html) |
| **Idaho** (`US-ID`) | [Idaho Statutes](https://keystonelegaldata.com/statutes/idaho.html) | 72 | 22,714 | 114,049 | 18,566 | [View Specs & Sample](https://keystonelegaldata.com/statutes/idaho.html) |
| **Illinois** (`US-IL`) | [Illinois Compiled Statutes](https://keystonelegaldata.com/statutes/illinois.html) | 68 | 72,163 | 521,235 | 42,349 | [View Specs & Sample](https://keystonelegaldata.com/statutes/illinois.html) |
| **Indiana** (`US-IN`) | [Indiana Code](https://keystonelegaldata.com/statutes/indiana.html) | 34 | 83,148 | 426,376 | 52,945 | [View Specs & Sample](https://keystonelegaldata.com/statutes/indiana.html) |
| **Iowa** (`US-IA`) | [Code of Iowa](https://keystonelegaldata.com/statutes/iowa.html) | 16 | 26,831 | 146,021 | 26,629 | [View Specs & Sample](https://keystonelegaldata.com/statutes/iowa.html) |
| **Kansas** (`US-KS`) | [Kansas Statutes](https://keystonelegaldata.com/statutes/kansas.html) | 85 | 29,217 | 153,066 | 30,830 | [View Specs & Sample](https://keystonelegaldata.com/statutes/kansas.html) |
| **Kentucky** (`US-KY`) | [Kentucky Revised Statutes](https://keystonelegaldata.com/statutes/kentucky.html) | 44 | 38,270 | 182,761 | 102,918 | [View Specs & Sample](https://keystonelegaldata.com/statutes/kentucky.html) |
| **Louisiana** (`US-LA`) | [Louisiana Revised Statutes & Codes](https://keystonelegaldata.com/statutes/louisiana.html) | 59 | 52,280 | 284,610 | 30,653 | [View Specs & Sample](https://keystonelegaldata.com/statutes/louisiana.html) |
| **Maine** (`US-ME`) | [Maine Revised Statutes](https://keystonelegaldata.com/statutes/maine.html) | 64 | 46,351 | 212,343 | 28,221 | [View Specs & Sample](https://keystonelegaldata.com/statutes/maine.html) |
| **Maryland** (`US-MD`) | [Code of Maryland](https://keystonelegaldata.com/statutes/maryland.html) | 36 | 40,043 | 430,852 | 32,790 | [View Specs & Sample](https://keystonelegaldata.com/statutes/maryland.html) |
| **Massachusetts** (`US-MA`) | [General Laws of Massachusetts](https://keystonelegaldata.com/statutes/massachusetts.html) | 34 | 26,812 | 97,555 | 25,827 | [View Specs & Sample](https://keystonelegaldata.com/statutes/massachusetts.html) |
| **Michigan** (`US-MI`) | [Michigan Compiled Laws](https://keystonelegaldata.com/statutes/michigan.html) | 241 | 45,542 | 293,284 | 50,935 | [View Specs & Sample](https://keystonelegaldata.com/statutes/michigan.html) |
| **Minnesota** (`US-MN`) | [Minnesota Statutes](https://keystonelegaldata.com/statutes/minnesota.html) | 105 | 54,435 | 304,750 | 58,748 | [View Specs & Sample](https://keystonelegaldata.com/statutes/minnesota.html) |
| **Mississippi** (`US-MS`) | [Mississippi Code of 1972](https://keystonelegaldata.com/statutes/mississippi.html) | 50 | 28,913 | 123,989 | 42,428 | [View Specs & Sample](https://keystonelegaldata.com/statutes/mississippi.html) |
| **Missouri** (`US-MO`) | [Revised Statutes of Missouri](https://keystonelegaldata.com/statutes/missouri.html) | 41 | 40,796 | 183,305 | 159,333 | [View Specs & Sample](https://keystonelegaldata.com/statutes/missouri.html) |
| **Montana** (`US-MT`) | [Montana Code](https://keystonelegaldata.com/statutes/montana.html) | 53 | 30,301 | 182,005 | 36,949 | [View Specs & Sample](https://keystonelegaldata.com/statutes/montana.html) |
| **Nebraska** (`US-NE`) | [Revised Statutes of Nebraska](https://keystonelegaldata.com/statutes/nebraska.html) | 88 | 36,528 | 141,981 | 101,495 | [View Specs & Sample](https://keystonelegaldata.com/statutes/nebraska.html) |
| **Nevada** (`US-NV`) | [Nevada Revised Statutes](https://keystonelegaldata.com/statutes/nevada.html) | 60 | 49,746 | 280,130 | 145,242 | [View Specs & Sample](https://keystonelegaldata.com/statutes/nevada.html) |
| **New Hampshire** (`US-NH`) | [New Hampshire Revised Statutes](https://keystonelegaldata.com/statutes/new-hampshire.html) | 66 | 26,384 | 127,947 | 22,150 | [View Specs & Sample](https://keystonelegaldata.com/statutes/new-hampshire.html) |
| **New Jersey** (`US-NJ`) | [New Jersey Revised Statutes](https://keystonelegaldata.com/statutes/new-jersey.html) | 69 | 56,373 | 224,975 | 52,398 | [View Specs & Sample](https://keystonelegaldata.com/statutes/new-jersey.html) |
| **New Mexico** (`US-NM`) | [New Mexico Statutes 1978](https://keystonelegaldata.com/statutes/new-mexico.html) | 82 | 31,091 | 148,592 | 53,833 | [View Specs & Sample](https://keystonelegaldata.com/statutes/new-mexico.html) |
| **New York** (`US-NY`) | [Consolidated Laws of New York](https://keystonelegaldata.com/statutes/new-york.html) | 94 | 36,612 | 559,918 | 7,971 | [View Specs & Sample](https://keystonelegaldata.com/statutes/new-york.html) |
| **North Carolina** (`US-NC`) | [General Statutes of North Carolina](https://keystonelegaldata.com/statutes/north-carolina.html) | 311 | 39,649 | 195,680 | 29,112 | [View Specs & Sample](https://keystonelegaldata.com/statutes/north-carolina.html) |
| **North Dakota** (`US-ND`) | [North Dakota Century Code](https://keystonelegaldata.com/statutes/north-dakota.html) | 66 | 29,116 | 115,856 | 17,373 | [View Specs & Sample](https://keystonelegaldata.com/statutes/north-dakota.html) |
| **Northern Mariana Islands** (`US-MP`) | [Northern Mariana Islands Commonwealth Code](https://keystonelegaldata.com/statutes/northern-mariana-islands.html) | 10 | 6,868 | 34,156 | 3,951 | [View Specs & Sample](https://keystonelegaldata.com/statutes/northern-mariana-islands.html) |
| **Ohio** (`US-OH`) | [Ohio Revised Code](https://keystonelegaldata.com/statutes/ohio.html) | 34 | 33,791 | 238,870 | 147,140 | [View Specs & Sample](https://keystonelegaldata.com/statutes/ohio.html) |
| **Oklahoma** (`US-OK`) | [Oklahoma Statutes](https://keystonelegaldata.com/statutes/oklahoma.html) | 86 | 33,134 | 279,932 | 31,360 | [View Specs & Sample](https://keystonelegaldata.com/statutes/oklahoma.html) |
| **Oregon** (`US-OR`) | [Oregon Revised Statutes](https://keystonelegaldata.com/statutes/oregon.html) | 60 | 39,225 | 274,785 | 248,424 | [View Specs & Sample](https://keystonelegaldata.com/statutes/oregon.html) |
| **Pennsylvania** (`US-PA`) | [Pennsylvania Consolidated Statutes](https://keystonelegaldata.com/statutes/pennsylvania.html) | 52 | 13,696 | 106,305 | 10,753 | [View Specs & Sample](https://keystonelegaldata.com/statutes/pennsylvania.html) |
| **Puerto Rico** (`US-PR`) | [Laws of Puerto Rico](https://keystonelegaldata.com/statutes/puerto-rico.html) | 34 | 30,081 | 38,871 | 3,118 | [View Specs & Sample](https://keystonelegaldata.com/statutes/puerto-rico.html) |
| **Rhode Island** (`US-RI`) | [General Laws of Rhode Island](https://keystonelegaldata.com/statutes/rhode-island.html) | 49 | 32,712 | 132,192 | 15,324 | [View Specs & Sample](https://keystonelegaldata.com/statutes/rhode-island.html) |
| **South Carolina** (`US-SC`) | [Code of Laws of South Carolina 1976](https://keystonelegaldata.com/statutes/south-carolina.html) | 63 | 30,948 | 140,380 | 16,153 | [View Specs & Sample](https://keystonelegaldata.com/statutes/south-carolina.html) |
| **South Dakota** (`US-SD`) | [South Dakota Codified Laws](https://keystonelegaldata.com/statutes/south-dakota.html) | 64 | 30,412 | 84,984 | 17,467 | [View Specs & Sample](https://keystonelegaldata.com/statutes/south-dakota.html) |
| **Tennessee** (`US-TN`) | [Tennessee Code](https://keystonelegaldata.com/statutes/tennessee.html) | 68 | 34,357 | 196,426 | 20,871 | [View Specs & Sample](https://keystonelegaldata.com/statutes/tennessee.html) |
| **Texas** (`US-TX`) | [Texas Statutes and Codes](https://keystonelegaldata.com/statutes/texas.html) | 31 | 124,884 | 613,309 | 45,821 | [View Specs & Sample](https://keystonelegaldata.com/statutes/texas.html) |
| **Utah** (`US-UT`) | [Utah Code](https://keystonelegaldata.com/statutes/utah.html) | 96 | 27,753 | 382,141 | 42,243 | [View Specs & Sample](https://keystonelegaldata.com/statutes/utah.html) |
| **Vermont** (`US-VT`) | [Vermont Statutes](https://keystonelegaldata.com/statutes/vermont.html) | 46 | 22,585 | 141,094 | 15,354 | [View Specs & Sample](https://keystonelegaldata.com/statutes/vermont.html) |
| **U.S. Virgin Islands** (`US-VI`) | [Virgin Islands Code](https://keystonelegaldata.com/statutes/virgin-islands.html) | 36 | 11,751 | 31,660 | 2,375 | [View Specs & Sample](https://keystonelegaldata.com/statutes/virgin-islands.html) |
| **Virginia** (`US-VA`) | [Code of Virginia](https://keystonelegaldata.com/statutes/virginia.html) | 76 | 31,306 | 148,696 | 43,171 | [View Specs & Sample](https://keystonelegaldata.com/statutes/virginia.html) |
| **Washington** (`US-WA`) | [Revised Code of Washington](https://keystonelegaldata.com/statutes/washington.html) | 101 | 52,036 | 273,712 | 61,768 | [View Specs & Sample](https://keystonelegaldata.com/statutes/washington.html) |
| **West Virginia** (`US-WV`) | [West Virginia Code](https://keystonelegaldata.com/statutes/west-virginia.html) | 139 | 26,379 | 191,690 | 10,098 | [View Specs & Sample](https://keystonelegaldata.com/statutes/west-virginia.html) |
| **Wisconsin** (`US-WI`) | [Wisconsin Statutes](https://keystonelegaldata.com/statutes/wisconsin.html) | 469 | 18,079 | 212,292 | 56,422 | [View Specs & Sample](https://keystonelegaldata.com/statutes/wisconsin.html) |
| **Wyoming** (`US-WY`) | [Wyoming Statutes](https://keystonelegaldata.com/statutes/wyoming.html) | 44 | 19,681 | 106,633 | 28,578 | [View Specs & Sample](https://keystonelegaldata.com/statutes/wyoming.html) |
| **Total (57 Jurisdictions)** | [**Complete US Master Medallion Corpus**](https://keystonelegaldata.com) | **4,048** | **2,129,709** | **12,613,059** | **2,556,423** | [**keystonelegaldata.com**](https://keystonelegaldata.com) |

---

## License & Attribution

The sample files in this repository are provided by **Keystone Data Services LLC (d/b/a Keystone Legal Data)** for technical evaluation, schema inspection, and non-bulk testing ([Terms & EULA](https://keystonelegaldata.com/terms.html) · [Privacy Policy](https://keystonelegaldata.com/privacy.html)). While underlying enacted government edicts are in the public domain, the normalized Medallion schema, hierarchical subsection shredding, OASIS Akoma Ntoso 3.0 XML markup, resolved citation graph topology, and cryptographic lineage manifests are proprietary data engineering deliverables of Keystone Data Services LLC.

For full commercial dataset licensing, enterprise PO/ACH wire invoicing, or custom snapshot quotes, visit [**https://keystonelegaldata.com**](https://keystonelegaldata.com), connect on [**LinkedIn**](https://www.linkedin.com/company/keystone-legal-data), or contact [**info@keystonelegaldata.com**](mailto:info@keystonelegaldata.com).
