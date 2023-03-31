#!/usr/bin/python
# Copyright (c) PLUMgrid, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

# run in project examples directory with:
# sudo ./hello_world.py"
# see trace_fields.py for a longer example

from bcc import BPF

# This may not work for 4.17 on x64, you need replace kprobe__sys_clone with kprobe____x64_sys_clone
BPF(text='int kprobe__kvm_set_cr0(void *ctx) { bpf_trace_printk("kvm_set_cr0!\\n"); return 0; };int kprobe__kvm_post_set_cr0(void *ctx) { bpf_trace_printk("kvm_post_set_cr0!\\n"); return 0; }').trace_print()

