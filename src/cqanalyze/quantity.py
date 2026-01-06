from cqanalyze.models import Query
from cqanalyze.util import r, q
from mip import *

def calc_fractional_edge_packing(query: Query) -> tuple[float, list[float]]:
    m = Model(sense=MAXIMIZE)
    relation_variables = [m.add_var(relation.name) for relation in query.relations]
    attributes = set()
    for relation in query.relations:
        attributes |= set(relation.attributes)
    for attr in attributes:
        target = []
        for relation in query.relations:
            if attr in relation.attributes:
                target.append(m.var_by_name(relation.name))
        m += xsum(target) <= 1
    m.objective = xsum(relation_variables)
    status = m.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL:
        print('optimal solution {} found'.format(m.objective_value))
        print('solution:')
        for v in m.vars:
            if abs(v.x) > 1e-6: # only printing non-zeros
                print('{} : {}'.format(v.name, v.x))
        return m.objective_value, [v.x for v in m.vars]
    else:
        raise Exception('optimal solution is not found')


def calc_fractional_edge_cover(query: Query) -> tuple[float, list[float]]:
    m = Model(sense=MINIMIZE)
    relation_variables = [m.add_var(relation.name) for relation in query.relations]
    attributes = set()
    for relation in query.relations:
        attributes |= set(relation.attributes)
    for attr in attributes:
        target = []
        for relation in query.relations:
            if attr in relation.attributes:
                target.append(m.var_by_name(relation.name))
        m += xsum(target) >= 1
    m.objective = xsum(relation_variables)
    status = m.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL:
        print('optimal solution {} found'.format(m.objective_value))
        print('solution:')
        for v in m.vars:
            if abs(v.x) > 1e-6: # only printing non-zeros
                print('{} : {}'.format(v.name, v.x))
        return m.objective_value, [v.x for v in m.vars]
    else:
        raise Exception('optimal solution is not found')

