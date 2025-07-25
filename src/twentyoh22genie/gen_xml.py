#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["xmlschema", "faker"]
# ///

import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import tostring
import xmlschema
from faker import Faker
import random
import uuid
from datetime import datetime, date, timedelta
from pathlib import Path

# Initialize Faker and XSD schema
fake = Faker()
# Faker.seed(15021984)
xsd_file = Path(__file__).parent.parent.parent / "resources" / "pain.001.001.09.xsd"
schema = xmlschema.XMLSchema(xsd_file)

# Type generators mapping XSD types to Faker functions
generators = {
    "Max35Text": lambda: fake.text(max_nb_chars=35).replace("\n", ""),
    "Max140Text": lambda: fake.text(max_nb_chars=140).replace("\n", ""),
    "Max70Text": lambda: fake.text(max_nb_chars=70).replace("\n", ""),
    "ISODateTime": lambda: fake.iso8601(),
    "ISODate": lambda: fake.date(),
    "ActiveOrHistoricCurrencyCode": lambda: random.choice(["EUR", "USD", "GBP"]),
    "BICFIDec2014Identifier": lambda: fake.swift(),
    "IBAN2007Identifier": lambda: fake.iban(),
    "LEIIdentifier": lambda: "".join(
        random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=20)
    ),
    "AnyBICDec2014Identifier": lambda: fake.swift(),
    "Max15NumericText": lambda: str(fake.random_number(digits=10)),
    "DecimalNumber": lambda: str(
        fake.pydecimal(left_digits=10, right_digits=2, positive=True)
    ),
    "BaseOneRate": lambda: str(
        fake.pydecimal(left_digits=1, right_digits=10, positive=True)
    ),
    "PercentageRate": lambda: str(
        fake.pydecimal(left_digits=2, right_digits=10, positive=True)
    ),
    "Boolean": lambda: str(fake.boolean()).lower(),
    "PhoneNumber": lambda: fake.phone_number()[:30],
    "CountryCode": lambda: fake.country_code(),
    "Max34Text": lambda: fake.text(max_nb_chars=34).replace("\n", ""),
    "Max350Text": lambda: fake.text(max_nb_chars=200).replace("\n", ""),
    "Max16Text": lambda: fake.text(max_nb_chars=16).replace("\n", ""),
    "Max2048Text": lambda: fake.text(max_nb_chars=200).replace("\n", ""),
    "Max4Text": lambda: fake.bothify(text="????"),
    "Max128Text": lambda: fake.text(max_nb_chars=128).replace("\n", ""),
    "UUIDv4Identifier": lambda: str(uuid.uuid4()),
    "Exact4AlphaNumericText": lambda: "".join(
        random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)
    ),
    "ChargeBearerType1Code": lambda: random.choice(["DEBT", "CRED", "SHAR", "SLEV"]),
    "PaymentMethod3Code": lambda: random.choice(["CHK", "TRF", "TRA"]),
    "Priority2Code": lambda: random.choice(["HIGH", "NORM"]),
    "DocumentType3Code": lambda: random.choice(
        ["RADM", "RPIN", "FXDR", "DISP", "PUOR", "SCOR"]
    ),
    "DocumentType6Code": lambda: random.choice(
        ["MSIN", "CNFA", "DNFA", "CINV", "CREN", "DEBN"]
    ),
    "AddressType2Code": lambda: random.choice(
        ["ADDR", "PBOX", "HOME", "BIZZ", "MLTO", "DLVY"]
    ),
    "Authorisation1Code": lambda: random.choice(["AUTH", "FDET", "FSUM", "ILEV"]),
    "ChequeDelivery1Code": lambda: random.choice(
        ["MLDB", "MLCD", "MLFA", "CRDB", "CRCD"]
    ),
    "ChequeType2Code": lambda: random.choice(["CCHQ", "CCCH", "BCHQ", "DRFT", "ELDR"]),
    "NamePrefix2Code": lambda: random.choice(["DOCT", "MADM", "MISS", "MIST", "MIKS"]),
    "PreferredContactMethod1Code": lambda: random.choice(
        ["LETT", "MAIL", "PHON", "FAXX", "CELL"]
    ),
    "RegulatoryReportingType1Code": lambda: random.choice(["CRED", "DEBT", "BOTH"]),
    "RemittanceLocationMethod2Code": lambda: random.choice(
        ["FAXI", "EDIC", "URID", "EMAL", "POST", "SMSM"]
    ),
    "TaxRecordPeriod1Code": lambda: random.choice(["MM01", "MM02", "QTR1", "HLF1"]),
    "TrueFalseIndicator": lambda: str(fake.boolean()).lower(),
    "Number": lambda: str(fake.random_number(digits=10)),
}


def get_generator(type_name):
    """Get appropriate generator function for a type"""
    if type_name in generators:
        return generators[type_name]
    # Handle complex types with simple content
    elif type_name.startswith("ActiveOrHistoricCurrencyAndAmount"):
        return lambda: {
            "_text": str(fake.pydecimal(left_digits=10, right_digits=2, positive=True)),
            "Ccy": random.choice(["EUR", "USD", "GBP"]),
        }
    return lambda: fake.text(max_nb_chars=20).replace("\n", "")


def generate_element(element, ns_prefix):
    """Recursively generate XML elements with dummy data"""
    name = element.local_name
    elem = ET.Element(f"{ns_prefix}{name}")

    # Handle simple types
    if hasattr(element, "type") and hasattr(element.type, "base_type"):
        base_type = element.type.base_type
        if base_type.is_simple():
            type_name = base_type.name or base_type.local_name
            value = get_generator(type_name)()
            if isinstance(value, dict):
                elem.text = str(value["_text"])
                for attr_name, attr_value in value.items():
                    if attr_name != "_text":
                        elem.set(attr_name, str(attr_value))
            else:
                elem.text = str(value)
            return elem

    # Handle complex types
    if hasattr(element, "type") and hasattr(element.type, "content_type"):
        content = element.type.content_type
        if hasattr(content, "elements"):
            for sub_element in content.elements.values():
                # Handle choice elements
                if hasattr(sub_element, "model") and sub_element.model == "choice":
                    choice_elem = random.choice(list(sub_element.elements.values()))
                    if random.choice([True, False]):  # 50% chance to include
                        elem.append(generate_element(choice_elem, ns_prefix))
                else:
                    # Handle optional elements (50% chance)
                    if sub_element.min_occurs == 0 and not random.choice([True, False]):
                        continue
                    # Handle multiple occurrences
                    max_occurs = (
                        min(sub_element.max_occurs, 3)
                        if sub_element.max_occurs != "unbounded"
                        else 3
                    )
                    for _ in range(random.randint(sub_element.min_occurs, max_occurs)):
                        elem.append(generate_element(sub_element, ns_prefix))

    return elem


def generate_xml():
    """Generate complete XML document"""
    # Create root element with namespace
    ns_url = "urn:iso:std:iso:20022:tech:xsd:pain.001.001.09"
    ET.register_namespace("", ns_url)
    root = ET.Element(f"{{{ns_url}}}Document")

    # Generate customer credit transfer initiation
    cstmr_cdt_trf_initn = ET.SubElement(root, f"{{{ns_url}}}CstmrCdtTrfInitn")

    # Generate group header
    grp_hdr = ET.SubElement(cstmr_cdt_trf_initn, f"{{{ns_url}}}GrpHdr")
    msg_id = ET.SubElement(grp_hdr, f"{{{ns_url}}}MsgId")
    msg_id.text = fake.uuid4()[:30]
    cre_dt_tm = ET.SubElement(grp_hdr, f"{{{ns_url}}}CreDtTm")
    cre_dt_tm.text = fake.iso8601()
    nb_of_txs = ET.SubElement(grp_hdr, f"{{{ns_url}}}NbOfTxs")
    nb_of_txs.text = str(random.randint(1, 5))
    initg_pty = ET.SubElement(grp_hdr, f"{{{ns_url}}}InitgPty")
    nm = ET.SubElement(initg_pty, f"{{{ns_url}}}Nm")
    nm.text = fake.company()

    # Generate payment information
    pmt_inf = ET.SubElement(cstmr_cdt_trf_initn, f"{{{ns_url}}}PmtInf")
    pmt_inf_id = ET.SubElement(pmt_inf, f"{{{ns_url}}}PmtInfId")
    pmt_inf_id.text = fake.uuid4()[:30]
    pmt_mtd = ET.SubElement(pmt_inf, f"{{{ns_url}}}PmtMtd")
    pmt_mtd.text = random.choice(["TRF", "CHK"])
    reqd_exctn_dt = ET.SubElement(pmt_inf, f"{{{ns_url}}}ReqdExctnDt")
    dt = ET.SubElement(reqd_exctn_dt, f"{{{ns_url}}}Dt")
    dt.text = fake.date()

    # Generate debtor information
    dbtr = ET.SubElement(pmt_inf, f"{{{ns_url}}}Dbtr")
    dbtr_nm = ET.SubElement(dbtr, f"{{{ns_url}}}Nm")
    dbtr_nm.text = fake.name()
    dbtr_acct = ET.SubElement(pmt_inf, f"{{{ns_url}}}DbtrAcct")
    dbtr_id = ET.SubElement(dbtr_acct, f"{{{ns_url}}}Id")
    iban = ET.SubElement(dbtr_id, f"{{{ns_url}}}IBAN")
    iban.text = fake.iban()
    dbtr_agt = ET.SubElement(pmt_inf, f"{{{ns_url}}}DbtrAgt")
    fin_instn_id = ET.SubElement(dbtr_agt, f"{{{ns_url}}}FinInstnId")
    bicfi = ET.SubElement(fin_instn_id, f"{{{ns_url}}}BICFI")
    bicfi.text = fake.swift()

    # Generate credit transfer transactions
    for _ in range(random.randint(1, 3)):
        cdt_trf_tx_inf = ET.SubElement(pmt_inf, f"{{{ns_url}}}CdtTrfTxInf")

        # 1. Payment Identification
        pmt_id = ET.SubElement(cdt_trf_tx_inf, f"{{{ns_url}}}PmtId")
        end_to_end_id = ET.SubElement(pmt_id, f"{{{ns_url}}}EndToEndId")
        end_to_end_id.text = fake.uuid4()[:30]

        # 2. Amount
        amt = ET.SubElement(cdt_trf_tx_inf, f"{{{ns_url}}}Amt")
        instd_amt = ET.SubElement(
            amt, f"{{{ns_url}}}InstdAmt", Ccy=random.choice(["EUR", "USD", "GBP"])
        )
        instd_amt.text = str(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        )

        # 3. Creditor Agent (CdtrAgt)
        cdtr_agt = ET.SubElement(cdt_trf_tx_inf, f"{{{ns_url}}}CdtrAgt")
        cdtr_fin_instn_id = ET.SubElement(cdtr_agt, f"{{{ns_url}}}FinInstnId")
        cdtr_bicfi = ET.SubElement(cdtr_fin_instn_id, f"{{{ns_url}}}BICFI")
        cdtr_bicfi.text = fake.swift()

        # 4. Creditor (Cdtr)
        cdtr = ET.SubElement(cdt_trf_tx_inf, f"{{{ns_url}}}Cdtr")
        cdtr_nm = ET.SubElement(cdtr, f"{{{ns_url}}}Nm")
        cdtr_nm.text = fake.name()

        # 5. Creditor Account (CdtrAcct)
        cdtr_acct = ET.SubElement(cdt_trf_tx_inf, f"{{{ns_url}}}CdtrAcct")
        cdtr_id = ET.SubElement(cdtr_acct, f"{{{ns_url}}}Id")
        cdtr_iban = ET.SubElement(cdtr_id, f"{{{ns_url}}}IBAN")
        cdtr_iban.text = fake.iban()

    return root


def prettify_xml(elem):
    """Return a pretty-printed XML string with proper formatting."""
    rough_string = tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def main():
    # Generate XML
    print("Generating XML...")
    root = generate_xml()

    # Save to file with proper XML declaration
    tree = ET.ElementTree(root)
    with open("generated_pain.xml", "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    print(prettify_xml(root))

    print("XML saved to generated_pain.xml")

    # Validate against XSD
    print("Validating XML against XSD...")
    try:
        schema.validate("generated_pain.xml")
        print("XML is valid according to the XSD schema!")
    except Exception as e:
        print(f"Validation failed: {e}")


if __name__ == "__main__":
    main()
