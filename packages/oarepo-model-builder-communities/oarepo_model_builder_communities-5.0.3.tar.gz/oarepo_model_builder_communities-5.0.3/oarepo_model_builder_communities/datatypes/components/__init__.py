from .communities_model import (
    CommunityMetadataModelComponent,
    RecordCommunitiesServiceModelComponent,
)
from .communities_component import RecordCommunitiesComponent

RECORD_COMMUNITIES_COMPONENTS = [
    RecordCommunitiesServiceModelComponent,
    RecordCommunitiesComponent,
    CommunityMetadataModelComponent,
]
