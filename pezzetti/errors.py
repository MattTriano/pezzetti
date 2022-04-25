class DataMetadataParityError(Exception):
    """Exception raised for when updating tables without data:metadata parity."""

    def __init__(
        self,
        prior_raw_data_file_exists: bool, 
        prior_metadata_file_exists: bool,
        table_name: str
    ) -> None:
        self.prior_raw_data_file_exists = prior_raw_data_file_exists
        self.prior_metadata_file_exists = prior_metadata_file_exists
        self.table_name = table_name
        self.message = self.make_message()
        super().__init__(self.message)

    def make_message(self) -> str:
        msg = ["Data inconsistency found!"]
        if self.prior_raw_data_file_exists and not self.prior_metadata_file_exists:
            msg.extend([f"(Table: {self.table_name}) raw_data file found without metadata file."])
        elif not self.prior_raw_data_file_exists and self.prior_metadata_file_exists:
            msg.extend([f"(Table: {self.table_name}) metadata file found without raw_data file."])
        msg.extend([f"If intentional, recreate {self.table_name} Table object with kwarg",
                    "'enforce_metadata_parity' = False."])
        return " ".join(msg)