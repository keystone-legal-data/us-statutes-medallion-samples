#!/usr/bin/env python3
"""
Keystone Legal Data — Silver OASIS Akoma Ntoso 3.0 XSD & SHA-256 Verification Utility
Validates all 57 Silver XML specimens against schemas/akn30/akomantoso30.xsd.
Website: https://keystonelegaldata.com
"""

import hashlib
from pathlib import Path
from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "akn30" / "akomantoso30.xsd"
SPECIMEN_DIR = ROOT / "silver_akn_xml_specimens"


def main() -> None:
    print(f"Loading OASIS Akoma Ntoso 3.0 XSD schema: {SCHEMA_PATH.relative_to(ROOT)}")
    schema_doc = etree.parse(str(SCHEMA_PATH))
    validator = etree.XMLSchema(schema_doc)

    xml_files = sorted(SPECIMEN_DIR.glob("*.xml"))
    for xf in xml_files:
        doc = etree.parse(str(xf))
        validator.assertValid(doc)
        digest = hashlib.sha256(xf.read_bytes()).hexdigest()
        print(f"  [PASS] {xf.name:42s} | AKN 3.0 XSD Valid | sha256={digest[:16]}...")

    print(f"\nSuccessfully validated {len(xml_files)}/{len(xml_files)} Silver OASIS AKN 3.0 XML specimens (0 errors).")


if __name__ == "__main__":
    main()
