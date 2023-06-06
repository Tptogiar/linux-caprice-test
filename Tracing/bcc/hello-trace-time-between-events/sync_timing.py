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
from bcc.utils import printb

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

BPF_HASH(last);
BPF_PERF_OUTPUT(events);
struct data_t {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
};



int do_trace(struct pt_regs *ctx) {
    u64 ts, *tsp, delta, key = 0;
    struct data_t data = {};

    // attempt to read stored timestamp
    tsp = last.lookup(&key);
    if (tsp != NULL) {
        delta = bpf_ktime_get_ns() - *tsp;
        if (delta < 1000000000) {
            data.ts = bpf_ktime_get_ns();
            data.pid = bpf_get_current_pid_tgid();
            bpf_get_current_comm(&data.comm, sizeof(data.comm));
            // output if time is less than 1 second
            // bpf_trace_printk("%d\\n", delta / 1000000);
            events.perf_submit(ctx, &data, sizeof(data));
        }
        last.delete(&key);
    }

    // update stored timestamp
    ts = bpf_ktime_get_ns();
    last.update(&key, &ts);
    return 0;
}
""")

b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="do_trace")
print("Tracing for quick sync's... Ctrl-C to end")

start_time = 0
def print_event(cpu, data, size):
    global start_time
    event = b["events"].event(data)
    if start_time == 0:
        start_time = event.ts
    time_s = float(event.ts - start_time)/1000000000
    print(b"%-18.9f %-16s %-6d %s" % (time_s, event.comm, event.pid, b"perf_output"))



b["events"].open_perf_buffer(print_event)





# format output
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()

