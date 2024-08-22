from time import sleep
from primitive.utils.actions import BaseAction
from loguru import logger


class Agent(BaseAction):
    def execute(
        self,
    ):
        logger.enable("primitive")
        logger.debug("Starting Primitive Agent")
        while True:
            hardware = self.primitive.hardware.get_own_hardware_details()

            active_reservation_id = None
            if hardware.get("activeReservation"):
                active_reservation_id = hardware["activeReservation"]["id"]
            if not active_reservation_id:
                logger.debug("No active reservation found")
                sleep(5)
                continue

            job_runs_data = self.primitive.projects.get_job_runs(
                status="pending", first=1, reservation_id=active_reservation_id
            )

            pending_job_runs = [
                edge["node"] for edge in job_runs_data["jobRuns"]["edges"]
            ]

            for job_run in pending_job_runs:
                logger.debug("Found pending Job Run")
                logger.debug(f"Job Run ID: {job_run['id']}")
                logger.debug(f"Job Name: {job_run['job']['name']}")

                if job_run["job"]["slug"] == "lint":
                    logger.debug("Executing Lint Job")

                    self.primitive.projects.job_run_update(
                        job_run["id"], status="request_completed"
                    )

                    result, message = self.primitive.lint.execute()
                    if result:
                        self.primitive.projects.job_run_update(
                            job_run["id"],
                            status="request_completed",
                            conclusion="success",
                            stdout=message,
                        )
                    else:
                        self.primitive.projects.job_run_update(
                            job_run["id"],
                            status="request_completed",
                            conclusion="failure",
                            stdout=message,
                        )

            sleep(5)
