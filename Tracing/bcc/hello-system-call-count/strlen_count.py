from __future__ import print_function
from bcc import BPF
from time import sleep

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>
#include <uapi/linux/string.h>
struct key_t {
    char c[80];
};
BPF_HASH(counts, struct key_t);

int count(struct pt_regs *ctx) {
    if (!PT_REGS_PARM1(ctx))
        return 0;

    struct key_t key = {};
    u64 zero = 0, *val;
    //bpf_trace_printk("ptr = %p ,val = %c str = %s \\n",PT_REGS_PARM1(ctx),*(char*)PT_REGS_PARM1(ctx),(char*)PT_REGS_PARM1(ctx));
    int res = bpf_probe_read_user(&key.c, sizeof(key.c), (void *)PT_REGS_PARM1(ctx));
    //bpf_trace_printk("key strlen = %d ,str =%s \\n",strlen(key.c), key.c);
    bpf_trace_printk("read result %d \\n",res);
    // could also use `counts.increment(key)`
    val = counts.lookup_or_init(&key, &zero);
    (*val)++;
    return 0;
};
""")
b.attach_uprobe(name="c", sym="strlen", fn_name="count")

# header
print("Tracing strlen()... Hit Ctrl-C to end.")

# sleep until Ctrl-C
try:
    sleep(99999999)
except KeyboardInterrupt:
    pass

# print output
print("%10s %s" % ("COUNT", "STRING"))
counts = b.get_table("counts")
for k, v in sorted(counts.items(), key=lambda counts: counts[1].value):
    print("%10d \"%s\"" % (v.value, k.c))
