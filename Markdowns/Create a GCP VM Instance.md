## Create a GCP VM Instance
**Date: October 2021**

After initiate a [Google Cloud Platform](https://cloud.google.com/) account we open the _navigation menu_ on the top left.

![](../Assets/GCP_navigation_menu.png)

Next, scroll down and hover over the _Compute Engine_ tab which will open a second indented menu where we should select the _VM instance_ tab.

![](../Assets/GCP_VM_instance.png)

It should looks like this (but without the _lisa-vm_ instance)

![](../Assets/GCP_new_instance.png)

Now, let us create a simple instance with a single GPU. For that, select **CREATE INSTANCE**, the next window should appear

![](../Assets/GCP_create_instance.png)

First, choose a name for your instance. Next, pick a _Region_ and a _Zone_. On the top right, under **Monthly estimate**, you can see the estimated cost for an instance in the chosen region and zone. For a detailed price calculation, down select **DETAILS**. Each region has a different price, with the cheapest one being the _us-central1_ (true for October 2021). You should know that different regions offer different services. For our purpose, the _us-central1_ region with any zone (i.e. _us-central1-c_) would do just fine. 

Next, under **Machine configuration** --> **Series** we choose the wanted CPU platform. In order to later being able to add a GPU to our instance, we need to choose a CPU platform that supports a GPU, so we choose the **N1** (**notice: a _Free-tier_ account does not support GPUs**). Under **Machine type** we can choose the amount of CPU cores and RAM from the discrete dropdown menu or create our own combination by choosing _custom_. An instance with 2 CPU cores and 7.5 GB RAM would be enough for general purpose _Machine Learning_ simulations. Notice that by changing the **Machine type** parameters, the estimated price also change. 

Next, in order to add a GPU we need to open the **CPU PLATFORM AND GPU**

![](../Assets/GCP_add_GPU.png)

such that we see the next window

![](../Assets/GCP_add_GPU1.png)

If the **+ ADD GPU** tab is coloured blue we can push it in order to add a GPU to our instance. If the tab is coloured grey it means that the CPU platform or the region we chose does not supports GPUs and we need to select one that does. 
 
Selecting the **+ ADD GPU** tab the next window will open

![](../Assets/GCP_GPU_added.png)

Here, we can choose the _type_ and _number_ of GPUs we would like to add to our instance. Both of these parameters would be reflected in the estimated price.

Next, under **Boot disk** we select the operating system, which I will leave as Debian GNU (Linux), and the disk size.

![](../Assets/GCP_BOOT_disk.png)

In order to later enable internet traffic to our instance we need to allow both **HTTP** and **HTTPS** traffic options. In the next sections we will see how to add some Firewall rules to enable _Jupyter-notebook_ workspace.

![](../Assets/GCP_Firewall.png)


Finally, we select **CREATE** to initiate the VM instance, which would take us to the next page

![](../Assets/GCP_instance_initiated.png)

The green circle under **STATUS** means our instance is currently running. A running instance cost money, to stop the instance, click the three vertical dots on the right and select **Stop**. If the instance is running we can start working with it with an SSH by pushing the SSH tag under **Connect**, the next window should pop up. Your instance is ready for work.

![](../Assets/GCP_SSH.png)


