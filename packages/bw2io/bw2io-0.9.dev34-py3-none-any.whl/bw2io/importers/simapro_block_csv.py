import functools
import warnings
from io import StringIO
from pathlib import Path
from typing import Optional, Union

from bw2data import Database, config, databases, labels
from bw_simapro_csv import SimaProCSV

from ..strategies import (
    change_electricity_unit_mj_to_kwh,
    convert_activity_parameters_to_list,
    drop_unspecified_subcategories,
    fix_localized_water_flows,
    fix_zero_allocation_products,
    link_iterable_by_fields,
    link_technosphere_based_on_name_unit_location,
    match_internal_simapro_simapro_with_unit_conversion,
    migrate_datasets,
    migrate_exchanges,
    normalize_biosphere_categories,
    normalize_biosphere_names,
    normalize_simapro_biosphere_categories,
    normalize_simapro_biosphere_names,
    normalize_units,
    override_process_name_using_single_functional_exchange,
    set_code_by_activity_hash,
    set_metadata_using_single_functional_exchange,
    split_simapro_name_geo,
    strip_biosphere_exc_locations,
    update_ecoinvent_locations,
)
from ..utils import activity_hash
from .base_lci import LCIImporter


class SimaProBlockCSVImporter(LCIImporter):
    format = "bw_simapro_csv"

    def __init__(
        self,
        path_or_stream: Union[Path, StringIO],
        database_name: Optional[str] = None,
        biosphere_database_name: Optional[str] = None,
    ):
        spcsv = SimaProCSV(path_or_stream=path_or_stream, database_name=database_name)
        data = spcsv.to_brightway()

        self.db_name = spcsv.database_name
        self.default_biosphere_database_name = biosphere_database_name
        self.metadata = data["database"]
        self.data = data["processes"]
        self.database_parameters = data["database_parameters"]
        self.project_parameters = data["project_parameters"]

        self.strategies = [
            set_metadata_using_single_functional_exchange,
            override_process_name_using_single_functional_exchange,
            drop_unspecified_subcategories,
            split_simapro_name_geo,
            link_technosphere_based_on_name_unit_location,
            functools.partial(
                link_iterable_by_fields,
                other=Database(biosphere_database_name or config.biosphere),
                kind=labels.biosphere_edge_types,
            ),
            match_internal_simapro_simapro_with_unit_conversion,
        ]

    def create_technosphere_placeholders(self, database_name: str):
        """Create new placeholder database from unlinked technosphere flows in ``self.data``"""
        if database_name in databases:
            raise ValueError(f"{database_name} database already exists")

        def reformat(exc):
            new_exc = exc | {
                "type": labels.process_node_default,
                "exchanges": [],
                "database": database_name,
                "code": activity_hash(exc),
            }
            if not new_exc.get("location"):
                # Also update original for correct linking
                # Location is required
                exc["location"] = new_exc["location"] = "GLO"
            return new_exc

        proc_data = {
            (ds["database"], ds["code"]): ds
            for ds in [
                reformat(exc)
                for ds in self.data
                for exc in ds.get("exchanges", [])
                if exc["type"] not in labels.biosphere_edge_types
                and not exc.get("input")
                and not exc.get("functional")
            ]
        }

        if not proc_data:
            print(
                "Skipping placeholder database creation as all technosphere flows are linked"
            )
            return

        print(
            f"Creating new placeholder database {database_name} with {len(proc_data)} processes"
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            new_db = Database(database_name)
            new_db.register(
                format=self.format,
                comment=f"Database for unlinked technosphere flows from {self.db_name}",
            )

        new_db.write(proc_data)
        self.apply_strategies(
            [
                functools.partial(
                    link_iterable_by_fields,
                    fields=["name", "unit", "location"],
                    other=list(proc_data.values()),
                ),
            ]
        )

    def use_ecoinvent_strategies(self) -> None:
        """Switch strategy selection to normalize data to ecoinvent flow lists"""
        self.strategies = [
            set_metadata_using_single_functional_exchange,
            drop_unspecified_subcategories,
            normalize_units,
            update_ecoinvent_locations,
            split_simapro_name_geo,
            strip_biosphere_exc_locations,
            functools.partial(migrate_datasets, migration="default-units"),
            functools.partial(migrate_exchanges, migration="default-units"),
            functools.partial(set_code_by_activity_hash, overwrite=True),
            change_electricity_unit_mj_to_kwh,
            link_technosphere_based_on_name_unit_location,
            normalize_biosphere_categories,
            normalize_simapro_biosphere_categories,
            normalize_biosphere_names,
            normalize_simapro_biosphere_names,
            functools.partial(migrate_exchanges, migration="simapro-water"),
            fix_localized_water_flows,
            functools.partial(
                link_iterable_by_fields,
                other=Database(
                    self.default_biosphere_database_name or config.biosphere
                ),
                kind="biosphere",
            ),
        ]

    def write_database(
        self,
        backend: Optional[str] = None,
        activate_parameters: bool = True,
        searchable: bool = True,
    ) -> Database:
        if activate_parameters:
            self.write_project_parameters(delete_existing=False)
        return super().write_database(
            backend=backend,
            activate_parameters=activate_parameters,
            searchable=searchable,
        )
