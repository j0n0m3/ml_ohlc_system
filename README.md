## ml_price_pedict

### real-time ML system that predicts future short term prices
-> data
<br> -> feature pipeline => feature store
<br> -> training pipeline => experiment tracker & model registry
<br> -> inference pipeline => price predict

#### data:
- ws api = live
- rest api = backfill

#### feature pipeline services:
- trade_producer (producer)
- trade_to_ohlc (transformer)
- kafka_to_feature_store (consumer)
