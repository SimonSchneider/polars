from __future__ import annotations

from typing import Callable, Generic, Sequence, TypeVar

import polars.internals as pli
from polars.internals.expr import ensure_list_of_pyexpr
from polars.utils import is_expr_sequence

try:
    from polars.polars import PyLazyGroupBy

    _DOCUMENTING = False
except ImportError:
    _DOCUMENTING = True

# Used to type any type or subclass of LazyFrame.
# Used to indicate when LazyFrame methods return the same type as self,
# including sub-classes.
LDF = TypeVar("LDF", bound="pli.LazyFrame")


class LazyGroupBy(Generic[LDF]):
    """Created by `df.lazy().groupby("foo)"`."""

    def __init__(self, lgb: PyLazyGroupBy, lazyframe_class: type[LDF]) -> None:
        self.lgb = lgb
        self._lazyframe_class = lazyframe_class

    def agg(self, aggs: pli.Expr | Sequence[pli.Expr]) -> LDF:
        """
        Describe the aggregation that need to be done on a group.

        Parameters
        ----------
        aggs
            Single / multiple aggregation expression(s).

        Examples
        --------
        >>> (
        ...     pl.scan_csv("data.csv")
        ...     .groupby("groups")
        ...     .agg(
        ...         [
        ...             pl.col("name").n_unique().alias("unique_names"),
        ...             pl.max("values"),
        ...         ]
        ...     )
        ... )  # doctest: +SKIP

        """
        if not (isinstance(aggs, pli.Expr) or is_expr_sequence(aggs)):
            msg = f"expected 'Expr | Sequence[Expr]', got '{type(aggs)}'"
            raise TypeError(msg)

        pyexprs = ensure_list_of_pyexpr(aggs)
        return self._lazyframe_class._from_pyldf(self.lgb.agg(pyexprs))

    def head(self, n: int = 5) -> LDF:
        """
        Return first n rows of each group.

        Parameters
        ----------
        n
            Number of values of the group to select

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "letters": ["c", "c", "a", "c", "a", "b"],
        ...         "nrs": [1, 2, 3, 4, 5, 6],
        ...     }
        ... )
        >>> df
        shape: (6, 2)
        ┌─────────┬─────┐
        │ letters ┆ nrs │
        │ ---     ┆ --- │
        │ str     ┆ i64 │
        ╞═════════╪═════╡
        │ c       ┆ 1   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ c       ┆ 2   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ a       ┆ 3   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ c       ┆ 4   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ a       ┆ 5   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ b       ┆ 6   │
        └─────────┴─────┘
        >>> df.groupby("letters").head(2).sort("letters")
        shape: (5, 2)
        ┌─────────┬─────┐
        │ letters ┆ nrs │
        │ ---     ┆ --- │
        │ str     ┆ i64 │
        ╞═════════╪═════╡
        │ a       ┆ 3   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ a       ┆ 5   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ b       ┆ 6   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ c       ┆ 1   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ c       ┆ 2   │
        └─────────┴─────┘

        """
        return self._lazyframe_class._from_pyldf(self.lgb.head(n))

    def tail(self, n: int = 5) -> LDF:
        """
        Return last n rows of each group.

        Parameters
        ----------
        n
            Number of values of the group to select

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "letters": ["c", "c", "a", "c", "a", "b"],
        ...         "nrs": [1, 2, 3, 4, 5, 6],
        ...     }
        ... )
        >>> df
        shape: (6, 2)
        ┌─────────┬─────┐
        │ letters ┆ nrs │
        │ ---     ┆ --- │
        │ str     ┆ i64 │
        ╞═════════╪═════╡
        │ c       ┆ 1   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ c       ┆ 2   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ a       ┆ 3   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ c       ┆ 4   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ a       ┆ 5   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ b       ┆ 6   │
        └─────────┴─────┘
        >>> df.groupby("letters").tail(2).sort("letters")
         shape: (5, 2)
        ┌─────────┬─────┐
        │ letters ┆ nrs │
        │ ---     ┆ --- │
        │ str     ┆ i64 │
        ╞═════════╪═════╡
        │ a       ┆ 3   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ a       ┆ 5   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ b       ┆ 6   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ c       ┆ 2   │
        ├╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌┤
        │ c       ┆ 4   │
        └─────────┴─────┘

        """
        return self._lazyframe_class._from_pyldf(self.lgb.tail(n))

    def apply(self, f: Callable[[pli.DataFrame], pli.DataFrame]) -> LDF:
        """
        Apply a function over the groups as a new `DataFrame`.

        Implementing logic using this .apply method is generally slower and more memory
        intensive than implementing the same logic using the expression API because:

        - with .apply the logic is implemented in Python but with an expression the
          logic is implemented in Rust
        - with .apply the DataFrame is materialized in memory
        - expressions can be parallelised
        - expressions can be optimised

        If possible use the expression API for best performance.

        Parameters
        ----------
        f
            Function to apply over each group of the `LazyFrame`.

        Examples
        --------
        The function is applied by group.

        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3, 1],
        ...         "bar": ["a", "b", "c", "c"],
        ...     }
        ... )
        >>> (
        ...     df.lazy()
        ...     .groupby("bar", maintain_order=True)
        ...     .agg(
        ...         [
        ...             pl.col("foo").apply(lambda x: x.sum()),
        ...         ]
        ...     )
        ...     .collect()
        ... )
        shape: (3, 2)
        ┌─────┬─────┐
        │ bar ┆ foo │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ a   ┆ 1   │
        ├╌╌╌╌╌┼╌╌╌╌╌┤
        │ b   ┆ 2   │
        ├╌╌╌╌╌┼╌╌╌╌╌┤
        │ c   ┆ 4   │
        └─────┴─────┘

        It is better to implement this with an expression:

        >>> (
        ...     df.groupby("bar", maintain_order=True).agg(
        ...         pl.col("foo").sum(),
        ...     )
        ... )  # doctest: +IGNORE_RESULT

        """
        return self._lazyframe_class._from_pyldf(self.lgb.apply(f))
