SQL create tables







ELF (Environment Log File)

CREATE TABLE `SPLUNK_ONBOARDING`.`environment_logfile_elf` (
  `elf_code` VARCHAR(16) NOT NULL,
  `elf_env_code` VARCHAR(3) NULL,
  `elf_lgf_id` INT NULL,
  `elf_is_created` INT NULL,
  PRIMARY KEY (`elf_code`));
