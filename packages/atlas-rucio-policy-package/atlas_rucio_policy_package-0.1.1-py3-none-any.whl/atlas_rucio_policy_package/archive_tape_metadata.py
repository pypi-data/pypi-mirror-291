from rucio.transfertool.fts3_plugins import FTS3TapeMetadataPlugin
from rucio.core.did import get_metadata, list_parent_dids
from typing import Any, Optional, Union


class ATLASCollocationFTSPlugin(FTS3TapeMetadataPlugin):
    def __init__(self, policy_algorithm: str = "atlas"):
        super().__init__(policy_algorithm)
        self.register(
            "policy_collocation_algorithm",
            func=lambda x: self._collocation(self._atlas_collocation, x)
        )

    def _atlas_collocation(self, **hints) -> dict[str, Optional[Union[str, dict[str, Any]]]]:
        """
        https://codimd.web.cern.ch/bmEXKlYqQbu529PUdAFfYw#

        Example filename:
        data23_13p6TeV.00452799.physics_Main.daq.RAW._lb0777._SFO-19._0001.data

        Levels:
        0 - project (e.g. "data23_13p6TeV")
        1 - datatype (e.g. "RAW")
        2 - runnumber (e.g. "00452799")
        3 - dataset (e.g. "data23_13p6TeV.00452799.physics_Main.daq.RAW")
        """
        scope, name = hints['scope'], hints['name']
        did_metadata = get_metadata(scope, name)

        return {
                "1": did_metadata['project'] or None,
                "2": did_metadata['datatype'] or None,
                "3": did_metadata['stream_name'] or None,
                "4": list_parent_dids(scope, name, order_by='created_at') or None,
            }


# Trigger registration
ATLASCollocationFTSPlugin()
