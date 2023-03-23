

//schdule.c

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/preempt.h>
#include <linux/device.h>
#include <linux/cdev.h>

#define DEVICE_NAME "mydev"
#define CLASS_NAME  "hello_class"

static struct class *helloClass;
static struct cdev my_dev;
struct preempt_notifier hello_preempt;
dev_t dev;

//任务被重新调度时通知机制操作
static void hello_sched_in(struct preempt_notifier *notifier, int cpu)
{
	printk("task is about to be rescheduled\n");
	printk("\n");
}

任务被抢占时通知机制操作
static void hello_sched_out(struct preempt_notifier *notifier,
	struct task_struct *next)
{
	printk("task is just been preempted\n");
}

//注册通知回调函数
struct preempt_ops hello_preempt_ops = {
	.sched_in = hello_sched_in,
	.sched_out = hello_sched_out,
};

static int my_dev_open(struct inode *inode, struct file *file){

    preempt_notifier_init(&hello_preempt, &hello_preempt_ops);
    preempt_notifier_inc();

    preempt_notifier_register(&hello_preempt);

    printk("open!\n");

    return 0;
}

static int my_dev_close(struct inode *inode, struct file *file){

    preempt_notifier_unregister(&hello_preempt);

    preempt_notifier_dec();


    printk("close!\n");

    return 0;
}

static const struct file_operations my_dev_fops = {
    .owner              = THIS_MODULE,
    .open               = my_dev_open,
    .release            = my_dev_close,
};

static int __init hello_init(void)
{
    int ret;
    dev_t dev_no;
    int Major;
    struct device *helloDevice;

	//动态地分配设备标识
    ret = alloc_chrdev_region(&dev_no, 0, 1, DEVICE_NAME);

    Major = MAJOR(dev_no);
    dev = MKDEV(Major, 0);

	//初始化字符设备
    cdev_init(&my_dev, &my_dev_fops);
    //将字符设备注册到内核
    ret = cdev_add(&my_dev, dev, 1);

	//创建类别class
    helloClass = class_create(THIS_MODULE, CLASS_NAME);
    if(IS_ERR(helloClass)){
        unregister_chrdev_region(dev, 1);
        cdev_del(&my_dev);
        return -1;
    }

	//创建设备节点
    helloDevice = device_create(helloClass, NULL, dev, NULL, DEVICE_NAME);
    if(IS_ERR(helloDevice)){
        class_destroy(helloClass);
        unregister_chrdev_region(dev, 1);
        cdev_del(&my_dev);

        return -1;
    }

    return 0;

}

static void __exit hello_exit(void)
{
    device_destroy(helloClass, dev);
    class_destroy(helloClass);
    cdev_del(&my_dev);
    unregister_chrdev_region(dev, 1);
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");


