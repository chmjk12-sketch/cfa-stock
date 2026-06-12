#!/usr/bin/env python3
"""
GitHub Actions 部署脚本 - 通过阿里云 RunCommand API 部署到 ECS
"""
import json, hmac, hashlib, base64, urllib.request, urllib.parse, uuid, os, sys, time
from datetime import datetime, timezone

AK_ID = os.environ.get("ALIYUN_ACCESS_KEY_ID", "")
AK_SECRET = os.environ.get("ALIYUN_ACCESS_KEY_SECRET", "")
REGISTRY_USER = os.environ.get("REGISTRY_USERNAME", "")
REGISTRY_PASS = os.environ.get("REGISTRY_PASSWORD", "")
REGISTRY_URL = os.environ.get("REGISTRY_URL", "")
IMAGE = os.environ.get("IMAGE", "")
APP_NAME = os.environ.get("APP_NAME", "cfa-stock")
APP_PORT = os.environ.get("APP_PORT", "4000")

def sign(p):
    sp = sorted(p.items())
    Q = urllib.parse.quote
    q = "&".join(Q(k, "") + "=" + Q(v, "") for k, v in sp)
    s = "GET&" + Q("/", "") + "&" + Q(q, "")
    sig = base64.b64encode(hmac.new((AK_SECRET + "&").encode(), s.encode(), hashlib.sha1).digest()).decode()
    return q + "&Signature=" + Q(sig, "")

def run_cmd(instance_id, cmd, timeout=120):
    b64 = base64.b64encode(cmd.encode()).decode()
    p = {
        "Action": "RunCommand", "RegionId": "cn-beijing", "InstanceId.1": instance_id,
        "Type": "RunShellScript", "CommandContent": b64, "ContentEncoding": "Base64",
        "Timeout": str(timeout), "Format": "JSON", "Version": "2014-05-26",
        "AccessKeyId": AK_ID, "SignatureMethod": "HMAC-SHA1", "SignatureVersion": "1.0",
        "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "SignatureNonce": str(uuid.uuid4()),
    }
    r = urllib.request.urlopen("https://ecs.aliyuncs.com/?" + sign(p), timeout=10)
    iid = json.loads(r.read())["InvokeId"]
    for _ in range(timeout // 3):
        time.sleep(3)
        p2 = {
            "Action": "DescribeInvocationResults", "RegionId": "cn-beijing", "InvokeId": iid,
            "Format": "JSON", "Version": "2014-05-26",
            "AccessKeyId": AK_ID, "SignatureMethod": "HMAC-SHA1", "SignatureVersion": "1.0",
            "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "SignatureNonce": str(uuid.uuid4()),
        }
        r2 = urllib.request.urlopen("https://ecs.aliyuncs.com/?" + sign(p2), timeout=10)
        for res in json.loads(r2.read()).get("Invocation", {}).get("InvocationResults", {}).get("InvocationResult", []):
            status = res.get("InvocationStatus")
            if status in ("Success", "Failed", "Finished"):
                output = res.get("Output", "") or ""
                text = base64.b64decode(output).decode("utf-8", "replace") if output else status
                print(text)
                return status == "Success"
    return False

def ensure_dns():
    p = {
        "Action": "AddDomainRecord", "DomainName": "chmjk67.top",
        "RR": "cfa-stock", "Type": "A", "Value": "39.105.86.184",
        "Format": "JSON", "Version": "2015-01-09",
        "AccessKeyId": AK_ID, "SignatureMethod": "HMAC-SHA1", "SignatureVersion": "1.0",
        "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "SignatureNonce": str(uuid.uuid4()),
    }
    try:
        r = urllib.request.urlopen("https://dns.aliyuncs.com/?" + sign(p), timeout=10)
        result = json.loads(r.read())
        if "RecordId" in result:
            print("DNS record added:", result["RecordId"])
        else:
            print("DNS result:", result)
    except Exception as e:
        print("DNS API unavailable:", e)

if __name__ == "__main__":
    instance_id = "i-2zeee6djmc1qhwptmz1l"

    # Step 1: Deploy
    deploy_cmd = f"""set -e
docker login --username={REGISTRY_USER} --password={REGISTRY_PASS} {REGISTRY_URL}
docker pull {IMAGE}
/opt/app/scripts/deploy.sh \\
  --app-name {APP_NAME} \\
  --image {IMAGE} \\
  --port {APP_PORT} \\
  --internal-port 80 \\
  --health-path /
"""
    print("Deploying via RunCommand...")
    ok = run_cmd(instance_id, deploy_cmd)
    print(f"Deploy {'OK' if ok else 'FAILED'}")

    # Step 2: DNS
    ensure_dns()

    sys.exit(0 if ok else 1)
