## real-time ml system that predicts short-term prices

### feature pipeline
#### trade_producer (producer)
- [x] set up logging
- [x] remove hard-coded values, load config params from .env variables
- [x] set up linting and formatting

### trade_to_ohlc (transformer)
- [x] dockerize
- [x] makefile with build, run, lint, and format cmds
- [x] remove hard-coded values, load config params from .env variables

### kafka_to_feature_store (consumer)
- [ ] dockerize
- [ ] makefile with build, run, lint, and format cmds
- [ ] remove hard-coded values, load config params from .env variables

### next
- [ ] write docker compose to run whole feature pipeline locally
- [ ] backfill feature group with historical data
