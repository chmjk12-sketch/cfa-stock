#!/usr/bin/env python3
"""
GitHub Actions 脚本 - 添加 DNS A 记录
"""
import json, hmac, hashlib, base64, urllib.request, urllib.parse, uuid, os
from datetime import datetime, timezone

AK_ID = os.environ.get("ALIYUN_ACCESS_KEY_ID", "")
AK_SECRET = os.environ.get("ALIYUN_ACCESS_KEY_SECRET", "")

def sign(p):
    sp = sorted(p.items())
    Q = urllib.parse.quote
    q = "&".join(Q(k, "") + "=" + Q(v, "") for k, v in sp)
    s = "GET&" + Q("/", "") + "&" + Q(q, "")
    sig = base64.b64encode(hmac.new((AK_SECRET + "&").encode(), s.encode(), hashlib.sha1).digest()).decode()
    return q + "&Signature=" + Q(sig, "")

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
        print("DNS result:", json.dumps(result, ensure_ascii=False))
except Exception as e:
    print("DNS API error:", e)
    print("Please manually add: cfa-stock.chmjk67.top  A  39.105.86.184")
