from pinjected import instances

default_design = instances(

)

__meta_design__ = instances(
    default_design_paths=[
        "pinjected_anthropic.default_design"
    ]
)
