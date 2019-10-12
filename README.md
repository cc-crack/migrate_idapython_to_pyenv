# Migrate idapython to pyenv

1. Install pyenv

    ```zsh
    brew install pyenv
    brew install pyenv-virtualenv
    ```

    Add Follow lines to your init shell script. Eg: ```~/.zshrc```

    ```zsh
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ```

2. Install python

    The default configure of pyenv installation will not compile dylib, so we have to change it by prefixing
    `env PYTHON_CONFIGURE_OPTS="--enable-shared CC=clang"`  to `pyenv install` command.

    Install python 2.7.16

    ```zsh
    env PYTHON_CONFIGURE_OPTS="--enable-shared CC=clang"  pyenv install 2.7.16
    ```

    or download manually to avoid chinese network issue

    ```zsh
    export v=2.7.16;wget https://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;env PYTHON_CONFIGURE_OPTS="--enable-shared CC=clang"  pyenv install $v
    ```

3. Create a virtual env

   ```pyenv virtualenv 2.7.16 idapython2716```

   Copy dylib file to virtual env

   ```zsh
    cp  ~/.pyenv/versions/2.7.16/lib/libpython2.7.dylib ~/.pyenv/versions/2.7.16/envs/idapython2716/libpython2.7.dylib
   ```

4. Patch IDA

   Using ```patchall.py``` to patch all IDA modules.

   Get it from

   ```git clone https://github.com/cc-crack/migrate_idapython_to_pyenv```

   Usage:

   ```zsh
   ╰─○ python2 ./patchall.py
   usage: patchall.py [-h] [-o OLD_LIB] [-n NEW_LIB]

    IDA pro python env patcher.

    optional arguments:
    -h, --help            show this help message and exit
    -o OLD_LIB, --old-lib OLD_LIB
                          Old Path to the python.dylib
    -n NEW_LIB, --new-lib NEW_LIB
                          New Path to the python.dylib
    ```

    For patching the default IDA python lib path

    ```zsh
    python2 ./patchall.py -n ~/.pyenv/versions/2.7.16/envs/idapython2716/libpython2.7.dylib
    ```

    ```pathcall.py``` depends on ```install_name_tool``` which is a part of Xcode tools. If it is missing please install Xcode.

5. Finally result

   So you can build a folder for your IDA script easily and active the python enviroment.

   ```zsh
   mkdir ~/idascript2716/
   cd ~/idapython2716
   ```

   Check all python envs.

   ```zsh
   pyenv versions
    * system (set by /Users/xxx/.pyenv/version)
    2.7.10
    2.7.10/envs/idapython
    2.7.10/envs/idapythonenv
    2.7.16
    2.7.16/envs/idapython2716
    idapython
    idapython2716
    idapythonenv
   ```

   After activating the target env you can free to pip install anything.

   ```zsh
   pyenv activate idapython2716
   pip install z3
    DEPRECATION: Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
    Looking in indexes: http://pypi.douban.com/simple
    Collecting z3
    Downloading http://pypi.doubanio.com/packages/bc/00/c1f1dfb34f5975c0d5f03e108b0669246026b83512b755e9bc725638219d/z3-0.2.0.tar.gz
    Collecting boto (from z3)
    Downloading http://pypi.doubanio.com/packages/23/10/c0b78c27298029e4454a472a1919bde20cb182dab1662cec7f2ca1dcc523/boto-2.49.0-py2.py3-none-any.whl (1.4MB)
        |████████████████████████████████| 1.4MB 2.7MB/s 
    Building wheels for collected packages: z3
    Building wheel for z3 (setup.py) ... done
    Created wheel for z3: filename=z3-0.2.0-cp27-none-any.whl size=26630 sha256=f0bba9e3010030667d05ac2817491ed5f82b510ac035a541433c6b6426feb78e
    Stored in directory: /Users/xxx/Library/Caches/pip/wheels/f3/ab/b7/909d74cd5a87893c34ed25b7bdfeccbe3dc6a4389fff9d1b4a
    Successfully built z3
    Installing collected packages: boto, z3
    Successfully installed boto-2.49.0 z3-0.2.0
   ```

   Open IDA and execute something

   ```python
    Python>sys.version
    2.7.16 (default, Oct 12 2019, 14:16:40)
    [GCC 4.2.1 Compatible Apple LLVM 11.0.0 (clang-1100.0.33.8)]

    Python>sys.executable
    /Applications/IDA Pro 7.0/ida.app/Contents/MacOS/ida

    Python>sys.path
    ['/Applications/IDA Pro 7.0/ida.app/Contents/MacOS/python/lib/python2.7/lib-dynload', '/Applications/IDA Pro 7.0/ida.app/Contents/MacOS/python/lib/python2.7/lib-dynload/ida_32', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python27.zip', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7/plat-darwin', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7/plat-mac', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7/plat-mac/lib-scriptpackages', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7/lib-tk', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7/lib-old', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7/lib-dynload', '/Applications/IDA Pro 7.0/ida.app/Contents/MacOS/python', '/Users/xxx/.pyenv/versions/2.7.16/lib/python2.7', '/Users/xxx/.pyenv/versions/2.7.16/lib/python2.7/plat-darwin', '/Users/xxx/.pyenv/versions/2.7.16/lib/python2.7/lib-tk', '/Users/xxx/.pyenv/versions/2.7.16/lib/python2.7/plat-mac', '/Users/xxx/.pyenv/versions/2.7.16/lib/python2.7/plat-mac/lib-scriptpackages', '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7/site-packages', '/Applications/IDA Pro 7.0/ida.app/Contents/MacOS/python', '/Users/xxx/.idapro', '/Users/xxx/code/idapythonenv']

    Python>import z3
    Python>z3
    <module 'z3' from '/Users/xxx/.pyenv/versions/2.7.16/envs/idapython2716/lib/python2.7/site-packages/z3/__init__.pyc'>
   ```
