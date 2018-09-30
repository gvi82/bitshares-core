BITSHARESD_WITNESS_ID=\"1.6.1\"
BITSHARESD_PRIVATE_KEY=[\"PVD6wGqbawxvcK7Bpgiu7QaaAD54CmaB9Hh8mRUVPzq4EthbEvJaN\",\"5Jg7GUoFL1YnUVQ5j7CjDcZPBSo83QgUHia9Et5t7D6n2f3M5Mj\"]

/usr/local/bin/witness_node \
 --genesis-json=/startup/genesis.json \
 --witness-id=$BITSHARESD_WITNESS_ID \
 --private-key=$BITSHARESD_PRIVATE_KEY \
 --enable-stale-production