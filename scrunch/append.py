from scrunch.datasets import Dataset
from scrunch.expressions import parse_expr, process_expr


def compare_datasets(ds_a, ds_b):
    """
    compare the difference in structure between datasets. The
    criterion is the following:

    (1) variables that, when matched across datasets by alias, have different types. 
    (2) variables that have the same name but don't match on alias.
    (3) for variables that match and have categories, any categories that have the 
    same id but don't match on name.
    (4) for array variables that match, any subvariables that have the same name but
    don't match on alias.
    (5) array variables that, after assembling the union of their subvariables, 
    point to subvariables that belong to other ds (Not implemented)

    :param: ds_a: Dataset instance to append to
    :param: ds_b: Daatset instance to append from
    :return: a dictionary of differences

    NOTE: this sould be done via: http://docs.crunch.io/#post217 
    but doesn't seem to be a working feature of Crunch
    """
    diff = {
        'variables': {
            'by_type': [],
            'by_alias': []
        },
        'categories': {},
        'subvariables': {}
    }

    array_types = ['multiple_response', 'categorical_array']

    vars_a = {v.alias: v.type for v in ds_a.values()}
    vars_b = {v.alias: v.type for v in ds_b.values()}

    # 1. match variables by alias and compare types
    common_aliases = frozenset(vars_a.keys()) & frozenset(vars_b.keys())
    for alias in common_aliases:
        if vars_a[alias] != vars_b[alias]:
            diff['variables']['by_type'].append(ds_b[alias].name)

        # 3. match variable alias and distcint categories names for same id's        
        if vars_b[alias] == 'categorical' and vars_a[alias] == 'categorical':
            a_ids = frozenset([v.id for v in ds_a[alias].categories.values()])
            b_ids = frozenset([v.id for v in ds_b[alias].categories.values()])
            common_ids = a_ids & b_ids

            for id in common_ids:
                a_name = ds_a[alias].categories[id].name
                b_name = ds_b[alias].categories[id].name
                if a_name != b_name:
                    if diff['categories'].get(ds_b[alias].name):
                        diff['categories'][ds_b[alias].name].append(id)
                    else:
                         diff['categories'][ds_b[alias].name] = []
                         diff['categories'][ds_b[alias].name].append(id)

    # 2. match variables by names and compare aliases
    common_names = frozenset(ds_a.variable_names()) & frozenset(ds_b.variable_names())
    for name in common_names:
        if ds_a[name].alias != ds_b[name].alias:
            diff['variables']['by_alias'].append(name)

        # 4. array types that match, subvars with same name and != alias
        if ds_b[name].type == ds_a[name].type and \
            ds_a[name].type in array_types and \
            ds_a[name].type in array_types:

            a_names = frozenset(ds_a[name].variable_names())
            b_names = frozenset(ds_b[name].variable_names())
            common_subnames = a_names & b_names
            print(common_subnames)

            for sv_name in common_subnames:
                if ds_a[name][sv_name].alias != ds_b[name][sv_name].alias:
                    if diff['subvariables'].get(name):
                        diff['subvariables'][name].append(ds_b[name][sv_name].alias)
                    else:
                        diff['subvariables'][name] = []
                        diff['subvariables'][name].append(ds_b[name][sv_name].alias)
    return diff


def append_dataset(ds_a, ds_b, filter=None, where=None, autorollback=True):
    """
    Append ds_b into ds_a. If this operation fails, the
    append is rolledback. Dataset variables and subvariables 
    are matched on their aliases and categories are matched by name.

    :param: ds_a: Dataset instance to append to
    :param: ds_b: Daatset instance to append from
    :param: filter: An expression to filter ds_b rows. cannot be a Filter
        according to: http://docs.crunch.io/#get211
    :param: where: A list of variable names to include from ds_b
    """
    if where and not isinstance(where, list):
        raise AttributeError("where must be a list of variable names")

    payload = {
        "element": "shoji:entity",
        "body": {
            'dataset': ds_a.self
        }
    }

    if where:
        if isinstance(where, list):
            id_vars = []
            for var in where:
                id_vars.append(self.ds[var].url)
            # Now build the payload with selected variables
            payload['where'] = {
                'function': 'select',
                'args': [{
                    'map': {
                        x: {'variable': x} for x in id_vars
                    }
                }]
            }
        else:
            raise ValueError("where param must be a list of variable names")

    if filter:
        payload['body']['filter'] = process_expr(parse_expr(expr), ds_b.resource)

