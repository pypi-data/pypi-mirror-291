from typing import List, Optional
from gql import gql


from primitive.utils.actions import BaseAction


class Projects(BaseAction):
    def get_job_run(self, id: str):
        query = gql(
            """
            query jobRun($id: GlobalID!) {
                jobRun(id: $id) {
                    id
                    organization {
                        id
                    }
                }
            }
            """
        )
        variables = {"id": id}
        result = self.primitive.session.execute(query, variable_values=variables)
        return result

    def job_run_update(
        self,
        id: str,
        status: str = None,
        conclusion: str = None,
        file_ids: Optional[List[str]] = [],
    ):
        mutation = gql(
            """
            mutation jobRunUpdate($input: JobRunUpdateInput!) {
                jobRunUpdate(input: $input) {
                    ... on JobRun {
                        id
                        status
                        conclusion
                    }
                }
            }
        """
        )
        input = {"id": id}
        if status:
            input["status"] = status
        if conclusion:
            input["conclusion"] = conclusion
        if file_ids and len(file_ids) > 0:
            input["files"] = file_ids
        variables = {"input": input}
        result = self.primitive.session.execute(mutation, variable_values=variables)
        return result
