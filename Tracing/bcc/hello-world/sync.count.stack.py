#!/usr/bin/python
# Copyright (c) PLUMgrid, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

# run in project examples directory with:
# sudo ./hello_world.py"
# see trace_fields.py for a longer example

from bcc import BPF

# This may not work for 4.17 on x64, you need replace kprobe__sys_clone with kprobe____x64_sys_clone
b = BPF(text="""

struct data_t {
    u64 stack_id;
};

BPF_HASH(counts);
BPF_STACK_TRACE(stack_traces,128);
BPF_PERF_OUTPUT(events);

int trace_sync(struct pt_regs *ctx) { 
    u64 key = 1, zero = 0, *count_ptr;
    u64 stack_id;
    count_ptr = counts.lookup_or_try_init(&key, &zero);
    if(count_ptr){
        *count_ptr = (*count_ptr) + 1;
        counts.update(&key, count_ptr);
        bpf_trace_printk("sync! count: %ld \\n",*count_ptr); 
	struct data_t data = {};
	data.stack_id = stack_traces.get_stackid(ctx,0);
	events.perf_submit(ctx,&data, sizeof(data));
    }
    return 0; 
};

""")
b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="trace_sync")
#b.trace_print()


stack_traces = b.get_table("stack_traces")


def print_event(cpu, data, size):
    event = b["events"].event(data)

    for addr in stack_traces.walk(event.stack_id):
        sym = b.ksym(addr).decode('utf-8', 'replace')
        print("\t%s" % sym)


b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
    except KerboardInterrupt:
        exit();

