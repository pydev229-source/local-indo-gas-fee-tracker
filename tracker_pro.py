import json
import os
import time
import urllib.request

RPC_URL = "https://polygon-amoy.drpc.org"
PROJECT_DIR = "/home/HANS@BISSCUTE/AGENT_TASK/polygon_gas_tracker_pro"
OUTPUT_FILE = os.path.join(PROJECT_DIR, "live_gas_stats.json")

def rpc_call(method, params=[]):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        RPC_URL,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get("result")
    except Exception as e:
        return None

def fetch_advanced_gas_metrics():
    block_hex = rpc_call("eth_blockNumber")
    gas_price_hex = rpc_call("eth_gasPrice")
    
    block_number = int(block_hex, 16) if block_hex else None
    gas_price_wei = int(gas_price_hex, 16) if gas_price_hex else None
    gas_price_gwei = gas_price_wei / 10**9 if gas_price_wei else None

    # Estimasi biaya transaksi standar (ERC-20 Transfer ~65000 gas, Native Transfer ~21000 gas)
    native_transfer_cost_matic = (21000 * gas_price_wei / 10**18) if gas_price_wei else None
    erc20_transfer_cost_matic = (65000 * gas_price_wei / 10**18) if gas_price_wei else None

    metrics = {
        "tracker_name": "Polygon Gas Fee Pro Tracker",
        "network": "Polygon Amoy Testnet",
        "rpc_endpoint": RPC_URL,
        "status": "active_automated",
        "latest_block": block_number,
        "gas_price": {
            "wei": gas_price_wei,
            "gwei": round(gas_price_gwei, 4) if gas_price_gwei else None
        },
        "estimated_costs": {
            "native_transfer_matic": round(native_transfer_cost_matic, 6) if native_transfer_cost_matic else None,
            "erc20_transfer_matic": round(erc20_transfer_cost_matic, 6) if erc20_transfer_cost_matic else None
        },
        "congestion_level": "Low / Normal",
        "timestamp": time.time()
    }

    os.makedirs(PROJECT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"[AGENT_TASK] Gas Fee Pro Tracker data updated successfully at {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_advanced_gas_metrics()
