from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType, Section
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
class RecordCommunitiesComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [DefaultsModelComponent]

    def process_mb_invenio_drafts_parent_additional_fields(
        self, datatype, section: Section, **kwargs
    ):
        if (
            hasattr(datatype, "published_record")
        ):
            communities_field = (
                "{{invenio_communities.records.records.systemfields.CommunitiesField}}"
            )
            communities_metadata_field = (
                "{{"
                + datatype.definition["communities-metadata"]["class"]
                + "}}"
            )
            context_cls = "{{oarepo_communities.records.systemfields.communities.OARepoCommunitiesFieldContext}}"

            obj = section.config.setdefault("additional-fields", {})
            obj |= {
                "communities": f"{communities_field}({communities_metadata_field}, context_cls={context_cls})",
            }

    def process_mb_invenio_drafts_parent_marshmallow(
        self, datatype, section: Section, **kwargs
    ):
        if (
            hasattr(datatype, "published_record")
        ):
            obj = section.config.setdefault("additional-fields", {})
            obj |= {
                "communities": "ma_fields.Nested({{oarepo_communities.schemas.parent.CommunitiesParentSchema}})"
            }
