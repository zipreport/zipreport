from zipreport.fileutils.pathcache import PathCache


class TestPathCache:

    items = [
        'item0.txt',
        'a/b/c/d/item1.txt',
        'a/b/item2.txt',
        'a/b/c/item3.txt',
        'a/b/c/d/item4.txt',
    ]
    total_dirs = 4
    total_files = 5

    def test_path_cache(self):
        cache = PathCache()
        for i in self.items:
            cache.add(i)

        assert cache.path_exists('d') is False
        assert cache.path_exists('item0.txt') is False
        assert cache.path_exists('a') is True
        assert cache.path_exists('a/b/c') is True
        assert cache.path_exists('a/b/c/d') is True

    def test_path_cache_list(self):
        cache = PathCache()
        for i in self.items:
            cache.add(i)

        all_items = cache.list('')
        assert len(all_items) == self.total_dirs + self.total_files

        # test list_files()
        items = cache.list_files('')
        assert len(items) == 1
        assert items[0] == 'item0.txt'

        items = cache.list_files('a')
        assert len(items) == 0

        items = cache.list_files('a/b/c/d')
        assert len(items) == 2
        for i in items:
            assert i in ['item4.txt', 'item1.txt']

        # test list_dirs()
        items = cache.list_dirs('a')
        assert len(items) == 1
        assert items[0] == 'b/'
