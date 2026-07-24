"""Video project lifecycle — the read-only resolver over the project folders.

One module owns where projects live (lifecycle **stage**) and what state each
one is in (**phase**), so the ~27 sites that used to glob
`video-projects/_IN_PRODUCTION/*` by hand share one interface.

See CONTEXT.md "Lifecycle stage" and "Phase" for the domain definitions, and
ADR-0008 for why this is a read-only resolver (mutation stays in reconcile).

Public surface:
    from tools.video_projects import VideoProjectRepo, VideoProject, Stage
    from tools.video_projects import AmbiguousSlugError
    from tools.video_projects import StatusDoc  # + the AUTO zones (ADR-0014)
"""
from tools.video_projects.repo import (
    AmbiguousSlugError,
    Stage,
    VideoProject,
    VideoProjectRepo,
)
from tools.video_projects.status_doc import (
    AutoZone,
    PACKAGING_LOCK_ZONE,
    RECONCILE_DASHBOARD_ZONE,
    RECONCILE_ZONE,
    StatusDoc,
    StatusDocError,
)

__all__ = [
    "AmbiguousSlugError",
    "AutoZone",
    "PACKAGING_LOCK_ZONE",
    "RECONCILE_DASHBOARD_ZONE",
    "RECONCILE_ZONE",
    "Stage",
    "StatusDoc",
    "StatusDocError",
    "VideoProject",
    "VideoProjectRepo",
]
