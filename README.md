## Blender Render
Render 3D Human with Blender

#### Requirement

- Python2.7
- Blender2.78

#### Install Blender
You need to download [Blender](http://download.blender.org/release/) and install scipy package to run the first part of the code. The provided code was tested with [Blender2.78](http://download.blender.org/release/Blender2.78/blender-2.78a-linux-glibc211-x86_64.tar.bz2), which is shipped with its own python executable as well as distutils package. Therefore, it is sufficient to do the following:

``` shell
# Install pip
/blenderpath/2.78/python/bin/python3.5m get-pip.py
# Install scipy
/blenderpath/2.78/python/bin/python3.5m pip install scipy
```

`get-pip.py` is downloaded from [pip](https://pip.pypa.io/en/stable/installing/). Replace the `blenderpath` with your own and set `BLENDER_PATH`.

Otherwise, you might need to point to your system installation of python, but be prepared for unexpected surprises due to version mismatches. There may not be support about questions regarding this installation.


#### Make a Directory:
Make a directory under ```.``` like this:
- xxxx(some name you like)
    - UV
    - image
    - obj
By:
```bash
mkdir xxxx
cd xxxx
mkdir UV
mkdir image
mkdir obj
```
and put the UV map in ```xxxx/UV```

**We have provided a directory called "example" for you.**

#### Generate Rendering Object

Install chumpy first:
```bash
pip install chumpy
```
Then run:
```bash
python2 get_obj_file.py xxxx
```

#### Generate Rendered Images
Modify the blender path in ```run.sh```

```bash
bash run.sh xxxx
```

You will see the rendered person in standing position in ```xxxx/image```.

#### Change the Pose:
The pose parameters are from ```./pose_standing.npy```, it is an array with 72 dimensions, open it in python with numpy and change it as you wish.

You can also get the 72-dimension pose vector from HMR.
