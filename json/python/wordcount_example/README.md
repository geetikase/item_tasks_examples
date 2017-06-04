This directory contains an example Python analysis with a JSON item_tasks spec,
built into a Dockerfile, inside the `task` directory.

The base Docker image is [python:3.4-onbuild](https://github.com/docker-library/python/blob/master/3.4/onbuild/Dockerfile),
which when built will copy all of files from the directory containing the Dockerfile into a work
directory on the Docker image, then pip install the requirements.txt into that Docker image. In 
the case of this example, `requirements.txt` is empty. Then the build Docker image will have an
entrypoint that will execute Python 3.4 on the `wordcount` module, which will run `__main__.py`.

When the `wordcount` module is run with no arguments, it will print out the `spec.json` file
that is bundled into the module. This JSON file is used to describe the two tasks built
into the module, `wordcount` and `topwordcount`.

To build this Dockerfile locally, e.g. in the item_tasks VM appliance, change to the
directory where the Dockerfile is located and run the following command, as a user in
the `docker` group, in the item_tasks VM appliance case, this is the `worker` user.

```
docker build . -t wordcount
```

Now you should be able to run this Docker container yourself and see the JSON spec output

```
docker run wordcount
```

At this point, you can ingest the wordcount Docker image into your item_tasks, by adding
a local (meaning do not check "pull from DockerHub") task in the Girder UI for `wordcount`.

item_tasks will call the Docker container with no arguments, producing the JSON spec, and
parse this JSON spec to create two new tasks.

The tasks are defined in `spec.json`.  Looking at the first task `wordcount`, we
can see that it has `container_args`, the first of which is the name of the task,
the second is the input file (a word list), and the third is an output file path
for writing the word counts.

```
    "container_args": [
      "wordcount",
      "$input{wordlistfile}",
      "/mnt/girder_worker/data/wordcounts"
    ],
```

You can see a correspondence between these arguments and the input and output
arguments defined in the spec.

The inputs show a single input that is a file, and whose id is `wordlistfile`, which
is the same as the argument to the `container_args` line of `"$input{wordlistfile}"`.

```
    "inputs": [
      {
        "description": "",
        "target": "filepath",
        "required": true,
        "type": "file",
        "id": "wordlistfile",
        "name": "The input word list file, with one word per line"
      }
    ],
```

Similarly, the outputs show a single output that is a file, and whose id is `wordcounts`,
which is the same as the argument to the `container_args` line of `"/mnt/girder_worker/data/wordcounts"`.
item_tasks will automatically mount any input and output files to /mnt/girder_worker/data, which is how
we end up with the full path of /mnt/girder_worker/data/wordcounts.  See the [Girder-Worker docs](http://girder-worker.readthedocs.io/en/latest/plugins.html#docker) for more details.

```
    "outputs": [
      {
        "id": "wordcounts",
        "name": "Word counts",
        "description": "Choose a directory and name for the output item",
        "type": "new-file",
        "target": "filepath"
      }
    ]
```

In the Python task itself, we expect these values to be populated and passed as
command line arguments in the right order, so that we can take their values like

```
        wordlist_filepath, wordcount_filepath = sys.argv[2:4]

```

The `topwordcount` task is very similar to the `wordcount` task, except that it
takes an additional argument which is the top n most frequent words to include
in the output file.

To run this task, first build the Dockerfile, then ingest it to your item_tasks
Girder instance.  There is an example input file included at `test_data/words.txt`, 
which was derived from the Wikipedia entry on [Wessex Lane Halls](https://en.wikipedia.org/wiki/Wessex_Lane_Halls),
which was found by looking through random articles until one was found of sufficient length and inoffensiveness.
You can upload this example file to your Girder instance and use it as an input to either
the `wordcount` or `topwordcount` tasks.
