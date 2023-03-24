obj-m:=traverse_pcb.o

CURRENT_PATH:=$(shell pwd)
LINUX_KERNEL:=$(shell uname -r)
LINUX_KERNEL_PATH:=/lib/modules/$(LINUX_KERNEL)/build

build-module:
	make -C $(LINUX_KERNEL_PATH) M=$(CURRENT_PATH) modules

insmod:
	insmod traverse_pcb.ko
rmmod:
	rmmod traverse_pcb.ko
	

clean:
	make -C $(LINUX_KERNEL_PATH) M=$(CURRENT_PATH) clean





