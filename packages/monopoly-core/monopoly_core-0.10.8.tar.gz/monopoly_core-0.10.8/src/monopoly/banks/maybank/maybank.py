import logging

from monopoly.config import CreditStatementConfig, DebitStatementConfig
from monopoly.constants import (
    BankNames,
    CreditTransactionPatterns,
    DebitTransactionPatterns,
    StatementBalancePatterns,
)
from monopoly.identifiers import MetadataIdentifier

from ..base import BankBase

logger = logging.getLogger(__name__)


class Maybank(BankBase):
    debit_config = DebitStatementConfig(
        bank_name=BankNames.MAYBANK,
        statement_date_pattern=r"(?:結單日期)[:\s]+(\d{2}\/\d{2}\/\d{2})",
        header_pattern=r"(DATE.*DESCRIPTION.*AMOUNT.*BALANCE)",
        transaction_pattern=DebitTransactionPatterns.MAYBANK,
        has_withdraw_deposit_column=False,
        multiline_transactions=True,
    )

    credit_config = CreditStatementConfig(
        bank_name=BankNames.MAYBANK,
        statement_date_pattern=r"(\d{2}\s[A-Z]{3}\s\d{2})",
        header_pattern=r"(Date.*Description.*Amount)",
        transaction_pattern=CreditTransactionPatterns.MAYBANK,
        prev_balance_pattern=StatementBalancePatterns.MAYBANK,
        multiline_transactions=True,
    )

    identifiers = [
        [
            MetadataIdentifier(
                author="Maybank2U.com",
                creator="Maybank2u.com",
                producer="iText",
            ),
        ],
        [
            MetadataIdentifier(
                title="Credit Card Statement",
                author="Maybank2U.com",
                producer="iText",
            ),
        ],
    ]
