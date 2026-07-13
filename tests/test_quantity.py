from cqanalyze import (
    calc_reduced_quasi_vertex_cover,
    q,
    r,
)


def test_reduced_quasi_vertex_cover_path_query() -> None:
    objective, _ = calc_reduced_quasi_vertex_cover(q(r("R", 1, 2), r("S", 2, 3)))

    assert objective == 2


def test_reduced_quasi_vertex_cover_loomis_whitney_query() -> None:
    objective, _ = calc_reduced_quasi_vertex_cover(
        q(
            r("S1", 1, 2, 3),
            r("S2", 1, 2, 4),
            r("S3", 1, 3, 4),
            r("S4", 2, 3, 4),
        )
    )

    assert abs(objective - 4 / 3) < 1e-6
