obj-m := my_dev.o

test_out :=test.dev.out

build-module:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

build-test:
	gcc test.c -o $(test_out)


insmod:
	insmod my_dev.ko

rmmod:
	rmmod my_dev


test:
	./test.out


clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
	rm -rf ./$(test_out)


