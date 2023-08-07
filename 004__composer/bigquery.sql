CREATE OR REPLACE PROCEDURE `<PROJECT_ID>.<DATASET>.SP1`()
BEGIN
  CREATE OR REPLACE TABLE `<PROJECT_ID>.<DATASET>.test_sp1` AS
  SELECT * FROM `<PROJECT_ID>.<DATASET>.test`;
END;


CREATE OR REPLACE PROCEDURE `<PROJECT_ID>.<DATASET>.SP2`()
BEGIN
  CREATE OR REPLACE TABLE `<PROJECT_ID>.<DATASET>.test_sp2` AS
  SELECT * FROM `<PROJECT_ID>.<DATASET>.test`;
END;


CREATE OR REPLACE PROCEDURE `<PROJECT_ID>.<DATASET>.SP3`()
BEGIN
  CREATE OR REPLACE TABLE `<PROJECT_ID>.<DATASET>.test_sp3` AS (
    SELECT * FROM `<PROJECT_ID>.<DATASET>.test_sp1`
    UNION ALL
    SELECT * FROM `<PROJECT_ID>.<DATASET>.test_sp2`
  );
END;