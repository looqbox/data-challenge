from data.load_and_run import run_query

def retrieve_data(
    product_code: int | None = None,
    store_code: int | None = None,
    date: list[str] | None = None
):

    conditions = []
    params = []

    if product_code is not None:
        conditions.append("PRODUCT_CODE = %s")
        params.append(product_code)

    if store_code is not None:
        conditions.append("STORE_CODE = %s")
        params.append(store_code)

    if date is not None:

        if len(date) != 2:
            raise ValueError(
                "date deve conter [inicio, fim]"
            )

        conditions.append(
            "DATE BETWEEN %s AND %s"
        )

        params.extend(date)

    where_clause = ""

    if conditions:
        conditions_sql = " AND ".join(conditions)
        where_clause = "WHERE " + conditions_sql

    sql = f"""
        SELECT *
        FROM data_product_sales
        {where_clause}
    """

    return run_query(sql, params)