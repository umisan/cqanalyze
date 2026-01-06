from cqanalyze.models import Relation, Query

def calc_residual_query(query: Query, attributes: list[str]) -> Query:
    new_relations = []
    for relation in query.relations:
        new_attribute_set = set(relation.attributes) - set(attributes)
        new_relations.append(Relation(name=relation.name, attributes = list(new_attribute_set)))
    return Query(relations=new_relations)
