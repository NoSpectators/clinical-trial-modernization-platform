/*---------------------------------------------------
Clinical Trial Vital Signs Edit Checks
---------------------------------------------------*/

DATA vs_validation;

    SET work.vs;

    LENGTH query_message $200;

    query_flag = 0;

    /*-----------------------------------------------
    Systolic Blood Pressure Check
    -----------------------------------------------*/

    IF systolic_bp < 40 OR systolic_bp > 250 THEN DO;

        query_flag = 1;

        query_message =
            "Systolic blood pressure out of range";

    END;

    /*-----------------------------------------------
    Temperature Check
    -----------------------------------------------*/

    IF temperature < 95 OR temperature > 105 THEN DO;

        query_flag = 1;

        query_message =
            "Temperature out of range";

    END;

RUN;


/*---------------------------------------------------
Extract Validation Findings
---------------------------------------------------*/

DATA validation_issues;

    SET vs_validation;

    IF query_flag = 1;

RUN;


/*---------------------------------------------------
Generate Summary Report
---------------------------------------------------*/

PROC FREQ DATA=validation_issues;

    TABLES query_message;

RUN;