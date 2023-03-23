obj-m := my_dev.o

test_out :=test.dev.out

build-module:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

install-module:
	insmod my_dev.ko

uninstall-module:
	rmmod my_dev

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
	rm -rf ./$(test_out)

build-test:
	gcc test.c -o $(test_out)

test:
	./test.out

