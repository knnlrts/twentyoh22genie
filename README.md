# 🧞‍♂️ 20022genie - Your ISO 20022 XML Wish-Granting Library

[![PyPI Version](https://img.shields.io/pypi/v/20022genie?color=blue)](https://pypi.org/project/20022genie/)
[![License: MIT](https://img.shields.io/badge/License-MIT-gold.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/20022genie)](https://pypi.org/project/20022genie/)

Tired of hand-crafting ISO 20022 XML test files? Rub this magic lamp and let **20022genie** grant your testing wishes! ✨
```python
from twentyoh22genie import Genie

# Summon the genie
genie = Genie()

# Make your wish!
payment_xml = genie.grant_wish(
    message_type="pain.001",
    transactions=5,
    currency="EUR"
)

# Poof! Your test file appears
with open("payment_test.xml", "w") as f:
    f.write(payment_xml)
```

## 🔮 What Magic Does This Genie Offer?
20022genie conjures up realistic ISO 20022 test files with a snap of your fingers:
- ✅ **Pain-free pain.001/pain.002/pain.008 generation**
- ✅ **Camt.053/054 bank statements on demand**
- ✅ **pacs.008 payment instructions in a flash**
- ✅ Fully compliant with ISO 20022 schemas
- ✅ Customizable transaction counts, amounts, and currencies
- ✅ Random but realistic financial data generation
- ✅ Namespaces and XML structure handled magically

## 🧞‍♂️ How to Summon the Genie
1. **Install the magic lamp**:
   ```bash
   pip install 20oh22genie
   ```
2. **Rub the lamp** (import the library):
   ```python
   from twentyoh22genie import Genie
   ```
3. **Make your wish** (generate XML):
   ```python
   # Generate a customer credit transfer file
   pain001 = Genie().grant_wish("pain.001")

   # Create a bank statement with 10 transactions
   camt053 = Genie().grant_wish("camt.053", transactions=10)

   # Generate specific currency payment
   pacs008 = Genie().grant_wish("pacs.008", currency="USD")
   ```

## ✨ Advanced Wizardry
Customize your wishes with these magical parameters:

```python
# Generate a pain.002 with custom parameters
report = Genie().grant_wish(
    message_type="pain.002",
    transactions=8,
    currency="GBP",
    date_range=("2023-01-01", "2023-06-30"),
    debtor_name="Aladdin Enterprises",
    creditor_name="Magic Carpet Inc.",
    status="RJCT",  # Rejected transactions
    reason_code="AC04"  # Closed account number
)
```

## 🪄 Genie Capabilities
| Message Type      | Key Features                          | Realistic Data? |
|-------------------|---------------------------------------|----------------|
| `pain.001`        | Credit transfers, batch payments      | ✅             |
| `pain.002`        | Payment status reports                | ✅             |
| `pain.008`        | Direct debit requests                 | ✅             |
| `camt.053`        | Bank statements                       | ✅             |
| `camt.054`        | Bank debit/credit notifications       | ✅             |
| `pacs.008`        | FI-to-FI customer credit transfers    | ✅             |
| `pacs.002`        | Payment status reports                | ✅             |

## 🌟 Why Choose This Genie?
- **No more XML headaches**: Forget complex schema details
- **Testing magic**: Create edge cases in seconds
- **Regulatory compliance**: Ready for PSD2, SEPA, and more
- **Time traveler mode**: Generate historical or future-dated files
- **Zero dependencies**: Pure Python magic

## 🧪 Laboratory (Examples)
See the genie in action in our [Example Jupyter Notebook](examples/magic_show.ipynb)!

```python
# Generate a problem scenario
rejected_payments = Genie().grant_wish(
    "pain.002",
    status="RJCT",
    transactions=3,
    reason_code=("AM04", "AC01", "AG02")
)

# Create massive test file
big_statement = Genie().grant_wish("camt.053", transactions=500)
```

## 🤝 Join Our Magic Circle
Contributions welcome! Help us grant more wishes:
1. Fork the magic lamp (repository)
2. Create your spell branch (`git checkout -b new-spell`)
3. Commit your incantations (`git commit -am 'Add new enchantment'`)
4. Push to the branch (`git push origin new-spell`)
5. Open a magic scroll (pull request)

## 📜 Genie's License
This magic is distributed under the MIT License - see the [LICENSE](LICENSE) file for details.
---
🧞‍♂️ **Remember: With great power comes great responsibility!**
*Use this magic only for good (testing)*
> "Test data generation shouldn't be a chore - let the genie handle the magic!"
> - Every Developer Who Hates Manual XML Crafting
Ready to stop wrestling with XML?
`pip install 20022genie` and let the magic begin!
