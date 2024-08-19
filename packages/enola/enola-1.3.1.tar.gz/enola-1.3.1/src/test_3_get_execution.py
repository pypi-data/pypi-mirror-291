from enola import get_executions
from enola.enola_types import CompareType, DataType, ExecutionDataFilter
#from enola.enola_types import ErrOrWarnKind
#from enola.base.enola_types import AgentResponseModel

#token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFTk9MQV9IVUVNVUwwNC1mYTIyOTZkNDBiYjUwMzNkYTdhZjE1N2JiMzUwYjc2ZiIsImlkIjoiZmNhZDY2MjYtMjM3MS00NTMxLWIwMDItNzhhODFhNjk5ZTdjIiwiZGlzcGxheU5hbWUiOiJudWV2aXRhIDEgLSBzb2xvIGdldCIsImFnZW50RGVwbG95SWQiOiJFTk9MQV9IVUVNVUwwNC1mYTIyOTZkNDBiYjUwMzNkYTdhZjE1N2JiMzUwYjc2ZiIsImNhblRyYWNraW5nIjpmYWxzZSwiY2FuRXZhbHVhdGUiOmZhbHNlLCJjYW5HZXRFeGVjdXRpb25zIjp0cnVlLCJ1cmwiOiJodHRwOi8vbG9jYWxob3N0OjcwNzIvYXBpIiwidXJsQmFja2VuZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NzA3MS9hcGkiLCJvcmdJZCI6IkVOT0xBX0hVRU1VTDA0IiwiaXNTZXJ2aWNlQWNjb3VudCI6dHJ1ZSwiaWF0IjoxNzE5MTYzNTA5LCJleHAiOjE4NDUyNTkxOTksImlzcyI6ImVub2xhIn0.wxcrvVB5lDtzm9VkYtilGXXWZIQsR820SQdS4ymkHUM"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFTk9MQV9IVUVNVUwwOC0xY2MzNjUwMTE0MGUzZjFmMWNkZWNlYjgwNjBhN2ZlZCIsImlkIjoiNTlkZDNlNDgtZmEyNi00ZmRhLWEwMmYtNmU2OWMxNDE2YTFiIiwiZGlzcGxheU5hbWUiOiJjdWVudGEgc2VydmljaW8gMSIsImFnZW50RGVwbG95SWQiOiJFTk9MQV9IVUVNVUwwOC0xY2MzNjUwMTE0MGUzZjFmMWNkZWNlYjgwNjBhN2ZlZCIsImNhblRyYWNraW5nIjp0cnVlLCJjYW5FdmFsdWF0ZSI6dHJ1ZSwiY2FuR2V0RXhlY3V0aW9ucyI6dHJ1ZSwidXJsIjoiaHR0cDovL2xvY2FsaG9zdDo3MDcyL2FwaSIsInVybEJhY2tlbmQiOiJodHRwOi8vbG9jYWxob3N0OjcwNzEvYXBpIiwib3JnSWQiOiJFTk9MQV9IVUVNVUwwOCIsImlzU2VydmljZUFjY291bnQiOnRydWUsImlhdCI6MTcyMTI1MTgzNCwiZXhwIjoxODQ3MzMyNzk5LCJpc3MiOiJlbm9sYSJ9.kU_VZEy_fsC3j0QRvgiF9XyhL9IVw6o4khgyp6PkSdI"
#token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFTk9MQV9IVUVNVUwwOC0xY2MzNjUwMTE0MGUzZjFmMWNkZWNlYjgwNjBhN2ZlZCIsImlkIjoiNmQ2YTY2ZjItMzkwMi00MzNhLTg1MjUtMmFlMzI1YmRkYTk2IiwiZGlzcGxheU5hbWUiOiIyMiIsImFnZW50RGVwbG95SWQiOiJFTk9MQV9IVUVNVUwwOC0xY2MzNjUwMTE0MGUzZjFmMWNkZWNlYjgwNjBhN2ZlZCIsImNhblRyYWNraW5nIjp0cnVlLCJjYW5FdmFsdWF0ZSI6dHJ1ZSwiY2FuR2V0RXhlY3V0aW9ucyI6dHJ1ZSwidXJsIjoiaHR0cHM6Ly9hcGlzZW5kLmVub2xhLWFpLmNvbS9hcGkiLCJ1cmxCYWNrZW5kIjoiaHR0cHM6Ly9hcGkuZW5vbGEtYWkuY29tL2FwaSIsIm9yZ0lkIjoiRU5PTEFfSFVFTVVMMDgiLCJpc1NlcnZpY2VBY2NvdW50Ijp0cnVlLCJpYXQiOjE3MjM4NDkyMDUsImV4cCI6MTg0OTkyNDc5OSwiaXNzIjoiZW5vbGEifQ.dTtuQapNayDr_ruMva6V76VKbEWYS3ULLht-70Eywqo"

exec = get_executions.GetExecutions(token=token, raise_error_if_fail=False)


exec.query(
    date_from="2024-06-23t22:00", 
    date_to="2024-12-01", 
    limit=30,

    #eval_id_auto=ExecutionEvalFilter(eval_id=["0", "11"], include=False),
    data_filter_list=[
        #ExecutionDataFilter(name="Input usuario", value="value1", type=DataType.STRING, compare=CompareType.CONTAINS),
        #ExecutionDataFilter(name="Input usuario", value="1894992", compare=CompareType.CONTAINS),
        #ExecutionDataFilter(name="info3", value="10", compare=CompareType.LESS_EQUAL, type=DataType.NUMBER),
    ],
    #agent_deploy_id=["ENOLA_HUEMUL04-fa2296d40bb5033da7af157bb350b76f"]
    #agent_deploy_id=["ENOLA_HUEMUL04-b11664d1b96d1df3f7e395ae3374d273"]
    )

continue_processing = True
while (exec.continue_execution == True and exec.get_page_number() < 2):
    result = exec.get_next_page()
    
    print("page:", exec.get_page_number() , " ,len data:",len(result.data))



    




