SELECT jsonb_pretty(
    jsonb_agg(
        jsonb_build_object(
            'table_name', table_name,
            'columns', columns
        )
    )
)
FROM (
    SELECT 
        c.table_name,
        jsonb_agg(
            jsonb_build_object(
                'column_name', c.column_name,
                'data_type', c.data_type,
                'is_nullable', c.is_nullable,
                'column_default', c.column_default
            )
        ) AS columns
    FROM information_schema.columns c
    WHERE c.table_schema = 'public'  -- Możesz zmienić schemat na inny
    GROUP BY c.table_name
) AS table_info;
