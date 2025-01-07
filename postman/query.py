from types import MethodType
from typing import Any, TYPE_CHECKING, cast

from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import INNER
from django.db.models.sql.query import Query

if TYPE_CHECKING:
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.models.fields import Field
    from django.db.models.query import ValuesQuerySet

    from .models import Message

    _QuerySetsAlias = tuple[ValuesQuerySet[Message, Any], ValuesQuerySet[Message, Any]]
    # not "Any" as in django-types, not "tuple[str, list[str | int]]" as in django-stubs
    # https://github.com/typeddjango/django-stubs/issues/2213
    _AsSqlType = tuple[str, tuple[Any, ...]]


class Proxy(object):
    """
    Code base for an instance proxy.
    """

    def __init__(self, target: SQLCompiler):
        self._target = target

    def __getattr__(self, name: str):
        target = self._target
        f = getattr(target, name)
        if isinstance(f, MethodType):
            return MethodType(f.__func__, self)
        else:
            return f

    def __setattr__(self, name: str, value: Any):
        if name != '_target':
            setattr(self._target, name, value)
        else:
            object.__setattr__(self, name, value)


class CompilerProxy(Proxy, SQLCompiler):
    """
    A proxy to a compiler.
    """

    query: 'PostmanQuery'  # is "Any" in django-types
    connection: 'BaseDatabaseWrapper'  # is "Any" in django-types

    # @Override
    def as_sql(self, *args: Any, **kwargs: Any) -> '_AsSqlType':
        sql, params = cast('_AsSqlType', self._target.as_sql(*args, **kwargs))
        if not sql:  # is the case with a Paginator on an empty folder
            return sql, params
        # mimics compiler.py/SQLCompiler/get_from_clause() and as_sql()
        qn = self.quote_name_unless_alias
        qn2 = self.connection.ops.quote_name
        alias = self.query.base_table
        from_clause = self.query.alias_map[alias]
        alias = cast(str, from_clause.table_alias)  # discard unexpected None
        clause_sql, _ = self.compile(from_clause)  # clause_sql, clause_params
        clause = ' '.join(['FROM', clause_sql])
        index = sql.index(clause) + len(clause)
        extra_table, extra_params = self.union(self.query.pm_get_extra())
        opts = self.query.get_meta()
        # cast() to discard unexpected None
        qn2_pk_col: str = qn2(cast('Field[Any, Any]', opts.pk).column)  # usually 'id' but not in case of model inheritance
        new_sql = [
            sql[:index],
            ' {0} ({1}) {2} ON ({3}.{4} = {2}.{5})'.format(
                INNER, extra_table, self.query.pm_alias_prefix, qn(alias), qn2_pk_col, self.query.pm_alias_id),
        ]
        if index < len(sql):
            new_sql.append(sql[index:])
        new_sql = ''.join(new_sql)
        heading_param_count = sql[:index].count('%s')
        return new_sql, params[:heading_param_count] + extra_params + params[heading_param_count:]

    def union(self, querysets: '_QuerySetsAlias | None') -> tuple[str, tuple[Any, ...]]:
        """
        Join several querysets by a UNION clause. Returns the SQL string and the list of parameters.
        """
        if querysets is None:
            raise RuntimeError('Internal error')
        qs = querysets[0].union(*querysets[1:])
        return qs.query.sql_with_params()


class PostmanQuery(Query):
    """
    A custom SQL query.
    """
    # present in django-stubs but missing in django-types
    # https://github.com/sbdchd/django-types/issues/249
    if TYPE_CHECKING:
        from django.db.models.options import Options
        def get_meta(self) -> 'Options[Message]': ...

    pm_alias_prefix = 'PM'
    pm_alias_id = 'id2'  # anything, but not 'id' to avoid annotation conflict

    # @Override
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._pm_table = None

    # @Override
    def clone(self, *args: Any, **kwargs: Any):
        obj = cast('PostmanQuery', super().clone(*args, **kwargs))
        obj._pm_table = self._pm_table
        return obj

    # @Override
    def get_compiler(self, *args: Any, **kwargs: Any):
        compiler = super().get_compiler(*args, **kwargs)
        return CompilerProxy(compiler)

    def pm_set_extra(self, table: '_QuerySetsAlias'):
        self._pm_table = table

    def pm_get_extra(self):
        return self._pm_table
