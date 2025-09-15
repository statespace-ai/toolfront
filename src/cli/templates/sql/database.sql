install shellfs from community;
load shellfs;


CREATE MACRO inspect_table(tbl_name) AS TABLE(
    SELECT * FROM read_csv(format('toolfront database inspect-table {} "{}" --csv |', getvariable('<PLACEHOLDER>'), tbl_name), header=TRUE)
);

CREATE MACRO query(code) AS TABLE(
    SELECT * FROM read_csv(format('toolfront database query {} "{}" --csv |', getvariable('<PLACEHOLDER>'), code), header=TRUE)
);

SELECT * from read_csv(format('toolfront database list-tables {} --csv |', getvariable('<PLACEHOLDER>')), header=TRUE);