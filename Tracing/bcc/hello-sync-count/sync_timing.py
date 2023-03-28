#!/usr/bin/python
#
# sync_timing.py    Trace time between syncs.
#                   For Linux, uses BCC, eBPF. Embedded C.
#
# Written as a basic example of tracing time between events.
#
# Copyright 2016 Netflix, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

from __future__ import print_function
from bcc import BPF

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>

BPF_HASH(last);


int do_trace(struct pt_regs *ctx) {
    u64 ts, *tsp, delta, key = 0,*pre_count_ptr,key_count = 1,zero = 0;


    pre_count_ptr = last.lookup_or_try_init(&key_count,&zero);
    if (pre_count_ptr != NULL) {
        *pre_count_ptr = *pre_count_ptr + 1;
        last.update(&key_count,pre_count_ptr);
        bpf_trace_printk("system call sync count = %ld ",*pre_count_ptr); 
    }

    // attempt to read stored timestamp
    tsp = last.lookup(&key);
    if (tsp != NULL) {
        delta = bpf_ktime_get_ns() - *tsp;
        if (delta < 1000000000) {
            // output if time is less than 1 second
            bpf_trace_printk("multiple sync detected , last %d ms ago", delta / 1000000);
        }
        last.delete(&key);
    }

    // update stored timestamp
    ts = bpf_ktime_get_ns();
    last.update(&key, &ts);
    bpf_trace_printk("\\n");

    return 0;
}
""")

b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="do_trace")
print("Tracing for quick sync's... Ctrl-C to end")

# format output
start = 0
while 1:
    try:
        (task, pid, cpu, flags, ts, ms) = b.trace_fields()
        if start == 0:
            start = ts
        ts = ts - start
        print(ms);
    except KeyboardInterrupt:
        exit()

