# item_tasks_examples
Examples of Dockerized analyses that are ingestible by item_tasks.

This repo aims to provide examples and documentation for building tasks ingestible by Girder's item_tasks plugins, and
is currently living outside of the Girder repo so that it can be developed more quickly and without adding committments
to Girder's codebase until the content in this repo has stabilized.

These examples are intended for people developing analyses that want to use item_tasks, but are not Girder developers.  The item_tasks Vagrantfile and Ansible code, located under item_tasks in the devops folder, is a good resource for algorithm developers to get an item_tasks "dev environment" up and running quickly, in this case that means a VirtualBox VM with item_tasks provisioned and configured.

## What Item Tasks is

Item Tasks is a Girder plugin that allows Girder items to be act as task specifications for the Girder Worker.  It also provides a facility to ingest tasks that have been wrapped into Docker containers, creating an item in Girder that is runnable as a task.  Any analysis or executable that is capable of being Dockerized and adhering to a self-describing specification is eligible to become a task in this system.  Upon ingest, the task will be runnable from Girder and can reference data in Girder as inputs.  The task will have a UI in Girder auto-generated from its specification, and all of the shipping and handling of the data and parameter inputs to the task will be automatically managed between Girder and Girder-Worker.  As the task will be run within Docker from Girder-Worker, there is some ability to scale up the execution of the task.

One way to think of Item Tasks is that it takes a command line executable and builds a simple Girder web application around that executable. Item Tasks can build a first, and simple UI for an executable, along with a naive approach to running the executable on the server side. 

There are two different ways to self-describe your task for Item Tasks, either using a JSON specification or using standard Slicer Execution Model XML.  Item Tasks aims for compatibility with Slicer XML, but the Slicer XML is designed for a CLI acting on a local filesystem, and so cannot be fully adapted to a CLI operating within the Girder and Girder-Worker environment, i.e. running a task on a remote machine transferring data through Girder.

Specifically the following Slicer XML schema properties are not currently supported in Item Tasks

* geometry
* point
* pointfile
* region
* table
* transform
* any output type that isn't a file
* the "multiple" modifier that allows the same flag to be provided more than once

If you want to include these input types to your task, the best thing to do is use the conversion tools to translate your XML into the JSON format, and then augment that starting point with the supported JSON spec fields to accomplish what you want.

The conversion script from XML to JSON is located [here](https://github.com/girder/girder/blob/master/plugins/item_tasks/server/cli_parser.py), and this is the code the item_tasks itself uses to convert from Slicer XML to item_tasks internal JSON based representation.

## What Items Tasks is not

Item Tasks is not magic.  It is intended to get simple executables with simple UIs up and running quickly in Girder, which provides great value.

There are many cases where Item Tasks will not suffice.  If the UI is required to be more complex, or customized, or if the algorithm needs to be optimized or scaled for a particular environment or problem, Item Tasks can be a great starting point for further bespoke software development.

## Desired examples

The focus for the examples is on wrapping the executable into the Dockerfile without adding extra complexity.  Having input test data is helpful, but it should be small so as to not pollute git repos.

Having a Dockerfile with a single task and a Dockerfile with multiple tasks are the easiest starting points, but this might be an oversimplification and
providing the multiple task Dockerfiles may suffice.

* R example, perhaps linear regression
* Python example, a wordcount example
* Python Slicer CLI
* C++ Slicer CLI
* GPU/CUDA example

## Questions these examples should answer

* I have a Slicer CLI, how do I get it to an ingestible Dockerfile?

* How do you build your Dockerfile locally for item_tasks ingest?

This will follow an example using the item_tasks devops VM.

There is a built in demo Dockerfile that is part of item_tasks plugin in Girder.  This is an example task that you can build locally and then ingest.

To follow this example, in your terminal:

# ssh into the vagrant machine from the girder/plugins/item_tasks/devops folder on your host
vagrant ssh
# change to worker user
sudo su worker
# go to the correct directory where the demo Dockerfile lives
cd girder/plugins/item_tasks/demo/
# build the Docker image
docker build . -t demo
# you can see the new image as name=demo tag=latest
docker images

Then in your browser, add a new task to a folder, give it the name "demo", and be sure to uncheck the checkbox to pull from Dockerhub.  This should import the new Docker image task as a new item_tasks task.  I would kind of expect this to work if you try to ingest "demo:latest", but it fails for some reason.

TODO: why does this fail?

* How do you push your Dockerfile to DockerHub for item_tasks ingest?
* How do you set permission flags on tasks?  Refer to item_tasks plugin docs.
* What should an item_tasks Dockerfile do with various args?  An opportunity to talk about conventions/expectations.
draft:   when the container is run with no args, it should print out the task descriptions for the tasks it wraps
* what is pull_image?
draft:
in girder_worker docs

By default, the image you specify will be pulled using the docker pull command. In some cases, you may not want to perform a pull, and instead want to rely on the image already being present on the worker system. If so, set pull_image to false.



