"""The definition for the actions section of the toolbox."""

from gaphas.item import SE

from gaphor import UML
from gaphor.core import gettext
from gaphor.diagram.diagramtoolbox import ToolDef, ToolSection
from gaphor.diagram.diagramtools import PlacementTool
from gaphor.UML import diagramitems


def activity_config(new_item):
    subject = new_item.subject
    subject.name = f"New{type(subject).__name__}"
    if subject.activity:
        return

    diagram = new_item.diagram
    package = diagram.namespace

    activities = (
        [i for i in package.ownedClassifier if isinstance(i, UML.Activity)]
        if package
        else diagram.model.lselect(
            lambda e: isinstance(e, UML.Activity) and e.package is None
        )
    )
    if activities:
        subject.activity = activities[0]
    else:
        activity = subject.model.create(UML.Activity)
        activity.name = "Activity"
        activity.package = package
        subject.activity = activity


def partition_config(partition_item: diagramitems.PartitionItem) -> None:
    partition_item.subject.name = "Partition"


actions = ToolSection(
    gettext("Actions"),
    (
        ToolDef(
            "toolbox-action",
            gettext("Action"),
            "gaphor-action-symbolic",
            "a",
            item_factory=PlacementTool.new_item_factory(
                diagramitems.ActionItem,
                UML.Action,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-initial-node",
            gettext("Initial node"),
            "gaphor-initial-node-symbolic",
            "j",
            item_factory=PlacementTool.new_item_factory(
                diagramitems.InitialNodeItem,
                UML.InitialNode,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-activity-final-node",
            gettext("Activity final node"),
            "gaphor-activity-final-node-symbolic",
            "f",
            item_factory=PlacementTool.new_item_factory(
                diagramitems.ActivityFinalNodeItem,
                UML.ActivityFinalNode,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-flow-final-node",
            gettext("Flow final node"),
            "gaphor-flow-final-node-symbolic",
            "w",
            item_factory=PlacementTool.new_item_factory(
                diagramitems.FlowFinalNodeItem,
                UML.FlowFinalNode,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-decision-node",
            gettext("Decision/merge node"),
            "gaphor-decision-node-symbolic",
            "g",
            item_factory=PlacementTool.new_item_factory(
                diagramitems.DecisionNodeItem,
                UML.DecisionNode,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-fork-node",
            gettext("Fork/join node"),
            "gaphor-fork-node-symbolic",
            "<Shift>R",
            item_factory=PlacementTool.new_item_factory(
                diagramitems.ForkNodeItem,
                UML.JoinNode,
                config_func=activity_config,
            ),
            handle_index=1,
        ),
        ToolDef(
            "toolbox-object-node",
            gettext("Object node"),
            "gaphor-object-node-symbolic",
            "<Shift>O",
            item_factory=PlacementTool.new_item_factory(
                diagramitems.ObjectNodeItem,
                UML.ObjectNode,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-partition",
            gettext("Partition"),
            "gaphor-partition-symbolic",
            "<Shift>P",
            item_factory=PlacementTool.new_item_factory(
                diagramitems.PartitionItem,
                UML.ActivityPartition,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-flow",
            gettext("Control/object flow"),
            "gaphor-control-flow-symbolic",
            "<Shift>F",
            item_factory=PlacementTool.new_item_factory(diagramitems.FlowItem),
        ),
        ToolDef(
            "toolbox-send-signal-action",
            gettext("Send signal action"),
            "gaphor-send-signal-action-symbolic",
            None,
            item_factory=PlacementTool.new_item_factory(
                diagramitems.SendSignalActionItem,
                UML.SendSignalAction,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-accept-event-action",
            gettext("Accept event action"),
            "gaphor-accept-event-action-symbolic",
            None,
            item_factory=PlacementTool.new_item_factory(
                diagramitems.AcceptEventActionItem,
                UML.AcceptEventAction,
                config_func=activity_config,
            ),
            handle_index=SE,
        ),
    ),
)
