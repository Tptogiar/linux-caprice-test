#!/usr/bin/python
# Copyright (c) PLUMgrid, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

# run in project examples directory with:
# sudo ./hello_world.py"
# see trace_fields.py for a longer example

from bcc import BPF

# This may not work for 4.17 on x64, you need replace kprobe__sys_clone with kprobe____x64_sys_clone
b = BPF(text="""

BPF_HASH(counts);

int trace_vmx_get_idt(void *ctx) { 
    u64 key = 1, zero = 0, *count_ptr;
    count_ptr = counts.lookup_or_try_init(&key, &zero);
    if(count_ptr){
        *count_ptr = (*count_ptr) + 1;
        counts.update(&key, count_ptr);
        bpf_trace_printk("vmx_get_idt! count: %ld \\n",*count_ptr); 
    }
    return 0; 
};

int trace_vmx_set_idt(void *ctx) { 
    u64 key = 1, zero = 0, *count_ptr;
    count_ptr = counts.lookup_or_try_init(&key, &zero);
    if(count_ptr){
        *count_ptr = (*count_ptr) + 1;
        counts.update(&key, count_ptr);
        bpf_trace_printk("vmx_set_idt! count: %ld \\n",*count_ptr); 
    }
    return 0; 
};




""")
b.attach_kprobe(event="vmx_get_idt",fn_name="trace_vmx_set_idt")
b.attach_kprobe(event="vmx_get_idt",fn_name="trace_vmx_get_idt")

b.trace_print()

