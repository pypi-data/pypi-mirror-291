from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class SetTemplateCommentRequest(BaseModel):
    """SetTemplateCommentRequest

    :param comment: Comment for the template
    :type comment: str
    """

    def __init__(self, comment: str):
        """SetTemplateCommentRequest

        :param comment: Comment for the template
        :type comment: str
        """
        self.comment = comment
