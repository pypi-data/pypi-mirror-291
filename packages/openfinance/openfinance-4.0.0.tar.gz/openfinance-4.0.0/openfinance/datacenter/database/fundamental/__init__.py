from openfinance.datacenter.database.fundamental.financial import *

from openfinance.datacenter.database.executor_generator import ExecutorGenerator

ExecutorGenerator.register_from_file(
    "openfinance/datacenter/database/config/common.json"
)
ExecutorGenerator.register_from_file(
    "openfinance/datacenter/database/config/company.json"
)
ExecutorGenerator.register_from_file(
    "openfinance/datacenter/database/config/macro.json"
)
ExecutorGenerator.register_from_file(
    "openfinance/datacenter/database/config/market.json"
)
ExecutorGenerator.register_from_file(
    "openfinance/datacenter/database/config/quant.json"
)