from NEMO.exceptions import NEMOException, ProjectChargeException
from NEMO.utilities import format_daterange

from NEMO_billing.invoices.models import BillableItemType
from NEMO_billing.invoices.utilities import display_amount
from NEMO_billing.models import ProjectBillingHardCap


# General billing exception class
class BillingException(NEMOException):
    pass


class ChargeTypeNotAllowedForProjectException(ProjectChargeException):
    def __init__(self, project, charge_type: BillableItemType, msg=None):
        self.charge_type = charge_type
        new_msg = f"{charge_type.friendly_display_name()} charges are not allowed for project {project.name}"
        super().__init__(project, None, msg or new_msg)


class HardCAPReachedException(ProjectChargeException):
    def __init__(self, project_hard_cap: ProjectBillingHardCap, msg=None):
        self.project_hard_cap = project_hard_cap
        new_msg = f"You reached the maximum amount allowed of {display_amount(project_hard_cap.amount, project_hard_cap.configuration)} for this project during the period {format_daterange(project_hard_cap.start_date, project_hard_cap.end_date)}"
        super().__init__(project_hard_cap.project, None, msg or new_msg)
