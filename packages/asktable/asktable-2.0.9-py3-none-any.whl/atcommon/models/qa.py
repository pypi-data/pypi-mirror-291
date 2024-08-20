from typing import List, Optional, Dict

from atcommon.models.base import BaseCoreModel
from atcommon.models.meta import MetaData

# try import
try:
    import sqlparse
except ImportError:
    sqlparse = None


class Question(BaseCoreModel):
    text: str
    keywords = []

    __properties_init__ = ["text"]

    def __str__(self):
        return f"Q[{self.text}]"


class UserQuestion(Question):

    def __str__(self):
        return f"USER-Q[{self.text}]"


class StrucQuery(BaseCoreModel):

    ds_id: str
    question: Question
    actual_used_table_names: list[str]
    prepared_statement: str
    params: dict
    table_meta: MetaData
    is_row_filtered: bool
    header: dict
    cache_id: str

    __properties_init__ = [
        "ds_id",
        "question",
        "actual_used_table_names",
        "prepared_statement",
        "params",
        "table_meta",
        "is_row_filtered",
        "header",
        "cache_id",
    ]

    @property
    def sql(self):
        """
        insert params into prepared_statement,
        return complete sql
        """
        sql = self.prepared_statement
        for key, value in self.params.items():
            placeholder = f":{key}"
            if isinstance(value, str):
                value = f"'{value}'"
            sql = sql.replace(placeholder, str(value))

        if not sqlparse:
            return sql
        return sqlparse.format(sql, reindent=True, keyword_case="upper")

    @property
    def formatted_prepared_statement(self):
        if not sqlparse:
            return self.prepared_statement
        return sqlparse.format(
            self.prepared_statement, reindent=True, keyword_case="upper"
        )

    @property
    def statement(self):
        return self.prepared_statement

    @property
    def params_tuple(self):
        return tuple(self.params.values())

    def to_dict(self):
        # 重写基类的 to_dict 方法
        return {
            "question": self.question.to_dict(),
            "actual_used_table_names": self.actual_used_table_names,
            "prepared_statement": self.prepared_statement,
            "params": self.params,
            "table_meta": self.table_meta.to_dict() if self.table_meta else {},
            "is_row_filtered": self.is_row_filtered,
            "header": self.header,
        }

    @classmethod
    def load_from_dict(cls, data: dict):
        # 重写基类的 load_from_dict 方法
        question = Question.load_from_dict(data.get("question"))
        data["question"] = question

        table_meta = MetaData.load_from_dict(data.get("table_meta", {}))
        data["table_meta"] = table_meta
        return cls(**data)

    def dump_for_prompt(self):
        return {
            "prepared_statement": self.prepared_statement,
            "params": self.params,
        }

    def to_string(self):
        output = "\n".join(
            [
                f"Q: {self.question.text}",
                f"SQL: \n{self.formatted_prepared_statement}",
                f"Params: {self.params}",
            ]
        )
        return output

    def get_table_names(self) -> list[str]:
        tables = []
        schemas = self.table_meta.schemas
        for s in schemas:
            tables.extend([t.name for t in s.tables])
        return tables

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        if len(self.question.text) < 20:
            question_text = self.question.text
        else:
            # 仅显示前20个字符
            question_text = self.question.text[:20]
        return (
            f"Query[{question_text}]->[{self.prepared_statement}]"
        )

class QueryResult:

    def __init__(
        self, query: StrucQuery, result, query_time_ms: int
    ):  # result: DataFrame
        self.query = query
        self.result = result
        self.query_time_ms = query_time_ms

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            f"\n{self.query} -> {self.summarize_result} Time: {self.query_time_ms} ms."
        )

    @property
    def summarize_result(self):
        return f"Result[{self.row_count} 行 {self.column_count} 列]"

    def to_dict(self):
        return {
            "query": self.query.to_string(),
            "result_info": {
                "row_count": self.row_count,
                "column_count": self.column_count,
                "columns": self.columns.tolist(),
            },
            "query_time_ms": self.query_time_ms,
        }

    def to_string(self, top_n=100, only_result=False) -> str:
        # 截取 前N行
        result_str = self.result.head(top_n).to_string(index=False)
        result_str = f"{self.summarize_result}:\n{result_str}\n"
        if only_result:
            return result_str
        else:
            return f"\nQuery: \n{self.query}\n{result_str}"

    @property
    def rows(self):
        return self.result.to_numpy()

    @property
    def columns(self):
        return self.result.columns

    @property
    def row_count(self):
        return len(self.result)

    @property
    def column_count(self):
        return len(self.columns)


class BIAnswer(BaseCoreModel):
    status: str
    elapsed_time: int
    text: str
    files: Optional[List] = None
    charts: Optional[List] = None
    query_insights: Optional[List] = None
    payload: Optional[Dict] = None

    __properties_init__ = [
        "status",
        "elapsed_time",
        "text",
        "files",
        "charts",
        "query_insights",  # Transparency Reports
        "payload",
    ]

    def __str__(self):
        file_str = f"[File:{[f.get('url') for f in self.files]}]" if self.files else ""
        image_str = (
            f"[Image:{[c.get('url') for c in self.charts]}]" if self.charts else ""
        )
        return (
            f"[{self.status}-{self.elapsed_time}s] {self.text} {file_str} {image_str}"
        )

    def __repr__(self):
        return self.__str__()

    def query_insights_to_string(self):
        """
        将query_insights转换为字符串
            [{
                    "question": "查询超过平均分的有多少人",
                    "datasource": data_source.id,
                    "queries": [


                    "results": [
                        {
                            "query_info": {
                                "query": "select count(*) from user where score > avg_score",
                                "time_line": [
                                    {"name": "meta", "time": 123},
                                    {"name": "sql", "time": 123},
                                    {"name": "privs", "time": 123},
                                    ],
                                "headers": ["name", "age"],
                            },                            "result_info": {
                                "row_count": self.row_count,
                                "column_count": self.column_count,
                                "columns": self.columns.tolist(),
                            },
                            "query_time_ms": 123,
                        },
                        {
                            "query_info": {
                                "query": "select count(*) from user where score > avg_score",
                                "time_line": [
                                    {"name": "meta", "time": 123},
                                    {"name": "sql", "time": 123},
                                    {"name": "privs", "time": 123},
                                    ],
                                "headers": ["name", "age"],
                            },
                            "result_info": {
                                "row_count": self.row_count,
                                "column_count": self.column_count,
                                "columns": self.columns.tolist(),
                            },
                            "query_time_ms": 123,
                        },
                    ],
                    "query_time": int(time.time() - _begin),
             },
            ]
        """
        if not self.query_insights:
            return ""

        output = []
        for task_index, task in enumerate(self.query_insights, start=1):
            # 添加任务标题
            output.append(
                f"任务{task_index}：[{task['query_time']}秒]{task['question']}"
            )
            output.append("详细步骤：")

            for step_index, result in enumerate(task["results"], start=1):
                query = result["query"]
                row_count = result["result_info"]["row_count"]
                column_count = result["result_info"]["column_count"]
                # 转换为秒，保留1位小数
                query_time = round(result["query_time_ms"] / 1000, 1)

                # 格式化每个查询步骤的描述
                output.append(
                    f"   {step_index}. [{query_time}秒]{query} -> [{row_count}行{column_count}列]"
                )
            output.append("")

        return "\n".join(output)
