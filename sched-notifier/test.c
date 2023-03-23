//用户层测试文件 test.c

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>

int main()
{
	//打开字符设备驱动程序
    int fd = open("/dev/mydev", O_RDWR);
	if(fd < 0) {
		perror("open");		
	}

	//调用三次sleep,主动进行调度，让出CPU
    for(int i = 0; i<3; i++) {
		sleep(1);
	}

    printf("success!!\n");

    close(fd);
    return 0;
}

