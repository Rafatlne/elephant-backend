# import logging
# from rq.job import Job
# from rq.timeouts import JobTimeoutException
#
# from api.async_services.services.job_create_and_enque_executions import (
#     priority_execution,
# )
#
# logger = logging.getLogger("rq.worker")
#
#
# def handle_submission_timeout_exception(
#     job: Job, exc_type, exc_value, traceback
# ) -> bool:
#     if job.func_name != (
#         "api.async_services.services.job_create_and_enque_executions"
#         ".create_and_enqueue_executions"
#     ):
#         return True
#
#     if exc_type != JobTimeoutException:
#         return True
#
#     logger.warning(
#         f"Submission {job.args[0]} timed out. Enqueuing for priority execution."
#     )
#     submission_id = job.args[0]
#
#     priority_execution.delay(submission_id)
#
#     return False
