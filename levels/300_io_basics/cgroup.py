import os

CGROUP_ROOT_DIR = "/sys/fs/cgroup"
CPU_SHARE_PER_CORE = 1024
CPU_CFS_PERIOD_US = 200000
MEMORY_DEFAULT = -1

class CgroupsException(Exception):
    pass


class Cgroup(object):
    def __init__(self, name):
        self.name = name
        self.hierarchies = {}
        self.hierarchies['blkio'] = os.path.join(CGROUP_ROOT_DIR, "blkio")
        # self.hierarchies['blkio'] = os.path.join(CGROUP_ROOT_DIR, "blkio", self.name)
        self.hierarchies['cpu'] = os.path.join(CGROUP_ROOT_DIR, "cpu,cpuacct", self.name)
        self.hierarchies['memory'] = os.path.join(CGROUP_ROOT_DIR, "memory", self.name)
        self.hierarchies['pids'] = os.path.join(CGROUP_ROOT_DIR, "pids", self.name)
        for hierarchy, path in self.hierarchies.items():
            if not os.path.exists(path):       
                os.mkdir(path)
        
    def delete(self):
        for hierarchy, path in self.hierarchies.items():
            os.rmdir(path)

    def set_shares(self, cores):
        shares = CPU_SHARE_PER_CORE * cores
        cpu_shares_file = os.path.join(self.hierarchies['cpu'], 'cpu.shares')
        with open(cpu_shares_file, 'w+') as f:
            f.write('%s\n' % shares)

    def add_task(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            raise CgroupsException('Pid %s does not exists' % pid)
        for hierarchy, path in self.hierarchies.items():
            tasks_file = os.path.join(path, 'tasks')
            with open(tasks_file, 'r+') as f:
                cgroups_pids = f.read().split('\n')
            if not str(pid) in cgroups_pids:
                with open(tasks_file, 'a+') as f:
                    f.write('%s\n' % pid)

    def remove_task(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            raise CgroupsException('Pid %s does not exists' % pid)
        for hierarchy, path in self.hierarchies.items():
            tasks_file = os.path.join(self.hierarchies['cpu'], 'tasks')
            with open(tasks_file, 'r+') as f:
                pids = f.read().split('\n')
                if str(pid) in pids:
                    user_tasks_file = os.path.join(self.hierarchies['cpu'], self.name, 'tasks')
                    with open(user_tasks_file, 'a+') as f:
                        f.write('%s\n' % pid)

    def set_cores(self, cores):
        # Set CFS Period
        cfs_period_file = os.path.join(self.hierarchies['cpu'], 'cpu.cfs_period_us')
        with open(cfs_period_file, 'w+') as f:
            f.write('%s\n' % CPU_CFS_PERIOD_US)

        # Set CFS Quota
        quota = CPU_CFS_PERIOD_US * cores
        cfs_quota_file = os.path.join(self.hierarchies['cpu'], 'cpu.cfs_quota_us')
        with open(cfs_quota_file, 'w+') as f:
            f.write('%s\n' % quota)

    def _format_memory_value(self, unit, limit=None):
        units = ('bytes', 'kilobytes', 'megabytes', 'gigabytes')
        if unit not in units:
            raise CgroupsException('Unit must be in %s' % units)
        if limit is None:
            value = MEMORY_DEFAULT
        else:
            try:
                limit = int(limit)
            except ValueError:
                raise CgroupsException('Limit must be convertible to an int')
            else:
                if unit == 'bytes':
                    value = limit
                elif unit == 'kilobytes':
                    value = limit * 1024
                elif unit == 'megabytes':
                    value = limit * 1024 * 1024
                elif unit == 'gigabytes':
                    value = limit * 1024 * 1024 * 1024
        return value

    def set_memory_limit(self, limit=None, unit='megabytes'):
        if 'memory' in self.hierarchies.keys():
            value = self._format_memory_value(unit, limit)
            memory_limit_file = os.path.join(self.hierarchies['memory'], 'memory.limit_in_bytes')
            with open(memory_limit_file, 'w+') as f:
                f.write('%s\n' % value)
        else:
            raise CgroupsException('MEMORY hierarchy not available in this cgroup')

    def set_io_read_bps(self, device_name, bytes_per_second):
        read_bps_file = os.path.join(self.hierarchies['blkio'], 'blkio.throttle.read_bps_device')
        value = '%s %s' % (device_name, str(bytes_per_second))
        with open(read_bps_file, 'w+') as f:
            f.write('%s' % value)

    def set_io_write_bps(self, device_name, bytes_per_second):
        write_bps_file = os.path.join(self.hierarchies['blkio'], 'blkio.throttle.write_bps_device')
        value = '%s %s' % (device_name, str(bytes_per_second))
        with open(write_bps_file, 'w+') as f:
            f.write('%s' % value)

    def set_io_read_iops(self, device_name, iops):
        read_iops_file = os.path.join(self.hierarchies['blkio'], 'blkio.throttle.read_iops_device')
        value = '%s %s' % (device_name, str(iops))
        with open(read_iops_file, 'w+') as f:
            f.write('%s' % value)

    def set_io_write_iops(self, device_name, iops):
        write_iops_file = os.path.join(self.hierarchies['blkio'], 'blkio.throttle.write_iops_device')
        value = '%s %s' % (device_name, str(bytes_per_second))
        with open(write_iops_file, 'w+') as f:
            f.write('%s' % value)

    def set_max_pids(self, pids):
        pids_max_file = os.path.join(self.hierarchies['pids'], 'pids.max')
        with open(pids_max_file, 'w+') as f:
            f.write('%s\n' % pids)
