def print_hearing_changes(changes):

    if not changes:
        print("  No hearing date changes detected")
        return

    print(f"  ⚠ Hearing changes detected: {len(changes)}")

    for ch in changes:

        print(
            f"  {ch['case_no']} "
            f"{ch['old_date']} → {ch['new_date']} "
            f"{ch.get('bench','')}"
        )
