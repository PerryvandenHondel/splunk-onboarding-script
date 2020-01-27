Definitions







Database Field Definitons
ID; A number as a field type for unique records

Code; A string field type with a code





Table Definitions

ENV; Environments, every Splunk instance gets a environment code of 3 letters

LGF; Log files


ELF; Environment Log File
CREATE TABLE `SPLUNK_ONBOARDING`.`environment_logfile_elf` (
  `elf_code` VARCHAR(16) NOT NULL,
  `elf_env_code` VARCHAR(3) NULL,
  `elf_lgf_id` INT NULL,
  `elf_is_created` INT NULL,
  PRIMARY KEY (`elf_code`));



SCS; Server Classes





Views
view_create_deployment_app
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `SPLUNK_ONBOARDING`.`view_create_new_da` AS
    SELECT 
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_id` AS `lgf_id`,
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_path` AS `lgf_path`,
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_env_code` AS `lgf_env_code`,
        `SPLUNK_ONBOARDING`.`environment_env`.`env_description` AS `env_description`,
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_sourcetype` AS `lgf_sourcetype`,
        `SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_created` AS `lgf_created`,
        `SPLUNK_ONBOARDING`.`environment_env`.`env_directory_da` AS `env_directory_da`
    FROM
        (`SPLUNK_ONBOARDING`.`logfile_lgf`
        JOIN `SPLUNK_ONBOARDING`.`environment_env` ON ((`SPLUNK_ONBOARDING`.`logfile_lgf`.`lgf_env_code` = `SPLUNK_ONBOARDING`.`environment_env`.`env_code`)))

