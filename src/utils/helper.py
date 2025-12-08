from collections.abc import Iterable, Iterator, ValuesView


class UnionFind[T]:
    """
    Manages a collection using the Union-Find (Disjoint Set Union) algorithm.
    """

    def __init__(self, iterable: Iterable[T] | None = None):
        self._parents: dict[T, T] = {}
        self._ranks: dict[T, int] = {}
        self._components: dict[T, set[T]] = {}

        if iterable is not None:
            for item in iterable:
                self.add(item)

    @property
    def components(self) -> ValuesView[set[T]]:
        """Return the disjoint sets."""
        return self._components.values()

    @property
    def size(self) -> int:
        """Number of items in all disjoint sets."""
        return len(self._parents)

    def __contains__(self, item: T) -> bool:
        return item in self._parents

    def __len__(self) -> int:
        return len(self._components)

    def __getitem__(self, item: T) -> set[T]:
        if item not in self:
            raise KeyError(item)

        root = self.find(item)
        return self._components[root]

    def __iter__(self) -> Iterator[set[T]]:
        """Yield each disjoint set."""
        yield from self._components.values()

    def elements(self) -> Iterator[T]:
        """Yield each element of each disjoint set."""
        yield from self._parents.keys()

    def add(self, item: T) -> None:
        """Add a new item to the disjoint set forest."""
        if item in self:
            return
        self._parents[item] = item
        self._ranks[item] = 0
        self._components[item] = {item}

    def find(self, item: T) -> T:
        """Find the representive of the item's disjoint set."""
        if item not in self:
            raise KeyError(item)

        if self._parents[item] != item:
            self._parents[item] = self.find(self._parents[item])
        return self._parents[item]

    def merge(self, a: T, b: T) -> None:
        """Merge the set containing ``a`` and the set containing ``b``."""
        a_root = self.find(a)
        b_root = self.find(b)
        if a_root == b_root:
            return

        if self._ranks[a_root] < self._ranks[b_root]:
            self._parents[a_root] = b_root
            self._components[b_root] |= self._components.pop(a_root)
        elif self._ranks[a_root] > self._ranks[b_root]:
            self._parents[b_root] = a_root
            self._components[a_root] |= self._components.pop(b_root)
        else:
            self._parents[a_root] = b_root
            self._ranks[b_root] += 1
            self._components[b_root] |= self._components.pop(a_root)