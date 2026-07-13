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

def calc_fractional_vertex_cover(query: Query) -> tuple[float, list[float]]:
    m = Model(sense=MINIMIZE)
    attributes = set()
    for relation in query.relations:
        attributes |= set(relation.attributes)
    attribute_variables = [m.add_var(name=attribute) for attribute in attributes]
    for relation in query.relations:
        target = []
        for attribute in relation.attributes:
            target.append(m.var_by_name(attribute))
        m += xsum(target) >= 1
    m.objective = xsum(attribute_variables)
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

def calc_generalized_fractional_vertex_packing(query: Query) -> tuple[float, list[float]]:
    m = Model(sense=MAXIMIZE)
    attributes = set()
    for relation in query.relations:
        attributes |= set(relation.attributes)
    attribute_variables = [m.add_var(name=attribute, lb=-float("inf")) for attribute in attributes]
    for relation in query.relations:
        target = []
        for attribute in relation.attributes:
            target.append(m.var_by_name(attribute))
        m += xsum(target) <= 1
    m.objective = xsum(attribute_variables)
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


def calc_reduced_quasi_vertex_cover(query: Query) -> tuple[float, list[float]]:
    m = Model(sense=MAXIMIZE)
    attributes = set()
    for relation in query.relations:
        attributes |= set(relation.attributes)
    big_l = len(query.relations)
    relation_variables = [
        m.add_var(name=relation.name, lb=0, ub=1)
        for relation in query.relations
    ]
    attribute_variables = [
        m.add_var(name=attribute, var_type=BINARY)
        for attribute in attributes
    ]
    for attribute in attributes:
        target = []
        for relation in query.relations:
            if attribute in relation.attributes:
                target.append(m.var_by_name(relation.name))
        t_x = m.var_by_name(attribute)
        m += xsum(target) <= t_x + (1 - t_x) * big_l
    for relation in query.relations:
        target = []
        for attribute in relation.attributes:
            target.append(m.var_by_name(attribute))
        m += m.var_by_name(relation.name) <= xsum(target)
    for relation_u in query.relations:
        attributes_u = set(relation_u.attributes)
        for relation_v in query.relations:
            attributes_v = set(relation_v.attributes)
            for attribute_y in attributes_u - attributes_v:
                target = []
                for attribute_x in attributes_v - attributes_u:
                    target.append(m.var_by_name(attribute_x))
                m += (
                    m.var_by_name(relation_v.name)
                    <= 1 + xsum(target) - m.var_by_name(attribute_y)
                )
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

