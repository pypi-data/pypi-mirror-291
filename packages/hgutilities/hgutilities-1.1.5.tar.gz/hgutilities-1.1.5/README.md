﻿# HGUtilities
This is a collection of useful tools I use regularly. There are three parts to this package:

- Defaults: manages settings for classes that can be controlled easily from an interface.
- Plotting: a front end for matplotlib to easily create subplots.
- Utils: a collection of generally useful functions

## Contents

1. [Defaults](#defaults)
1. [Plotting](#plotting)
1. [Utils](#utils)
1. [Development](#development)

## Defaults

### The Problem

Usually at the beginning of a class there will be a list of class variables with default values set. The aim of this part of the package is to deal with the following issues:

- To view all the defaults you need to go into the script itself
- It is awkward to change the value of those variables from an interface
- It is impossible to change the default values without digging into the code itself.
- Passing in many arguments to functions is messy
- Mutable default values need to be implemented more carefully

Normally there are two ways of handling keyword arguments with default values.The simpler way is to have the keyword in the function signature being set equal to it's default value. If it's default value is mutable, it will need to be set to None. Code will then need to be implemented to check if it has been changed, and if not, set it to it's default value. Once there are several keyword arguemnts, this becomes messy however, and it would be preferred to pack the keywords together with **kwargs. With this second method, there will need to be code that detects if a keyword is in the **kwargs dict, and if so change it. This means we have a method for every keyword argument a function takes in, and so we can easily end up with dozens of lines of code that clogs up our classes and is a chore to implement every time we change the keyword arguments a function takes in.

In the second case, we cannot see what keyword arguments a function takes in, and can only do so in the first case if the we are calling a function directly unless each function in the middle also has all the keywords in the signature. Modifying the default values would also mean going into the code, finding the method where the keyword is processed, and editing the code directly.

### The Solution

For each class, we store the default values in a json file. After the class definition, we pass the class itself into a function that loads the values from the file, and sets them as class variables. This code is only run once when the file with the class is imported. The class will also have the attribute "defaults" assigned to it with all the default values. This allows the user to read what the defaults are from the interface, but beyond that it serves to purpose after the default values have been loaded in. If the user overwrites it, they will no longer be able to see the defaults for that object (with `my_obj.defaults`), and will need to look at the class attribute itself (with `MyClass.defaults`).

Whenever a method takes in keyword arguments, they can be passed into a function that processes the kwargs, along with a reference to the instance itself. This will automate the process described in the previous section, and if there are any keyword arguments that were not in the list of defaults, the file will be opened and overwritten with the new keyword arguments added. Their default value will be set to `None`. Below is an example of how this is implemented.

    from hgutilities import defaults

    class MyClass():

        def __init__(self, **kwargs):
            defaults.kwargs(self, **kwargs)

    defaults.load(MyClass)

We note that `defaults.kwargs` can be called from anywhere within the class and not just at initialisation, and that `**kwargs` or `kwargs` can be fed in as the second argument. If there are kwargs that require more complicated processing, they can be processed after the call to `defaults.kwargs`, and the default value of such keyword arguments should be set to `null` in the json file of defaults.

The path to the json file is stored as a class attribute `defaults_path`. In the directory that contains the script with the class, there will be another directory called "Default Settings", and this has the json files for all scripts in the original directory.

## Plotting

For full documentation, see the specific README inside the "plotting" module folder.

When creating a figure with varying characteristics, the user needs to change their code in potentially non-trivial ways in order to get the desired result. For example, if they had 12 subplots on a figure, and they decide that they want two figures with six subplots each instead, a single for loop would need to be split into two different for loops. If one of the subplots needed two lines plotted instead of one, they would either need to add that in manually outside of the loop, or change the whole data structure to make it more general. When the number of subplots is unknown, these problems are even worse. The aim of this part of the package is to make the creation of such figures easier.

The user creates data objects that store the information to be plotted. For example an instance of `Line` would have a list of $x$ values, a list of $y$ values, and optional settings such as a label and linestyle. A `Lines` object would have a collection of `Line` objects, and other information such as a subplot title, axes labels, whether it has a legend, etc. These objects can be passed in to a `Figures` object, and this does the work of deciding how they should be distributed among figures. The purpose of this is to give the user a way to easily specify what data needs to be plotted where, without needing to hardcode in the structure of the subplots.

It also provides other functions such as easily applying a rainbow pattern to the lines, adding a legend that corresponds to multiple subplots, and applying prefixes to the axes. The ability to animate figures is also built in, although this should only be used for short gifs, on the order of a few dozen frames.

## Utils

The aim of this is to improve quality of coding life by implementing some common functions. For example when reading a json file, you cannot simply open the file and load the json, you must first check whether it is empty. Such annoyances are handled by the functions in this part of the package. We split the utilities into several categories to make it easier to organise them. The functions implemented here are tailored to my personal needs, and they may not have the desired functionality for a general use case. Backwards compatibility is not guaranteed.

## Development

### Features and functionality to add or change

- automatic prefixing to axes
- more control over subplot placement
- automatic paragraph organisation for documentation
- better distribution of subplots over multiple figures
- control over tick labels
- horizontal bar charts
- better file extension handling for Defaults package
- inherit function should be able to take in a single attribute as a non-iterable
- animations need to be made compatible with more plot types

### Version 1.1 Changes

- Changed the default separator in utils/save_to_path from a tab to a comma to be in line with the standard csv format.
- Added separator kwarg to utils/save_to_path.
- utils/save_combined_files now returns the data it has just saved.
- utils/print_iterable now also returns the string it has just printed.
- utils/read_from_path now handles non-float data types.
- utils/dict renames to utils/iterables
- Added print_dict_aligned to utils/dict