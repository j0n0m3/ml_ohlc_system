## ml system to predict prices

### feature pipeline services:
- trade_producer (producer)
- trade_to_ohlc (transformer)
- kafka_to_feature_store (consumer)

### data
- ws api = live
- rest api = backfill
