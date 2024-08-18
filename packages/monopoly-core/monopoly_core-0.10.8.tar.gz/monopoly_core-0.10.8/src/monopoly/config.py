import re
from dataclasses import field
from typing import Any, Optional

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from monopoly.constants import BankNames, EntryType, InternalBankNames


@dataclass
class DateOrder:
    """
    Supported `dateparser` DATE_ORDER arguments can be found here:
    https://dateparser.readthedocs.io/en/latest/settings.html#date-order
    """

    date_order: str

    @property
    def settings(self):
        return {"DATE_ORDER": self.date_order}


# pylint: disable=too-many-instance-attributes
@dataclass(kw_only=True)
class StatementConfig:
    """
    Base configuration class storing configuration values for debit and
    credit card statements

    - `transaction_pattern` refers to the regex pattern used to capture transactions,
    where a pattern like:
        "(?P<transaction_date>\\d+/\\d+)\\s*"
        "(?P<description>.*?)\\s*"
        "(?P<amount>[\\d.,]+)$"
    is used to capture a transaction like:
        06/07 URBAN TRANSIT CO. SINGAPORE SG  1.38
    - `transaction_date_order` represents the datetime format that a specific bank uses
    for transactions. For example, "DMY" will parse 01/02/2024 as 1 Feb 2024.
    Defaults to DMY.
    - `multiline_transactions` controls whether Monopoly tries to concatenate
    transactions that are split across two lines
    - `header_pattern` is a regex pattern that is used to find the 'header' line
    of a statement, and determine if it is a debit or credit card statement.
    """

    bank_name: BankNames | InternalBankNames
    transaction_pattern: str
    statement_date_pattern: str
    transaction_date_order: DateOrder = field(default_factory=lambda: DateOrder("DMY"))
    statement_date_order: DateOrder = field(default_factory=lambda: DateOrder("DMY"))
    multiline_transactions: bool = False
    has_withdraw_deposit_column: bool = False
    header_pattern: str


@dataclass(config=ConfigDict(extra="forbid"), kw_only=True)
class DebitStatementConfig(StatementConfig):
    """
    Dataclass storing configuration values unique to debit statements
    """

    statement_type = EntryType.DEBIT
    has_withdraw_deposit_column: bool = True


@dataclass(config=ConfigDict(extra="forbid"))
class CreditStatementConfig(StatementConfig):
    """
    Dataclass storing configuration values unique to credit statements

    - `prev_balance_pattern` is a regex pattern used to match the previous balance
    line in a credit statements, which is then treated as a transaction.
    """

    statement_type = EntryType.CREDIT
    prev_balance_pattern: Optional[Any | re.Pattern] = None

    def __post_init__(self):
        if self.prev_balance_pattern:
            self.prev_balance_pattern = re.compile(self.prev_balance_pattern)


@dataclass
class PdfConfig:
    """Stores PDF configuration values for the `PdfParser` class

    - `password`: The password used to unlock the PDF (if it is locked)
    - `page_range`: A slice representing which pages to process. For
    example, a range of (1, -1) will mean that the first and last pages
    are skipped.
    - `page_bbox`: A tuple representing the bounding box range for every
    page. This is used to avoid weirdness like vertical text, and other
    PDF artifacts that may affect parsing.
    """

    page_range: tuple[Optional[int], Optional[int]] = (None, None)
    page_bbox: Optional[tuple[float, float, float, float]] = None
