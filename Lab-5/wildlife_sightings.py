"""Sightings log for a wildlife sanctuary.

Records which species were seen in which zone, summarises each zone
and finds the rarest species.
"""
import hashlib
import sqlite3


def create_db():
    """Create an in-memory database with an empty sightings table."""
    db = sqlite3.connect(":memory:")
    db.execute(
        "CREATE TABLE sightings "
        "(id INTEGER PRIMARY KEY, species TEXT, zone TEXT, count INTEGER)"
    )
    return db


def log_sighting(db, species, zone, count, extras=None):
    """Store one sighting and add its count to the running totals dict."""
    if extras is None:
        extras = {}
    db.execute(
        "INSERT INTO sightings (species, zone, count) VALUES (?, ?, ?)",
        (species, zone, count),
    )
    extras[species] = extras.get(species, 0) + count
    return extras


def observer_id(observer):
    """Return a short, non-security ID derived from the observer's name."""
    digest = hashlib.md5(observer.encode(), usedforsecurity=False)
    return digest.hexdigest()[:6]


def zone_summary(db, zone):
    """Return the total number of animals sighted in a zone (0 if none)."""
    row = db.execute(
        "SELECT SUM(count) FROM sightings WHERE zone = ?", (zone,)
    ).fetchone()
    if row[0] is None:
        return 0
    return row[0]


def rarest(db):
    """Return the species with the smallest total count."""
    rows = db.execute(
        "SELECT species, SUM(count) FROM sightings GROUP BY species"
    ).fetchall()
    least = min(rows, key=lambda r: r[1])
    return least[0]


def main():
    """Run a short demonstration of the sightings log."""
    db = create_db()
    totals = log_sighting(db, "Leopard", "North", 1)
    log_sighting(db, "Chital", "North", 24, totals)
    log_sighting(db, "Hornbill", "East", 3, totals)
    if len(totals) != 3:
        raise RuntimeError("expected 3 species in totals")
    print(observer_id("Arun"), zone_summary(db, "North"), rarest(db))


if __name__ == "__main__":
    main()
