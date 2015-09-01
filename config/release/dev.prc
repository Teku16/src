# Distribution:
distribution dev

# Art assets:
model-path ../resources

# Server:
server-version tte_tests
min-access-level 100
accountdb-type local
shard-low-pop 50
shard-mid-pop 100

# RPC:
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/

# DClass files (in reverse order):
dc-file astron/dclass/toon.dc
dc-file astron/dclass/otp.dc

# Core features:
want-pets #f
want-parties #t
want-cogdominiums #f
want-achievements #f

# Chat:
want-whitelist #f

# Cashbot boss:
want-resistance-toonup #t
want-resistance-restock #t

# Optional:
want-yin-yang #t
use-libpandadna #f
libpandadna-pyreader #f

# Developer options:
show-population #t
force-skip-tutorial #f
want-instant-parties #t
