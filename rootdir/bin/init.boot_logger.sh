#!/vendor/bin/sh
#
# Copyright (C) 2026 Slate. All Rights Reserved.
#
# PROPRIETARY AND CONFIDENTIAL.
# This software is the sole property of Slate. Unauthorized copying,
# distribution, or use of this file is strictly prohibited.
#

LOG_DIR="/metadata/boot_logs"
MAX_DMESG_BYTES=1572864

mkdir -p "$LOG_DIR/pstore" "$LOG_DIR/tombstones"
chmod 0775 "$LOG_DIR"

# Preserve previous boot's dmesg/status if present (keep disk usage bounded on /metadata)
if [ -f "$LOG_DIR/dmesg.txt" ]; then
    mv -f "$LOG_DIR/dmesg.txt" "$LOG_DIR/prev_dmesg.txt" 2>/dev/null
fi
if [ -f "$LOG_DIR/status.txt" ]; then
    mv -f "$LOG_DIR/status.txt" "$LOG_DIR/prev_status.txt" 2>/dev/null
fi

# Capture pstore/ramoops from previous crash/watchdog reboot immediately
if [ -d /sys/fs/pstore ]; then
    rm -f "$LOG_DIR/pstore/"* 2>/dev/null
    for f in /sys/fs/pstore/*; do
        [ -f "$f" ] && cp "$f" "$LOG_DIR/pstore/" 2>/dev/null
    done
fi

# Capture static early-boot diagnostics once
{
    echo "=== UNAME / VERSION ==="
    cat /proc/version 2>/dev/null
    echo "=== CMDLINE ==="
    cat /proc/cmdline 2>/dev/null
    echo "=== LSMOD (early) ==="
    lsmod 2>/dev/null
    echo "=== /dev/block/by-name ==="
    ls -la /dev/block/by-name 2>/dev/null
    echo "=== /vendor/bin/hw ==="
    ls -la /vendor/bin/hw 2>/dev/null
    echo "=== /vendor/lib64/hw ==="
    ls -la /vendor/lib64/hw 2>/dev/null
    echo "=== /vendor/lib64/hw/mt6789 ==="
    ls -la /vendor/lib64/hw/mt6789 2>/dev/null
    echo "=== /sys/fs/pstore ==="
    ls -la /sys/fs/pstore 2>/dev/null
    echo "=== DF /metadata ==="
    df -h /metadata 2>/dev/null
} > "$LOG_DIR/early_info.txt" 2>&1

: > "$LOG_DIR/dmesg.txt"
sync

tick=0
while true; do
    # Append incremental kernel + init (kmsg) logs up to MAX_DMESG_BYTES
    cur_size=$(wc -c < "$LOG_DIR/dmesg.txt" 2>/dev/null)
    [ -z "$cur_size" ] && cur_size=0
    if [ "$cur_size" -lt "$MAX_DMESG_BYTES" ]; then
        dmesg -c >> "$LOG_DIR/dmesg.txt" 2>/dev/null
    fi

    # Every 5 seconds, overwrite status.txt with a full live snapshot
    if [ $((tick % 5)) -eq 0 ]; then
        {
            echo "=== UPTIME ==="
            cat /proc/uptime 2>/dev/null
            echo "=== DF /metadata ==="
            df -h /metadata 2>/dev/null
            echo "=== MOUNTS ==="
            cat /proc/mounts 2>/dev/null
            echo "=== LSMOD ==="
            lsmod 2>/dev/null
            echo "=== KEY PROPS ==="
            getprop 2>/dev/null | grep -E "^\[(init\.svc\.|sys\.|vendor\.|vold\.|ro\.crypto\.|ro\.boot\.|ro\.hardware|persist\.sys\.)"
            echo "=== PROCESSES ==="
            ps -A -o PID,PPID,USER,S,NAME 2>/dev/null
            echo "=== TOMBSTONES ==="
            ls -la /data/tombstones 2>/dev/null
        } > "$LOG_DIR/status.txt.tmp" 2>&1
        mv -f "$LOG_DIR/status.txt.tmp" "$LOG_DIR/status.txt" 2>/dev/null

        # Grab up to 2 most recent native crash tombstones (capped at 128KB each)
        if [ -d /data/tombstones ]; then
            count=0
            for t in $(ls -t /data/tombstones/tombstone_* 2>/dev/null); do
                [ -f "$t" ] || continue
                base=$(basename "$t")
                if [ ! -f "$LOG_DIR/tombstones/$base" ]; then
                    head -c 131072 "$t" > "$LOG_DIR/tombstones/$base" 2>/dev/null
                fi
                count=$((count + 1))
                [ "$count" -ge 2 ] && break
            done
        fi
    fi

    sync
    tick=$((tick + 1))
    sleep 1
done
