#!/usr/bin/python
# Copyright (c) PLUMgrid, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

# run in project examples directory with:
# sudo ./hello_world.py"
# see trace_fields.py for a longer example

from bcc import BPF

# This may not work for 4.17 on x64, you need replace kprobe__sys_clone with kprobe____x64_sys_clone
b = BPF(text="""
#include<linux/sched.h>


BPF_HASH(counts);

int trace_kvm_set_cr3(void *ctx) { 
    u64 key = 1, zero = 0, *count_ptr;
    count_ptr = counts.lookup_or_try_init(&key, &zero);
    if(count_ptr){
        *count_ptr = (*count_ptr) + 1;
        counts.update(&key, count_ptr);
        struct pt_regs *regs = (struct pt_regs *) ctx;
        unsigned long cr3 =  regs->si;
        //unsigned long cr3 =  PT_REGS_PARM2(ctx);
        bpf_trace_printk("kvm_set_cr3:%lx, count: %ld \\n",cr3, *count_ptr); 


    }
    return 0; 
};


""")
b.attach_kprobe(event="kvm_set_cr3",fn_name="trace_kvm_set_cr3")

b.trace_print()

