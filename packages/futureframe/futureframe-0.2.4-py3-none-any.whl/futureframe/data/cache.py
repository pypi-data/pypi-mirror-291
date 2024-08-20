import collections
import os
import shelve


class CacheDict:
    def __init__(self, memory_limit=100, root="cache/cache_dict"):
        self.memory_limit = memory_limit
        self.root = root

        self.memory_data = collections.OrderedDict()

        os.makedirs(root, exist_ok=True)
        self.disk_data = shelve.open(os.path.join(root, "cache_dict.db"), writeback=True)

    def __setitem__(self, key, value):
        if key in self.memory_data:
            self.memory_data.move_to_end(key)
        elif len(self.memory_data) >= self.memory_limit:
            oldest_key, oldest_value = self.memory_data.popitem(last=False)
            self.disk_data[oldest_key] = oldest_value
        self.memory_data[key] = value

    def __getitem__(self, key):
        if key in self.memory_data:
            self.memory_data.move_to_end(key)
            return self.memory_data[key]
        elif key in self.disk_data:
            return self.disk_data[key]
        else:
            raise KeyError(f"Key {key} not found.")

    def __delitem__(self, key):
        if key in self.memory_data:
            del self.memory_data[key]
        elif key in self.disk_data:
            del self.disk_data[key]
        else:
            raise KeyError(f"Key {key} not found.")

    def __contains__(self, key):
        return key in self.memory_data or key in self.disk_data

    def close(self):
        self.disk_data.close()

    def __del__(self):
        self.close()
