from tests.utils import (
    ImageTagComponents,
    create_version_tag_for_example_images,
)


def test_fast_api_multistage_build_versions(
    fast_api_multistage_production_image,
    version,
) -> None:
    production_image_components: ImageTagComponents = (
        ImageTagComponents.create_from_tag(fast_api_multistage_production_image)
    )
    production_image_version_tag = create_version_tag_for_example_images(
        version, "production-image"
    )
    assert production_image_components.version == production_image_version_tag
