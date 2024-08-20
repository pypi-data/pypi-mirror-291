from quantguard.config import settings
from clickhouse_driver import Client


class ClickHouseConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.client = Client(
            host=settings.CLICKHOUSE.HOST,
            port=settings.CLICKHOUSE.PORT,
            user=settings.CLICKHOUSE.USERNAME,
            password=settings.CLICKHOUSE.PASSWORD,
            database=settings.CLICKHOUSE.DATABASE,
        )

    def execute(self, query):
        return self.client.execute(query)

    def close(self):
        self.client.disconnect()


def init_clickhouse():
    return ClickHouseConnector(
        host=settings.CLICKHOUSE.HOST,
        port=settings.CLICKHOUSE.PORT,
        user=settings.CLICKHOUSE.USERNAME,
        password=settings.CLICKHOUSE.PASSWORD,
        database=settings.CLICKHOUSE.DATABASE,
    )
