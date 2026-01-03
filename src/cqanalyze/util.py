from cqanalyze.models import Relation, Query

def r(name: str, *attributes: int) -> Relation:
    return Relation(name=name, attributes=[f"a{str(attr)}" for attr in attributes])

def q(*relations: Relation) -> Query:
    return Query(relations=list(relations))
