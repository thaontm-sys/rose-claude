"""Shopify Partner API: lấy event install/uninstall/subscription của app.

Đây chính là nguồn dữ liệu Ranksy dùng. Gọi trực tiếp thì miễn phí.

Cần 3 biến môi trường:
  SHOPIFY_PARTNER_ORG_ID   - số trong URL partners.shopify.com/<ORG_ID>/...
  SHOPIFY_PARTNER_TOKEN    - Partner Dashboard > Settings > Partner API clients
                             > Create, tick "Manage apps" + "View financials"
  SHOPIFY_APP_ID           - số trong URL partners.shopify.com/<ORG>/apps/<APP_ID>
"""
from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests

API_VERSION = os.getenv("SHOPIFY_PARTNER_API_VERSION", "2026-07")

EVENT_TYPES = [
    "RELATIONSHIP_INSTALLED",
    "RELATIONSHIP_UNINSTALLED",
    "RELATIONSHIP_REACTIVATED",
    "RELATIONSHIP_DEACTIVATED",
    "SUBSCRIPTION_CHARGE_ACTIVATED",
    "SUBSCRIPTION_CHARGE_ACCEPTED",
    "SUBSCRIPTION_CHARGE_CANCELED",
    "SUBSCRIPTION_CHARGE_DECLINED",
    "SUBSCRIPTION_CHARGE_EXPIRED",
    "SUBSCRIPTION_CHARGE_FROZEN",
    "SUBSCRIPTION_CHARGE_UNFROZEN",
]

QUERY = """
query($appId: ID!, $after: String, $min: DateTime, $types: [AppEventTypes!]) {
  app(id: $appId) {
    events(first: 100, after: $after, occurredAtMin: $min, types: $types) {
      pageInfo { hasNextPage }
      edges {
        cursor
        node {
          type
          occurredAt
          shop { id myshopifyDomain name }
          ... on RelationshipUninstalled { reason description }
          ... on AppSubscriptionEvent {
            charge { id name test amount { amount currencyCode } billingOn }
          }
        }
      }
    }
  }
}
"""


def fetch_events(days: int = 120) -> pd.DataFrame:
    org = os.environ["SHOPIFY_PARTNER_ORG_ID"]
    token = os.environ["SHOPIFY_PARTNER_TOKEN"]
    app_id = os.environ["SHOPIFY_APP_ID"]
    url = f"https://partners.shopify.com/{org}/api/{API_VERSION}/graphql.json"
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    rows, after = [], None
    while True:
        r = requests.post(
            url,
            json={
                "query": QUERY,
                "variables": {
                    "appId": f"gid://partners/App/{app_id}",
                    "after": after,
                    "min": since,
                    "types": EVENT_TYPES,
                },
            },
            headers={"X-Shopify-Access-Token": token},
            timeout=60,
        )
        r.raise_for_status()
        body = r.json()
        if body.get("errors"):
            raise RuntimeError(body["errors"])
        ev = body["data"]["app"]["events"]
        for e in ev["edges"]:
            n = e["node"]
            charge = n.get("charge") or {}
            amount = (charge.get("amount") or {}).get("amount")
            rows.append(
                {
                    "type": n["type"],
                    "occurred_at": n["occurredAt"],
                    "shop_id": n["shop"]["id"],
                    "shop_domain": n["shop"].get("myshopifyDomain"),
                    "plan_name": charge.get("name"),
                    "amount": float(amount) if amount else None,
                    "is_test": charge.get("test"),
                    "uninstall_reason": n.get("reason"),
                    "uninstall_description": n.get("description"),
                }
            )
            after = e["cursor"]
        if not ev["pageInfo"]["hasNextPage"]:
            break
        time.sleep(0.5)  # nhẹ nhàng với rate limit

    df = pd.DataFrame(rows)
    if not df.empty:
        df["occurred_at"] = pd.to_datetime(df["occurred_at"], utc=True)
        df = df[df["is_test"] != True]  # noqa: E712 - bỏ charge test
    return df


def load_events_csv(path: str) -> pd.DataFrame:
    """Dùng khi chưa có token: export CSV từ Partner Dashboard hoặc Ranksy.

    Cần tối thiểu các cột: type, occurred_at, shop_id (tên cột khác thì đổi
    trong COLUMN_ALIASES).
    """
    COLUMN_ALIASES = {
        "event": "type", "Event": "type",
        "date": "occurred_at", "Date": "occurred_at",
        "shop": "shop_id", "Shop": "shop_id", "Shop domain": "shop_id",
        "Charge name": "plan_name", "Amount": "amount",
        "Reason": "uninstall_reason", "Description": "uninstall_description",
    }
    df = pd.read_csv(path).rename(columns=COLUMN_ALIASES)
    df["occurred_at"] = pd.to_datetime(df["occurred_at"], utc=True)
    # Partner Dashboard ghi "Uninstalled", "Installed"... -> chuẩn hoá
    mapping = {
        "installed": "RELATIONSHIP_INSTALLED",
        "uninstalled": "RELATIONSHIP_UNINSTALLED",
        "subscription charge activated": "SUBSCRIPTION_CHARGE_ACTIVATED",
        "subscription charge canceled": "SUBSCRIPTION_CHARGE_CANCELED",
        "subscription charge frozen": "SUBSCRIPTION_CHARGE_FROZEN",
    }
    df["type"] = df["type"].map(lambda t: mapping.get(str(t).strip().lower(), t))
    for col in ["plan_name", "amount", "uninstall_reason", "uninstall_description"]:
        if col not in df:
            df[col] = None
    return df
