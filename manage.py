#!/usr/bin/env python3
"""Offline administrative commands, never publicly exposed as endpoints."""
import argparse
import getpass
import json
import os
from pathlib import Path
from backend.store import Store
from backend.security import hash_password
from backend.providers import apply_snapshot

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description="Survivor Pool administrieren")
sub = parser.add_subparsers(dest="command", required=True)
sub.add_parser("hash-password", help="Passwort verdeckt eingeben und Hash erzeugen")
admin = sub.add_parser("make-admin", help="Vorhandenen Account zum Administrator machen")
admin.add_argument("username")
admin.add_argument("--db", default=os.environ.get("POOL_DB", str(ROOT / "data/pool.sqlite3")))
feed = sub.add_parser("import-feed", help="Normalisierte NFL-JSON-Datei importieren")
feed.add_argument("file")
feed.add_argument("--db", default=os.environ.get("POOL_DB", str(ROOT / "data/pool.sqlite3")))
args = parser.parse_args()
if args.command == "hash-password":
    first = getpass.getpass("Neues Pool-Passwort: ")
    if len(first) < 10 or first != getpass.getpass("Wiederholen: "):
        raise SystemExit("Mindestens 10 Zeichen und identische Eingaben erforderlich.")
    print(hash_password(first))
elif args.command == "make-admin":
    if not Path(args.db).is_file():
        raise SystemExit("Datenbank nicht gefunden. Zuerst den Pool starten und registrieren.")
    store = Store(args.db, demo_mode=False)
    with store.transaction() as db:
        cursor = db.execute("UPDATE users SET role='admin' WHERE username=?", (args.username.lower(),))
        if cursor.rowcount != 1:
            raise SystemExit("Account nicht gefunden.")
    print("Administrator gesetzt.")
elif args.command == "import-feed":
    store = Store(args.db, demo_mode=False)
    apply_snapshot(store, json.loads(Path(args.file).read_text(encoding="utf-8")))
    print("Spieldaten validiert und importiert.")
