from morningstar.spec.web_service_spec import FieldNames


class Instrument:
    def __init__(self, exchange: str, security_type: str, symbol: str) -> None:
        self.exchange = exchange
        self.security_type = security_type
        self.symbol = symbol

    @staticmethod
    def from_string(s: str):
        l = s.split('.')
        if len(l) != 3:
            raise ValueError('Instrument not in format exchange.security_type.symbol')
        return Instrument(exchange=l[0], security_type=l[1], symbol=l[2])

    @staticmethod
    def from_dict(d: dict):
        return Instrument(
            exchange=d[FieldNames.Exchange.value],
            security_type=d[FieldNames.SecurityType.value],
            symbol=d[FieldNames.Symbol.value]
        )

    def __repr__(self):
        return '{}.{}.{}'.format(self.exchange, self.security_type, self.symbol)
