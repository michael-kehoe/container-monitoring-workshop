from collections import defaultdict
import numpy
import subprocess

def calculate_percentile(data_list, percentile):
    """
       Calculate percentile among an array of data points.
    """
    return numpy.percentile(data_list, percentile)


def parse_nlsv(content):
    """
        Parse New-line separated values (nlsv)    

        New-line separated values
        (when only one value can be written at once)

	VAL0\n
	VAL1\n
	...
    """
    ret = list()
    for line in content.split('\n')[:-1]:
        ret.append(long(line))
    return ret


def parse_ssv(content):
    """
      Parse a space-separated value

      Space separated values
      (when read-only or multiple values can be written at once)

       	VAL0 VAL1 ...\n
    """   
    line = content.split('\n')[0]
    stats = line.split(' ')
    # A line may end with a redundant space
    stats = [stat for stat in stats if stat != '']
    return stats


def parse_fk(content):
    """
        Parse Flat Keyed data (fk)

        Flat keyed

	KEY0 VAL0\n
	KEY1 VAL1\n
	...
    """
    ret = {}
    for line in content.split('\n')[:-1]:
        name, val = line.split(' ')
        ret[name] = long(val)
    return ret


def parse_nk(content):
    """
        Parse Nested Keyed data (nk)

        Nested keyed

        KEY0 SUB_KEY0 VAL\n
        KEY1 SUB_KEY1 VAL\n
        ...
    """
    ret = defaultdict()
    for line in content.split('\n')[:-1]:
        values = line.split(' ')
        try:
            ret[str(values[0])][values[1]] = long(values[2])
        except KeyError:
            ret[values[0]] = {}
            ret[values[0]][values[1]] = long(values[2])
        except IndexError:
           pass
    return ret


def dd():
    """
        get the patch for sysbench so it will work on ubuntu/redhat 
    """
    output = str(subprocess.check_output(['which','dd'])).replace("\n","")
    return output
