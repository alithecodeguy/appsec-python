"""Manifest preflight only. No archive is opened or extracted."""
import json
import re


def load_manifest(raw):
    if len(raw) > 4096:
        raise ValueError("manifest_too_large")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate_json_key")
            result[key] = value
        return result

    def constant(value):
        raise ValueError("non_json_number")

    entries = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    if not isinstance(entries, list) or not 1 <= len(entries) <= 5:
        raise ValueError("entry_count")
    return entries


def review_manifest(raw):
    entries = load_manifest(raw)
    seen = set()
    total = 0
    results = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"name", "kind", "compressed", "expanded"}:
            raise ValueError("entry_schema")
        name = entry["name"]
        compressed, expanded = entry["compressed"], entry["expanded"]
        if (not isinstance(name, str) or len(name) > 200 or type(compressed) is not int
                or type(expanded) is not int or not 1 <= compressed <= 4096 or expanded < 0):
            raise ValueError("entry_types")
        parts = name.split("/")
        folded = name.casefold()
        reason = "accept"
        if (not 1 <= len(parts) <= 3 or any(re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9_.-]{0,63}", p) is None for p in parts)):
            reason = "unsafe_path"
        elif entry["kind"] != "file":
            reason = "not_regular_file"
        elif not name.endswith(".txt"):
            reason = "unsupported_entry"
        elif any(folded == old or folded.startswith(old + "/") or old.startswith(folded + "/") for old in seen):
            reason = "name_collision"
        elif not 1 <= expanded <= 64:
            reason = "entry_size"
        elif expanded > 20 * compressed:
            reason = "expansion_ratio"
        total += expanded
        if reason == "accept" and total > 128:
            reason = "total_expansion"
        seen.add(folded)
        results.append((name, reason))
    return {"entries": results, "declared_total": total,
            "archive_accepted": all(reason == "accept" for _, reason in results)}
